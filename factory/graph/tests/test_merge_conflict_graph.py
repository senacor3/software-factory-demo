# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for merge_conflict_graph.py. Run:
uv run --with pytest pytest factory/graph/tests/test_merge_conflict_graph.py

Covers the I/O & Edge-Case Matrix in story-bounded-merge-conflict-resolution-loop-plan.md:
no conflict (skip the loop entirely, commit/push immediately, attempts: 0), a conflict
resolved on attempt 1, a conflict resolved on attempt 2 (the loop re-invokes the agent
against the same conflicted paths), the hard cap of 2 attempts still unresolved
(ConflictCapReachedError, merge aborted, no commit), the orchestrator claim call
failing, the agent's own tooling call failing, the initial merge-attempt's git step
failing, and the final commit/push step failing.

`attempt_target_merge.attempt_merge`/`has_unresolved_markers`/`abort_merge` and
`claim_merge_attempt.claim` are mocked wholesale (their own bodies are tested
elsewhere); `commit_push_implementation.commit_and_push` is mocked too.
`merge_conflict_graph`'s own `subprocess.run` (the `claude` CLI invocation inside
`invoke_skill`) is mocked separately -- a distinct module attribute from
`attempt_target_merge.subprocess`, so mocking one never affects the other.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import merge_conflict_graph

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import attempt_target_merge
import checkout_branch
import claim_merge_attempt
import commit_push_implementation

FAKE_BRANCH = "software-factory/foo/run-1"
ORCHESTRATOR_URL = "https://orchestrator.example/callback"
SECRET = "the-shared-secret"


def _fake_proc(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _call_kwargs():
    return {
        "orchestrator_url": ORCHESTRATOR_URL,
        "stage_callback_secret": SECRET,
    }


# --- I/O Matrix row 1: no conflict ----------------------------------------------------


def test_no_conflict_commits_immediately_with_zero_attempts():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge", return_value=(False, [])
    ), \
         patch("merge_conflict_graph.claim_merge_attempt.claim") as mock_claim, \
         patch("merge_conflict_graph.subprocess.run") as mock_run, \
         patch(
             "merge_conflict_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ) as mock_commit:
        outcome = merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    assert outcome == {"resolved": True, "attempts": 0}
    mock_claim.assert_not_called()
    mock_run.assert_not_called()
    mock_commit.assert_called_once_with(
        FAKE_BRANCH, "foo", "run-1", cwd=None, label="Conflict Resolution"
    )


# --- AD-5's second enforcement layer: the owned-state-file deny rule -------------------


def test_build_command_includes_ad5_deny_settings():
    cmd = merge_conflict_graph._build_command(["a.py"], "claude")

    assert "--settings" in cmd
    settings = json.loads(cmd[cmd.index("--settings") + 1])
    assert settings == merge_conflict_graph.DENY_SETTINGS
    assert "Edit(.factory/**/plan.md)" in settings["permissions"]["deny"]
    assert "Edit(.factory/**/decisions.md)" in settings["permissions"]["deny"]
    assert "Edit(.factory/**/review.md)" in settings["permissions"]["deny"]
    assert "Edit(.factory/**/checks.md)" in settings["permissions"]["deny"]


# --- I/O Matrix row 2: resolved on attempt 1 -------------------------------------------


def test_conflict_resolved_on_first_attempt():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py", "b.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch("merge_conflict_graph.claim_merge_attempt.claim", return_value=1) as mock_claim, \
         patch("merge_conflict_graph.subprocess.run", return_value=_fake_proc(stdout="done")) as mock_run, \
         patch(
             "merge_conflict_graph.attempt_target_merge.has_unresolved_markers", return_value=False
         ) as mock_markers, \
         patch(
             "merge_conflict_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ) as mock_commit:
        outcome = merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    assert outcome == {"resolved": True, "attempts": 1}
    mock_claim.assert_called_once_with(ORCHESTRATOR_URL, SECRET, "foo", "run-1")
    mock_run.assert_called_once()
    prompt = mock_run.call_args.args[0][2]
    assert prompt == "/software-factory-merge-conflict-resolution a.py b.py"
    mock_markers.assert_called_once_with(["a.py", "b.py"], cwd=None)
    mock_commit.assert_called_once_with(
        FAKE_BRANCH, "foo", "run-1", cwd=None, label="Conflict Resolution"
    )


# --- I/O Matrix row 3: resolved on attempt 2 -------------------------------------------


def test_conflict_resolved_on_second_attempt_reinvokes_same_paths():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch(
             "merge_conflict_graph.claim_merge_attempt.claim", side_effect=[1, 2]
         ) as mock_claim, \
         patch(
             "merge_conflict_graph.subprocess.run", return_value=_fake_proc(stdout="done")
         ) as mock_run, \
         patch(
             "merge_conflict_graph.attempt_target_merge.has_unresolved_markers",
             side_effect=[True, False],
         ) as mock_markers, \
         patch(
             "merge_conflict_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ) as mock_commit:
        outcome = merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    assert outcome == {"resolved": True, "attempts": 2}
    assert mock_claim.call_count == 2
    assert mock_run.call_count == 2  # the agent was re-invoked
    assert mock_markers.call_count == 2
    # same conflicted-path list both times -- never re-derived
    for call in mock_run.call_args_list:
        assert call.args[0][2] == "/software-factory-merge-conflict-resolution a.py"
    mock_commit.assert_called_once()


# --- I/O Matrix row 4: still unresolved after the cap -----------------------------------


def test_cap_reached_aborts_merge_and_raises_no_commit():
    # Exactly 2 real agent attempts, both still conflicted, must cost exactly 2
    # claim() calls -- the 3rd (cap-reached) iteration is decided from this
    # execution's own already-claimed count, never a 3rd claim (so the DynamoDB
    # counter ends at exactly the cap, not one past it).
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch(
             "merge_conflict_graph.claim_merge_attempt.claim", side_effect=[1, 2]
         ) as mock_claim, \
         patch(
             "merge_conflict_graph.subprocess.run", return_value=_fake_proc(stdout="done")
         ) as mock_run, \
         patch(
             "merge_conflict_graph.attempt_target_merge.has_unresolved_markers", return_value=True
         ), \
         patch("merge_conflict_graph.attempt_target_merge.abort_merge") as mock_abort, \
         patch(
             "merge_conflict_graph.commit_push_implementation.commit_and_push"
         ) as mock_commit:
        with pytest.raises(merge_conflict_graph.ConflictCapReachedError, match="cap of 2 reached"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    assert mock_claim.call_count == 2
    assert mock_run.call_count == 2  # exactly 2 real agent attempts, never a 3rd
    mock_abort.assert_called_once_with(cwd=None)
    mock_commit.assert_not_called()


def test_cap_reached_via_a_claim_already_over_cap_also_aborts():
    # The rarer case: this execution's own first claim() already comes back over the
    # cap (e.g. a prior, crashed job attempt already spent some of the budget) --
    # caught right after that single claim, no agent invocation at all.
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch(
             "merge_conflict_graph.claim_merge_attempt.claim", return_value=3
         ) as mock_claim, \
         patch("merge_conflict_graph.subprocess.run") as mock_run, \
         patch(
             "merge_conflict_graph.attempt_target_merge.has_unresolved_markers", return_value=True
         ), \
         patch("merge_conflict_graph.attempt_target_merge.abort_merge") as mock_abort, \
         patch(
             "merge_conflict_graph.commit_push_implementation.commit_and_push"
         ) as mock_commit:
        with pytest.raises(merge_conflict_graph.ConflictCapReachedError, match="attempt 3 exceeds"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    mock_claim.assert_called_once()
    mock_run.assert_not_called()
    mock_abort.assert_called_once_with(cwd=None)
    mock_commit.assert_not_called()


# --- fail-safe: a conflicted path with no content-marker conflict ----------------------


def test_unsupported_conflict_type_aborts_before_any_claim():
    def markers_side_effect(paths, cwd=None):
        # The fail-safe check calls has_unresolved_markers once per path -- "b.py"
        # has no marker at all (e.g. a delete/modify conflict).
        return paths != ["b.py"]

    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py", "b.py"]),
    ), \
         patch(
             "merge_conflict_graph.attempt_target_merge.has_unresolved_markers",
             side_effect=markers_side_effect,
         ), \
         patch("merge_conflict_graph.attempt_target_merge.abort_merge") as mock_abort, \
         patch("merge_conflict_graph.claim_merge_attempt.claim") as mock_claim, \
         patch("merge_conflict_graph.subprocess.run") as mock_run, \
         patch(
             "merge_conflict_graph.commit_push_implementation.commit_and_push"
         ) as mock_commit:
        with pytest.raises(merge_conflict_graph.UnsupportedConflictTypeError, match="b.py"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    mock_abort.assert_called_once_with(cwd=None)
    mock_claim.assert_not_called()
    mock_run.assert_not_called()
    mock_commit.assert_not_called()


# --- I/O Matrix row 5: the claim-merge-conflict-attempt request -------------------------


def test_claim_failure_propagates_before_any_agent_invocation():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch(
             "merge_conflict_graph.claim_merge_attempt.claim",
             side_effect=claim_merge_attempt.ClaimMergeAttemptError("orchestrator unreachable"),
         ), \
         patch("merge_conflict_graph.subprocess.run") as mock_run:
        with pytest.raises(claim_merge_attempt.ClaimMergeAttemptError, match="orchestrator unreachable"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    mock_run.assert_not_called()


# --- agent tooling failure --------------------------------------------------------------


def test_agent_invocation_failure_propagates_no_commit():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch("merge_conflict_graph.claim_merge_attempt.claim", return_value=1), \
         patch(
             "merge_conflict_graph.subprocess.run",
             return_value=_fake_proc(returncode=1, stderr="claude CLI broke"),
         ), \
         patch(
             "merge_conflict_graph.commit_push_implementation.commit_and_push"
         ) as mock_commit:
        with pytest.raises(merge_conflict_graph.MergeConflictInvocationError, match="claude CLI broke"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    mock_commit.assert_not_called()


# --- initial merge-attempt git step failure ----------------------------------------------


def test_initial_merge_attempt_checkout_error_propagates():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ), patch("merge_conflict_graph.claim_merge_attempt.claim") as mock_claim:
        with pytest.raises(checkout_branch.CheckoutError, match="branch not found"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())

    mock_claim.assert_not_called()


def test_initial_merge_attempt_merge_error_propagates():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        side_effect=attempt_target_merge.MergeAttemptError("couldn't find remote ref"),
    ):
        with pytest.raises(attempt_target_merge.MergeAttemptError, match="couldn't find remote ref"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())


# --- commit/push failure -----------------------------------------------------------------


def test_commit_push_failure_propagates_after_clean_resolution():
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge", return_value=(False, [])
    ), patch(
        "merge_conflict_graph.commit_push_implementation.commit_and_push",
        side_effect=commit_push_implementation.CommitPushError("push rejected"),
    ):
        with pytest.raises(commit_push_implementation.CommitPushError, match="push rejected"):
            merge_conflict_graph.run_conflict_resolution("foo", "run-1", **_call_kwargs())


# --- CLI exit codes -----------------------------------------------------------------------


def _cli_args():
    return [
        "--story-slug", "foo",
        "--run-id", "run-1",
        "--orchestrator-url", ORCHESTRATOR_URL,
        "--stage-callback-secret", SECRET,
    ]


def test_cli_success_exits_0(capsys):
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge", return_value=(False, [])
    ), patch(
        "merge_conflict_graph.commit_push_implementation.commit_and_push",
        return_value={"committed": True},
    ):
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 0
    assert json.loads(captured.out.strip()) == {"ok": True, "resolved": True, "attempts": 0}


def test_cli_invocation_failure_exits_3(capsys):
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch("merge_conflict_graph.claim_merge_attempt.claim", return_value=1), \
         patch(
             "merge_conflict_graph.subprocess.run",
             return_value=_fake_proc(returncode=1, stderr="claude CLI broke"),
         ):
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 3
    assert "claude CLI broke" in captured.err


def test_cli_claim_failure_also_exits_3(capsys):
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), patch("merge_conflict_graph._paths_without_markers", return_value=[]), patch(
        "merge_conflict_graph.claim_merge_attempt.claim",
        side_effect=claim_merge_attempt.ClaimMergeAttemptError("orchestrator unreachable"),
    ):
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 3
    assert "orchestrator unreachable" in captured.err


def test_cli_git_checkout_failure_exits_4(capsys):
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ):
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 4
    assert "branch not found" in captured.err


def test_cli_merge_attempt_error_exits_4(capsys):
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        side_effect=attempt_target_merge.MergeAttemptError("couldn't find remote ref"),
    ):
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 4
    assert "couldn't find remote ref" in captured.err


def test_cli_commit_push_failure_exits_5(capsys):
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge", return_value=(False, [])
    ), patch(
        "merge_conflict_graph.commit_push_implementation.commit_and_push",
        side_effect=commit_push_implementation.CommitPushError("push rejected"),
    ):
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 5
    assert "push rejected" in captured.err


def test_cli_cap_reached_exits_6(capsys):
    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py"]),
    ), \
         patch("merge_conflict_graph._paths_without_markers", return_value=[]), \
         patch(
             "merge_conflict_graph.claim_merge_attempt.claim", side_effect=[1, 2]
         ) as mock_claim, \
         patch(
             "merge_conflict_graph.subprocess.run", return_value=_fake_proc(stdout="done")
         ), \
         patch(
             "merge_conflict_graph.attempt_target_merge.has_unresolved_markers", return_value=True
         ), \
         patch("merge_conflict_graph.attempt_target_merge.abort_merge"):
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 6
    assert "cap" in captured.err.lower()
    assert mock_claim.call_count == 2


def test_cli_unsupported_conflict_type_exits_7(capsys):
    def markers_side_effect(paths, cwd=None):
        return paths != ["b.py"]

    with patch(
        "merge_conflict_graph.attempt_target_merge.attempt_merge",
        return_value=(True, ["a.py", "b.py"]),
    ), \
         patch(
             "merge_conflict_graph.attempt_target_merge.has_unresolved_markers",
             side_effect=markers_side_effect,
         ), \
         patch("merge_conflict_graph.attempt_target_merge.abort_merge"), \
         patch("merge_conflict_graph.claim_merge_attempt.claim") as mock_claim:
        rc = merge_conflict_graph.main(_cli_args())

    captured = capsys.readouterr()
    assert rc == 7
    assert "b.py" in captured.err
    mock_claim.assert_not_called()
