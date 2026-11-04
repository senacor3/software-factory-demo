"""Caller-authentication primitives for the orchestrator's Function URL.

Two of the 3-caller auth model's checks live here (story 3): GitHub webhook
HMAC-SHA256 signature verification, and the stage-completion callback's
shared-secret comparison. The third caller type (UI OAuth) is a reserved
stub only (AD-17/AD-23) and has no real primitive yet -- `handler.py` owns
that heuristic directly.

Stdlib only (`hmac`, `hashlib`) -- no new pip dependency, per this story's
Boundaries & Constraints. Both checks are constant-time (`hmac.compare_digest`),
never a plain `==`, to avoid leaking timing information byte-by-byte.
"""

import hashlib
import hmac


def verify_github_webhook_signature(
    raw_body: bytes, signature_header: str | None, secret: str
) -> bool:
    """Verify a GitHub webhook's `X-Hub-Signature-256` header value.

    HMAC-SHA256 over the exact raw body bytes (the caller must pass the
    already base64-decoded bytes when the Function URL delivered a
    base64-encoded body -- never a re-parsed/re-serialized form), compared
    constant-time against the header's `sha256=<hex digest>` value.

    Only SHA-256 is accepted. The legacy `X-Hub-Signature` (SHA-1) header is
    never consulted here, even as a fallback -- it is deprecated/weak and
    this function has no SHA-1 code path at all.
    """
    if not signature_header:
        return False

    digest = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    expected_header = f"sha256={digest}"

    return hmac.compare_digest(expected_header, signature_header)


def verify_stage_callback_secret(provided: str | None, expected: str) -> bool:
    """Constant-time comparison of the stage-completion callback's shared
    secret against the configured value. Never a plain `==`.
    """
    if provided is None:
        return False

    return hmac.compare_digest(provided, expected)
