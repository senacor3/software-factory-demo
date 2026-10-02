# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for open_implementation_pr.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_open_implementation_pr.py

Covers the amendment's Acceptance Criterion 3 (idempotent-reuse) plus fresh-create and
subprocess-failure, with `subprocess.run` mocked throughout -- no real `git`/`gh`
process in the committed suite (mirrors how test_analysis_graph.py mocks the `claude`
CLI call).
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import open_implementation_pr  # noqa: E402
import state_io  # noqa: E402


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stderr="boom"):
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


def _pr_list_output(prs):
    return json.dumps(prs)


# --- fresh-create success path -----------------------------------------------------------


def test_fresh_create_creates_branch_commits_pushes_and_opens_pr(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if cmd[:3] == ["gh", "pr", "list"]:
            # First call (pre-create check): nothing open yet. Second call (post-create
            # read-back): the PR gh pr create just made.
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 42, "url": "https://github.com/org/repo/pull/42"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        result = open_implementation_pr.open_pr_for_story(
            "foo", "run-1", state_base=tmp_path
        )

    assert result == {
        "branch": "light-factory/foo/run-1",
        "pr_number": 42,
        "pr_url": "https://github.com/org/repo/pull/42",
    }

    checkout_calls = [c for c in calls if c[:2] == ["git", "checkout"]]
    assert checkout_calls == [["git", "checkout", "-b", "light-factory/foo/run-1"]]

    commit_calls = [c for c in calls if "commit" in c]
    assert len(commit_calls) == 1
    assert "-c" in commit_calls[0] and "user.name=light-factory-bot" in commit_calls[0]
    assert "user.email=light-factory-bot@users.noreply.github.com" in commit_calls[0]

    push_calls = [c for c in calls if c[:2] == ["git", "push"]]
    assert push_calls == [["git", "push", "-u", "origin", "light-factory/foo/run-1"]]

    create_calls = [c for c in calls if c[:3] == ["gh", "pr", "create"]]
    assert len(create_calls) == 1


def test_fresh_create_commits_the_correct_state_files(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if cmd[:3] == ["gh", "pr", "list"]:
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 1, "url": "https://github.com/org/repo/pull/1"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)

    add_calls = [c for c in calls if c[:2] == ["git", "add"]]
    assert len(add_calls) == 1
    added_paths = set(add_calls[0][2:])
    expected_dir = state_io.state_dir("foo", "run-1", base=tmp_path)
    assert added_paths == {str(expected_dir / "plan.md"), str(expected_dir / "decisions.md")}


# --- idempotent-reuse (Acceptance Criterion 3) ---------------------------------------------


def test_idempotent_reuse_returns_existing_pr_without_recreating(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if cmd[:3] == ["gh", "pr", "list"]:
            return _ok(_pr_list_output([{"number": 7, "url": "https://github.com/org/repo/pull/7"}]))
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        result = open_implementation_pr.open_pr_for_story(
            "foo", "run-1", state_base=tmp_path
        )

    assert result == {
        "branch": "light-factory/foo/run-1",
        "pr_number": 7,
        "pr_url": "https://github.com/org/repo/pull/7",
    }
    # only the pre-create existence check ran -- no git/gh mutation calls.
    assert calls == [["gh", "pr", "list", "--head", "light-factory/foo/run-1", "--state", "open", "--json", "number,url"]]


# --- git/gh subprocess failure raises PROpenError -------------------------------------------


def test_git_checkout_failure_raises_pr_open_error(tmp_path):
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[:3] == ["gh", "pr", "list"]:
            return _ok(_pr_list_output([]))
        if cmd[:2] == ["git", "checkout"]:
            return _fail(stderr="fatal: a branch named 'light-factory/foo/run-1' already exists")
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="already exists"):
            open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)


def test_gh_pr_create_failure_raises_pr_open_error(tmp_path):
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[:3] == ["gh", "pr", "list"]:
            return _ok(_pr_list_output([]))
        if cmd[:3] == ["gh", "pr", "create"]:
            return _fail(stderr="gh: authentication required")
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="authentication required"):
            open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)


def test_subprocess_oserror_raises_pr_open_error(tmp_path):
    with patch("open_implementation_pr.subprocess.run", side_effect=OSError("gh not found")):
        with pytest.raises(open_implementation_pr.PROpenError, match="gh not found"):
            open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)


# --- state_base is forwarded to state_io.state_dir, not hardcoded -------------------------


# --- close_for_clarification --------------------------------------------------------------


def test_close_for_clarification_posts_comment_and_closes_pr():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.close_for_clarification(42, ["what about X?", "and Y?"])

    assert len(calls) == 1
    cmd = calls[0]
    assert cmd[:3] == ["gh", "pr", "close"]
    assert cmd[3] == "42"
    assert "--comment" in cmd
    comment = cmd[cmd.index("--comment") + 1]
    assert "what about X?" in comment
    assert "and Y?" in comment
    assert "--delete-branch" not in cmd


def test_close_for_clarification_subprocess_failure_raises_pr_open_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _fail(stderr="gh: pull request not found")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="not found"):
            open_implementation_pr.close_for_clarification(42, ["what about X?"])


def test_state_base_override_is_used_for_git_add_paths(tmp_path):
    custom_base = tmp_path / "custom-factory-base"
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if cmd[:3] == ["gh", "pr", "list"]:
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 1, "url": "https://github.com/org/repo/pull/1"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=custom_base)

    add_calls = [c for c in calls if c[:2] == ["git", "add"]]
    assert str(custom_base) in add_calls[0][2]
