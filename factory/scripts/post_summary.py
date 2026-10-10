#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""post_summary -- AD-4's shared gate-summary PR-comment step.

Posts a concise, human-readable summary as a PR comment at each stage ending in a human
gate. Named by the architecture's Structural Seed as the shared file for both
`plan-approval` (this ticket's caller, `factory/graph/analysis_graph.py`) and
`evidence-approval` (entry 11's caller, `implementation_graph.py`) -- deliberately kept
separate from `open_implementation_pr.py`, which is about branch/PR lifecycle (open,
close), not formatting stage-specific summaries.

All `gh` subprocess failures raise a single `PostCommentError`, carrying the failing
command and its output, so callers can distinguish this failure mode from other stages'
own errors.
"""

from __future__ import annotations

import os
import subprocess


class PostCommentError(RuntimeError):
    """A `gh` subprocess call failed while posting the gate-summary PR comment."""


def _run(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise PostCommentError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise PostCommentError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout.strip()


def post_comment(pr_number: int, body: str, *, cwd: str | os.PathLike | None = None) -> None:
    """Post `body` as a comment on `pr_number`. Raises PostCommentError on any `gh`
    subprocess failure."""
    _run(["gh", "pr", "comment", str(pr_number), "--body", body], cwd=cwd)
