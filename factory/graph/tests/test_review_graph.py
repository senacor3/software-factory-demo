# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for review_graph.py. Run: uv run --with pytest pytest factory/graph/tests/test_review_graph.py

Covers the I/O & Edge-Case Matrix in story-independent-review-agent-plan.md: a clean
implementation (empty findings -> resolved), an implementation with findings
(findings-open, a legitimate outcome, not a failure), and a `claude` CLI tooling
failure (distinct exception, nothing written). The `claude` subprocess call is mocked
throughout -- no live CLI/network dependency, no real `git`/`gh` process ever runs in
this suite.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import review_graph  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import state_io  # noqa: E402


def _fake_proc(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _result(**overrides):
    base = {"findings": []}
    base.update(overrides)
    return base


def _cli_output(result):
    return json.dumps({"result": "final text", "structured_output": result})


# --- I/O Matrix row 1: clean implementation -----------------------------------------------


def test_clean_implementation_writes_resolved(tmp_path):
    result = _result()
    with patch("review_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        outcome = review_graph.run_review("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "resolved"
    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "review.md")
    assert meta["status"] == "resolved"
    assert meta["stage"] == "review"
    assert "_none_" in body

    findings_path = tmp_path / "foo" / "run-1" / "evidence" / "review" / "findings.json"
    findings = json.loads(findings_path.read_text(encoding="utf-8"))
    assert findings == {"findings": []}


# --- I/O Matrix row 2: implementation has findings -----------------------------------------


def test_findings_write_findings_open_and_are_not_a_failure(tmp_path):
    result = _result(
        findings=[
            {"location": "factory/graph/foo.py:12", "description": "subtask 2 was never implemented"},
            {"location": "factory/graph/tests/test_foo.py", "description": "no test for the error path"},
        ]
    )
    with patch("review_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        outcome = review_graph.run_review("foo", "run-1", state_base=tmp_path)

    assert outcome["status"] == "findings-open"
    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "review.md")
    assert meta["status"] == "findings-open"
    assert "subtask 2 was never implemented" in body
    assert "no test for the error path" in body

    findings_path = tmp_path / "foo" / "run-1" / "evidence" / "review" / "findings.json"
    findings = json.loads(findings_path.read_text(encoding="utf-8"))
    assert findings == {"findings": result["findings"]}


# --- I/O Matrix row 3: claude CLI invocation itself fails -----------------------------------


def test_cli_nonzero_exit_raises_invocation_error_nothing_written(tmp_path):
    with patch("review_graph.subprocess.run", return_value=_fake_proc(returncode=1, stderr="boom")):
        with pytest.raises(review_graph.ReviewInvocationError, match="boom"):
            review_graph.run_review("foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_cli_malformed_json_raises_invocation_error(tmp_path):
    with patch("review_graph.subprocess.run", return_value=_fake_proc(stdout="not json")):
        with pytest.raises(review_graph.ReviewInvocationError, match="not valid JSON"):
            review_graph.run_review("foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_cli_missing_structured_output_raises_invocation_error(tmp_path):
    with patch(
        "review_graph.subprocess.run",
        return_value=_fake_proc(stdout=json.dumps({"result": "no structured_output here"})),
    ):
        with pytest.raises(review_graph.ReviewInvocationError, match="structured_output"):
            review_graph.run_review("foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_cli_missing_required_field_raises_invocation_error(tmp_path):
    with patch(
        "review_graph.subprocess.run",
        return_value=_fake_proc(stdout=json.dumps({"result": "x", "structured_output": {}})),
    ):
        with pytest.raises(review_graph.ReviewInvocationError, match="missing required field"):
            review_graph.run_review("foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_subprocess_oserror_raises_invocation_error(tmp_path):
    with patch("review_graph.subprocess.run", side_effect=OSError("claude not found")):
        with pytest.raises(review_graph.ReviewInvocationError, match="claude not found"):
            review_graph.run_review("foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


# --- command construction: AD-5's no-write-tool-at-all enforcement -------------------------


def test_build_command_never_uses_bare():
    schema_text = review_graph.SCHEMA_PATH.read_text(encoding="utf-8")
    cmd = review_graph._build_command("plan.md", "decisions.md", schema_text, "claude")
    assert "--bare" not in cmd
    assert cmd[0] == "claude"
    assert "/light-factory-review plan.md decisions.md" in cmd


def test_build_command_allows_no_write_edit_bash_git_gh_tool():
    schema_text = review_graph.SCHEMA_PATH.read_text(encoding="utf-8")
    cmd = review_graph._build_command("plan.md", "decisions.md", schema_text, "claude")
    allowed_idx = cmd.index("--allowedTools") + 1
    allowed_tools = cmd[allowed_idx]
    assert allowed_tools == "Read Grep Glob"
    for forbidden in ("Write", "Edit", "Bash", "git", "gh"):
        assert forbidden not in allowed_tools


def test_build_command_passes_schema_and_json_output():
    schema_text = review_graph.SCHEMA_PATH.read_text(encoding="utf-8")
    cmd = review_graph._build_command("plan.md", "decisions.md", schema_text, "claude")
    assert "--output-format" in cmd
    assert "json" in cmd
    assert "--json-schema" in cmd
    assert schema_text in cmd


# --- CLI exit codes --------------------------------------------------------------------------


def test_cli_main_invocation_error_exits_3(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    with patch("review_graph.subprocess.run", return_value=_fake_proc(returncode=2, stderr="tool broke")):
        rc = review_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 3
    assert "tool broke" in captured.err


def test_cli_main_success_exits_0_on_clean_pass(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    result = _result()
    with patch("review_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        rc = review_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out == {"ok": True, "status": "resolved"}


def test_cli_main_success_exits_0_with_findings(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    result = _result(findings=[{"location": "foo.py", "description": "bad"}])
    with patch("review_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        rc = review_graph.main(["--story-slug", "foo", "--run-id", "run-1"])
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out == {"ok": True, "status": "findings-open"}
