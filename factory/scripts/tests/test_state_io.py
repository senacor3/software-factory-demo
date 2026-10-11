# /// script
# requires-python = ">=3.11"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for state_io.py. Run: uv run --with pytest pytest factory/scripts/tests/test_state_io.py

Covers the I/O & Edge-Case Matrix in story-shared-state-library-plan.md: round-trip
read/write of AD-10's exact frontmatter schema, invalid-status rejection before any
write, non-kebab-case story-file rejection (function and CLI), and the directory layout
AD-8/AD-15 require.
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import state_io

# --- derive_story_slug / derive_run_id (AD-8 / AD-15) -----------------------


def test_derive_story_slug_valid_kebab_case():
    assert state_io.derive_story_slug("stories/trivial-test-story.md") == "trivial-test-story"


def test_derive_story_slug_non_kebab_case_raises():
    with pytest.raises(ValueError):
        state_io.derive_story_slug("stories/Not_Kebab.md")


def test_derive_story_slug_requires_md_extension():
    with pytest.raises(ValueError):
        state_io.derive_story_slug("stories/trivial-test-story.txt")


def test_derive_story_slug_rejects_empty_slug():
    with pytest.raises(ValueError):
        state_io.derive_story_slug("stories/.md")


def test_derive_story_slug_rejects_leading_or_trailing_hyphen():
    with pytest.raises(ValueError):
        state_io.derive_story_slug("stories/-leading.md")
    with pytest.raises(ValueError):
        state_io.derive_story_slug("stories/trailing-.md")


def test_derive_story_slug_rejects_double_hyphen():
    with pytest.raises(ValueError):
        state_io.derive_story_slug("stories/double--hyphen.md")


def test_derive_story_slug_allows_digits():
    assert state_io.derive_story_slug("stories/story-v2.md") == "story-v2"


def test_derive_story_slug_rejects_file_outside_stories_dir():
    with pytest.raises(ValueError, match="other/foo.md"):
        state_io.derive_story_slug("other/foo.md")


def test_derive_story_slug_rejects_bare_filename():
    with pytest.raises(ValueError):
        state_io.derive_story_slug("foo.md")


def test_derive_story_slug_rejects_stories_subfolder():
    with pytest.raises(ValueError):
        state_io.derive_story_slug("stories/billing/foo.md")


def test_derive_story_slug_accepts_leading_path():
    assert state_io.derive_story_slug("./stories/foo.md") == "foo"
    assert state_io.derive_story_slug("/repo/stories/foo.md") == "foo"


def test_derive_run_id_formats_run_dash_prefix():
    assert state_io.derive_run_id(12345) == "run-12345"
    assert state_io.derive_run_id("12345") == "run-12345"


def test_derive_run_id_rejects_empty():
    with pytest.raises(ValueError):
        state_io.derive_run_id("")


# --- state_dir / ensure_layout (AD-8) ---------------------------------------


def test_state_dir_shape(tmp_path):
    d = state_io.state_dir("foo-bar", "run-1", base=tmp_path)
    assert d == tmp_path / "foo-bar" / "run-1"


def test_ensure_layout_creates_evidence_dirs(tmp_path):
    d = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    assert (d / "evidence" / "checks").is_dir()
    assert (d / "evidence" / "review").is_dir()


def test_ensure_layout_does_not_create_state_files(tmp_path):
    d = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    assert not (d / "plan.md").exists()
    assert not (d / "decisions.md").exists()
    assert not (d / "review.md").exists()


def test_ensure_layout_is_idempotent(tmp_path):
    state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)
    d = state_io.ensure_layout("foo-bar", "run-1", base=tmp_path)  # no error on re-call
    assert (d / "evidence" / "checks").is_dir()


# --- write_state / read_state round-trip (AD-10) ----------------------------


def test_round_trip_all_five_ad10_fields(tmp_path):
    path = tmp_path / "foo-bar" / "run-1" / "plan.md"
    state_io.write_state(
        path, story_slug="foo-bar", stage="analysis", status="drafted", body="## Plan\n\nhello"
    )
    meta, body = state_io.read_state(path)
    assert set(meta.keys()) == {"schema_version", "story_slug", "stage", "status", "updated"}
    assert meta["story_slug"] == "foo-bar"
    assert meta["stage"] == "analysis"
    assert meta["status"] == "drafted"
    assert meta["schema_version"] == 1
    assert isinstance(meta["schema_version"], int)
    assert meta.get("updated")
    assert body.strip() == "## Plan\n\nhello"


def test_round_trip_empty_body(tmp_path):
    path = tmp_path / "review.md"
    state_io.write_state(path, story_slug="foo-bar", stage="review", status="in-review")
    meta, body = state_io.read_state(path)
    assert meta["stage"] == "review"
    assert body == ""


def test_write_state_creates_missing_parent_dirs(tmp_path):
    path = tmp_path / "deeply" / "nested" / "dir" / "plan.md"
    state_io.write_state(path, story_slug="foo-bar", stage="analysis", status="drafted")
    assert path.is_file()


def test_write_state_is_atomic_no_leftover_tmp(tmp_path):
    path = tmp_path / "plan.md"
    state_io.write_state(path, story_slug="foo-bar", stage="analysis", status="drafted")
    assert not list(tmp_path.glob("*.tmp"))


def test_write_state_returns_meta_written(tmp_path):
    path = tmp_path / "plan.md"
    meta = state_io.write_state(path, story_slug="foo-bar", stage="analysis", status="drafted")
    assert meta["story_slug"] == "foo-bar"


# --- invalid status rejection (AD-10 per-stage enum) ------------------------


def test_invalid_status_for_review_stage_raises_before_write(tmp_path):
    path = tmp_path / "review.md"
    with pytest.raises(ValueError):
        state_io.write_state(path, story_slug="foo-bar", stage="review", status="drafted")
    assert not path.exists()  # nothing written on validation failure


def test_invalid_status_for_analysis_stage_raises(tmp_path):
    path = tmp_path / "plan.md"
    with pytest.raises(ValueError):
        state_io.write_state(path, story_slug="foo-bar", stage="analysis", status="in-review")
    assert not path.exists()


def test_unknown_stage_raises(tmp_path):
    path = tmp_path / "x.md"
    with pytest.raises(ValueError):
        state_io.write_state(path, story_slug="foo-bar", stage="bogus-stage", status="drafted")


def test_empty_status_raises(tmp_path):
    path = tmp_path / "x.md"
    with pytest.raises(ValueError):
        state_io.write_state(path, story_slug="foo-bar", stage="analysis", status="")


def test_empty_story_slug_raises(tmp_path):
    path = tmp_path / "x.md"
    with pytest.raises(ValueError):
        state_io.write_state(path, story_slug="", stage="analysis", status="drafted")


@pytest.mark.parametrize("status", sorted(state_io.STATUS_BY_STAGE["analysis"]))
def test_all_analysis_statuses_accepted(tmp_path, status):
    path = tmp_path / f"{status}.md"
    state_io.write_state(path, story_slug="foo-bar", stage="analysis", status=status)
    meta, _ = state_io.read_state(path)
    assert meta["status"] == status


@pytest.mark.parametrize("status", sorted(state_io.STATUS_BY_STAGE["review"]))
def test_all_review_statuses_accepted(tmp_path, status):
    path = tmp_path / f"{status}.md"
    state_io.write_state(path, story_slug="foo-bar", stage="review", status=status)
    meta, _ = state_io.read_state(path)
    assert meta["status"] == status


# --- implementation stage: no closed enum (Design Notes) --------------------


def test_implementation_stage_accepts_arbitrary_nonempty_status(tmp_path):
    path = tmp_path / "x.md"
    state_io.write_state(
        path, story_slug="foo-bar", stage="implementation", status="anything-goes"
    )
    meta, _ = state_io.read_state(path)
    assert meta["status"] == "anything-goes"


def test_implementation_stage_still_rejects_empty_status(tmp_path):
    path = tmp_path / "x.md"
    with pytest.raises(ValueError):
        state_io.write_state(path, story_slug="foo-bar", stage="implementation", status="")


# --- write_state's optional extra kwarg (fix_loop_graph.py's fix_cycle counter) --


def test_write_state_extra_merged_after_fixed_fields(tmp_path):
    path = tmp_path / "review.md"
    meta = state_io.write_state(
        path,
        story_slug="foo-bar",
        stage="review",
        status="resolved",
        extra={"fix_cycle": 2},
    )
    assert meta["fix_cycle"] == 2
    read_meta, _ = state_io.read_state(path)
    assert read_meta["fix_cycle"] == "2"  # frontmatter values round-trip as strings


def test_write_state_omitted_extra_unchanged_behavior(tmp_path):
    path = tmp_path / "plan.md"
    meta = state_io.write_state(path, story_slug="foo-bar", stage="analysis", status="drafted")
    assert set(meta.keys()) == {"schema_version", "story_slug", "stage", "status", "updated"}


def test_write_state_extra_none_unchanged_behavior(tmp_path):
    path = tmp_path / "plan.md"
    meta = state_io.write_state(
        path, story_slug="foo-bar", stage="analysis", status="drafted", extra=None
    )
    assert set(meta.keys()) == {"schema_version", "story_slug", "stage", "status", "updated"}


# --- robustness: frontmatter edge cases (mirrors memlog.py's split/render) --


def test_roundtrip_render_is_stable(tmp_path):
    path = tmp_path / "plan.md"
    state_io.write_state(path, story_slug="foo-bar", stage="analysis", status="drafted", body="x")
    first = path.read_text(encoding="utf-8")
    meta, body = state_io.split(first)
    assert state_io.render(meta, body) == first


def test_triple_dash_in_body_does_not_break_frontmatter(tmp_path):
    path = tmp_path / "plan.md"
    state_io.write_state(
        path, story_slug="foo-bar", stage="analysis", status="drafted", body="line\n---\nmore"
    )
    meta, body = state_io.read_state(path)
    assert meta["story_slug"] == "foo-bar"
    assert "line" in body and "more" in body


# --- CLI ---------------------------------------------------------------------


def test_cli_derive_success(capsys):
    rc = state_io.main(
        ["derive", "--story-file", "stories/trivial-test-story.md", "--github-run-id", "999"]
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert "story-slug=trivial-test-story" in out
    assert "run-id=run-999" in out


def test_cli_derive_non_kebab_case_exits_2_and_prints_stderr(capsys):
    rc = state_io.main(
        ["derive", "--story-file", "stories/Not_Kebab.md", "--github-run-id", "999"]
    )
    captured = capsys.readouterr()
    assert rc == 2
    assert captured.out == ""
    assert "error" in captured.err


def test_cli_derive_file_outside_stories_dir_exits_2_and_prints_stderr(capsys):
    rc = state_io.main(["derive", "--story-file", "other/foo.md", "--github-run-id", "999"])
    captured = capsys.readouterr()
    assert rc == 2
    assert captured.out == ""
    assert "error" in captured.err


def test_cli_write_then_read_round_trip(tmp_path, capsys):
    path = tmp_path / "plan.md"
    rc = state_io.main(
        [
            "write",
            "--path",
            str(path),
            "--story-slug",
            "foo-bar",
            "--stage",
            "analysis",
            "--status",
            "drafted",
            "--body",
            "hello world",
        ]
    )
    assert rc == 0
    capsys.readouterr()  # drain the write ack

    rc = state_io.main(["read", "--path", str(path)])
    out = json.loads(capsys.readouterr().out.strip())
    assert rc == 0
    assert out["ok"] is True
    assert out["meta"]["story_slug"] == "foo-bar"
    assert out["meta"]["status"] == "drafted"
    assert "hello world" in out["body"]


def test_cli_write_invalid_status_exits_2_and_writes_nothing(tmp_path, capsys):
    path = tmp_path / "review.md"
    rc = state_io.main(
        [
            "write",
            "--path",
            str(path),
            "--story-slug",
            "foo-bar",
            "--stage",
            "review",
            "--status",
            "drafted",
        ]
    )
    captured = capsys.readouterr()
    assert rc == 2
    assert "error" in captured.err
    assert not path.exists()


def test_cli_write_rejects_unknown_stage_choice():
    with pytest.raises(SystemExit):
        state_io.main(
            [
                "write",
                "--path",
                "x.md",
                "--story-slug",
                "foo-bar",
                "--stage",
                "bogus",
                "--status",
                "drafted",
            ]
        )


def test_cli_write_body_file_reads_body_from_disk(tmp_path, capsys):
    body_file = tmp_path / "body.txt"
    body_file.write_text("from a file", encoding="utf-8")
    path = tmp_path / "plan.md"
    rc = state_io.main(
        [
            "write",
            "--path",
            str(path),
            "--story-slug",
            "foo-bar",
            "--stage",
            "analysis",
            "--status",
            "drafted",
            "--body-file",
            str(body_file),
        ]
    )
    capsys.readouterr()
    assert rc == 0
    _, body = state_io.read_state(path)
    assert "from a file" in body


def test_cli_write_body_file_missing_exits_2_not_traceback(tmp_path, capsys):
    path = tmp_path / "plan.md"
    rc = state_io.main(
        [
            "write",
            "--path",
            str(path),
            "--story-slug",
            "foo-bar",
            "--stage",
            "analysis",
            "--status",
            "drafted",
            "--body-file",
            str(tmp_path / "does-not-exist.txt"),
        ]
    )
    captured = capsys.readouterr()
    assert rc == 2
    assert "error" in captured.err
    assert not path.exists()


def test_cli_write_body_and_body_file_together_exits_2(tmp_path, capsys):
    body_file = tmp_path / "body.txt"
    body_file.write_text("from a file", encoding="utf-8")
    path = tmp_path / "plan.md"
    rc = state_io.main(
        [
            "write",
            "--path",
            str(path),
            "--story-slug",
            "foo-bar",
            "--stage",
            "analysis",
            "--status",
            "drafted",
            "--body",
            "inline",
            "--body-file",
            str(body_file),
        ]
    )
    captured = capsys.readouterr()
    assert rc == 2
    assert "error" in captured.err
    assert not path.exists()
