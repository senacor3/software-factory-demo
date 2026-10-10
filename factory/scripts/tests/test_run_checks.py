# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for run_checks.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_run_checks.py

Covers the I/O & Edge-Case Matrix in story-mechanical-checks-plan.md: build/test/lint
pass and fail (status, exit code, evidence content), security's always-skipped
placeholder (never "pass", never runs a command), and that evidence is written
before the CLI's exit-code decision. `subprocess.run` is mocked throughout -- no
real `compileall`/`pytest` subprocess in the committed suite (mirrors
test_commit_push_implementation.py).
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_checks  # noqa: E402
import state_io  # noqa: E402


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(returncode=1, stderr="boom", stdout=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _evidence_path(tmp_path, name):
    return state_io.state_dir("foo-bar", "run-1", base=tmp_path) / "evidence" / "checks" / f"{name}.json"


# --- run_build / run_test: pass -----------------------------------------------


def test_run_build_pass_writes_pass_evidence(tmp_path):
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = run_checks.run_build("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "pass"
    cmd = mock_run.call_args.args[0]
    assert cmd == [sys.executable, "-m", "compileall", "factory", "-q"]

    written = json.loads(_evidence_path(tmp_path, "build").read_text())
    assert written["status"] == "pass"


def test_run_test_pass_writes_pass_evidence(tmp_path):
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = run_checks.run_test("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "pass"
    cmd = mock_run.call_args.args[0]
    assert cmd == [
        "uv",
        "run",
        "--with",
        "pytest",
        "pytest",
        "factory/graph/tests/",
        "factory/scripts/tests/",
    ]

    written = json.loads(_evidence_path(tmp_path, "test").read_text())
    assert written["status"] == "pass"


# --- run_build / run_test: fail -------------------------------------------------


def test_run_build_fail_captures_error_and_writes_evidence(tmp_path):
    with patch("run_checks.subprocess.run", return_value=_fail(stderr="SyntaxError: bad token")):
        result = run_checks.run_build("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "fail"
    assert "SyntaxError" in result["detail"]

    written = json.loads(_evidence_path(tmp_path, "build").read_text())
    assert written["status"] == "fail"
    assert "SyntaxError" in written["detail"]


def test_run_test_fail_captures_error_and_writes_evidence(tmp_path):
    with patch("run_checks.subprocess.run", return_value=_fail(stderr="1 failed, 2 passed")):
        result = run_checks.run_test("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "fail"
    assert "failed" in result["detail"]

    written = json.loads(_evidence_path(tmp_path, "test").read_text())
    assert written["status"] == "fail"


def test_run_build_oserror_is_reported_as_fail_not_raised(tmp_path):
    with patch("run_checks.subprocess.run", side_effect=OSError("python not found")):
        result = run_checks.run_build("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "fail"
    assert "python not found" in result["detail"]
    assert json.loads(_evidence_path(tmp_path, "build").read_text())["status"] == "fail"


# --- run_lint: real ruff check; run_security: always-skipped placeholder ---------


def test_run_lint_pass_writes_pass_evidence(tmp_path):
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = run_checks.run_lint("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "pass"
    cmd = mock_run.call_args.args[0]
    assert cmd == ["uv", "run", "--with", "ruff", "ruff", "check", "factory/"]

    written = json.loads(_evidence_path(tmp_path, "lint").read_text())
    assert written["status"] == "pass"


def test_run_lint_fail_captures_output_and_writes_evidence(tmp_path):
    with patch(
        "run_checks.subprocess.run",
        return_value=_fail(stdout="F401 `os` imported but unused", stderr=""),
    ):
        result = run_checks.run_lint("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "fail"
    assert "F401" in result["detail"]

    written = json.loads(_evidence_path(tmp_path, "lint").read_text())
    assert written["status"] == "fail"
    assert "F401" in written["detail"]


def test_run_lint_oserror_is_reported_as_fail_not_raised(tmp_path):
    with patch("run_checks.subprocess.run", side_effect=OSError("uv not found")):
        result = run_checks.run_lint("foo-bar", "run-1", state_base=tmp_path)

    assert result["status"] == "fail"
    assert "uv not found" in result["detail"]
    assert json.loads(_evidence_path(tmp_path, "lint").read_text())["status"] == "fail"


def test_run_security_is_always_skipped_and_runs_no_command(tmp_path):
    with patch("run_checks.subprocess.run") as mock_run:
        result = run_checks.run_security("foo-bar", "run-1", state_base=tmp_path)

    mock_run.assert_not_called()
    assert result["status"] == "skipped"
    assert result["command"] is None
    assert result["status"] != "pass"

    written = json.loads(_evidence_path(tmp_path, "security").read_text())
    assert written["status"] == "skipped"


# --- CLI: exit codes -------------------------------------------------------------


def test_cli_exits_zero_on_pass(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("run_checks.subprocess.run", return_value=_ok()):
        rc = run_checks.main(["build", "--story-slug", "foo-bar", "--run-id", "run-1"])

    assert rc == 0


def test_cli_exits_nonzero_on_fail(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("run_checks.subprocess.run", return_value=_fail()):
        rc = run_checks.main(["test", "--story-slug", "foo-bar", "--run-id", "run-1"])

    assert rc == 1


def test_cli_exits_zero_on_skipped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rc = run_checks.main(["security", "--story-slug", "foo-bar", "--run-id", "run-1"])

    assert rc == 0


def test_cli_lint_exits_one_on_fail_and_zero_on_pass(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("run_checks.subprocess.run", return_value=_fail()):
        assert run_checks.main(["lint", "--story-slug", "foo-bar", "--run-id", "run-1"]) == 1
    with patch("run_checks.subprocess.run", return_value=_ok()):
        assert run_checks.main(["lint", "--story-slug", "foo-bar", "--run-id", "run-1"]) == 0


def test_cli_requires_story_slug_and_run_id():
    with pytest.raises(SystemExit):
        run_checks.main(["build"])
