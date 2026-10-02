# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for commit_push_implementation.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_commit_push_implementation.py

Covers the I/O & Edge-Case Matrix's committed and no-op rows plus commit/push-failure,
with `subprocess.run` mocked throughout -- no real `git` process in the committed
suite (mirrors test_open_implementation_pr.py).
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import commit_push_implementation  # noqa: E402


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stderr="boom"):
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


# --- no-op: clean working tree --------------------------------------------------------


def test_no_changes_returns_not_committed_and_attempts_no_commit():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if cmd[:2] == ["git", "status"]:
            return _ok(stdout="")
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("commit_push_implementation.subprocess.run", side_effect=fake_run):
        result = commit_push_implementation.commit_and_push("light-factory/foo/run-1", "foo", "run-1")

    assert result == {"committed": False}
    assert calls == [["git", "status", "--porcelain"]]


# --- committed: dirty working tree -----------------------------------------------------


def test_changes_adds_commits_and_pushes():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if cmd[:2] == ["git", "status"]:
            return _ok(stdout=" M some_file.py\n")
        return _ok()

    with patch("commit_push_implementation.subprocess.run", side_effect=fake_run):
        result = commit_push_implementation.commit_and_push("light-factory/foo/run-1", "foo", "run-1")

    assert result == {"committed": True}

    add_calls = [c for c in calls if c[:2] == ["git", "add"]]
    assert add_calls == [["git", "add", "-A"]]

    commit_calls = [c for c in calls if "commit" in c]
    assert len(commit_calls) == 1
    assert "user.name=light-factory-bot" in commit_calls[0]
    assert "user.email=light-factory-bot@users.noreply.github.com" in commit_calls[0]
    assert "foo" in commit_calls[0][-1] and "run-1" in commit_calls[0][-1]

    push_calls = [c for c in calls if c[:2] == ["git", "push"]]
    assert push_calls == [["git", "push", "origin", "light-factory/foo/run-1"]]


# --- failures raise CommitPushError, distinct from CheckoutError/ImplementationInvocationError --


def test_git_status_failure_raises_commit_push_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _fail(stderr="fatal: not a git repository")

    with patch("commit_push_implementation.subprocess.run", side_effect=fake_run):
        with pytest.raises(commit_push_implementation.CommitPushError, match="not a git repository"):
            commit_push_implementation.commit_and_push("light-factory/foo/run-1", "foo", "run-1")


def test_commit_failure_raises_commit_push_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[:2] == ["git", "status"]:
            return _ok(stdout=" M some_file.py\n")
        if "commit" in cmd:
            return _fail(stderr="fatal: unable to create commit")
        return _ok()

    with patch("commit_push_implementation.subprocess.run", side_effect=fake_run):
        with pytest.raises(commit_push_implementation.CommitPushError, match="unable to create commit"):
            commit_push_implementation.commit_and_push("light-factory/foo/run-1", "foo", "run-1")


def test_push_failure_raises_commit_push_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[:2] == ["git", "status"]:
            return _ok(stdout=" M some_file.py\n")
        if cmd[:2] == ["git", "push"]:
            return _fail(stderr="! [rejected] fetch first")
        return _ok()

    with patch("commit_push_implementation.subprocess.run", side_effect=fake_run):
        with pytest.raises(commit_push_implementation.CommitPushError, match="rejected"):
            commit_push_implementation.commit_and_push("light-factory/foo/run-1", "foo", "run-1")


def test_subprocess_oserror_raises_commit_push_error():
    with patch("commit_push_implementation.subprocess.run", side_effect=OSError("git not found")):
        with pytest.raises(commit_push_implementation.CommitPushError, match="git not found"):
            commit_push_implementation.commit_and_push("light-factory/foo/run-1", "foo", "run-1")
