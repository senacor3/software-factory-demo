# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for fix_loop_graph.py. Run:
uv run --with pytest pytest factory/graph/tests/test_fix_loop_graph.py

Covers the I/O & Edge-Case Matrix in story-bounded-fix-loop-plan.md: a clean initial
review (no fix cycle, fix_cycle: 0), one fix cycle resolving the findings (fix_cycle:
1), the hard cap of 2 fix cycles still unresolved (unresolved-after-cap, fix_cycle:
2, carrying the last review's findings), a fix cycle's recheck regressing build/test
(CheckRegressionError, no further review invocation), review tooling failing mid-loop
(ReviewInvocationError propagates), and the fix-cycle implementation tooling failing
(ImplementationInvocationError propagates, no recheck/re-review attempted).

`review_graph.subprocess` and `implementation_graph.subprocess` are both the same
stdlib `subprocess` module object, so patching `review_graph.subprocess.run` and
`implementation_graph.subprocess.run` independently in the same test clobber each
other. Instead this file patches the one shared `subprocess.run` with a single
dispatcher that routes on which skill's prompt (`/software-factory-review` vs.
`/software-factory-implementation`) the call is for -- so review_graph.run_review and
implementation_graph.run_implementation still run for real against tmp_path,
including the real review.md writes this module reads back and re-stamps.
checkout_branch.checkout_branch and commit_push_implementation.commit_and_push are
mocked wholesale (their own bodies are tested elsewhere); run_checks.run_build/
run_test are mocked directly to avoid actually invoking compileall/pytest.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import fix_loop_graph
import implementation_graph
import review_graph

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import checkout_branch
import commit_push_implementation
import state_io

FAKE_BRANCH = "software-factory/foo/run-1"


def _fake_proc(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _review_result(**overrides):
    base = {"findings": []}
    base.update(overrides)
    return base


def _review_cli_output(result):
    return json.dumps({"result": "final text", "structured_output": result})


def _findings_proc(description="needs a fix"):
    return _fake_proc(
        stdout=_review_cli_output(
            _review_result(findings=[{"location": "foo.py:1", "description": description}])
        )
    )


def _clean_proc():
    return _fake_proc(stdout=_review_cli_output(_review_result()))


def _passing_check(name):
    return {"status": "pass", "command": ["x"], "returncode": 0, "detail": ""}


def _failing_check(name):
    return {"status": "fail", "command": ["x"], "returncode": 1, "detail": f"{name} broke"}


@pytest.fixture(autouse=True)
def run_setup():
    """Default every test to a config with no `setup:` commands; setup tests re-patch.

    Also keeps the loop's setup call off the real `subprocess.run`/checks config.
    """
    skipped = {"status": "skipped", "command": None, "returncode": None, "detail": "", "commands": []}
    with patch("fix_loop_graph.run_checks.run_setup", return_value=skipped) as mock:
        yield mock


def _dispatcher(review_results=None, impl_result=None):
    """A `subprocess.run` side_effect that routes to a review-call queue or a fixed
    implementation-call result, based on which skill the `-p` prompt invokes."""
    review_iter = iter(review_results or [])

    def run(cmd, **kwargs):
        prompt = cmd[cmd.index("-p") + 1]
        if "/software-factory-review" in prompt:
            return next(review_iter)
        if "/software-factory-implementation" in prompt:
            if impl_result is None:
                raise AssertionError("unexpected implementation invocation in this test")
            return impl_result
        raise AssertionError(f"unexpected subprocess invocation: {cmd}")

    return run


# --- I/O Matrix row 1: initial review is clean ----------------------------------------


def test_clean_initial_review_runs_no_fix_cycle(tmp_path):
    with patch(
        "subprocess.run", side_effect=_dispatcher(review_results=[_clean_proc()])
    ) as mock_run, \
         patch("fix_loop_graph.run_checks.run_build") as mock_build, \
         patch("fix_loop_graph.run_checks.run_test") as mock_test:
        outcome = fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 0
    mock_run.assert_called_once()  # only the initial review; no implementation call
    mock_build.assert_not_called()
    mock_test.assert_not_called()

    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "review.md")
    assert meta["status"] == "resolved"
    assert meta["fix_cycle"] == "0"


# --- I/O Matrix row 2: one fix cycle resolves it --------------------------------------


def test_one_fix_cycle_resolves_findings(tmp_path):
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(
            review_results=[_findings_proc(), _clean_proc()], impl_result=_fake_proc(stdout="done")
        ),
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", return_value=_passing_check("build")) as mock_build, \
         patch("fix_loop_graph.run_checks.run_test", return_value=_passing_check("test")) as mock_test:
        outcome = fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert outcome["fix_cycle"] == 1
    assert mock_run.call_count == 3  # 2 reviews + 1 implementation call
    mock_build.assert_called_once()
    mock_test.assert_called_once()

    # the implementation re-invocation carried review.md as its added context
    impl_calls = [c for c in mock_run.call_args_list if "/software-factory-implementation" in c.args[0][2]]
    assert len(impl_calls) == 1
    assert impl_calls[0].args[0][2].endswith("review.md")

    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "review.md")
    assert meta["status"] == "resolved"
    assert meta["fix_cycle"] == "1"


# --- I/O Matrix row 3: two fix cycles, still unresolved -------------------------------


def test_two_fix_cycles_still_unresolved_stops_at_cap(tmp_path):
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(
            review_results=[
                _findings_proc("first pass issue"),
                _findings_proc("second pass issue"),
                _findings_proc("third pass issue"),
            ],
            impl_result=_fake_proc(stdout="done"),
        ),
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", return_value=_passing_check("build")), \
         patch("fix_loop_graph.run_checks.run_test", return_value=_passing_check("test")):
        outcome = fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "unresolved-after-cap"
    assert outcome["fix_cycle"] == 2
    review_calls = [c for c in mock_run.call_args_list if "/software-factory-review" in c.args[0][2]]
    impl_calls = [c for c in mock_run.call_args_list if "/software-factory-implementation" in c.args[0][2]]
    assert len(review_calls) == 3  # initial + 2 re-reviews, never a 3rd fix cycle
    assert len(impl_calls) == 2  # exactly 2 fix cycles, never 3

    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "review.md")
    assert meta["status"] == "unresolved-after-cap"
    assert meta["fix_cycle"] == "2"
    assert "third pass issue" in body  # carries the last (3rd) review's findings
    assert "first pass issue" not in body


# --- I/O Matrix row 4: a fix cycle regresses build/test --------------------------------


def test_build_regression_stops_loop_immediately_raises_check_regression_error(tmp_path):
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(review_results=[_findings_proc()], impl_result=_fake_proc(stdout="done")),
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", return_value=_failing_check("build")), \
         patch("fix_loop_graph.run_checks.run_test") as mock_test:
        with pytest.raises(fix_loop_graph.CheckRegressionError, match="build"):
            fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    mock_test.assert_not_called()  # test check never run once build already failed
    review_calls = [c for c in mock_run.call_args_list if "/software-factory-review" in c.args[0][2]]
    assert len(review_calls) == 1  # no further review invocation


def test_test_regression_stops_loop_immediately_raises_check_regression_error(tmp_path):
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(review_results=[_findings_proc()], impl_result=_fake_proc(stdout="done")),
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", return_value=_passing_check("build")), \
         patch("fix_loop_graph.run_checks.run_test", return_value=_failing_check("test")):
        with pytest.raises(fix_loop_graph.CheckRegressionError, match="test"):
            fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    review_calls = [c for c in mock_run.call_args_list if "/software-factory-review" in c.args[0][2]]
    assert len(review_calls) == 1  # no further review invocation


# --- I/O Matrix row 5: review tooling fails mid-loop ------------------------------------


def test_review_tooling_failure_mid_loop_propagates(tmp_path):
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(
            review_results=[_findings_proc(), _fake_proc(returncode=1, stderr="review CLI broke")],
            impl_result=_fake_proc(stdout="done"),
        ),
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", return_value=_passing_check("build")), \
         patch("fix_loop_graph.run_checks.run_test", return_value=_passing_check("test")):
        with pytest.raises(review_graph.ReviewInvocationError, match="review CLI broke"):
            fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    impl_calls = [c for c in mock_run.call_args_list if "/software-factory-implementation" in c.args[0][2]]
    assert len(impl_calls) == 1  # the one fix cycle before the failing re-review


# --- I/O Matrix row 6: fix-cycle implementation tooling fails ---------------------------


def test_implementation_tooling_failure_stops_loop_no_recheck_or_rereview(tmp_path):
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(
            review_results=[_findings_proc()],
            impl_result=_fake_proc(returncode=1, stderr="impl CLI broke"),
        ),
    ) as mock_run, \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
         ) as mock_commit, \
         patch("fix_loop_graph.run_checks.run_build") as mock_build, \
         patch("fix_loop_graph.run_checks.run_test") as mock_test:
        with pytest.raises(
            implementation_graph.ImplementationInvocationError, match="impl CLI broke"
        ):
            fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    mock_commit.assert_not_called()
    mock_build.assert_not_called()
    mock_test.assert_not_called()
    review_calls = [c for c in mock_run.call_args_list if "/software-factory-review" in c.args[0][2]]
    assert len(review_calls) == 1  # no re-review attempted


# --- CLI exit codes ----------------------------------------------------------------------


def test_cli_main_review_invocation_error_exits_3(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(review_results=[_fake_proc(returncode=1, stderr="boom")]),
    ):
        rc = fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 3
    assert "boom" in captured.err


def test_cli_main_implementation_invocation_error_exits_4(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(
            review_results=[_findings_proc()],
            impl_result=_fake_proc(returncode=1, stderr="impl broke"),
        ),
    ), patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH):
        rc = fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 4
    assert "impl broke" in captured.err


def test_cli_main_checkout_error_exits_5(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch(
        "subprocess.run", side_effect=_dispatcher(review_results=[_findings_proc()])
    ), patch(
        "implementation_graph.checkout_branch.checkout_branch",
        side_effect=checkout_branch.CheckoutError("branch not found"),
    ):
        rc = fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 5
    assert "branch not found" in captured.err


def test_cli_main_commit_push_error_exits_5(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(review_results=[_findings_proc()], impl_result=_fake_proc(stdout="done")),
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             side_effect=commit_push_implementation.CommitPushError("push rejected"),
         ):
        rc = fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 5
    assert "push rejected" in captured.err


def test_cli_main_check_regression_error_exits_6(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(review_results=[_findings_proc()], impl_result=_fake_proc(stdout="done")),
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", return_value=_failing_check("build")):
        rc = fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 6
    assert "build" in captured.err


def test_cli_main_success_exits_0_clean(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("subprocess.run", side_effect=_dispatcher(review_results=[_clean_proc()])):
        rc = fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out == {"ok": True, "status": "resolved", "fix_cycle": 0}


def test_cli_main_success_exits_0_unresolved_after_cap(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch(
        "subprocess.run",
        side_effect=_dispatcher(
            review_results=[_findings_proc(), _findings_proc(), _findings_proc()],
            impl_result=_fake_proc(stdout="done"),
        ),
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", return_value=_passing_check("build")), \
         patch("fix_loop_graph.run_checks.run_test", return_value=_passing_check("test")):
        rc = fix_loop_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out == {"ok": True, "status": "unresolved-after-cap", "fix_cycle": 2}


# --- backlog bug 5: the recheck prepares its own checkout --------------------------------


def test_recheck_prepares_the_checkout_before_build_and_test(tmp_path, run_setup):
    """`build` no longer installs dependencies as a side effect, and this job's runner
    is as fresh as the `checks-fix-loop` job's -- so setup runs first, every cycle."""
    order = []
    run_setup.side_effect = lambda *a, **k: order.append("setup") or {"status": "pass", "command": ["npm", "ci"], "returncode": 0, "detail": ""}

    with patch(
        "subprocess.run",
        side_effect=_dispatcher(review_results=[_findings_proc(), _clean_proc()], impl_result=_fake_proc(stdout="done")),
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build", side_effect=lambda *a, **k: order.append("build") or _passing_check("build")), \
         patch("fix_loop_graph.run_checks.run_test", side_effect=lambda *a, **k: order.append("test") or _passing_check("test")):
        outcome = fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    assert order == ["setup", "build", "test"]
    run_setup.assert_called_once_with("foo", "run-1", state_base=tmp_path, cwd=None)


def test_failing_setup_stops_the_loop_before_any_recheck(tmp_path, run_setup):
    run_setup.return_value = {"status": "fail", "command": ["npm", "ci"], "returncode": 1, "detail": "npm error network"}

    with patch(
        "subprocess.run",
        side_effect=_dispatcher(review_results=[_findings_proc()], impl_result=_fake_proc(stdout="done")),
    ), \
         patch("implementation_graph.checkout_branch.checkout_branch", return_value=FAKE_BRANCH), \
         patch(
             "implementation_graph.commit_push_implementation.commit_and_push",
             return_value={"committed": True},
         ), \
         patch("fix_loop_graph.run_checks.run_build") as mock_build, \
         patch("fix_loop_graph.run_checks.run_test") as mock_test:
        with pytest.raises(fix_loop_graph.CheckRegressionError, match="setup.*npm error network"):
            fix_loop_graph.run_review_with_fix_loop("foo", "run-1", state_base=tmp_path)

    mock_build.assert_not_called()
    mock_test.assert_not_called()
