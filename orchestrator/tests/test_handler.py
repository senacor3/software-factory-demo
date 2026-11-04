"""Dispatch-level tests for the orchestrator's caller-type auth
(orchestrator/handler.py): webhook accepted, forged webhook rejected,
stage-callback accepted, UI-OAuth stub rejected-as-not-implemented, and a
fully unrecognized caller rejected -- replacing entry 2's now-removed
`_verify_post_comment` tests (that diagnostic backdoor is gone entirely).
Also covers this entry's `issue_comment` command-grammar wiring: `/approve`
dispatches + comments, `/rework` appends + re-dispatches, `/reject` marks
terminal + closes + comments, and non-command/non-PR/bot-authored comments
make zero GitHub-API/DynamoDB calls.

Run via `cd orchestrator && uv run --with pytest pytest tests/ -v` (per the
story's Verification section) -- no deploy, no AWS credentials needed:
`_load_github_app_credentials` is mocked out in every test below, so no
real Secrets Manager call ever happens here, and every
`github_app.*`/`dynamodb_state.mark_terminal` call in the command-grammar
tests below is mocked too, so no real GitHub API or DynamoDB call ever
happens here either.
"""

import hashlib
import hmac
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from handler import handler  # noqa: E402

_WEBHOOK_SECRET = "the-configured-webhook-secret"
_STAGE_CALLBACK_SECRET = "the-configured-stage-callback-secret"

_FAKE_CREDENTIALS = {
    "github_pat": "github_pat_fake123",
    "webhook_secret": _WEBHOOK_SECRET,
    "stage_callback_secret": _STAGE_CALLBACK_SECRET,
}


def _signature_header_for(raw_body: bytes, secret: str = _WEBHOOK_SECRET) -> str:
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def _event(headers: dict, body: str = "", is_base64_encoded: bool = False) -> dict:
    return {
        "headers": headers,
        "body": body,
        "isBase64Encoded": is_base64_encoded,
    }


@patch("handler._load_github_app_credentials", return_value=_FAKE_CREDENTIALS)
class TestHandlerDispatch:
    def test_valid_webhook_signature_is_accepted(self, _mock_credentials):
        raw_body = b'{"action": "opened"}'
        event = _event({"X-Hub-Signature-256": _signature_header_for(raw_body)}, body=raw_body.decode())

        response = handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["status"] == "accepted"
        assert body["caller"] == "github-webhook"

    def test_forged_webhook_signature_is_rejected(self, _mock_credentials):
        raw_body = b'{"action": "opened"}'
        forged_header = _signature_header_for(raw_body, secret="attacker-controlled-secret")
        event = _event({"X-Hub-Signature-256": forged_header}, body=raw_body.decode())

        response = handler(event, None)

        assert response["statusCode"] == 401
        body = json.loads(response["body"])
        assert body["status"] == "rejected"
        assert "signature" in body["reason"].lower()

    def test_valid_stage_callback_secret_is_accepted(self, _mock_credentials):
        event = _event({"X-Stage-Callback-Secret": _STAGE_CALLBACK_SECRET})

        response = handler(event, None)

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["status"] == "accepted"
        assert body["caller"] == "stage-callback"

    def test_invalid_stage_callback_secret_is_rejected(self, _mock_credentials):
        event = _event({"X-Stage-Callback-Secret": "wrong-secret"})

        response = handler(event, None)

        assert response["statusCode"] == 401
        body = json.loads(response["body"])
        assert body["status"] == "rejected"
        assert "stage-callback" in body["reason"].lower()

    def test_authorization_header_alone_is_rejected_as_not_implemented(self, _mock_credentials):
        event = _event({"Authorization": "Bearer some-ui-session-token"})

        response = handler(event, None)

        assert response["statusCode"] == 501
        body = json.loads(response["body"])
        assert body["status"] == "rejected"
        assert "not yet implemented" in body["reason"].lower()

    def test_fully_unrecognized_caller_is_rejected(self, _mock_credentials):
        event = _event({"User-Agent": "curl/8.0"})

        response = handler(event, None)

        assert response["statusCode"] == 401
        body = json.loads(response["body"])
        assert body["status"] == "rejected"
        assert "unrecognized" in body["reason"].lower()

    def test_unrecognized_caller_reason_is_distinguishable_from_signature_failure(
        self, _mock_credentials
    ):
        raw_body = b'{"action": "opened"}'
        forged_header = _signature_header_for(raw_body, secret="attacker-controlled-secret")
        forged_response = handler(
            _event({"X-Hub-Signature-256": forged_header}, body=raw_body.decode()), None
        )
        unrecognized_response = handler(_event({"User-Agent": "curl/8.0"}), None)

        forged_reason = json.loads(forged_response["body"])["reason"]
        unrecognized_reason = json.loads(unrecognized_response["body"])["reason"]

        assert forged_reason != unrecognized_reason

    def test_base64_encoded_body_signature_is_verified_on_decoded_bytes(self, _mock_credentials):
        import base64

        raw_body = b'{"action": "opened", "number": 42}'
        encoded_body = base64.b64encode(raw_body).decode()
        signature_header = _signature_header_for(raw_body)
        event = _event(
            {"X-Hub-Signature-256": signature_header}, body=encoded_body, is_base64_encoded=True
        )

        response = handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"])["caller"] == "github-webhook"

    def test_header_lookup_is_case_insensitive(self, _mock_credentials):
        # Function URL / client header casing is not guaranteed -- handler.py
        # must lowercase-key headers itself rather than relying on exact case.
        event = _event({"x-stage-callback-secret": _STAGE_CALLBACK_SECRET})

        response = handler(event, None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"])["caller"] == "stage-callback"


def _issue_comment_payload(
    body: str,
    *,
    pr_number: int = 42,
    action: str = "created",
    comment_user_type: str = "User",
) -> bytes:
    # The PR's head branch (story-slug/run-id source for /approve and /reject)
    # is never read off the webhook payload itself -- handler.py fetches it
    # via github_app.get_pull_request, which every test below mocks directly.
    payload = {
        "action": action,
        "issue": {"number": pr_number, "pull_request": {"url": "..."}},
        "comment": {"body": body, "user": {"type": comment_user_type}},
    }
    return json.dumps(payload).encode("utf-8")


def _webhook_event(raw_body: bytes) -> dict:
    return _event(
        {"X-Hub-Signature-256": _signature_header_for(raw_body)}, body=raw_body.decode()
    )


_GITHUB_PAT = _FAKE_CREDENTIALS["github_pat"]


@patch("handler._load_github_app_credentials", return_value=_FAKE_CREDENTIALS)
class TestCommentCommandGrammar:
    def test_approve_dispatches_workflow_and_posts_comment(self, _mock_credentials):
        with (
            patch("handler.github_app.get_pull_request") as mock_get_pr,
            patch("handler.github_app.dispatch_workflow") as mock_dispatch,
            patch("handler.github_app.post_comment") as mock_post_comment,
        ):
            mock_get_pr.return_value = {
                "head": {"ref": "software-factory/my-story-slug/run-7"}
            }

            raw_body = _issue_comment_payload("/approve")
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_dispatch.assert_called_once_with(
                _GITHUB_PAT,
                "implementation-checks-review.yml",
                "main",
                {"story-slug": "my-story-slug", "run-id": "run-7"},
            )
            mock_post_comment.assert_called_once()
            assert mock_post_comment.call_args[0][0] == _GITHUB_PAT
            assert mock_post_comment.call_args[0][1] == 42

    def test_rework_appends_feedback_and_redispatches_analysis(self, _mock_credentials):
        with (
            patch("handler.github_app.get_pull_request") as mock_get_pr,
            patch("handler.github_app.get_file_content") as mock_get_file,
            patch("handler.github_app.update_file_content") as mock_update_file,
            patch("handler.github_app.dispatch_workflow") as mock_dispatch,
            patch("handler.github_app.post_comment") as mock_post_comment,
        ):
            mock_get_pr.return_value = {
                "head": {"ref": "software-factory/my-story-slug/run-7"}
            }
            mock_get_file.return_value = ("original story text\n", "sha-123")

            raw_body = _issue_comment_payload("/rework please also handle X")
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_get_file.assert_called_once_with(
                _GITHUB_PAT, "stories/light-factory/my-story-slug.md", "main"
            )
            mock_update_file.assert_called_once()
            args = mock_update_file.call_args[0]
            assert args[0] == _GITHUB_PAT
            assert args[1] == "stories/light-factory/my-story-slug.md"
            assert args[2] == "main"
            assert "please also handle X" in args[3]
            assert args[4] == "sha-123"

            mock_dispatch.assert_called_once_with(
                _GITHUB_PAT,
                "analysis.yml",
                "main",
                {"story_file": "stories/light-factory/my-story-slug.md"},
            )
            mock_post_comment.assert_called_once()

    def test_rework_falls_back_to_freight_tenders_project_path(self, _mock_credentials):
        with (
            patch("handler.github_app.get_pull_request") as mock_get_pr,
            patch("handler.github_app.get_file_content") as mock_get_file,
            patch("handler.github_app.update_file_content"),
            patch("handler.github_app.dispatch_workflow") as mock_dispatch,
            patch("handler.github_app.post_comment"),
        ):
            mock_get_pr.return_value = {
                "head": {"ref": "software-factory/my-story-slug/run-7"}
            }

            def _get_file_content(_token, path, _ref):
                if path == "stories/light-factory/my-story-slug.md":
                    raise RuntimeError("GitHub get-file-content request failed (404): not found")
                return ("original text\n", "sha-456")

            mock_get_file.side_effect = _get_file_content

            raw_body = _issue_comment_payload("/rework please also handle X")
            handler(_webhook_event(raw_body), None)

            mock_dispatch.assert_called_once_with(
                _GITHUB_PAT,
                "analysis.yml",
                "main",
                {"story_file": "stories/freight-tenders/my-story-slug.md"},
            )

    def test_rework_story_file_not_found_under_either_project_posts_rejection(
        self, _mock_credentials
    ):
        with (
            patch("handler.github_app.get_pull_request") as mock_get_pr,
            patch("handler.github_app.get_file_content") as mock_get_file,
            patch("handler.github_app.update_file_content") as mock_update_file,
            patch("handler.github_app.dispatch_workflow") as mock_dispatch,
            patch("handler.github_app.post_comment") as mock_post_comment,
        ):
            mock_get_pr.return_value = {
                "head": {"ref": "software-factory/my-story-slug/run-7"}
            }
            mock_get_file.side_effect = RuntimeError(
                "GitHub get-file-content request failed (404): not found"
            )

            raw_body = _issue_comment_payload("/rework please also handle X")
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_update_file.assert_not_called()
            mock_dispatch.assert_not_called()
            mock_post_comment.assert_called_once()
            assert "not" in mock_post_comment.call_args[0][2].lower()

    def test_reject_marks_terminal_closes_pr_and_comments(self, _mock_credentials):
        with (
            patch("handler.github_app.get_pull_request") as mock_get_pr,
            patch("handler.dynamodb_state.mark_terminal") as mock_mark_terminal,
            patch("handler.github_app.close_pull_request") as mock_close_pr,
            patch("handler.github_app.post_comment") as mock_post_comment,
        ):
            mock_get_pr.return_value = {
                "head": {"ref": "software-factory/my-story-slug/run-7"}
            }

            raw_body = _issue_comment_payload("/reject")
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_mark_terminal.assert_called_once()
            assert mock_mark_terminal.call_args[0][0] == "my-story-slug"
            assert mock_mark_terminal.call_args[0][1] == "run-7"
            mock_close_pr.assert_called_once_with(_GITHUB_PAT, 42)
            mock_post_comment.assert_called_once()

    def test_reject_on_a_pr_with_a_non_matching_branch_makes_no_close_or_comment_call(
        self, _mock_credentials
    ):
        # A PR whose head branch isn't this pipeline's own naming scheme
        # (AD-12/AD-20) is not one this pipeline opened -- /reject must not
        # close or comment on it, same guard as /approve and /rework.
        with (
            patch("handler.github_app.get_pull_request") as mock_get_pr,
            patch("handler.dynamodb_state.mark_terminal") as mock_mark_terminal,
            patch("handler.github_app.close_pull_request") as mock_close_pr,
            patch("handler.github_app.post_comment") as mock_post_comment,
        ):
            mock_get_pr.return_value = {"head": {"ref": "some-unrelated-branch"}}

            raw_body = _issue_comment_payload("/reject")
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_mark_terminal.assert_not_called()
            mock_close_pr.assert_not_called()
            mock_post_comment.assert_not_called()

    def test_non_command_comment_makes_zero_api_calls(self, _mock_credentials):
        with (
            patch("handler.github_app.get_pull_request") as mock_get_pr,
            patch("handler.github_app.dispatch_workflow") as mock_dispatch,
            patch("handler.github_app.post_comment") as mock_post_comment,
            patch("handler.github_app.close_pull_request") as mock_close_pr,
            patch("handler.dynamodb_state.mark_terminal") as mock_mark_terminal,
        ):
            raw_body = _issue_comment_payload("looks good, thanks!")
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_get_pr.assert_not_called()
            mock_dispatch.assert_not_called()
            mock_post_comment.assert_not_called()
            mock_close_pr.assert_not_called()
            mock_mark_terminal.assert_not_called()

    def test_comment_on_a_plain_issue_is_ignored(self, _mock_credentials):
        payload = {
            "action": "created",
            "issue": {"number": 42},  # no "pull_request" key
            "comment": {"body": "/approve", "user": {"type": "User"}},
        }
        raw_body = json.dumps(payload).encode("utf-8")

        with patch("handler.github_app.get_pull_request") as mock_get_pr:
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_get_pr.assert_not_called()

    def test_comment_by_a_bot_is_ignored(self, _mock_credentials):
        raw_body = _issue_comment_payload("/approve", comment_user_type="Bot")

        with patch("handler.github_app.get_pull_request") as mock_get_pr:
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_get_pr.assert_not_called()

    def test_rework_with_no_feedback_text_is_ignored_like_a_non_command(
        self, _mock_credentials
    ):
        raw_body = _issue_comment_payload("/rework")

        with patch("handler.github_app.get_pull_request") as mock_get_pr:
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_get_pr.assert_not_called()

    def test_edited_comment_action_is_ignored(self, _mock_credentials):
        raw_body = _issue_comment_payload("/approve", action="edited")

        with patch("handler.github_app.get_pull_request") as mock_get_pr:
            response = handler(_webhook_event(raw_body), None)

            assert response["statusCode"] == 200
            mock_get_pr.assert_not_called()
