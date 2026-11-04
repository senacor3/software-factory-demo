# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for attempt_target_merge.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_attempt_target_merge.py

Covers the I/O & Edge-Case Matrix rows for the merge-conflict probe: a clean merge, a
real conflict (conflicted paths captured from `git diff --name-only --diff-filter=U`),
a fetch/merge failure for a reason other than a conflict (`MergeAttemptError`), a
checkout failure propagating `checkout_branch.CheckoutError` untouched,
`has_unresolved_markers`'s marker-scan, and the CLI's always-abort + `has-conflict=`
output. `checkout_branch.checkout_branch` is mocked wholesale (its own body is tested
in test_checkout_branch.py); `subprocess.run` is mocked throughout -- no real `git`
process in the committed suite.
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import attempt_target_merge
import checkout_branch

FAKE_BRANCH = "software-factory/foo/run-1"


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stdout="", stderr="boom"):
    return SimpleNamespace(returncode=1, stdout=stdout, stderr=stderr)


def _dispatcher(merge_result, diff_stdout=""):
    """Routes `subprocess.run` calls: fetch/abort succeed, merge returns the given
    result, diff (only reached on a real conflict) returns `diff_stdout`."""

    def run(cmd, **kwargs):
        if cmd[:2] == ["git", "fetch"]:
            return _ok()
        if cmd[:2] == ["git", "merge"] and "--abort" in cmd:
            return _ok()
        if cmd[:2] == ["git", "merge"]:
            return merge_result
        if cmd[:3] == ["git", "diff", "--name-only"]:
            return _ok(stdout=diff_stdout)
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    return run


# --- attempt_merge: clean merge -------------------------------------------------------


def test_clean_merge_returns_false_and_no_conflicted_paths():
    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("attempt_target_merge.subprocess.run", side_effect=_dispatcher(_ok())):
        has_conflict, paths = attempt_target_merge.attempt_merge("foo", "run-1", "main")

    assert has_conflict is False
    assert paths == []


# --- attempt_merge: real conflict -----------------------------------------------------


def test_conflict_returns_true_and_conflicted_paths_from_git_diff():
    merge_fail = _fail(stdout="CONFLICT (content): Merge conflict in a.py\nAutomatic merge failed")

    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "attempt_target_merge.subprocess.run",
             side_effect=_dispatcher(merge_fail, diff_stdout="a.py\nb.py\n"),
         ):
        has_conflict, paths = attempt_target_merge.attempt_merge("foo", "run-1", "main")

    assert has_conflict is True
    assert paths == ["a.py", "b.py"]


def test_conflict_detected_from_stderr_too():
    merge_fail = _fail(stderr="CONFLICT (content): Merge conflict in a.py")

    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "attempt_target_merge.subprocess.run",
             side_effect=_dispatcher(merge_fail, diff_stdout="a.py\n"),
         ):
        has_conflict, paths = attempt_target_merge.attempt_merge("foo", "run-1", "main")

    assert has_conflict is True
    assert paths == ["a.py"]


# --- attempt_merge: failures other than a real conflict -------------------------------


def test_fetch_failure_raises_merge_attempt_error():
    def run(cmd, **kwargs):
        if cmd[:2] == ["git", "fetch"]:
            return _fail(stderr="fatal: couldn't find remote ref main")
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("attempt_target_merge.subprocess.run", side_effect=run):
        with pytest.raises(attempt_target_merge.MergeAttemptError, match="couldn't find remote ref"):
            attempt_target_merge.attempt_merge("foo", "run-1", "main")


def test_merge_failure_without_conflict_text_raises_merge_attempt_error():
    merge_fail = _fail(stderr="fatal: not something we can merge")

    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("attempt_target_merge.subprocess.run", side_effect=_dispatcher(merge_fail)):
        with pytest.raises(attempt_target_merge.MergeAttemptError, match="not something we can merge"):
            attempt_target_merge.attempt_merge("foo", "run-1", "main")


def test_subprocess_oserror_during_merge_raises_merge_attempt_error():
    def run(cmd, **kwargs):
        if cmd[:2] == ["git", "fetch"]:
            return _ok()
        if cmd[:2] == ["git", "merge"]:
            raise OSError("git not found")
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("attempt_target_merge.subprocess.run", side_effect=run):
        with pytest.raises(attempt_target_merge.MergeAttemptError, match="git not found"):
            attempt_target_merge.attempt_merge("foo", "run-1", "main")


# --- attempt_merge: checkout failure propagates untouched -----------------------------


def test_checkout_failure_propagates_checkout_error_before_any_fetch():
    with patch(
        "attempt_target_merge.checkout_branch.checkout_branch",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ), patch("attempt_target_merge.subprocess.run") as mock_run:
        with pytest.raises(checkout_branch.CheckoutError, match="branch not found"):
            attempt_target_merge.attempt_merge("foo", "run-1", "main")

    mock_run.assert_not_called()


# --- has_unresolved_markers -----------------------------------------------------------


def test_has_unresolved_markers_true_when_marker_present(tmp_path):
    path = tmp_path / "a.py"
    path.write_text("<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> main\n")

    assert attempt_target_merge.has_unresolved_markers(["a.py"], cwd=tmp_path) is True


def test_has_unresolved_markers_false_when_resolved(tmp_path):
    path = tmp_path / "a.py"
    path.write_text("resolved content\n")

    assert attempt_target_merge.has_unresolved_markers(["a.py"], cwd=tmp_path) is False


def test_has_unresolved_markers_checks_every_given_path(tmp_path):
    (tmp_path / "a.py").write_text("resolved\n")
    (tmp_path / "b.py").write_text("<<<<<<< HEAD\nstill conflicted\n")

    assert attempt_target_merge.has_unresolved_markers(["a.py", "b.py"], cwd=tmp_path) is True


# --- CLI -------------------------------------------------------------------------------


def test_cli_prints_has_conflict_false_and_always_aborts(capsys):
    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("attempt_target_merge.subprocess.run", side_effect=_dispatcher(_ok())) as mock_run:
        rc = attempt_target_merge.main(["--story-slug", "foo", "--run-id", "run-1"])

    assert rc == 0
    assert capsys.readouterr().out.strip() == "has-conflict=false"
    abort_calls = [c for c in mock_run.call_args_list if "--abort" in c.args[0]]
    assert len(abort_calls) == 1


def test_cli_prints_has_conflict_true_and_always_aborts(capsys):
    merge_fail = _fail(stdout="CONFLICT (content): Merge conflict in a.py")
    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "attempt_target_merge.subprocess.run",
             side_effect=_dispatcher(merge_fail, diff_stdout="a.py\n"),
         ) as mock_run:
        rc = attempt_target_merge.main(["--story-slug", "foo", "--run-id", "run-1"])

    assert rc == 0
    assert capsys.readouterr().out.strip() == "has-conflict=true"
    abort_calls = [c for c in mock_run.call_args_list if "--abort" in c.args[0]]
    assert len(abort_calls) == 1


def test_cli_checkout_failure_exits_1_and_aborts(capsys):
    with patch(
        "attempt_target_merge.checkout_branch.checkout_branch",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ), patch("attempt_target_merge.subprocess.run", return_value=_ok()) as mock_run:
        rc = attempt_target_merge.main(["--story-slug", "foo", "--run-id", "run-1"])

    captured = capsys.readouterr()
    assert rc == 1
    assert "branch not found" in captured.err
    mock_run.assert_called_once()
    assert "--abort" in mock_run.call_args.args[0]


def test_cli_merge_attempt_error_exits_2_and_aborts(capsys):
    def run(cmd, **kwargs):
        if cmd[:2] == ["git", "fetch"]:
            return _fail(stderr="fatal: couldn't find remote ref main")
        if "--abort" in cmd:
            return _ok()
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("attempt_target_merge.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("attempt_target_merge.subprocess.run", side_effect=run):
        rc = attempt_target_merge.main(["--story-slug", "foo", "--run-id", "run-1"])

    captured = capsys.readouterr()
    assert rc == 2
    assert "couldn't find remote ref" in captured.err
