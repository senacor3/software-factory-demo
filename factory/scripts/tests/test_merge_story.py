# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for merge_story.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_merge_story.py

Covers the plan's I/O & Edge-Case Matrix: a successful squash-merge-with-branch-delete,
a `gh pr merge` failure (conflict or otherwise) raising `MergeError`, and no open PR
found also raising `MergeError`. `open_implementation_pr.find_open_pr`/`subprocess.run`
are mocked throughout -- no real `gh` process in the committed suite (mirrors
test_open_implementation_pr.py).
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import merge_story
import open_implementation_pr


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stderr="boom"):
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


def _open_pr(pr_number=7, pr_url="https://github.com/org/repo/pull/7"):
    return {"branch": "light-factory/foo-bar/run-1", "pr_number": pr_number, "pr_url": pr_url}


# --- merge succeeds --------------------------------------------------------------------


def test_merge_succeeds_runs_squash_delete_branch():
    with patch("merge_story.open_implementation_pr.find_open_pr", return_value=_open_pr()) as find_pr, \
         patch("merge_story.subprocess.run", return_value=_ok()) as mock_run:
        outcome = merge_story.merge_story("foo-bar", "run-1")

    find_pr.assert_called_once_with("light-factory/foo-bar/run-1", cwd=None)
    cmd = mock_run.call_args.args[0]
    assert cmd == ["gh", "pr", "merge", "7", "--squash", "--delete-branch"]
    assert outcome["pr"]["pr_number"] == 7


# --- merge fails (conflict or other gh failure) -----------------------------------------


def test_gh_pr_merge_failure_raises_merge_error():
    with patch("merge_story.open_implementation_pr.find_open_pr", return_value=_open_pr()), \
         patch("merge_story.subprocess.run", return_value=_fail(stderr="CONFLICT: merge conflict in foo.py")):
        with pytest.raises(merge_story.MergeError, match="CONFLICT"):
            merge_story.merge_story("foo-bar", "run-1")


def test_subprocess_oserror_raises_merge_error():
    with patch("merge_story.open_implementation_pr.find_open_pr", return_value=_open_pr()), \
         patch("merge_story.subprocess.run", side_effect=OSError("gh not found")):
        with pytest.raises(merge_story.MergeError, match="gh not found"):
            merge_story.merge_story("foo-bar", "run-1")


# --- no open PR found --------------------------------------------------------------------


def test_no_open_pr_raises_merge_error():
    with patch("merge_story.open_implementation_pr.find_open_pr", return_value=None), \
         patch("merge_story.subprocess.run") as mock_run:
        with pytest.raises(merge_story.MergeError, match="no open PR"):
            merge_story.merge_story("foo-bar", "run-1")

    mock_run.assert_not_called()


def test_find_open_pr_failure_raises_merge_error():
    with patch(
        "merge_story.open_implementation_pr.find_open_pr",
        side_effect=open_implementation_pr.PROpenError("gh: authentication required"),
    ), pytest.raises(merge_story.MergeError, match="authentication required"):
        merge_story.merge_story("foo-bar", "run-1")
