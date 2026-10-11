#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""commit_push_implementation -- the implementation/checks/review jobs' deterministic
commit+push step.

Runs *after* the implementation agent (AD-6: deterministic git writes never become
graph nodes or agent tool calls -- mirrors AD-12's "script does the git write"
precedent). `git status --porcelain` decides committed-vs-no-op -- never the agent's
own report (see story-implementation-agent-plan.md's Design Notes) -- so a trivial
plan that needed no file changes is a distinguishable no-op, not an error.

All `git` subprocess failures raise a single `CommitPushError`, distinct from
`checkout_branch.CheckoutError` and `implementation_graph.ImplementationInvocationError`
(see the plan's I/O & Edge-Case Matrix).

`commit_and_push`'s `label` keyword (default `"Implementation"`) names the stage in
the commit message -- the `checks`/`review` jobs' own evidence-commit steps pass
`"Checks"`/`"Review"` via this module's CLI (`--story-slug`/`--run-id`/`--label`),
reusing this same persistence mechanism rather than duplicating it. Existing
in-process callers that omit `label` are unaffected.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


class CommitPushError(RuntimeError):
    """A `git` subprocess call failed while committing/pushing the implementation
    agent's edits."""


def _run(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise CommitPushError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise CommitPushError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout


def commit_and_push(
    branch: str,
    story_slug: str,
    run_id: str,
    *,
    cwd: str | os.PathLike | None = None,
    label: str = "Implementation",
) -> dict:
    """Commit and push the current working tree's edits, if any.

    Returns `{"committed": bool}` -- False and no commit attempted when the working
    tree is clean (a legitimate no-op, not an error). Raises CommitPushError on any
    git failure.

    `label` (keyword-only, default `"Implementation"`) names the stage in the commit
    message -- e.g. `"Checks"`/`"Review"` when this is reused by those jobs' own
    evidence-commit steps -- and otherwise changes nothing about this function's
    behavior.
    """
    status = _run(["git", "status", "--porcelain"], cwd=cwd)
    if not status.strip():
        return {"committed": False}

    _run(["git", "add", "-A"], cwd=cwd)
    _run(
        [
            "git",
            "-c",
            "user.name=light-factory-bot",
            "-c",
            "user.email=light-factory-bot@users.noreply.github.com",
            "commit",
            "-m",
            f"{label}: {story_slug} ({run_id})",
        ],
        cwd=cwd,
    )
    _run(["git", "push", "origin", branch], cwd=cwd)
    return {"committed": True}


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument(
        "--label",
        default="Implementation",
        help="commit message stage label, e.g. Checks/Review (default: Implementation)",
    )
    args = p.parse_args(argv)

    branch = f"light-factory/{args.story_slug}/{args.run_id}"
    try:
        result = commit_and_push(branch, args.story_slug, args.run_id, label=args.label)
    except CommitPushError as e:
        print(f"commit/push failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "committed": result["committed"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
