#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""state_io — shared `.factory/<story-slug>/<run-id>/` state I/O for the light-factory pipeline.

Every later pipeline stage (analysis, checks, review, fix-loop) needs one shared way to
read/write state files with AD-10's exact frontmatter schema, and one shared way to
derive the `story-slug`/`run-id` identifiers AD-8/AD-15 require every job to thread via
`needs:` rather than independently re-derive. This module is that shared library,
mirroring `_bmad/scripts/memlog.py`'s pattern: stdlib-only, PEP 723 inline header, a
hand-rolled `key: value` frontmatter split/render, atomic writes (temp + fsync + rename),
and a thin `argparse` CLI.

Scope, deliberately narrow (see story-shared-state-library-plan.md Design Notes):

  - Only the per-stage status enums AD-10 actually defines are enforced: `analysis`
    (governs `plan.md`/`decisions.md`) and `review` (governs `review.md`). AD-10 defines
    no `implementation`-stage state file in v1, so `write_state(stage="implementation",
    ...)` accepts any non-empty status with no closed-enum check -- don't invent one.
  - `evidence/checks/` and `evidence/review/`'s file *format* is NOT decided here --
    only that the directories exist (`ensure_layout`). Later entries own their contents.
  - No `plan.md`/`decisions.md`/`review.md` content is written here -- only the generic
    frontmatter + body read/write pair every later stage's writer calls into.

The state file shape (any of plan.md / decisions.md / review.md):

    ---
    schema_version: 1
    story_slug: my-story-name
    stage: analysis
    status: drafted
    updated: 2026-10-01T12:34:56Z
    ---

    <body -- stage-specific content, opaque to this module>

Commands:
  derive (--story-file PATH --github-run-id ID)        print story-slug=... / run-id=...
  write  (--path FILE --story-slug S --stage T --status U [--body TEXT|--body-file FILE]
          [--schema-version N])                        write a stage's state file
  read   (--path FILE)                                 print the state file back as JSON

`derive`'s stdout is shaped for direct `>> "$GITHUB_OUTPUT"` redirection in a workflow step.
"""

from __future__ import (
    annotations,  # keep type-hint syntax lazy so the script runs on 3.8+
)

import argparse
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

FACTORY_DIR = ".factory"
SCHEMA_VERSION = 1

# AD-10's canonical per-stage stages and status enums. `implementation` deliberately has
# no entry here -- no AD-10-defined implementation-stage state file exists in v1, so any
# non-empty status is accepted for it (see module docstring / plan Design Notes).
STAGES = ("analysis", "implementation", "review")
STATUS_BY_STAGE = {
    "analysis": frozenset(
        {"drafted", "awaiting-clarification", "clarification-cap-reached", "ready-for-review"}
    ),
    "review": frozenset(
        {"in-review", "findings-open", "fix-in-progress", "resolved", "unresolved-after-cap"}
    ),
}

# kebab-case: lowercase letters/digits, single hyphens between segments, no leading/
# trailing hyphen, no underscores or uppercase.
_KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# --- AD-8 / AD-15: slug and run-id derivation -------------------------------


def derive_story_slug(story_file: str | os.PathLike) -> str:
    """Derive the story-slug from the triggering story file's name (AD-8).

    Expects `stories/<story-slug>.md` relative to the repository root (the current
    working directory), with the slug itself kebab-case. The path is resolved first,
    so `./stories/foo.md`, `stories//foo.md` and an absolute path to the same file
    all yield the same slug. Raises ValueError if the file has no `.md` extension,
    the slug isn't kebab-case, or the resolved path isn't exactly
    `stories/<name>.md` under the repository root (including paths outside it) --
    AD-8 requires kebab-case on the input file, with no fallback normalization.
    The file need not exist.
    """
    name = Path(story_file).name
    if not name.endswith(".md"):
        raise ValueError(f"story file {str(story_file)!r} must have a .md extension")
    slug = name[: -len(".md")]
    if not slug or not _KEBAB_RE.match(slug):
        raise ValueError(
            f"story file name {name!r} is not kebab-case "
            "(expected lowercase letters/digits/hyphens only, e.g. 'my-story-name.md')"
        )
    try:
        parts = Path(story_file).resolve().relative_to(Path.cwd().resolve()).parts
    except ValueError:
        parts = ()
    if parts != ("stories", name):
        raise ValueError(
            f"story file {str(story_file)!r} must be 'stories/<slug>.md' "
            "relative to the repository root"
        )
    return slug


def derive_run_id(github_run_id: str | int) -> str:
    """Derive the run-id from GitHub's own run identifier (AD-15): `run-<github.run_id>`."""
    run_id = str(github_run_id).strip()
    if not run_id:
        raise ValueError("github_run_id must not be empty")
    return f"run-{run_id}"


# --- AD-8 / AD-15: directory layout -----------------------------------------


def state_dir(story_slug: str, run_id: str, base: str | os.PathLike = FACTORY_DIR) -> Path:
    """The per-story, per-run state directory: `.factory/<story-slug>/<run-id>/` (AD-8/AD-15)."""
    if not story_slug:
        raise ValueError("story_slug must not be empty")
    if not run_id:
        raise ValueError("run_id must not be empty")
    return Path(base) / story_slug / run_id


def ensure_layout(story_slug: str, run_id: str, base: str | os.PathLike = FACTORY_DIR) -> Path:
    """Create the run's directory tree and return it.

    Only creates directories -- `evidence/checks/` (deterministic pipeline-step output)
    and `evidence/review/` (the independent review agent's output), split by writer per
    AD-8. Does NOT create or touch plan.md/decisions.md/review.md: each stage writes its
    own file via write_state, and this module doesn't prescribe evidence-file contents.
    """
    d = state_dir(story_slug, run_id, base)
    (d / "evidence" / "checks").mkdir(parents=True, exist_ok=True)
    (d / "evidence" / "review").mkdir(parents=True, exist_ok=True)
    return d


# --- AD-10: frontmatter schema ----------------------------------------------


def validate_status(stage: str, status: str) -> None:
    """Raise ValueError unless `status` is valid for `stage` under AD-10's enum.

    `implementation` has no closed enum defined by AD-10 in v1 -- any non-empty status
    is accepted for it. `analysis` and `review` are checked against their exact enums.
    """
    if stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r}; must be one of {STAGES}")
    if not status:
        raise ValueError("status must not be empty")
    allowed = STATUS_BY_STAGE.get(stage)
    if allowed is not None and status not in allowed:
        raise ValueError(
            f"status {status!r} is not valid for stage {stage!r}; "
            f"must be one of {sorted(allowed)}"
        )


def split(text: str) -> tuple[dict, str]:
    """Return (frontmatter dict in source order, body str). Mirrors memlog.py's split.

    The closing fence is the first line that is *exactly* `---`, so a `---` inside a
    field value never truncates the frontmatter.
    """
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("state file has no frontmatter")
    end = next((i for i in range(1, len(lines)) if lines[i] == "---"), None)
    if end is None:
        raise ValueError("state file frontmatter is not terminated")
    meta: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, "\n".join(lines[end + 1 :]).lstrip("\n")


def render(meta: dict, body: str) -> str:
    # Neutralize newlines in values so a multi-line field can't break the fence on re-read.
    fm = "\n".join(f"{k}: {' '.join(str(v).splitlines())}" for k, v in meta.items())
    return "---\n" + fm + "\n---\n\n" + body.rstrip("\n") + "\n"


def write_atomic(path: Path, text: str) -> None:
    """Temp + flush + fsync + atomic rename, so a crash never half-writes a state file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def write_state(
    path: str | os.PathLike,
    *,
    story_slug: str,
    stage: str,
    status: str,
    body: str = "",
    schema_version: int = SCHEMA_VERSION,
    extra: dict | None = None,
) -> dict:
    """Write a stage's state file with AD-10's exact frontmatter schema.

    Validates `stage`/`status` against AD-10's per-stage enum (and that `story_slug` is
    non-empty) BEFORE touching disk -- on an invalid combination this raises ValueError
    and no file is written or modified. Returns the frontmatter dict actually written.

    `extra`, when given, is merged into `meta` after the fixed AD-10 fields (so it can
    add fields an AD-10 reader doesn't know about, e.g. the fix loop's `fix_cycle`
    counter) -- never overrides a fixed field name. Every existing caller omits it;
    behavior for them is unchanged.
    """
    validate_status(stage, status)
    if not story_slug:
        raise ValueError("story_slug must not be empty")
    meta = {
        "schema_version": int(schema_version),
        "story_slug": story_slug,
        "stage": stage,
        "status": status,
        "updated": now(),
    }
    if extra:
        meta.update(extra)
    write_atomic(Path(path), render(meta, body))
    return meta


def read_state(path: str | os.PathLike) -> tuple[dict, str]:
    """Read a state file back as (meta, body). `schema_version` is parsed back to int."""
    text = Path(path).read_text(encoding="utf-8")
    meta, body = split(text)
    if "schema_version" in meta:
        try:
            meta["schema_version"] = int(meta["schema_version"])
        except ValueError:
            pass  # leave as-is; a corrupted field is a read-time concern for the caller
    return meta, body


# --- CLI ---------------------------------------------------------------------


def cmd_derive(args) -> int:
    try:
        slug = derive_story_slug(args.story_file)
        run_id = derive_run_id(args.github_run_id)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    # Shaped for direct `>> "$GITHUB_OUTPUT"` redirection.
    print(f"story-slug={slug}")
    print(f"run-id={run_id}")
    return 0


def cmd_write(args) -> int:
    if args.body and args.body_file:
        print("error: --body and --body-file are mutually exclusive", file=sys.stderr)
        return 2
    body = args.body or ""
    try:
        if args.body_file:
            body = Path(args.body_file).read_text(encoding="utf-8")
        meta = write_state(
            args.path,
            story_slug=args.story_slug,
            stage=args.stage,
            status=args.status,
            body=body,
            schema_version=args.schema_version,
        )
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "path": str(args.path), "meta": meta}))
    return 0


def cmd_read(args) -> int:
    try:
        meta, body = read_state(args.path)
    except (ValueError, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, "path": str(args.path), "meta": meta, "body": body}))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    pd = sub.add_parser("derive", help="derive story-slug and run-id (AD-8/AD-15)")
    pd.add_argument("--story-file", required=True, help="triggering story file path")
    pd.add_argument("--github-run-id", required=True, help="GitHub's github.run_id")
    pd.set_defaults(func=cmd_derive)

    pw = sub.add_parser("write", help="write a stage's state file (AD-10)")
    pw.add_argument("--path", required=True)
    pw.add_argument("--story-slug", required=True)
    pw.add_argument("--stage", required=True, choices=STAGES)
    pw.add_argument("--status", required=True)
    pw.add_argument("--body", default="", help="body text (mutually exclusive with --body-file)")
    pw.add_argument("--body-file", help="read body text from this file instead of --body")
    pw.add_argument("--schema-version", type=int, default=SCHEMA_VERSION)
    pw.set_defaults(func=cmd_write)

    pr = sub.add_parser("read", help="read a stage's state file back, printed as JSON")
    pr.add_argument("--path", required=True)
    pr.set_defaults(func=cmd_read)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    if sys.platform == "win32":
        # Piped output on Windows defaults to a legacy code page, not UTF-8.
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
