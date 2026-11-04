"""Unit tests for PR-comment posting and the GitHub API surface the
`/approve`/`/rework`/`/reject` comment-command grammar needs
(orchestrator/github_app.py): post_comment, get_pull_request,
dispatch_workflow, get_file_content, update_file_content,
close_pull_request.

No real network calls: every function mocks urllib.request.urlopen. Auth
is a fine-grained GitHub PAT (AD-18) passed straight through as the Bearer
token -- no JWT minting or installation-token exchange.

Run via `cd orchestrator && uv run --with pytest pytest tests/ -v`.
"""

import base64
import json
import sys
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from github_app import (  # noqa: E402
    close_pull_request,
    dispatch_workflow,
    get_file_content,
    get_pull_request,
    post_comment,
    update_file_content,
)


def _fake_http_response(payload: dict) -> MagicMock:
    response = MagicMock()
    response.read.return_value = json.dumps(payload).encode("utf-8")
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class TestPostComment:
    @patch("github_app.urllib.request.urlopen")
    def test_posts_comment_to_fixed_repo_and_pr(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response({"id": 1, "body": "hello"})

        result = post_comment("ghs_abc123", 42, "hello")

        assert result == {"id": 1, "body": "hello"}
        request = mock_urlopen.call_args[0][0]
        assert request.full_url == (
            "https://api.github.com/repos/senacor3/software-factory-demo/issues/42/comments"
        )
        assert request.get_header("Authorization") == "Bearer ghs_abc123"
        assert json.loads(request.data.decode("utf-8")) == {"body": "hello"}

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_github_error_body_on_failure(self, mock_urlopen):
        error_body = json.dumps({"message": "Not Found"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url=(
                "https://api.github.com/repos/senacor3/software-factory-demo"
                "/issues/42/comments"
            ),
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match="Not Found"):
            post_comment("ghs_abc123", 42, "hello")


class TestGetPullRequest:
    @patch("github_app.urllib.request.urlopen")
    def test_returns_pr_resource_from_fixed_repo(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response(
            {"number": 42, "head": {"ref": "software-factory/my-slug/run-7"}}
        )

        result = get_pull_request("ghs_abc123", 42)

        assert result["head"]["ref"] == "software-factory/my-slug/run-7"
        request = mock_urlopen.call_args[0][0]
        assert request.full_url == (
            "https://api.github.com/repos/senacor3/software-factory-demo/pulls/42"
        )
        assert request.get_header("Authorization") == "Bearer ghs_abc123"

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_github_error_body_on_failure(self, mock_urlopen):
        error_body = json.dumps({"message": "Not Found"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/repos/senacor3/software-factory-demo/pulls/42",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match="Not Found"):
            get_pull_request("ghs_abc123", 42)


class TestDispatchWorkflow:
    @patch("github_app.urllib.request.urlopen")
    def test_posts_dispatch_with_ref_and_inputs(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response({})

        dispatch_workflow(
            "ghs_abc123",
            "implementation-checks-review.yml",
            "main",
            {"story-slug": "my-slug", "run-id": "run-7"},
        )

        request = mock_urlopen.call_args[0][0]
        assert request.full_url == (
            "https://api.github.com/repos/senacor3/software-factory-demo/actions/"
            "workflows/implementation-checks-review.yml/dispatches"
        )
        assert request.get_method() == "POST"
        assert request.get_header("Authorization") == "Bearer ghs_abc123"
        payload = json.loads(request.data.decode("utf-8"))
        assert payload == {
            "ref": "main",
            "inputs": {"story-slug": "my-slug", "run-id": "run-7"},
        }

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_github_error_body_on_failure(self, mock_urlopen):
        error_body = json.dumps({"message": "Unprocessable Entity"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/repos/senacor3/software-factory-demo",
            code=422,
            msg="Unprocessable Entity",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match="Unprocessable Entity"):
            dispatch_workflow("ghs_abc123", "analysis.yml", "main", {"story_file": "x.md"})


class TestGetFileContent:
    @patch("github_app.urllib.request.urlopen")
    def test_decodes_base64_content_and_returns_sha(self, mock_urlopen):
        encoded = base64.b64encode(b"story file text\nmore text").decode("ascii")
        mock_urlopen.return_value = _fake_http_response(
            {"content": encoded, "sha": "abc123sha"}
        )

        content, sha = get_file_content(
            "ghs_abc123", "stories/light-factory/my-slug.md", "main"
        )

        assert content == "story file text\nmore text"
        assert sha == "abc123sha"
        request = mock_urlopen.call_args[0][0]
        assert request.full_url == (
            "https://api.github.com/repos/senacor3/software-factory-demo/contents/"
            "stories/light-factory/my-slug.md?ref=main"
        )

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_404_in_error_message_for_a_missing_path(self, mock_urlopen):
        error_body = json.dumps({"message": "Not Found"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/repos/senacor3/software-factory-demo/contents/x.md",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match=r"\(404\)"):
            get_file_content("ghs_abc123", "stories/freight-tenders/my-slug.md", "main")


class TestUpdateFileContent:
    @patch("github_app.urllib.request.urlopen")
    def test_puts_base64_encoded_content_with_sha_and_branch(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response({"commit": {"sha": "newsha"}})

        update_file_content(
            "ghs_abc123",
            "stories/light-factory/my-slug.md",
            "main",
            "new story content",
            "oldsha",
            "Append /rework feedback",
        )

        request = mock_urlopen.call_args[0][0]
        assert request.full_url == (
            "https://api.github.com/repos/senacor3/software-factory-demo/contents/"
            "stories/light-factory/my-slug.md"
        )
        assert request.get_method() == "PUT"
        payload = json.loads(request.data.decode("utf-8"))
        assert payload["sha"] == "oldsha"
        assert payload["branch"] == "main"
        assert payload["message"] == "Append /rework feedback"
        assert base64.b64decode(payload["content"]).decode("utf-8") == "new story content"

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_github_error_body_on_failure(self, mock_urlopen):
        error_body = json.dumps({"message": "sha does not match"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/repos/senacor3/software-factory-demo/contents/x.md",
            code=409,
            msg="Conflict",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match="sha does not match"):
            update_file_content(
                "ghs_abc123", "x.md", "main", "content", "oldsha", "message"
            )


class TestClosePullRequest:
    @patch("github_app.urllib.request.urlopen")
    def test_patches_state_closed(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response({"number": 42, "state": "closed"})

        close_pull_request("ghs_abc123", 42)

        request = mock_urlopen.call_args[0][0]
        assert request.full_url == (
            "https://api.github.com/repos/senacor3/software-factory-demo/pulls/42"
        )
        assert request.get_method() == "PATCH"
        assert json.loads(request.data.decode("utf-8")) == {"state": "closed"}

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_github_error_body_on_failure(self, mock_urlopen):
        error_body = json.dumps({"message": "Not Found"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/repos/senacor3/software-factory-demo/pulls/42",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match="Not Found"):
            close_pull_request("ghs_abc123", 42)
