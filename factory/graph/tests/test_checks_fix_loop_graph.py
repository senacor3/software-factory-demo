# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for checks_fix_loop_graph.py. Run:
uv run --with pytest pytest factory/graph/tests/test_checks_fix_loop_graph.py

Covers the I/O & Edge-Case Matrix in story-checks-failure-fix-loop-plan.md: one check
failing and fixed within the cap (fix_cycle: 1), the hard cap of 2 fix cycles still
failing (unresolved-after-cap, fix_cycle: 2), multiple simultaneous check failures
counted as one cycle (not two), and the implementation tooling failing mid-loop
(ImplementationInvocationError propagates, no recheck attempted). `implementation_graph`
is exercised for real (its own `claude` CLI invocation is mocked via the shared
`subprocess.run`, same pattern as test_fix_loop_graph.py); `run_checks.run_check` writes
real evidence files under tmp_path so this module's own evidence reads are exercised
for real too.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import checks_fix_loop_graph
import implementation_graph

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import checkout_branch
import commit_push_implementation
import run_checks
import state_io

FAKE_BRANCH = "light-factory/foo/run-1"


def _fake_proc(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _dispatcher(impl_result=None):
    """A `subprocess.run` side_effect routing only `/light-factory-implementation`
    calls (this graph never invokes `/light-factory-review`)."""

    def run(cmd, **kwargs):
        prompt = cmd[cmd.index("-p") + 1]
        if "/light-factory-implementation" in prompt:
            if impl_result is None:
                raise AssertionError("unexpected implementation invocation in this test")
            return impl_result
        raise AssertionError(f"unexpected subprocess invocation: {cmd}")

    return run


def _write_evidence(tmp_path, name, status, detail=""):
    path = state_io.state_dir("foo", "run-1", base=tmp_path) / "evidence" / "checks" / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": status, "command": ["x"], "returncode": 0 if status == "pass" else 1, "detail": detail}))


def _all_checks_initially_passing_except(tmp_path, failing_names, detail="broke"):
    for name in run_checks.CHECK_NAMES:
        if name in failing_names:
            _write_evidence(tmp_path, name, "fail", detail)
        else:
            _write_evidence(tmp_path, name, "pass")


# --- I/O Matrix row: one check fails, fixed in cycle 1 --------------------------------


def test_one_fix_cycle_resolves_a_single_failing_check(tmp_path):
    _all_checks_initially_passing_except(tmp_path, ["lint"], detail="lint broke")

    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("checks_fix_loop_graph.run_checks.run_check", return_value={"status": "pass", "command": ["x"], "returncode": 0, "detail": ""}) as mock_run_check:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 1
    assert outcome["failing"] == []
    mock_run.assert_called_once()  # exactly one implementation call
    mock_run_check.assert_called_once_with("lint", "foo", "run-1", state_base=tmp_path, cwd=None)

    # the implementation re-invocation carried checks.md as its added context
    impl_calls = [c for c in mock_run.call_args_list if "/light-factory-implementation" in c.args[0][2]]
    assert len(impl_calls) == 1
    assert impl_calls[0].args[0][2].endswith("checks.md")

    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert meta["status"] == "resolved"
    assert meta["fix_cycle"] == "1"
    assert "lint" not in body or "_none_" in body


# --- I/O Matrix row: multiple checks fail together, counted as one cycle --------------


def test_multiple_simultaneous_failures_counted_as_one_cycle(tmp_path):
    _all_checks_initially_passing_except(tmp_path, ["build", "lint"], detail="broke")

    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch(
             "checks_fix_loop_graph.run_checks.run_check",
             return_value={"status": "pass", "command": ["x"], "returncode": 0, "detail": ""},
         ) as mock_run_check:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 1  # one cycle, not two, despite two failing checks
    impl_calls = [c for c in mock_run.call_args_list if "/light-factory-implementation" in c.args[0][2]]
    assert len(impl_calls) == 1
    rerun_names = sorted(c.args[0] for c in mock_run_check.call_args_list)
    assert rerun_names == ["build", "lint"]  # only the failing checks are rerun, never the full suite

    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert meta["status"] == "resolved"
    assert meta["fix_cycle"] == "1"


# --- I/O Matrix row: same check still failing after 2 cycles --------------------------


def test_two_fix_cycles_still_failing_stops_at_cap(tmp_path):
    _all_checks_initially_passing_except(tmp_path, ["build"], detail="still broken")

    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch(
             "checks_fix_loop_graph.run_checks.run_check",
             return_value={"status": "fail", "command": ["x"], "returncode": 1, "detail": "still broken"},
         ):
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "unresolved-after-cap"
    assert outcome["fix_cycle"] == 2
    assert outcome["failing"] == ["build"]
    impl_calls = [c for c in mock_run.call_args_list if "/light-factory-implementation" in c.args[0][2]]
    assert len(impl_calls) == 2  # exactly 2 fix cycles, never a 3rd

    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert meta["status"] == "unresolved-after-cap"
    assert meta["fix_cycle"] == "2"
    assert "build" in body
    assert "still broken" in body


# --- I/O & Edge-Case Matrix row: checks job errored for a non-check reason -------------


def test_no_evidence_at_all_still_triggers_a_fix_cycle_against_every_check(tmp_path):
    """No evidence files at all (e.g. the checks job crashed in toolchain setup,
    before any of the 4 check steps ran) is handled like any other fix-cycle attempt:
    implementation is still re-engaged with whatever evidence exists (none)."""
    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch(
             "checks_fix_loop_graph.run_checks.run_check",
             return_value={"status": "pass", "command": ["x"], "returncode": 0, "detail": ""},
         ) as mock_run_check:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 1
    impl_calls = [c for c in mock_run.call_args_list if "/light-factory-implementation" in c.args[0][2]]
    assert len(impl_calls) == 1
    rerun_names = sorted(c.args[0] for c in mock_run_check.call_args_list)
    assert rerun_names == sorted(run_checks.CHECK_NAMES)  # every check treated as unknown/failing


# --- implementation tooling fails mid-loop ---------------------------------------------


def test_implementation_tooling_failure_stops_loop_no_recheck(tmp_path):
    _all_checks_initially_passing_except(tmp_path, ["build"], detail="broke")

    with patch(
        "subprocess.run",
        side_effect=_dispatcher(impl_result=_fake_proc(returncode=1, stderr="impl CLI broke")),
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
         ) as mock_commit, \
         patch("checks_fix_loop_graph.run_checks.run_check") as mock_run_check:
        with pytest.raises(
            implementation_graph.ImplementationInvocationError, match="impl CLI broke"
        ):
            checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    mock_commit.assert_not_called()
    mock_run_check.assert_not_called()  # no recheck attempted


# --- CLI exit codes ----------------------------------------------------------------------


def test_cli_main_success_exits_0_resolved(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _all_checks_initially_passing_except(tmp_path, ["lint"], detail="lint broke")

    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch(
             "checks_fix_loop_graph.run_checks.run_check",
             return_value={"status": "pass", "command": ["x"], "returncode": 0, "detail": ""},
         ):
        rc = checks_fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out == {"ok": True, "status": "resolved", "fix_cycle": 1}


def test_cli_main_capped_out_exits_1_not_0(capsys, tmp_path, monkeypatch):
    """Unlike fix_loop_graph.py's review loop (whose cap-out is a legitimate,
    non-failing outcome left to the evidence-approval gate), checks-fix-loop's
    cap-out must fail the job -- otherwise `review`'s widened `if:` would see a
    `success` result and proceed despite checks never actually passing."""
    monkeypatch.chdir(tmp_path)
    _all_checks_initially_passing_except(tmp_path, ["build"], detail="still broken")

    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch(
             "checks_fix_loop_graph.run_checks.run_check",
             return_value={"status": "fail", "command": ["x"], "returncode": 1, "detail": "still broken"},
         ):
        rc = checks_fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 1
    out = json.loads(captured.out.strip())
    assert out == {"ok": True, "status": "unresolved-after-cap", "fix_cycle": 2}


def test_cli_main_implementation_invocation_error_exits_4(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _all_checks_initially_passing_except(tmp_path, ["build"], detail="broke")

    with patch(
        "subprocess.run",
        side_effect=_dispatcher(impl_result=_fake_proc(returncode=1, stderr="impl broke")),
    ), patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH):
        rc = checks_fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 4
    assert "impl broke" in captured.err


def test_cli_main_checkout_error_exits_5(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _all_checks_initially_passing_except(tmp_path, ["build"], detail="broke")

    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ), patch(
        "implementation_graph.checkout_branch.checkout_branch",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ):
        rc = checks_fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 5
    assert "branch not found" in captured.err


def test_cli_main_commit_push_error_exits_5(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    _all_checks_initially_passing_except(tmp_path, ["build"], detail="broke")

    with patch(
        "subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             side_effect=commit_push_implementation.CommitPushError("push rejected"),
         ):
        rc = checks_fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 5
    assert "push rejected" in captured.err
