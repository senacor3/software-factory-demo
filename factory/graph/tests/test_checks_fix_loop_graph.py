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


def _write_evidence(tmp_path, name, status, detail="", returncode=None):
    if returncode is None:
        returncode = 0 if status == "pass" else 1
    path = state_io.state_dir("foo", "run-1", base=tmp_path) / "evidence" / "checks" / f"{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": status, "command": ["x"], "returncode": returncode, "detail": detail}))


# The autouse fixture below replaces `run_checks.run_setup`; keep the real one.
_real_run_setup = run_checks.run_setup

SETUP_SKIPPED = {"status": "skipped", "command": None, "returncode": None, "detail": "", "commands": []}


@pytest.fixture(autouse=True)
def run_setup():
    """Default every test to a config with no `setup:` commands; setup tests re-patch.

    Also keeps the loop's setup call off the real `subprocess.run`/checks config.
    """
    with patch("checks_fix_loop_graph.run_checks.run_setup", return_value=dict(SETUP_SKIPPED)) as mock:
        yield mock


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


# --- backlog bug 5: a re-check runs under the conditions the first check had -----------


def _impl_patches():
    return (
        patch("subprocess.run", side_effect=_dispatcher(impl_result=_fake_proc(stdout="done"))),
        patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH),
        patch(
            "implementation_graph.commit_push_implementation.commit_and_push",
            return_value={"committed": True},
        ),
    )


class _Workspace:
    """A fake runner whose frontend tools exist only once the setup command ran --
    the fresh `checks-fix-loop` runner of runs 38377603346 and 38387681388, where
    `npm ci` had only ever run as part of the `build` check in another job."""

    SETUP = ("npm", "ci")

    def __init__(self, findings=0):
        self.installed = False
        self.findings = findings  # how many more runs of a frontend command still report a real finding
        self.log = []

    def commands_for(self, name):
        return [["backend-tool", name], ["npm", "run", name]]

    def run_command(self, cmd, *, cwd=None):
        self.log.append(cmd)
        if cmd == list(self.SETUP):
            self.installed = True
        elif cmd[0] == "npm" and not self.installed:
            return {"status": "fail", "command": cmd, "returncode": 127, "detail": "sh: 1: ng: not found"}
        elif cmd[0] == "npm" and self.findings:
            self.findings -= 1
            return {"status": "fail", "command": cmd, "returncode": 1, "detail": "1 real finding"}
        return {"status": "pass", "command": cmd, "returncode": 0, "detail": ""}

    def patches(self):
        return (
            patch("run_checks._load_config", side_effect=lambda name, cwd=None: (self.commands_for(name), "origin/main")),
            patch("run_checks.load_setup_commands", return_value=[list(self.SETUP)]),
            patch("run_checks._run_command", side_effect=self.run_command),
        )


@pytest.mark.parametrize("name", ["test", "lint", "static_analysis"])
def test_recheck_of_one_check_after_build_passed_runs_setup_first_and_resolves(tmp_path, name, run_setup):
    """`build` passed in the `checks` job, so the loop never re-runs it -- the
    re-check of `name` alone must still find the dependencies `build` used to
    install as a side effect."""
    _all_checks_initially_passing_except(tmp_path, [name], detail="1 real finding")
    workspace = _Workspace()
    run_setup.side_effect = _real_run_setup  # the real setup, against the fake workspace

    a, b, c = _impl_patches()
    d, e, f = workspace.patches()
    with a, b, c, d, e, f:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 1
    # setup first, then only the failed check's own commands -- never `build`, never the full suite
    assert workspace.log == [["npm", "ci"], ["backend-tool", name], ["npm", "run", name]]
    assert state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")[0]["status"] == "resolved"


def test_setup_runs_again_before_each_cycles_recheck(tmp_path, run_setup):
    """A fix cycle may change what there is to install (e.g. the lockfile), so setup
    is not a one-off at the start of the job."""
    _all_checks_initially_passing_except(tmp_path, ["test"], detail="1 real finding")
    workspace = _Workspace(findings=1)  # cycle 1's re-check still reports it, cycle 2's passes
    run_setup.side_effect = _real_run_setup

    a, b, c = _impl_patches()
    d, e, f = workspace.patches()
    with a as mock_run, b, c, d, e, f:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 2
    assert mock_run.call_count == 2
    cycle = [["npm", "ci"], ["backend-tool", "test"], ["npm", "run", "test"]]
    assert workspace.log == cycle + cycle


# --- backlog bug 5: a tooling failure is not counted as a code finding ------------------


@pytest.mark.parametrize("returncode", [127, 126, None])
def test_tool_missing_on_recheck_stops_the_loop_without_another_agent_call(tmp_path, returncode):
    _all_checks_initially_passing_except(tmp_path, ["lint"], detail="1 real finding")
    missing = {"status": "fail", "command": ["npm", "run", "lint"], "returncode": returncode, "detail": "sh: 1: ng: not found"}

    a, b, c = _impl_patches()
    with a as mock_run, b, c, patch("checks_fix_loop_graph.run_checks.run_check", return_value=missing) as mock_run_check:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "tooling-failure"
    assert outcome["fix_cycle"] == 1  # the cycle that ran; no second one spent on a missing tool
    assert sorted(outcome["tooling"]) == ["lint"]
    mock_run.assert_called_once()
    mock_run_check.assert_called_once()

    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert meta["status"] == "tooling-failure"
    assert meta["fix_cycle"] == "1"
    assert "lint" in body and "npm run lint" in body and "ng: not found" in body


def test_tool_missing_in_the_first_evidence_stops_before_any_fix_cycle(tmp_path, run_setup):
    _all_checks_initially_passing_except(tmp_path, [])
    _write_evidence(tmp_path, "test", "fail", detail="sh: 1: ng: not found", returncode=127)

    with patch("subprocess.run", side_effect=_dispatcher()) as mock_run, \
         patch("checks_fix_loop_graph.run_checks.run_check") as mock_run_check:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "tooling-failure"
    assert outcome["fix_cycle"] == 0
    assert sorted(outcome["tooling"]) == ["test"]
    mock_run.assert_not_called()  # the implementation agent is never engaged for it
    mock_run_check.assert_not_called()
    run_setup.assert_not_called()

    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert meta["status"] == "tooling-failure"
    assert meta["fix_cycle"] == "0"
    assert "test" in body and "ng: not found" in body


def test_a_tooling_failure_beside_a_real_finding_still_stops_the_loop(tmp_path):
    _all_checks_initially_passing_except(tmp_path, ["lint", "test"], detail="1 real finding")
    results = {
        "lint": {"status": "fail", "command": ["npm", "run", "lint"], "returncode": 1, "detail": "1 real finding"},
        "test": {"status": "fail", "command": ["npm", "test"], "returncode": 127, "detail": "sh: 1: ng: not found"},
    }

    a, b, c = _impl_patches()
    with a as mock_run, b, c, \
         patch("checks_fix_loop_graph.run_checks.run_check", side_effect=lambda name, *args, **kwargs: results[name]):
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "tooling-failure"
    assert outcome["fix_cycle"] == 1
    assert sorted(outcome["tooling"]) == ["test"]
    assert outcome["failing"] == ["lint", "test"]
    mock_run.assert_called_once()

    # the real finding is not lost behind the tooling failure
    _, body = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert "## Tooling failures" in body and "npm test" in body
    assert "## Failing checks" in body and "**lint**: 1 real finding" in body
    assert "**test**" not in body  # named once, as what it is


def test_failing_setup_command_is_a_tooling_failure_naming_that_command(tmp_path, run_setup):
    _all_checks_initially_passing_except(tmp_path, ["lint"], detail="1 real finding")
    run_setup.return_value = {
        "status": "fail",
        "command": ["npm", "ci"],
        "returncode": 1,
        "detail": "npm error network",
        "commands": [["npm", "ci"]],
    }

    a, b, c = _impl_patches()
    with a as mock_run, b, c, patch("checks_fix_loop_graph.run_checks.run_check") as mock_run_check:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "tooling-failure"
    assert outcome["fix_cycle"] == 1
    assert sorted(outcome["tooling"]) == ["setup"]
    mock_run.assert_called_once()
    mock_run_check.assert_not_called()  # nothing is re-checked on a checkout setup could not prepare

    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert meta["status"] == "tooling-failure"
    assert "setup" in body and "npm ci" in body and "npm error network" in body


def test_cli_main_tooling_failure_exits_6_and_names_the_cause(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # main() uses the default state base, `.factory/` under the working directory
    _all_checks_initially_passing_except(tmp_path / state_io.FACTORY_DIR, ["lint"], detail="1 real finding")
    missing = {"status": "fail", "command": ["npm", "run", "lint"], "returncode": 127, "detail": "sh: 1: ng: not found"}

    a, b, c = _impl_patches()
    with a, b, c, patch("checks_fix_loop_graph.run_checks.run_check", return_value=missing):
        rc = checks_fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])

    captured = capsys.readouterr()
    assert rc == 6
    assert json.loads(captured.out.strip()) == {
        "ok": False,
        "status": "tooling-failure",
        "fix_cycle": 1,
        "tooling": ["lint"],
    }
    assert "tooling failure: lint" in captured.err
    assert "npm run lint" in captured.err and "return code 127" in captured.err


def _write_setup_evidence(tmp_path, status="fail"):
    path = state_io.state_dir("foo", "run-1", base=tmp_path) / "evidence" / "checks" / "setup.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"status": status, "command": ["npm", "ci"], "returncode": 1, "detail": "npm error network", "commands": [["npm", "ci"]]}))


@pytest.mark.parametrize(
    "failing_names, returncode",
    [
        (["build", "test"], 1),  # the checks then failed for want of it, with an ordinary exit code
        (["build"], 127),
        ([], 0),  # or did not need it and passed: the attempt is still not green
    ],
)
def test_setup_that_failed_in_the_checks_job_is_named_before_any_fix_cycle(tmp_path, run_setup, failing_names, returncode):
    _all_checks_initially_passing_except(tmp_path, [])
    for name in failing_names:
        _write_evidence(tmp_path, name, "fail", detail="Cannot find module", returncode=returncode)
    _write_setup_evidence(tmp_path)

    with patch("subprocess.run", side_effect=_dispatcher()) as mock_run, \
         patch("checks_fix_loop_graph.run_checks.run_check") as mock_run_check:
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "tooling-failure"
    assert outcome["fix_cycle"] == 0
    assert sorted(outcome["tooling"]) == ["setup"]
    mock_run.assert_not_called()  # never a fix cycle for a checkout that was not prepared
    mock_run_check.assert_not_called()
    run_setup.assert_not_called()

    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "checks.md")
    assert meta["status"] == "tooling-failure"
    assert "setup" in body and "npm ci" in body and "npm error network" in body


def test_recorded_setup_that_passed_does_not_stop_the_loop(tmp_path):
    _all_checks_initially_passing_except(tmp_path, ["lint"], detail="1 real finding")
    _write_setup_evidence(tmp_path, status="pass")
    passing = {"status": "pass", "command": ["x"], "returncode": 0, "detail": ""}

    a, b, c = _impl_patches()
    with a, b, c, patch("checks_fix_loop_graph.run_checks.run_check", return_value=passing):
        outcome = checks_fix_loop_graph.run_checks_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 1
