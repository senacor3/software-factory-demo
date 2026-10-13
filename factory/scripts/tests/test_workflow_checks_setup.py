# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0", "pyyaml>=6,<7"]
# ///
"""Tests that the `checks` and `checks-fix-loop` jobs set up their runner the same way.
Run: uv run --with pytest --with pyyaml pytest factory/scripts/tests/test_workflow_checks_setup.py

Backlog bug 5: the fix loop re-checked on a runner that had neither the configured
toolchains nor the dependencies the `checks` job's runner had, because each job
carried its own setup steps and only one of them was kept up. These read the workflow
and the shared composite action as data -- no job is run -- and fail when the two
jobs' setup drifts apart again.
"""

from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "light-factory.yml"
TOOLCHAIN_ACTION = "./.github/actions/checks-toolchain"
ACTION_FILE = REPO_ROOT / ".github" / "actions" / "checks-toolchain" / "action.yml"

CHECK_STEP_IDS = ["build", "test", "lint", "security", "static_analysis"]


@pytest.fixture(scope="module")
def jobs():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]


def _index(steps, **match):
    """Index of the one step whose fields equal `match`; fails the test otherwise."""
    found = [i for i, step in enumerate(steps) if all(step.get(k) == v for k, v in match.items())]
    assert len(found) == 1, f"expected exactly one step matching {match}, found {len(found)}"
    return found[0]


@pytest.mark.parametrize("job", ["checks", "checks-fix-loop"])
def test_job_sets_up_the_shared_checks_toolchain_on_the_story_branch(jobs, job):
    steps = jobs[job]["steps"]
    toolchain = _index(steps, uses=TOOLCHAIN_ACTION)
    assert _index(steps, name="Install uv") < toolchain  # the action runs run_checks.py via uv
    assert _index(steps, name="Checkout implementation branch") < toolchain


@pytest.mark.parametrize("job", ["checks", "checks-fix-loop"])
def test_job_carries_no_toolchain_setup_of_its_own(jobs, job):
    """A second, job-local copy of the setup is how the two jobs drifted apart."""
    for step in jobs[job]["steps"]:
        assert "run_checks.py toolchains" not in step.get("run", "")
        assert not step.get("uses", "").startswith("actions/setup-java")
        if step.get("uses", "").startswith("actions/setup-node"):
            # Only as the Claude Code CLI's fallback, never in place of the configured Node.
            assert job == "checks-fix-loop"
            assert step.get("if") == "steps.toolchain.outputs.node == ''"
            assert steps_id(jobs[job]["steps"], TOOLCHAIN_ACTION) == "toolchain"


def steps_id(steps, uses):
    return steps[_index(steps, uses=uses)].get("id")


def test_fix_loop_job_runs_the_loop_after_the_toolchain_setup(jobs):
    steps = jobs["checks-fix-loop"]["steps"]
    assert _index(steps, uses=TOOLCHAIN_ACTION) < _index(steps, name="Run checks fix loop")


def test_checks_job_prepares_the_checkout_before_any_check(jobs):
    steps = jobs["checks"]["steps"]
    setup = _index(steps, id="setup")
    assert "run_checks.py setup" in steps[setup]["run"]
    assert "--story-slug" in steps[setup]["run"] and "--run-id" in steps[setup]["run"]
    assert steps[setup].get("continue-on-error") is True
    assert _index(steps, uses=TOOLCHAIN_ACTION) < setup
    assert all(setup < _index(steps, id=check) for check in CHECK_STEP_IDS)


def test_checks_job_fails_when_setup_failed(jobs):
    steps = jobs["checks"]["steps"]
    fail_step = steps[_index(steps, name="Fail job if any check failed")]
    for step_id in ["setup", *CHECK_STEP_IDS]:
        assert f"steps.{step_id}.outcome" in fail_step["run"]


def test_checks_job_reconciles_checks_state_after_the_checks_and_before_committing(jobs):
    steps = jobs["checks"]["steps"]
    reconcile = _index(steps, name="Reconcile checks state")
    assert "run_checks.py reconcile" in steps[reconcile]["run"]
    assert steps[reconcile].get("if") == "always()"
    assert all(_index(steps, id=check) < reconcile for check in CHECK_STEP_IDS)
    assert reconcile < _index(steps, name="Commit checks evidence")


def test_toolchain_action_reads_the_config_and_sets_up_each_named_toolchain():
    action = yaml.safe_load(ACTION_FILE.read_text(encoding="utf-8"))
    assert action["runs"]["using"] == "composite"
    steps = action["runs"]["steps"]

    read = steps[_index(steps, id="toolchain")]
    assert "run_checks.py toolchains" in read["run"]
    assert read["shell"] == "bash"

    java = next(s for s in steps if s.get("uses", "").startswith("actions/setup-java"))
    assert java["if"] == "steps.toolchain.outputs.java != ''"
    assert java["with"]["java-version"] == "${{ steps.toolchain.outputs.java }}"
    node = next(s for s in steps if s.get("uses", "").startswith("actions/setup-node"))
    assert node["if"] == "steps.toolchain.outputs.node != ''"
    assert node["with"]["node-version"] == "${{ steps.toolchain.outputs.node }}"

    assert _index(steps, id="toolchain") < steps.index(java)
    assert _index(steps, id="toolchain") < steps.index(node)
    for name in ("java", "node"):
        assert action["outputs"][name]["value"] == f"${{{{ steps.toolchain.outputs.{name} }}}}"
