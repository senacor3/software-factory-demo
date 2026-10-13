#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""close_rejected_pr -- the trailing job's reject-cleanup step (AD-2, AD-16): a
deterministic pipeline script, never an agent action.

A reviewer rejecting `plan-approval` or `evidence-approval` ends the run, but the gated
job never runs a step and its result reads `failure` exactly like an ordinary crash, so
`needs.<job>.result` alone cannot tell the two apart. This script asks the run's own
review history instead (`GET /repos/{owner}/{repo}/actions/runs/{run_id}/approvals`): only
an entry with `state: "rejected"` naming `--gate`'s Environment counts as a reject. `gh
api` resolves `{owner}/{repo}` itself inside a checkout.

On a real reject, finds this run's PR via `open_implementation_pr.find_open_pr` (same
branch-name formula every other stage uses: `software-factory/<story-slug>/<run-id>`) and
closes it with a comment naming the gate, the rejecting reviewer, and their review comment
when they left one. Only the PR closes -- never `--delete-branch`, no label, no state-file
write (AD-10/AD-12/AD-15's audit-trail-over-cleanup posture). An ordinary failure, a
reject of the other gate only, or an already-closed PR all leave everything untouched and
exit 0.

Any `gh` failure or malformed review-history response raises a single `RejectCloseError`,
carrying the failing command and its output.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import open_implementation_pr

GATES = ("plan-approval", "evidence-approval")


class RejectCloseError(RuntimeError):
    """The reject check or the close could not be completed -- the review-history call,
    the PR lookup, or `gh pr close` failed, or the review history was malformed."""


def _run(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise RejectCloseError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise RejectCloseError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout.strip()


def find_rejection(
    github_run_id: int, gate: str, *, cwd: str | os.PathLike | None = None
) -> dict | None:
    """Return `{"reviewer": str, "comment": str}` for the review-history entry that
    rejected `gate` on this run, or `None` if there is none (the gate was approved, never
    reviewed, or only the other gate was rejected). Raises RejectCloseError if the call
    fails or the response is not the expected JSON array of review objects."""
    cmd = ["gh", "api", f"repos/{{owner}}/{{repo}}/actions/runs/{github_run_id}/approvals"]
    out = _run(cmd, cwd=cwd)

    try:
        reviews = json.loads(out)
    except json.JSONDecodeError as e:
        raise RejectCloseError(f"{cmd!r} returned malformed JSON: {e}: {out!r}") from e
    if not isinstance(reviews, list) or not all(isinstance(r, dict) for r in reviews):
        raise RejectCloseError(f"{cmd!r} returned an unexpected shape: {out!r}")

    for review in reviews:
        environments = review.get("environments") or []
        if not isinstance(environments, list) or not all(isinstance(e, dict) for e in environments):
            raise RejectCloseError(f"{cmd!r} returned an unexpected shape: {out!r}")
        if review.get("state") != "rejected":
            continue
        if gate not in (e.get("name") for e in environments):
            continue
        user = review.get("user")
        reviewer = user.get("login") if isinstance(user, dict) else None
        return {"reviewer": reviewer or "", "comment": (review.get("comment") or "").strip()}

    return None


def render_comment(gate: str, rejection: dict) -> str:
    reviewer = f"@{rejection['reviewer']}" if rejection["reviewer"] else "a reviewer"
    lines = [f"Rejected at the `{gate}` gate by {reviewer} -- this run ends without merging."]
    if rejection["comment"]:
        quoted = "\n".join(f"> {line}" for line in rejection["comment"].splitlines())
        lines += ["", "Review comment:", "", quoted]
    retrigger = (
        "This PR is closed, not deleted: its branch and state files stay in place. "
        "Re-triggering the pipeline for this story starts a new run with a new PR."
    )
    lines += ["", retrigger]
    return "\n".join(lines)


def close_rejected_pr(
    story_slug: str,
    run_id: str,
    github_run_id: int,
    gate: str,
    *,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Close this run's PR if, and only if, `gate` was rejected on this run. Returns
    `{"rejected": bool, "pr": dict | None}` -- `pr` is the PR that was closed, `None` when
    this was not a reject or the PR was already closed. Raises RejectCloseError on any
    `gh` failure or malformed review history."""
    if gate not in GATES:
        raise RejectCloseError(f"unknown gate {gate!r}, expected one of {GATES!r}")

    rejection = find_rejection(github_run_id, gate, cwd=cwd)
    if rejection is None:
        return {"rejected": False, "pr": None}

    branch = f"software-factory/{story_slug}/{run_id}"
    try:
        pr = open_implementation_pr.find_open_pr(branch, cwd=cwd)
    except (open_implementation_pr.PROpenError, ValueError, KeyError, TypeError) as e:
        raise RejectCloseError(f"PR lookup for branch {branch!r} failed: {e}") from e
    if pr is None:
        return {"rejected": True, "pr": None}

    _run(
        ["gh", "pr", "close", str(pr["pr_number"]), "--comment", render_comment(gate, rejection)],
        cwd=cwd,
    )

    return {"rejected": True, "pr": pr}


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--github-run-id", required=True, type=int)
    p.add_argument("--gate", required=True, choices=GATES)
    args = p.parse_args(argv)

    try:
        outcome = close_rejected_pr(args.story_slug, args.run_id, args.github_run_id, args.gate)
    except RejectCloseError as e:
        print(f"reject cleanup failed: {e}", file=sys.stderr)
        return 1

    pr = outcome["pr"]
    print(
        json.dumps(
            {
                "ok": True,
                "gate": args.gate,
                "rejected": outcome["rejected"],
                "closed_pr_number": pr["pr_number"] if pr else None,
            }
        )
    )
    if not outcome["rejected"]:
        print(f"not a reject: {args.gate} was not rejected on this run; PR left untouched", file=sys.stderr)
    elif pr is None:
        print(f"{args.gate} was rejected, but this run has no open PR; nothing to close", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
