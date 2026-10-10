#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""post_evidence_summary -- Job 2's final step: CAP-8's evidence-approval gate summary (AD-4).

Reads the 4 `evidence/checks/<name>.json` files (ticket 8), `review.md`'s frontmatter
(`status`/`fix_cycle`, tickets 9/10), and `evidence/review/findings.json`, renders a
concise Markdown summary, and posts it as a PR comment via the shared `post_summary`
module (AD-4) -- the same mechanism ticket 5 used for the `plan-approval` gate.

Runs whether review.md's status is `resolved` or `unresolved-after-cap` -- both are
legitimate, human-decides-at-the-gate outcomes, not failures (see the plan's I/O & Edge-
Case Matrix). CAP-8's "drillable diff" is satisfied by pointing at the PR's own Files-
changed tab -- this never inlines the diff.

Finds the PR via `open_implementation_pr.find_open_pr` (same branch-name formula every
other stage uses: `light-factory/<story-slug>/<run-id>`). Any failure to find the PR or
post the comment raises `EvidenceSummaryError`, distinguishable from a legitimate summary.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import open_implementation_pr
import post_summary
import state_io

CHECK_NAMES = ("build", "test", "lint", "security")


class EvidenceSummaryError(RuntimeError):
    """No open PR was found for this story/run, or posting the summary comment itself
    failed (a `gh` subprocess failure) -- distinct from a legitimate summary, which
    always succeeds regardless of the checks'/review's own outcome."""


def _read_check(state_directory: Path, name: str) -> dict:
    path = state_directory / "evidence" / "checks" / f"{name}.json"
    if not path.exists():
        return {"status": "not-run"}
    return json.loads(path.read_text(encoding="utf-8"))


def _read_findings(state_directory: Path) -> list:
    path = state_directory / "evidence" / "review" / "findings.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("findings") or []


def _render_summary(checks: dict, review_meta: dict, findings: list) -> str:
    lines = ["## Evidence summary", "", "### Checks", ""]
    for name in CHECK_NAMES:
        lines.append(f"- {name}: {checks[name].get('status', 'unknown')}")

    lines += ["", "### Review", ""]
    lines.append(f"- status: {review_meta.get('status', 'unknown')}")
    lines.append(f"- fix cycles: {review_meta.get('fix_cycle', 0)}")
    lines.append(f"- findings: {len(findings)}")

    if findings:
        lines += ["", "#### Outstanding findings", ""]
        for f in findings:
            location = f.get("location", "")
            description = f.get("description", "")
            lines.append(f"- **{location}**: {description}")

    lines += ["", "See the PR's Files changed tab for the full diff."]
    return "\n".join(lines)


def post_evidence_summary(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Render and post the evidence-approval gate summary. Returns `{"pr": dict, "body":
    str, "review_status": str}`. Raises EvidenceSummaryError if no open PR is found or
    posting the comment fails."""
    state_directory = state_io.state_dir(story_slug, run_id, base=state_base)

    checks = {name: _read_check(state_directory, name) for name in CHECK_NAMES}
    review_meta, _ = state_io.read_state(state_directory / "review.md")
    findings = _read_findings(state_directory)

    body = _render_summary(checks, review_meta, findings)

    branch = f"light-factory/{story_slug}/{run_id}"
    try:
        pr = open_implementation_pr.find_open_pr(branch, cwd=cwd)
    except open_implementation_pr.PROpenError as e:
        raise EvidenceSummaryError(str(e)) from e
    if pr is None:
        raise EvidenceSummaryError(f"no open PR found for branch {branch!r}")

    try:
        post_summary.post_comment(pr["pr_number"], body, cwd=cwd)
    except post_summary.PostCommentError as e:
        raise EvidenceSummaryError(str(e)) from e

    return {"pr": pr, "body": body, "review_status": review_meta.get("status")}


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    args = p.parse_args(argv)

    try:
        outcome = post_evidence_summary(args.story_slug, args.run_id)
    except EvidenceSummaryError as e:
        print(f"evidence summary failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "review_status": outcome["review_status"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
