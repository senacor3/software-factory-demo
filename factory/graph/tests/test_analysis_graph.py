# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for analysis_graph.py. Run: uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py

Covers the I/O & Edge-Case Matrix in story-job-1-intake-analysis-plan.md: complete/in-scope
with no open questions (ready-for-review), complete/in-scope with open questions
(awaiting-clarification), incomplete-or-out-of-scope (halt, no file written), and a `claude`
CLI tooling failure (distinct exception, no file written). The `claude` subprocess call is
mocked throughout -- no live CLI/network dependency.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import analysis_graph  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import state_io  # noqa: E402


def _fake_proc(returncode=0, stdout="", stderr=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _result(**overrides):
    base = {
        "complete": True,
        "in_scope": True,
        "reason": "",
        "proposal": "do the thing",
        "subtasks": ["step one"],
        "tests": ["test one"],
        "open_questions": [],
    }
    base.update(overrides)
    return base


def _cli_output(result):
    return json.dumps({"result": "final text", "structured_output": result})


# --- I/O Matrix row 1: complete, in-scope, no open questions -----------------------------


def test_complete_no_open_questions_writes_ready_for_review(tmp_path):
    result = _result()
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        outcome = analysis_graph.run_analysis(
            "stories/foo.md", "foo", "run-1", state_base=tmp_path
        )

    assert outcome["status"] == "ready-for-review"
    meta, body = state_io.read_state(tmp_path / "foo" / "run-1" / "plan.md")
    assert meta["status"] == "ready-for-review"
    assert meta["stage"] == "analysis"
    assert "do the thing" in body

    dmeta, dbody = state_io.read_state(tmp_path / "foo" / "run-1" / "decisions.md")
    assert dmeta["status"] == "ready-for-review"
    assert "_none_" in dbody  # no open questions


# --- I/O Matrix row 2: complete, in-scope, open questions remain --------------------------


def test_complete_with_open_questions_writes_awaiting_clarification(tmp_path):
    result = _result(open_questions=["what about X?"])
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        outcome = analysis_graph.run_analysis(
            "stories/foo.md", "foo", "run-1", state_base=tmp_path
        )

    assert outcome["status"] == "awaiting-clarification"
    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "plan.md")
    assert meta["status"] == "awaiting-clarification"
    dmeta, dbody = state_io.read_state(tmp_path / "foo" / "run-1" / "decisions.md")
    assert dmeta["status"] == "awaiting-clarification"
    assert "what about X?" in dbody


# --- I/O Matrix row 3: incomplete or out-of-scope -----------------------------------------


def test_incomplete_halts_with_reason_and_writes_nothing(tmp_path):
    result = _result(
        complete=False,
        in_scope=True,
        reason="story is too vague to design a solution from",
        proposal=None,
        subtasks=[],
        tests=[],
    )
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        with pytest.raises(analysis_graph.AnalysisHalted) as exc_info:
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert "too vague" in exc_info.value.reason
    assert not (tmp_path / "foo").exists()


def test_out_of_scope_halts_with_reason_and_writes_nothing(tmp_path):
    result = _result(
        complete=True,
        in_scope=False,
        reason="not something this codebase builds",
        proposal=None,
        subtasks=[],
        tests=[],
    )
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        with pytest.raises(analysis_graph.AnalysisHalted) as exc_info:
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert "not something this codebase builds" in exc_info.value.reason
    assert not (tmp_path / "foo").exists()


# --- I/O Matrix row 4: claude CLI invocation itself fails ---------------------------------


def test_cli_nonzero_exit_raises_invocation_error_not_halted(tmp_path):
    with patch(
        "analysis_graph.subprocess.run",
        return_value=_fake_proc(returncode=1, stderr="boom"),
    ):
        with pytest.raises(analysis_graph.AnalysisInvocationError, match="boom"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_cli_malformed_json_raises_invocation_error(tmp_path):
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout="not json")):
        with pytest.raises(analysis_graph.AnalysisInvocationError, match="not valid JSON"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_cli_missing_structured_output_raises_invocation_error(tmp_path):
    with patch(
        "analysis_graph.subprocess.run",
        return_value=_fake_proc(stdout=json.dumps({"result": "no structured_output here"})),
    ):
        with pytest.raises(analysis_graph.AnalysisInvocationError, match="structured_output"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_cli_missing_required_field_raises_invocation_error(tmp_path):
    incomplete_result = _result()
    del incomplete_result["reason"]
    with patch(
        "analysis_graph.subprocess.run",
        return_value=_fake_proc(stdout=_cli_output(incomplete_result)),
    ):
        with pytest.raises(analysis_graph.AnalysisInvocationError, match="missing required field"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


def test_subprocess_oserror_raises_invocation_error(tmp_path):
    with patch("analysis_graph.subprocess.run", side_effect=OSError("no such file")):
        with pytest.raises(analysis_graph.AnalysisInvocationError, match="no such file"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert not (tmp_path / "foo").exists()


# --- command construction ------------------------------------------------------------------


def test_build_command_never_uses_bare():
    schema_text = analysis_graph.SCHEMA_PATH.read_text(encoding="utf-8")
    cmd = analysis_graph._build_command("stories/foo.md", schema_text, "claude")
    assert "--bare" not in cmd
    assert cmd[0] == "claude"
    assert "/light-factory-analysis stories/foo.md" in cmd
    assert "Read Grep Glob" in cmd


def test_build_command_passes_schema_and_json_output():
    schema_text = analysis_graph.SCHEMA_PATH.read_text(encoding="utf-8")
    cmd = analysis_graph._build_command("stories/foo.md", schema_text, "claude")
    assert "--output-format" in cmd
    assert "json" in cmd
    assert "--json-schema" in cmd
    assert schema_text in cmd


# --- CLI exit codes -------------------------------------------------------------------------


def test_cli_main_halted_exits_1(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = _result(complete=False, reason="nope", proposal=None, subtasks=[], tests=[])
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        rc = analysis_graph.main(
            ["--story-file", "stories/foo.md", "--story-slug", "foo", "--run-id", "run-1"]
        )
    captured = capsys.readouterr()
    assert rc == 1
    assert "nope" in captured.err


def test_cli_main_invocation_error_exits_3(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(returncode=2, stderr="tool broke")):
        rc = analysis_graph.main(
            ["--story-file", "stories/foo.md", "--story-slug", "foo", "--run-id", "run-1"]
        )
    captured = capsys.readouterr()
    assert rc == 3
    assert "tool broke" in captured.err


def test_cli_main_success_exits_0(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = _result()
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))):
        rc = analysis_graph.main(
            ["--story-file", "stories/foo.md", "--story-slug", "foo", "--run-id", "run-1"]
        )
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out["ok"] is True
    assert out["status"] == "ready-for-review"
