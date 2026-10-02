#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""open_implementation_pr -- AD-12's deterministic branch+PR-open step.

Once Job 1's `run_analysis` (factory/graph/analysis_graph.py) decides to proceed (a
non-halted result), this script -- not the agent -- creates the isolated branch
(`light-factory/<story-slug>/<run-id>`), commits the analysis stage's own just-written
`plan.md`/`decisions.md` as the branch's first real commit, and opens a PR against the
target branch. Mirrors `state_io.py`'s "script writes, not agent" precedent (AD-5).

Idempotent: if an open PR already exists for this exact branch name, its info is
returned instead of recreating anything -- entry 4's clarification rounds re-call
`run_analysis` and must not fail or duplicate work against an already-open PR.

Does NOT implement AD-15 supersession-closing (searching other branches for this
story-slug) -- out of scope for this ticket, see deferred-work.md.

All `git`/`gh` subprocess failures raise a single `PROpenError`, carrying the failing
command and its output, so callers can distinguish this failure mode from a CAP-1
judgment halt or a `claude` CLI tooling failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state_io  # noqa: E402


class PROpenError(RuntimeError):
    """A `git` or `gh` subprocess call failed while opening the implementation PR."""


def _run(cmd: "list[str]", *, cwd: "str | os.PathLike | None" = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise PROpenError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise PROpenError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout.strip()


def _find_existing_pr(branch: str, *, cwd: "str | os.PathLike | None" = None) -> "dict | None":
    out = _run(
        ["gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number,url"],
        cwd=cwd,
    )
    import json

    prs = json.loads(out) if out else []
    if not prs:
        return None
    pr = prs[0]
    return {"branch": branch, "pr_number": pr["number"], "pr_url": pr["url"]}


def open_pr_for_story(
    story_slug: str,
    run_id: str,
    *,
    target_branch: str = "main",
    state_base: "str | os.PathLike" = state_io.FACTORY_DIR,
    cwd: "str | os.PathLike | None" = None,
) -> dict:
    """Create the isolated branch, commit plan.md/decisions.md, push, and open the PR.

    Idempotent: returns the existing open PR's info if one is already open for this
    branch, without creating anything new. Raises PROpenError on any git/gh failure.
    """
    branch = f"light-factory/{story_slug}/{run_id}"

    existing = _find_existing_pr(branch, cwd=cwd)
    if existing is not None:
        return existing

    state_directory = state_io.state_dir(story_slug, run_id, base=state_base)
    plan_path = state_directory / "plan.md"
    decisions_path = state_directory / "decisions.md"

    _run(["git", "checkout", "-b", branch], cwd=cwd)
    _run(["git", "add", str(plan_path), str(decisions_path)], cwd=cwd)
    _run(
        [
            "git",
            "-c",
            "user.name=light-factory-bot",
            "-c",
            "user.email=light-factory-bot@users.noreply.github.com",
            "commit",
            "-m",
            f"Analysis: {story_slug} ({run_id})",
        ],
        cwd=cwd,
    )
    _run(["git", "push", "-u", "origin", branch], cwd=cwd)
    _run(
        [
            "gh",
            "pr",
            "create",
            "--head",
            branch,
            "--base",
            target_branch,
            "--title",
            f"light-factory: {story_slug} ({run_id})",
            "--body",
            f"Automated analysis-stage PR for `{story_slug}` (`{run_id}`). See `plan.md`/`decisions.md`.",
        ],
        cwd=cwd,
    )

    created = _find_existing_pr(branch, cwd=cwd)
    if created is None:
        raise PROpenError(f"gh pr create reported success but no open PR found for branch {branch!r}")
    return created


def close_for_clarification(
    pr_number: int,
    open_questions: "list[str]",
    *,
    cwd: "str | os.PathLike | None" = None,
) -> None:
    """Post `open_questions` as a comment on `pr_number` and close it in the same call
    (AD-13/AD-15) -- never `--delete-branch`, per AD-10/AD-12/AD-15's audit-trail-over-
    cleanup posture. Raises PROpenError on any subprocess failure."""
    comment = "Open questions from analysis:\n\n" + "\n".join(f"- {q}" for q in open_questions)
    _run(["gh", "pr", "close", str(pr_number), "--comment", comment], cwd=cwd)
