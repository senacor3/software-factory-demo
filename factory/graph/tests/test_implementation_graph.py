# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for implementation_graph.py. Run:
uv run --with pytest pytest factory/graph/tests/test_implementation_graph.py

Covers the I/O & Edge-Case Matrix in story-implementation-agent-plan.md: full-sequence
success (changes made -> committed), full-sequence no-op (no changes -> not committed),
checkout failure (agent never invoked), `claude` CLI tooling failure (no commit
attempted), and commit/push failure after the agent succeeded. The `claude` subprocess
call is mocked throughout -- no live CLI/network dependency -- and
`checkout_branch.checkout_branch` / `commit_push_implementation.commit_and_push` are
mocked wholesale here (their own real bodies are tested in
factory/scripts/tests/test_checkout_branch.py and
factory/scripts/tests/test_commit_push_implementation.py); no real `git` process ever
runs in this suite.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import implementation_graph

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import checkout_branch
import commit_push_implementation


def _fake_proc(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


FAKE_BRANCH = "light-factory/foo/run-1"


# --- full sequence: agent makes changes, committed = True --------------------------------


def test_full_sequence_success_commits_and_pushes(tmp_path):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH) as mock_checkout, \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(stdout="done")) as mock_run, \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ) as mock_commit:
        outcome = implementation_graph.run_implementation("foo", "run-1", state_base=tmp_path)

    assert outcome == {"branch": FAKE_BRANCH, "output": "done", "committed": True}
    mock_checkout.assert_called_once_with("foo", "run-1", cwd=None)
    mock_run.assert_called_once()
    mock_commit.assert_called_once_with(FAKE_BRANCH, "foo", "run-1", cwd=None)


# --- full sequence: agent makes no changes, committed = False (not an error) -------------


def test_full_sequence_no_op_is_not_an_error(tmp_path):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(stdout="nothing to do")), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": False},
         ):
        outcome = implementation_graph.run_implementation("foo", "run-1", state_base=tmp_path)

    assert outcome["committed"] is False


# --- checkout failure: agent is never invoked ---------------------------------------------


def test_checkout_failure_prevents_agent_invocation(tmp_path):
    with patch(
        "implementation_graph.checkout_branch.checkout_branch",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ), patch("implementation_graph.subprocess.run") as mock_run, patch(
        "implementation_graph.commit_push_implementation.commit_and_push"
    ) as mock_commit:
        with pytest.raises(checkout_branch.CheckoutError, match="branch not found"):
            implementation_graph.run_implementation("foo", "run-1", state_base=tmp_path)

    mock_run.assert_not_called()
    mock_commit.assert_not_called()


# --- claude CLI invocation itself fails: no commit attempted ------------------------------


def test_cli_nonzero_exit_raises_invocation_error_no_commit_attempted(tmp_path):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(returncode=1, stderr="boom")), \
         patch("implementation_graph.commit_push_implementation.commit_and_push") as mock_commit:
        with pytest.raises(implementation_graph.ImplementationInvocationError, match="boom"):
            implementation_graph.run_implementation("foo", "run-1", state_base=tmp_path)

    mock_commit.assert_not_called()


def test_subprocess_oserror_raises_invocation_error(tmp_path):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", side_effect=OSError("claude not found")), \
         patch("implementation_graph.commit_push_implementation.commit_and_push") as mock_commit:
        with pytest.raises(implementation_graph.ImplementationInvocationError, match="claude not found"):
            implementation_graph.run_implementation("foo", "run-1", state_base=tmp_path)

    mock_commit.assert_not_called()


# --- commit/push fails after the agent succeeded -------------------------------------------


def test_commit_push_failure_raises_commit_push_error_distinct_from_others(tmp_path):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(stdout="done")), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             side_effect=commit_push_implementation.CommitPushError("push rejected"),
         ):
        with pytest.raises(commit_push_implementation.CommitPushError, match="push rejected"):
            implementation_graph.run_implementation("foo", "run-1", state_base=tmp_path)


# --- command construction: AD-5's two enforcement layers ------------------------------------


def test_build_command_never_includes_bash_git_gh_or_merge_tools():
    cmd = implementation_graph._build_command("plan.md", "decisions.md", "claude")
    allowed_idx = cmd.index("--allowedTools") + 1
    allowed_tools = cmd[allowed_idx]
    assert allowed_tools == "Read Write Edit Grep Glob"
    for forbidden in ("Bash", "git", "gh"):
        assert forbidden not in allowed_tools


def test_build_command_includes_settings_deny_rule_for_state_files():
    cmd = implementation_graph._build_command("plan.md", "decisions.md", "claude")
    settings_idx = cmd.index("--settings") + 1
    settings = json.loads(cmd[settings_idx])
    deny = settings["permissions"]["deny"]
    assert "Edit(.factory/**/plan.md)" in deny
    assert "Edit(.factory/**/decisions.md)" in deny
    assert "Edit(.factory/**/review.md)" in deny


def test_build_command_passes_both_plan_and_decisions_paths():
    cmd = implementation_graph._build_command("some/plan.md", "some/decisions.md", "claude")
    assert "/light-factory-implementation some/plan.md some/decisions.md" in cmd


# --- review_path (fix cycle, AD-11) -----------------------------------------------------


def test_build_command_omits_review_path_when_not_given():
    cmd = implementation_graph._build_command("plan.md", "decisions.md", "claude")
    assert "/light-factory-implementation plan.md decisions.md" in cmd


def test_build_command_appends_review_path_when_given():
    cmd = implementation_graph._build_command(
        "plan.md", "decisions.md", "claude", review_path="review.md"
    )
    assert "/light-factory-implementation plan.md decisions.md review.md" in cmd


def test_run_implementation_passes_review_path_through_to_invoke_skill(tmp_path):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(stdout="done")) as mock_run, \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ):
        implementation_graph.run_implementation(
            "foo", "run-1", state_base=tmp_path, review_path="some/review.md"
        )

    cmd = mock_run.call_args[0][0]
    prompt = cmd[cmd.index("-p") + 1]
    assert prompt.endswith("some/review.md")


def test_run_implementation_without_review_path_unchanged_behavior(tmp_path):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(stdout="done")) as mock_run, \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ):
        implementation_graph.run_implementation("foo", "run-1", state_base=tmp_path)

    cmd = mock_run.call_args[0][0]
    prompt = cmd[cmd.index("-p") + 1]
    assert len(prompt.split(" ")) == 3  # "/light-factory-implementation <plan> <decisions>" only


# --- CLI exit codes --------------------------------------------------------------------------


def test_cli_main_checkout_error_exits_2(capsys):
    with patch(
        "implementation_graph.checkout_branch.checkout_branch",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ):
        rc = implementation_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 2
    assert "branch not found" in captured.err


def test_cli_main_invocation_error_exits_3(capsys):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(returncode=2, stderr="tool broke")):
        rc = implementation_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 3
    assert "tool broke" in captured.err


def test_cli_main_commit_push_error_exits_4(capsys):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(stdout="done")), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             side_effect=commit_push_implementation.CommitPushError("push rejected"),
         ):
        rc = implementation_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 4
    assert "push rejected" in captured.err


def test_cli_main_success_exits_0(capsys):
    with patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch("implementation_graph.subprocess.run", return_value=_fake_proc(stdout="done")), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ):
        rc = implementation_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out == {"ok": True, "committed": True}
