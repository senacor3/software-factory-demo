# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for close_rejected_pr.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_close_rejected_pr.py

Covers the plan's I/O & Edge-Case Matrix: a reject at either gate closes the PR with a
comment naming the gate and reviewer (quoting the review comment when there is one); an
ordinary failure, a reject of the other gate only, and an already-closed PR all leave the
PR alone and succeed; any `gh` failure or malformed review history raises
`RejectCloseError`. `open_implementation_pr.find_open_pr`/`subprocess.run` are mocked
throughout -- no real `gh` process in the committed suite (mirrors test_merge_story.py).
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import close_rejected_pr
import open_implementation_pr

FIND_PR = "close_rejected_pr.open_implementation_pr.find_open_pr"
RUN = "close_rejected_pr.subprocess.run"


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stderr="boom"):
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


def _open_pr(pr_number=9, pr_url="https://github.com/org/repo/pull/9"):
    return {"branch": "software-factory/foo-bar/run-42", "pr_number": pr_number, "pr_url": pr_url}


def _review(state, environment, comment="", login="octo-reviewer"):
    return {
        "state": state,
        "comment": comment,
        "environments": [{"id": 1, "name": environment}],
        "user": {"login": login},
    }


def _gh(history, close=None):
    """`subprocess.run` stand-in: answers the review-history call with `history` (a
    Python object, JSON-encoded here, or a ready-made result) and `gh pr close` with
    `close`."""

    def run(cmd, **_kwargs):
        if cmd[:2] == ["gh", "api"]:
            return history if isinstance(history, SimpleNamespace) else _ok(json.dumps(history))
        if cmd[:3] == ["gh", "pr", "close"]:
            return close or _ok()
        raise AssertionError(f"unexpected command {cmd!r}")

    return run


def _close_calls(mock_run):
    return [c.args[0] for c in mock_run.call_args_list if c.args[0][:3] == ["gh", "pr", "close"]]


# --- reject closes the PR --------------------------------------------------------------


def test_reject_at_plan_approval_closes_pr():
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, return_value=_open_pr()) as find_pr, \
         patch(RUN, side_effect=_gh(history)) as mock_run:
        outcome = close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    assert mock_run.call_args_list[0].args[0] == [
        "gh", "api", "repos/{owner}/{repo}/actions/runs/42/approvals",
    ]
    find_pr.assert_called_once_with("software-factory/foo-bar/run-42", cwd=None)
    (close,) = _close_calls(mock_run)
    assert close[:5] == ["gh", "pr", "close", "9", "--comment"]
    assert "`plan-approval`" in close[5]
    assert "@octo-reviewer" in close[5]
    assert outcome == {"rejected": True, "pr": _open_pr()}


def test_reject_at_evidence_approval_closes_pr():
    history = [_review("approved", "plan-approval"), _review("rejected", "evidence-approval")]
    with patch(FIND_PR, return_value=_open_pr()), \
         patch(RUN, side_effect=_gh(history)) as mock_run:
        outcome = close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "evidence-approval")

    (close,) = _close_calls(mock_run)
    assert close[3] == "9"
    assert "`evidence-approval`" in close[5]
    assert "plan-approval" not in close[5]
    assert outcome["rejected"] is True
    assert outcome["pr"]["pr_number"] == 9


def test_reject_comment_quotes_review_comment_and_mentions_retrigger():
    history = [_review("rejected", "plan-approval", comment="Wrong approach.\nSplit the story.")]
    with patch(FIND_PR, return_value=_open_pr()), \
         patch(RUN, side_effect=_gh(history)) as mock_run:
        close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    (close,) = _close_calls(mock_run)
    assert "> Wrong approach.\n> Split the story." in close[5]
    assert "Re-triggering" in close[5]
    assert "new run" in close[5]


def test_reject_without_review_comment_has_no_quote():
    history = [_review("rejected", "plan-approval", comment="")]
    with patch(FIND_PR, return_value=_open_pr()), \
         patch(RUN, side_effect=_gh(history)) as mock_run:
        close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    (close,) = _close_calls(mock_run)
    assert "Review comment" not in close[5]
    assert ">" not in close[5]
    assert "new run" in close[5]


def test_close_never_deletes_branch_or_labels():
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, return_value=_open_pr()), \
         patch(RUN, side_effect=_gh(history)) as mock_run:
        close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    assert len(mock_run.call_args_list) == 2
    for call in mock_run.call_args_list:
        assert "--delete-branch" not in call.args[0]
        assert "--add-label" not in call.args[0]


# --- not a reject: PR left open ---------------------------------------------------------


def test_ordinary_job_2_failure_leaves_pr_open():
    history = [_review("approved", "plan-approval")]
    with patch(FIND_PR) as find_pr, patch(RUN, side_effect=_gh(history)) as mock_run:
        outcome = close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    assert outcome == {"rejected": False, "pr": None}
    find_pr.assert_not_called()
    assert _close_calls(mock_run) == []


def test_ordinary_job_3_failure_leaves_pr_open():
    history = [_review("approved", "plan-approval"), _review("approved", "evidence-approval")]
    with patch(FIND_PR) as find_pr, patch(RUN, side_effect=_gh(history)) as mock_run:
        outcome = close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "evidence-approval")

    assert outcome == {"rejected": False, "pr": None}
    find_pr.assert_not_called()
    assert _close_calls(mock_run) == []


def test_reject_of_other_gate_only_leaves_pr_open():
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR) as find_pr, patch(RUN, side_effect=_gh(history)) as mock_run:
        outcome = close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "evidence-approval")

    assert outcome == {"rejected": False, "pr": None}
    find_pr.assert_not_called()
    assert _close_calls(mock_run) == []


def test_empty_review_history_is_not_a_reject():
    with patch(FIND_PR) as find_pr, patch(RUN, side_effect=_gh([])) as mock_run:
        outcome = close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    assert outcome == {"rejected": False, "pr": None}
    find_pr.assert_not_called()
    assert _close_calls(mock_run) == []


def test_rejected_but_pr_already_closed_closes_nothing():
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, return_value=None), patch(RUN, side_effect=_gh(history)) as mock_run:
        outcome = close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    assert outcome == {"rejected": True, "pr": None}
    assert _close_calls(mock_run) == []


# --- API or gh failure ------------------------------------------------------------------


def test_review_history_call_failure_raises():
    with patch(FIND_PR) as find_pr, \
         patch(RUN, side_effect=_gh(_fail(stderr="HTTP 403: Resource not accessible"))):
        with pytest.raises(close_rejected_pr.RejectCloseError, match="HTTP 403"):
            close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    find_pr.assert_not_called()


def test_subprocess_oserror_raises():
    with patch(RUN, side_effect=OSError("gh not found")):
        with pytest.raises(close_rejected_pr.RejectCloseError, match="gh not found"):
            close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")


@pytest.mark.parametrize(
    "stdout",
    [
        "not json",
        "",
        '{"message": "Not Found"}',
        '["rejected"]',
        '[{"state": "rejected", "environments": "plan-approval"}]',
    ],
)
def test_malformed_review_history_raises(stdout):
    with patch(FIND_PR) as find_pr, patch(RUN, side_effect=_gh(_ok(stdout))) as mock_run:
        with pytest.raises(close_rejected_pr.RejectCloseError):
            close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    find_pr.assert_not_called()
    assert _close_calls(mock_run) == []


def test_pr_lookup_failure_raises():
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, side_effect=open_implementation_pr.PROpenError("gh: authentication required")), \
         patch(RUN, side_effect=_gh(history)) as mock_run:
        with pytest.raises(close_rejected_pr.RejectCloseError, match="authentication required"):
            close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")

    assert _close_calls(mock_run) == []


def test_pr_lookup_malformed_json_raises():
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, side_effect=json.JSONDecodeError("Expecting value", "oops", 0)), \
         patch(RUN, side_effect=_gh(history)):
        with pytest.raises(close_rejected_pr.RejectCloseError, match="PR lookup"):
            close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")


def test_gh_pr_close_failure_raises():
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, return_value=_open_pr()), \
         patch(RUN, side_effect=_gh(history, close=_fail(stderr="GraphQL: Resource not accessible"))):
        with pytest.raises(close_rejected_pr.RejectCloseError, match="Resource not accessible"):
            close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "plan-approval")


def test_unknown_gate_raises_without_calling_gh():
    with patch(RUN) as mock_run:
        with pytest.raises(close_rejected_pr.RejectCloseError, match="unknown gate"):
            close_rejected_pr.close_rejected_pr("foo-bar", "run-42", 42, "prod")

    mock_run.assert_not_called()


# --- CLI --------------------------------------------------------------------------------

ARGV = ["--story-slug", "foo-bar", "--run-id", "run-42", "--github-run-id", "42", "--gate", "plan-approval"]


def test_main_reject_prints_closed_pr(capsys):
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, return_value=_open_pr()), patch(RUN, side_effect=_gh(history)):
        assert close_rejected_pr.main(ARGV) == 0

    assert json.loads(capsys.readouterr().out) == {
        "ok": True, "gate": "plan-approval", "rejected": True, "closed_pr_number": 9,
    }


def test_main_not_a_reject_succeeds_and_says_so(capsys):
    history = [_review("approved", "plan-approval")]
    with patch(FIND_PR), patch(RUN, side_effect=_gh(history)):
        assert close_rejected_pr.main(ARGV) == 0

    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "ok": True, "gate": "plan-approval", "rejected": False, "closed_pr_number": None,
    }
    assert "not a reject" in captured.err


def test_main_reject_without_open_pr_succeeds_and_says_so(capsys):
    history = [_review("rejected", "plan-approval")]
    with patch(FIND_PR, return_value=None), patch(RUN, side_effect=_gh(history)):
        assert close_rejected_pr.main(ARGV) == 0

    captured = capsys.readouterr()
    assert json.loads(captured.out) == {
        "ok": True, "gate": "plan-approval", "rejected": True, "closed_pr_number": None,
    }
    assert "nothing to close" in captured.err


def test_main_failure_exits_1_with_command_and_output(capsys):
    with patch(RUN, side_effect=_gh(_fail(stderr="HTTP 500"))):
        assert close_rejected_pr.main(ARGV) == 1

    err = capsys.readouterr().err
    assert "actions/runs/42/approvals" in err
    assert "HTTP 500" in err
