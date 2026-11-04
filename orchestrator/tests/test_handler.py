"""Dispatch-level tests for the orchestrator's caller-type auth
(orchestrator/handler.py): webhook accepted, forged webhook rejected,
stage-callback accepted, UI-OAuth stub rejected-as-not-implemented, and a
fully unrecognized caller rejected -- replacing entry 2's now-removed
`_verify_post_comment` tests (that diagnostic backdoor is gone entirely).

Run via `cd orchestrator && uv run --with pytest --with "PyJWT[crypto]"
pytest tests/ -v` (per the story's Verification section) -- no deploy, no
AWS credentials needed: `_load_github_app_credentials` is mocked out in
every test below, so no real Secrets Manager call ever happens here.
PyJWT[crypto] is not needed to import handler.py itself -- its only
module-level import besides stdlib is now `auth`, which is stdlib-only.
It's required because `pytest tests/` also collects tests/test_github_app.py
in the same run, which imports `jwt` at module level, unrelated to
handler.py's own import chain.
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
    "app_id": "123456",
    "installation_id": "987654",
    "private_key_pem": "-----BEGIN PRIVATE KEY-----\nfake\n-----END PRIVATE KEY-----\n",
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
