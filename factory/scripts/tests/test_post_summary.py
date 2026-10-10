# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for post_summary.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_post_summary.py

Covers `post_comment` success (right `gh pr comment` call shape) and subprocess-failure
raising `PostCommentError`, with `subprocess.run` mocked throughout -- no real `gh`
process in the committed suite (mirrors test_open_implementation_pr.py).
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import post_summary


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stderr="boom"):
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


def test_post_comment_posts_the_right_gh_call():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        return _ok()

    with patch("post_summary.subprocess.run", side_effect=fake_run):
        post_summary.post_comment(42, "## Plan ready for review\n\nsome body")

    assert len(calls) == 1
    cmd = calls[0]
    assert cmd[:3] == ["gh", "pr", "comment"]
    assert cmd[3] == "42"
    assert "--body" in cmd
    assert cmd[cmd.index("--body") + 1] == "## Plan ready for review\n\nsome body"


def test_post_comment_subprocess_failure_raises_post_comment_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _fail(stderr="gh: pull request not found")

    with patch("post_summary.subprocess.run", side_effect=fake_run):
        with pytest.raises(post_summary.PostCommentError, match="not found"):
            post_summary.post_comment(42, "body")


def test_post_comment_oserror_raises_post_comment_error():
    with patch("post_summary.subprocess.run", side_effect=OSError("gh not found")):
        with pytest.raises(post_summary.PostCommentError, match="gh not found"):
            post_summary.post_comment(42, "body")
