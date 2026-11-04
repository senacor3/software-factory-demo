"""Unit tests for the gate-agnostic PR-comment command grammar
(orchestrator/comment_commands.py): approve/reject/rework-with-feedback/
rework-without-feedback/plain-comment parsing, per this story's I/O
matrix.

Pure parsing logic, no network/AWS -- run via `cd orchestrator && uv run
--with pytest pytest tests/ -v`.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from comment_commands import GateCommand, parse_gate_command  # noqa: E402


class TestApprove:
    def test_bare_approve_is_recognized(self):
        assert parse_gate_command("/approve") == GateCommand(kind="approve")

    def test_approve_with_surrounding_whitespace_is_recognized(self):
        assert parse_gate_command("   /approve   \n") == GateCommand(kind="approve")

    def test_approve_followed_by_free_text_on_a_later_line_is_still_approve(self):
        assert parse_gate_command("/approve\nLGTM, go ahead!") == GateCommand(kind="approve")

    def test_approve_with_trailing_text_on_the_same_line_is_not_recognized(self):
        # First-line match is exact -- "/approve please proceed" isn't
        # "/approve", so the whole comment is unrecognized.
        assert parse_gate_command("/approve please proceed").kind == "none"


class TestReject:
    def test_bare_reject_is_recognized(self):
        assert parse_gate_command("/reject") == GateCommand(kind="reject")

    def test_reject_with_surrounding_whitespace_is_recognized(self):
        assert parse_gate_command("  /reject  ") == GateCommand(kind="reject")


class TestRework:
    def test_rework_with_feedback_is_recognized(self):
        result = parse_gate_command("/rework please also handle X")
        assert result.kind == "rework"
        assert result.feedback == "please also handle X"

    def test_rework_with_multiline_feedback_is_recognized(self):
        result = parse_gate_command("/rework please also handle X\nand also Y")
        assert result.kind == "rework"
        assert result.feedback == "please also handle X\nand also Y"

    def test_rework_with_no_feedback_text_is_unrecognized(self):
        assert parse_gate_command("/rework").kind == "none"

    def test_rework_with_only_whitespace_feedback_is_unrecognized(self):
        assert parse_gate_command("/rework    ").kind == "none"

    def test_rework_word_that_merely_starts_with_rework_is_unrecognized(self):
        assert parse_gate_command("/reworking this story").kind == "none"


class TestNonCommand:
    def test_plain_comment_is_ignored(self):
        assert parse_gate_command("looks good, thanks!") == GateCommand(kind="none")

    def test_empty_body_is_ignored(self):
        assert parse_gate_command("") == GateCommand(kind="none")

    def test_whitespace_only_body_is_ignored(self):
        assert parse_gate_command("   \n  ") == GateCommand(kind="none")

    def test_unrelated_slash_command_is_ignored(self):
        assert parse_gate_command("/merge").kind == "none"
