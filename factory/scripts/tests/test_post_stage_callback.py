# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for post_stage_callback.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_post_stage_callback.py

Covers `post`'s request shape (URL, header, JSON body) and non-2xx/transport-failure
handling, plus the CLI's `--status-file`/`--status` mutually exclusive status source.
No real network call: `urllib.request.urlopen` is mocked throughout.
"""

import json
import sys
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import post_stage_callback
import state_io


def _fake_http_response() -> MagicMock:
    response = MagicMock()
    response.read.return_value = b""
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class TestPost:
    @patch("post_stage_callback.urllib.request.urlopen")
    def test_posts_expected_url_header_and_body(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response()

        post_stage_callback.post(
            "https://orchestrator.example/callback",
            "the-shared-secret",
            "analysis",
            "my-story-slug",
            "run-7",
            "ready-for-review",
        )

        request = mock_urlopen.call_args[0][0]
        assert request.full_url == "https://orchestrator.example/callback"
        assert request.get_method() == "POST"
        assert request.get_header("X-stage-callback-secret") == "the-shared-secret"
        assert json.loads(request.data.decode("utf-8")) == {
            "stage": "analysis",
            "story-slug": "my-story-slug",
            "run-id": "run-7",
            "status": "ready-for-review",
        }

    @patch("post_stage_callback.urllib.request.urlopen")
    def test_surfaces_http_error_body_on_non_2xx(self, mock_urlopen):
        error_body = json.dumps({"status": "rejected", "reason": "bad secret"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://orchestrator.example/callback",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(post_stage_callback.StageCallbackError, match="bad secret"):
            post_stage_callback.post(
                "https://orchestrator.example/callback",
                "wrong-secret",
                "merge",
                "my-story-slug",
                "run-7",
                "merged",
            )

    @patch("post_stage_callback.urllib.request.urlopen")
    def test_surfaces_transport_failure(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("connection refused")

        with pytest.raises(post_stage_callback.StageCallbackError, match="connection refused"):
            post_stage_callback.post(
                "https://orchestrator.example/callback",
                "the-shared-secret",
                "merge",
                "my-story-slug",
                "run-7",
                "merged",
            )


class TestCli:
    def test_status_file_reads_status_from_state_file(self, tmp_path):
        plan_path = tmp_path / "plan.md"
        state_io.write_state(
            plan_path,
            story_slug="my-story-slug",
            stage="analysis",
            status="ready-for-review",
            body="## Proposal\n\ndo the thing",
        )

        with patch("post_stage_callback.post") as mock_post:
            rc = post_stage_callback.main(
                [
                    "--url", "https://orchestrator.example/callback",
                    "--secret", "the-shared-secret",
                    "--stage", "analysis",
                    "--story-slug", "my-story-slug",
                    "--run-id", "run-7",
                    "--status-file", str(plan_path),
                ]
            )

        assert rc == 0
        mock_post.assert_called_once_with(
            "https://orchestrator.example/callback",
            "the-shared-secret",
            "analysis",
            "my-story-slug",
            "run-7",
            "ready-for-review",
        )

    def test_literal_status_is_used_verbatim(self):
        with patch("post_stage_callback.post") as mock_post:
            rc = post_stage_callback.main(
                [
                    "--url", "https://orchestrator.example/callback",
                    "--secret", "the-shared-secret",
                    "--stage", "merge",
                    "--story-slug", "my-story-slug",
                    "--run-id", "run-7",
                    "--status", "merged",
                ]
            )

        assert rc == 0
        mock_post.assert_called_once_with(
            "https://orchestrator.example/callback",
            "the-shared-secret",
            "merge",
            "my-story-slug",
            "run-7",
            "merged",
        )

    def test_status_file_and_status_are_mutually_exclusive(self):
        with pytest.raises(SystemExit):
            post_stage_callback.main(
                [
                    "--url", "https://orchestrator.example/callback",
                    "--secret", "the-shared-secret",
                    "--stage", "merge",
                    "--story-slug", "my-story-slug",
                    "--run-id", "run-7",
                    "--status", "merged",
                    "--status-file", "plan.md",
                ]
            )

    def test_neither_status_source_is_rejected(self):
        with pytest.raises(SystemExit):
            post_stage_callback.main(
                [
                    "--url", "https://orchestrator.example/callback",
                    "--secret", "the-shared-secret",
                    "--stage", "merge",
                    "--story-slug", "my-story-slug",
                    "--run-id", "run-7",
                ]
            )

    def test_post_failure_exits_1(self, capsys):
        with patch(
            "post_stage_callback.post",
            side_effect=post_stage_callback.StageCallbackError("stage-callback POST failed (401): bad secret"),
        ):
            rc = post_stage_callback.main(
                [
                    "--url", "https://orchestrator.example/callback",
                    "--secret", "wrong-secret",
                    "--stage", "merge",
                    "--story-slug", "my-story-slug",
                    "--run-id", "run-7",
                    "--status", "merged",
                ]
            )

        captured = capsys.readouterr()
        assert rc == 1
        assert "bad secret" in captured.err
