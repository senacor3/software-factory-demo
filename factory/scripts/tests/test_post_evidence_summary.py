# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for post_evidence_summary.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_post_evidence_summary.py

Covers the plan's I/O & Edge-Case Matrix: summary posts whether review.md's status is
`resolved` or `unresolved-after-cap`, a missing evidence/checks/<name>.json is reported
as `status: "not-run"`, and both "no open PR found" and a `gh pr comment` failure raise
`EvidenceSummaryError`. `open_implementation_pr.find_open_pr`/`post_summary.post_comment`
are mocked throughout -- no real `gh` process in the committed suite (mirrors
test_open_implementation_pr.py).
"""

import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import open_implementation_pr
import post_evidence_summary
import post_summary
import state_io


def _write_checks(state_directory, statuses):
    for name, status in statuses.items():
        path = state_directory / "evidence" / "checks" / f"{name}.json"
        state_io.write_atomic(path, json.dumps({"status": status}) + "\n")


def _write_review(state_directory, status, *, fix_cycle=None, body="## Findings\n\n_none_"):
    extra = {"fix_cycle": fix_cycle} if fix_cycle is not None else None
    state_io.write_state(
        state_directory / "review.md",
        story_slug="foo-bar",
        stage="review",
        status=status,
        body=body,
        extra=extra,
    )


def _write_findings(state_directory, findings):
    path = state_directory / "evidence" / "review" / "findings.json"
    state_io.write_atomic(path, json.dumps({"findings": findings}) + "\n")


def _open_pr(pr_number=7, pr_url="https://github.com/org/repo/pull/7"):
    return {"branch": "light-factory/foo-bar/run-1", "pr_number": pr_number, "pr_url": pr_url}


# --- posts regardless of review outcome ----------------------------------------------


def test_posts_summary_when_review_resolved(tmp_path):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_checks(state_directory, {"build": "pass", "test": "pass", "lint": "skipped", "security": "skipped"})
    _write_review(state_directory, "resolved", fix_cycle=0)
    _write_findings(state_directory, [])

    with patch("post_evidence_summary.open_implementation_pr.find_open_pr", return_value=_open_pr()) as find_pr, \
         patch("post_evidence_summary.post_summary.post_comment") as post_comment:
        outcome = post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)

    find_pr.assert_called_once_with("light-factory/foo-bar/run-1", cwd=None)
    assert post_comment.call_count == 1
    args, _kwargs = post_comment.call_args
    assert args[0] == 7
    body = args[1]
    assert "build: pass" in body
    assert "status: resolved" in body
    assert "findings: 0" in body
    assert "Files changed" in body
    assert outcome["review_status"] == "resolved"


def test_posts_summary_when_review_unresolved_after_cap(tmp_path):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_checks(state_directory, {"build": "pass", "test": "pass", "lint": "skipped", "security": "skipped"})
    _write_review(state_directory, "unresolved-after-cap", fix_cycle=2)
    findings = [{"location": "foo.py:10", "description": "still broken"}]
    _write_findings(state_directory, findings)

    with patch("post_evidence_summary.open_implementation_pr.find_open_pr", return_value=_open_pr()), \
         patch("post_evidence_summary.post_summary.post_comment") as post_comment:
        outcome = post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)

    body = post_comment.call_args.args[1]
    assert "status: unresolved-after-cap" in body
    assert "fix cycles: 2" in body
    assert "findings: 1" in body
    assert "foo.py:10" in body
    assert "still broken" in body
    assert outcome["review_status"] == "unresolved-after-cap"


def test_missing_check_file_reported_as_not_run(tmp_path):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_checks(state_directory, {"build": "pass", "test": "pass"})  # lint/security missing
    _write_review(state_directory, "resolved", fix_cycle=0)
    _write_findings(state_directory, [])

    with patch("post_evidence_summary.open_implementation_pr.find_open_pr", return_value=_open_pr()), \
         patch("post_evidence_summary.post_summary.post_comment") as post_comment:
        post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)

    body = post_comment.call_args.args[1]
    assert "lint: not-run" in body
    assert "security: not-run" in body


# --- config source ----------------------------------------------------------------------


def _write_sources(state_directory, sources):
    for name, source in sources.items():
        path = state_directory / "evidence" / "checks" / f"{name}.json"
        data = {"status": "pass"}
        if source != "<absent>":
            data["config_source"] = source
        state_io.write_atomic(path, json.dumps(data) + "\n")


def _summary_body(tmp_path, sources):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_sources(state_directory, sources)
    _write_review(state_directory, "resolved", fix_cycle=0)
    _write_findings(state_directory, [])
    with patch("post_evidence_summary.open_implementation_pr.find_open_pr", return_value=_open_pr()), \
         patch("post_evidence_summary.post_summary.post_comment") as post_comment:
        post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)
    return post_comment.call_args.args[1]


def _all(source):
    return {name: source for name in post_evidence_summary.CHECK_NAMES}


def test_config_line_shows_shared_source(tmp_path):
    body = _summary_body(tmp_path, _all("origin/main"))
    assert "- config: origin/main" in body
    assert body.index("- security:") < body.index("- config:") < body.index("### Review")


def test_config_line_unknown_when_sources_disagree(tmp_path):
    sources = _all("origin/main")
    sources["lint"] = "working-tree"
    assert "- config: unknown" in _summary_body(tmp_path, sources)


def test_config_line_unknown_when_key_missing(tmp_path):
    sources = _all("origin/main")
    sources["build"] = "<absent>"
    assert "- config: unknown" in _summary_body(tmp_path, sources)


def test_config_line_unknown_when_null(tmp_path):
    assert "- config: unknown" in _summary_body(tmp_path, _all(None))


def test_config_line_unknown_when_a_check_was_not_run(tmp_path):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_sources(state_directory, {"build": "origin/main", "test": "origin/main"})
    _write_review(state_directory, "resolved", fix_cycle=0)
    _write_findings(state_directory, [])
    with patch("post_evidence_summary.open_implementation_pr.find_open_pr", return_value=_open_pr()), \
         patch("post_evidence_summary.post_summary.post_comment") as post_comment:
        post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)
    assert "- config: unknown" in post_comment.call_args.args[1]


# --- posting fails --------------------------------------------------------------------


def test_no_open_pr_raises_evidence_summary_error(tmp_path):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_checks(state_directory, {"build": "pass", "test": "pass", "lint": "skipped", "security": "skipped"})
    _write_review(state_directory, "resolved", fix_cycle=0)
    _write_findings(state_directory, [])

    with patch("post_evidence_summary.open_implementation_pr.find_open_pr", return_value=None), \
         patch("post_evidence_summary.post_summary.post_comment") as post_comment:
        with pytest.raises(post_evidence_summary.EvidenceSummaryError, match="no open PR"):
            post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)

    post_comment.assert_not_called()


def test_gh_pr_comment_failure_raises_evidence_summary_error(tmp_path):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_checks(state_directory, {"build": "pass", "test": "pass", "lint": "skipped", "security": "skipped"})
    _write_review(state_directory, "resolved", fix_cycle=0)
    _write_findings(state_directory, [])

    with patch("post_evidence_summary.open_implementation_pr.find_open_pr", return_value=_open_pr()), \
         patch(
             "post_evidence_summary.post_summary.post_comment",
             side_effect=post_summary.PostCommentError("gh: pull request not found"),
         ):
        with pytest.raises(post_evidence_summary.EvidenceSummaryError, match="not found"):
            post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)


def test_find_open_pr_failure_raises_evidence_summary_error(tmp_path):
    state_directory = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    _write_checks(state_directory, {"build": "pass", "test": "pass", "lint": "skipped", "security": "skipped"})
    _write_review(state_directory, "resolved", fix_cycle=0)
    _write_findings(state_directory, [])

    with patch(
        "post_evidence_summary.open_implementation_pr.find_open_pr",
        side_effect=open_implementation_pr.PROpenError("gh: authentication required"),
    ):
        with pytest.raises(post_evidence_summary.EvidenceSummaryError, match="authentication required"):
            post_evidence_summary.post_evidence_summary("foo-bar", "run-1", state_base=tmp_path)
