"""Unit tests for the caller-authentication primitives
(orchestrator/auth.py): GitHub webhook HMAC-SHA256 signature verification
and the stage-completion callback's shared-secret comparison.

No network, no AWS -- pure stdlib hmac/hashlib logic, per the story's I/O
matrix and Verification section.

Run via `cd orchestrator && uv run --with pytest pytest tests/ -v`.
"""

import base64
import hashlib
import hmac
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from auth import verify_github_webhook_signature, verify_stage_callback_secret  # noqa: E402

_SECRET = "a-shared-webhook-secret"


def _signature_header_for(raw_body: bytes, secret: str = _SECRET) -> str:
    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


class TestVerifyGithubWebhookSignature:
    def test_valid_signature_is_accepted(self):
        raw_body = b'{"action": "opened"}'
        signature_header = _signature_header_for(raw_body)

        assert verify_github_webhook_signature(raw_body, signature_header, _SECRET) is True

    def test_forged_signature_is_rejected(self):
        # Deliberate forged-signature attempt: correctly-shaped header,
        # computed with the wrong secret -- the ticket's own named check.
        raw_body = b'{"action": "opened"}'
        forged_header = _signature_header_for(raw_body, secret="attacker-controlled-secret")

        assert verify_github_webhook_signature(raw_body, forged_header, _SECRET) is False

    def test_tampered_body_is_rejected(self):
        raw_body = b'{"action": "opened"}'
        signature_header = _signature_header_for(raw_body)
        tampered_body = b'{"action": "closed"}'

        assert verify_github_webhook_signature(tampered_body, signature_header, _SECRET) is False

    def test_missing_header_is_rejected(self):
        raw_body = b'{"action": "opened"}'

        assert verify_github_webhook_signature(raw_body, None, _SECRET) is False

    def test_malformed_header_is_rejected(self):
        raw_body = b'{"action": "opened"}'

        assert verify_github_webhook_signature(raw_body, "not-a-real-signature", _SECRET) is False

    def test_legacy_sha1_shaped_header_is_rejected(self):
        # Only sha256=<hex> is ever accepted -- a sha1=<hex>-shaped value
        # (what the legacy X-Hub-Signature header carries) must not verify,
        # even though this function has no SHA-1 code path to fall back to.
        raw_body = b'{"action": "opened"}'
        sha1_digest = hmac.new(_SECRET.encode("utf-8"), raw_body, hashlib.sha1).hexdigest()

        assert verify_github_webhook_signature(raw_body, f"sha1={sha1_digest}", _SECRET) is False

    def test_base64_encoded_body_is_verified_on_decoded_bytes(self):
        # Simulates handler.py's own base64-decode step: the signature must
        # be computed/verified over the decoded raw bytes, never the
        # base64 text itself.
        raw_body = b'{"action": "opened", "number": 42}'
        encoded_body = base64.b64encode(raw_body)
        signature_header = _signature_header_for(raw_body)

        decoded_body = base64.b64decode(encoded_body)
        assert verify_github_webhook_signature(decoded_body, signature_header, _SECRET) is True

        # Hashing the still-encoded (base64 text) bytes must NOT verify --
        # proves decoding happens before hashing, not after/never.
        assert verify_github_webhook_signature(encoded_body, signature_header, _SECRET) is False


class TestVerifyStageCallbackSecret:
    def test_matching_secret_is_accepted(self):
        assert verify_stage_callback_secret("correct-secret", "correct-secret") is True

    def test_mismatched_secret_is_rejected(self):
        assert verify_stage_callback_secret("wrong-secret", "correct-secret") is False

    def test_missing_value_is_rejected(self):
        assert verify_stage_callback_secret(None, "correct-secret") is False
