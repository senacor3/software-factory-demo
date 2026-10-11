# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for analysis_graph.py. Run: uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py

Covers the I/O & Edge-Case Matrix in story-job-1-intake-analysis-plan.md: complete/in-scope
with no open questions (ready-for-review), complete/in-scope with open questions
(awaiting-clarification), incomplete-or-out-of-scope (halt, no file written), a `claude`
CLI tooling failure (distinct exception, no file written), and -- per the
`change-pr-at-intake` amendment -- the deterministic branch/PR-open step's own failure
mode. The `claude` subprocess call is mocked throughout -- no live CLI/network dependency
-- and `open_implementation_pr.open_pr_for_story` is mocked wholesale here (its own real
body is tested in factory/scripts/tests/test_open_implementation_pr.py); no real
`git`/`gh` process ever runs in this suite.
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import analysis_graph

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import open_implementation_pr
import post_summary
import state_io


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
    fake_pr = {"branch": "light-factory/foo/run-1", "pr_number": 1, "pr_url": "https://example/1"}
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story", return_value=fake_pr) as mock_open_pr, \
         patch("analysis_graph.open_implementation_pr.close_for_clarification") as mock_close, \
         patch("analysis_graph.post_summary.post_comment") as mock_post_summary:
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

    assert outcome["pr"] == fake_pr
    mock_open_pr.assert_called_once_with("foo", "run-1", state_base=tmp_path, cwd=None)
    mock_close.assert_not_called()

    mock_post_summary.assert_called_once()
    posted_pr_number, posted_body = mock_post_summary.call_args[0]
    assert posted_pr_number == 1
    assert "do the thing" in posted_body
    assert mock_post_summary.call_args[1] == {"cwd": None}


# --- I/O Matrix row 2: complete, in-scope, open questions remain --------------------------


def test_complete_with_open_questions_writes_awaiting_clarification(tmp_path):
    result = _result(open_questions=["what about X?"])
    fake_pr = {"branch": "light-factory/foo/run-1", "pr_number": 2, "pr_url": "https://example/2"}
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch(
             "analysis_graph.open_implementation_pr.clarification_status",
             return_value="awaiting-clarification",
         ) as mock_status, \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story", return_value=fake_pr) as mock_open_pr, \
         patch("analysis_graph.open_implementation_pr.label_clarification_round") as mock_label, \
         patch("analysis_graph.open_implementation_pr.close_for_clarification") as mock_close, \
         patch("analysis_graph.open_implementation_pr.post_clarification_cap_notice") as mock_cap_notice, \
         patch("analysis_graph.post_summary.post_comment") as mock_post_summary:
        outcome = analysis_graph.run_analysis(
            "stories/foo.md", "foo", "run-1", state_base=tmp_path
        )

    assert outcome["status"] == "awaiting-clarification"
    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "plan.md")
    assert meta["status"] == "awaiting-clarification"
    dmeta, dbody = state_io.read_state(tmp_path / "foo" / "run-1" / "decisions.md")
    assert dmeta["status"] == "awaiting-clarification"
    assert "what about X?" in dbody

    assert outcome["pr"] == fake_pr
    mock_status.assert_called_once_with("foo", "run-1", cwd=None)
    mock_open_pr.assert_called_once_with("foo", "run-1", state_base=tmp_path, cwd=None)
    mock_label.assert_called_once_with(2, cwd=None)
    mock_close.assert_called_once_with(2, ["what about X?"], cwd=None)
    mock_cap_notice.assert_not_called()
    mock_post_summary.assert_not_called()


# --- cap-reached path (AD-13's bounded-rounds mechanism, ticket 2.2) ----------------------


def test_complete_with_open_questions_at_cap_writes_clarification_cap_reached(tmp_path):
    result = _result(open_questions=["what about X?"])
    fake_pr = {"branch": "light-factory/foo/run-1", "pr_number": 3, "pr_url": "https://example/3"}
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch(
             "analysis_graph.open_implementation_pr.clarification_status",
             return_value="clarification-cap-reached",
         ) as mock_status, \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story", return_value=fake_pr) as mock_open_pr, \
         patch("analysis_graph.open_implementation_pr.label_clarification_round") as mock_label, \
         patch("analysis_graph.open_implementation_pr.close_for_clarification") as mock_close, \
         patch("analysis_graph.open_implementation_pr.post_clarification_cap_notice") as mock_cap_notice, \
         patch("analysis_graph.post_summary.post_comment") as mock_post_summary:
        outcome = analysis_graph.run_analysis(
            "stories/foo.md", "foo", "run-1", state_base=tmp_path
        )

    assert outcome["status"] == "clarification-cap-reached"
    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "plan.md")
    assert meta["status"] == "clarification-cap-reached"
    dmeta, dbody = state_io.read_state(tmp_path / "foo" / "run-1" / "decisions.md")
    assert dmeta["status"] == "clarification-cap-reached"
    assert "what about X?" in dbody

    assert outcome["pr"] == fake_pr
    mock_status.assert_called_once_with("foo", "run-1", cwd=None)
    mock_open_pr.assert_called_once_with("foo", "run-1", state_base=tmp_path, cwd=None)
    mock_cap_notice.assert_called_once_with(3, ["what about X?"], cwd=None)
    # at-cap never labels/closes/comments via the below-cap or ready-for-review paths --
    # post_clarification_cap_notice (mocked above) owns its own labeling internally.
    mock_label.assert_not_called()
    mock_close.assert_not_called()
    mock_post_summary.assert_not_called()


def test_clarification_status_failure_raises_analysis_pr_open_error_with_no_state_files(tmp_path):
    result = _result(open_questions=["what about X?"])
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch(
             "analysis_graph.open_implementation_pr.clarification_status",
             side_effect=open_implementation_pr.PROpenError("gh pr list failed: rate limited"),
         ), \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story") as mock_open_pr:
        with pytest.raises(analysis_graph.AnalysisPROpenError, match="rate limited"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    # this is the new, earlier failure point: it runs before the state write, so -- unlike
    # every other AnalysisPROpenError case -- no state files exist at all.
    assert not (tmp_path / "foo").exists()
    mock_open_pr.assert_not_called()


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
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story") as mock_open_pr:
        with pytest.raises(analysis_graph.AnalysisHalted) as exc_info:
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert "too vague" in exc_info.value.reason
    assert not (tmp_path / "foo").exists()
    mock_open_pr.assert_not_called()


def test_out_of_scope_halts_with_reason_and_writes_nothing(tmp_path):
    result = _result(
        complete=True,
        in_scope=False,
        reason="not something this codebase builds",
        proposal=None,
        subtasks=[],
        tests=[],
    )
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story") as mock_open_pr:
        with pytest.raises(analysis_graph.AnalysisHalted) as exc_info:
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    assert "not something this codebase builds" in exc_info.value.reason
    assert not (tmp_path / "foo").exists()
    mock_open_pr.assert_not_called()


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


# --- I/O Matrix row 5: branch/PR-open step itself fails ----------------------------------


def test_pr_open_failure_raises_analysis_pr_open_error_but_state_files_remain(tmp_path):
    result = _result()
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch(
             "analysis_graph.open_implementation_pr.open_pr_for_story",
             side_effect=open_implementation_pr.PROpenError("gh pr create failed: auth error"),
         ):
        with pytest.raises(analysis_graph.AnalysisPROpenError, match="auth error"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    # plan.md/decisions.md were written before the PR-open step ran -- they stay on disk.
    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "plan.md")
    assert meta["status"] == "ready-for-review"
    dmeta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "decisions.md")
    assert dmeta["status"] == "ready-for-review"


def test_close_for_clarification_failure_raises_analysis_pr_open_error_but_state_files_remain(tmp_path):
    result = _result(open_questions=["what about X?"])
    fake_pr = {"branch": "light-factory/foo/run-1", "pr_number": 2, "pr_url": "https://example/2"}
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch(
             "analysis_graph.open_implementation_pr.clarification_status",
             return_value="awaiting-clarification",
         ), \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story", return_value=fake_pr), \
         patch("analysis_graph.open_implementation_pr.label_clarification_round"), \
         patch(
             "analysis_graph.open_implementation_pr.close_for_clarification",
             side_effect=open_implementation_pr.PROpenError("gh pr close failed: not found"),
         ):
        with pytest.raises(analysis_graph.AnalysisPROpenError, match="not found"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    # plan.md/decisions.md and the PR (per the mock) remain exactly as entry 3 left them --
    # only the comment/close step itself failed.
    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "plan.md")
    assert meta["status"] == "awaiting-clarification"
    dmeta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "decisions.md")
    assert dmeta["status"] == "awaiting-clarification"


def test_post_summary_failure_raises_analysis_pr_open_error_but_state_files_remain(tmp_path):
    result = _result()
    fake_pr = {"branch": "light-factory/foo/run-1", "pr_number": 1, "pr_url": "https://example/1"}
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story", return_value=fake_pr), \
         patch(
             "analysis_graph.post_summary.post_comment",
             side_effect=post_summary.PostCommentError("gh pr comment failed: rate limited"),
         ):
        with pytest.raises(analysis_graph.AnalysisPROpenError, match="rate limited"):
            analysis_graph.run_analysis("stories/foo.md", "foo", "run-1", state_base=tmp_path)

    # plan.md/decisions.md and the PR remain exactly as entry 3 left them -- only the
    # gate-summary comment step itself failed.
    meta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "plan.md")
    assert meta["status"] == "ready-for-review"
    dmeta, _ = state_io.read_state(tmp_path / "foo" / "run-1" / "decisions.md")
    assert dmeta["status"] == "ready-for-review"


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
    fake_pr = {"branch": "light-factory/foo/run-1", "pr_number": 1, "pr_url": "https://example/1"}
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch("analysis_graph.open_implementation_pr.open_pr_for_story", return_value=fake_pr), \
         patch("analysis_graph.post_summary.post_comment"):
        rc = analysis_graph.main(
            ["--story-file", "stories/foo.md", "--story-slug", "foo", "--run-id", "run-1"]
        )
    captured = capsys.readouterr()
    assert rc == 0
    out = json.loads(captured.out.strip())
    assert out["ok"] is True
    assert out["status"] == "ready-for-review"


def test_cli_main_pr_open_error_exits_4(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = _result()
    with patch("analysis_graph.subprocess.run", return_value=_fake_proc(stdout=_cli_output(result))), \
         patch(
             "analysis_graph.open_implementation_pr.open_pr_for_story",
             side_effect=open_implementation_pr.PROpenError("gh pr create failed: auth error"),
         ):
        rc = analysis_graph.main(
            ["--story-file", "stories/foo.md", "--story-slug", "foo", "--run-id", "run-1"]
        )
    captured = capsys.readouterr()
    assert rc == 4
    assert "auth error" in captured.err


# --- CLI: status step output (AD-13) --------------------------------------------------------

_MAIN_ARGS = ["--story-file", "stories/foo.md", "--story-slug", "foo", "--run-id", "run-1"]


@pytest.fixture(autouse=True)
def _no_inherited_github_output(monkeypatch):
    """This suite is itself the pipeline's `test` check, so it runs inside GitHub
    Actions: no test here may append to the runner's real step-output file."""
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)


@pytest.mark.parametrize("status", ["ready-for-review", "awaiting-clarification", "clarification-cap-reached"])
def test_cli_main_appends_status_to_github_output(tmp_path, monkeypatch, status):
    output = tmp_path / "github_output"
    output.write_text("story-slug=foo\n")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    with patch("analysis_graph.run_analysis", return_value={"status": status}):
        rc = analysis_graph.main(_MAIN_ARGS)

    assert rc == 0
    assert output.read_text() == f"story-slug=foo\nstatus={status}\n"


@pytest.mark.parametrize("target", ["dir", "missing_parent"])
def test_cli_main_status_output_write_failure_exits_5(tmp_path, monkeypatch, capsys, target):
    path = tmp_path if target == "dir" else tmp_path / "nope" / "github_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(path))
    with patch("analysis_graph.run_analysis", return_value={"status": "ready-for-review"}):
        rc = analysis_graph.main(_MAIN_ARGS)

    captured = capsys.readouterr()
    assert rc == 5
    assert "status output write failed" in captured.err
    assert str(path) in captured.err
    assert captured.out == ""


def test_write_status_output_raises_analysis_status_output_error(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_OUTPUT", str(tmp_path))
    with pytest.raises(analysis_graph.AnalysisStatusOutputError) as exc:
        analysis_graph._write_status_output("ready-for-review")

    assert str(tmp_path) in str(exc.value)
    assert isinstance(exc.value.__cause__, OSError)


def test_cli_main_without_github_output_writes_no_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
    with patch("analysis_graph.run_analysis", return_value={"status": "ready-for-review"}):
        rc = analysis_graph.main(_MAIN_ARGS)

    assert rc == 0
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    ("error", "exit_code"),
    [
        (analysis_graph.AnalysisHalted("incomplete story"), 1),
        (analysis_graph.AnalysisInvocationError("tool broke"), 3),
        (analysis_graph.AnalysisPROpenError("gh pr create failed"), 4),
    ],
    ids=["halted", "invocation error", "pr-open error"],
)
def test_cli_main_failure_writes_no_status_output(tmp_path, monkeypatch, error, exit_code):
    output = tmp_path / "github_output"
    output.write_text("")
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    with patch("analysis_graph.run_analysis", side_effect=error):
        rc = analysis_graph.main(_MAIN_ARGS)

    assert rc == exit_code
    assert output.read_text() == ""
