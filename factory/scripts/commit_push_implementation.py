#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""commit_push_implementation -- Job 2's deterministic commit+push step.

Runs *after* the implementation agent (AD-6: deterministic git writes never become
graph nodes or agent tool calls -- mirrors AD-12's "script does the git write"
precedent). `git status --porcelain` decides committed-vs-no-op -- never the agent's
own report (see story-implementation-agent-plan.md's Design Notes) -- so a trivial
plan that needed no file changes is a distinguishable no-op, not an error.

All `git` subprocess failures raise a single `CommitPushError`, distinct from
`checkout_branch.CheckoutError` and `implementation_graph.ImplementationInvocationError`
(see the plan's I/O & Edge-Case Matrix).
"""

from __future__ import annotations

import os
import subprocess


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
) -> dict:
    """Commit and push the implementation agent's edits, if any.

    Returns `{"committed": bool}` -- False and no commit attempted when the working
    tree is clean (a legitimate no-op, not an error). Raises CommitPushError on any
    git failure.
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
            f"Implementation: {story_slug} ({run_id})",
        ],
        cwd=cwd,
    )
    _run(["git", "push", "origin", branch], cwd=cwd)
    return {"committed": True}
