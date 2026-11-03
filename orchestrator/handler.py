"""Lambda entry point for the orchestrator: caller-type auth dispatch.

Three recognized caller types, checked in this order, each header checked
only once and -- when present -- resolved immediately (either accepted or
rejected) rather than falling through to a later check:

1. GitHub webhook -- `X-Hub-Signature-256` present: verified via
   HMAC-SHA256 over the exact raw body bytes (base64-decoded first when the
   Function URL delivered a base64-encoded body). A present-but-wrong
   signature is rejected immediately as forged; it never falls through to
   a different caller type.
2. Stage-completion callback -- `X-Stage-Callback-Secret` present:
   verified via constant-time comparison against the configured shared
   secret. Same immediate-reject-on-mismatch behavior as the webhook check.
3. UI OAuth (reserved stub, AD-17/AD-23) -- `Authorization` present but
   neither of the above matched: rejected as "not yet implemented", a
   reason distinct from the generic unrecognized-caller rejection, so
   epic-pipeline-dashboard only has to fill in real validation later
   instead of restructuring this dispatch.

A request matching none of the three is rejected as unrecognized, with a
reason distinguishable from a signature failure.

No DynamoDB state transitions or FSM logic here (entries 5/6/9 own that) --
a successful dispatch returns 200 naming the recognized caller type and
does no further processing. The old `_verify_post_comment` diagnostic
backdoor (entry 2) is gone: leaving an unauthenticated path reachable
alongside real caller-type auth would contradict this story's own
"unrecognized caller is rejected" criterion.
"""

import base64
import json
from typing import Any

from auth import verify_github_webhook_signature, verify_stage_callback_secret

# Must match the `name` of `aws_secretsmanager_secret.github_app` in
# infra/main.tf -- the Lambda's IAM role is scoped to read only this one
# secret's ARN (AD-18), so the name is fixed rather than configurable. The
# same blob also carries `webhook_secret` and `stage_callback_secret`
# (story 3) alongside the GitHub App credentials (story 2) -- one secret,
# at most one uncached `get_secret_value` call per invocation (fetched
# lazily, only when the webhook or stage-callback branch actually needs
# it -- never for the UI-OAuth-stub or unrecognized-caller branches, which
# don't read it); see Design Notes on why a second secret was rejected
# rather than splitting these fields across two.
_GITHUB_APP_SECRET_NAME = "light-factory-orchestrator-github-app"

_WEBHOOK_SIGNATURE_HEADER = "x-hub-signature-256"
_STAGE_CALLBACK_SECRET_HEADER = "x-stage-callback-secret"
_AUTHORIZATION_HEADER = "authorization"


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Dispatch a Function URL request to its caller type and respond.

    Dispatch order: GitHub webhook signature -> stage-callback secret ->
    UI-OAuth stub heuristic -> unrecognized. See module docstring.
    """
    headers = _lowercase_headers(event.get("headers"))
    raw_body = _raw_body(event)

    # Credentials are fetched lazily, only inside the two branches that
    # actually read them -- the Function URL is public
    # (authorization_type = "NONE"), so every unauthenticated garbage
    # request must not trigger a billed Secrets Manager call, and must not
    # risk a Secrets Manager failure crashing a request that should have
    # been cleanly rejected instead.
    signature_header = headers.get(_WEBHOOK_SIGNATURE_HEADER)
    if signature_header is not None:
        credentials = _load_github_app_credentials()
        if verify_github_webhook_signature(
            raw_body, signature_header, credentials["webhook_secret"]
        ):
            return _accepted("github-webhook")
        return _rejected("invalid GitHub webhook signature")

    stage_callback_header = headers.get(_STAGE_CALLBACK_SECRET_HEADER)
    if stage_callback_header is not None:
        credentials = _load_github_app_credentials()
        if verify_stage_callback_secret(
            stage_callback_header, credentials["stage_callback_secret"]
        ):
            return _accepted("stage-callback")
        return _rejected("invalid stage-callback secret")

    if headers.get(_AUTHORIZATION_HEADER) is not None:
        return _not_implemented("UI OAuth caller authentication is not yet implemented")

    return _rejected("unrecognized caller: no recognized auth header present")


def _lowercase_headers(headers: dict[str, Any] | None) -> dict[str, str]:
    return {key.lower(): value for key, value in (headers or {}).items()}


def _raw_body(event: dict[str, Any]) -> bytes:
    """Return the exact raw body bytes.

    Base64-decodes first when the Function URL delivered a base64-encoded
    body -- signature verification must run on these exact bytes, never a
    re-parsed/re-serialized form.
    """
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        return base64.b64decode(body)
    return body.encode("utf-8")


def _accepted(caller_type: str) -> dict[str, Any]:
    return _response(200, {"status": "accepted", "caller": caller_type})


def _rejected(reason: str) -> dict[str, Any]:
    return _response(401, {"status": "rejected", "reason": reason})


def _not_implemented(reason: str) -> dict[str, Any]:
    return _response(501, {"status": "rejected", "reason": reason})


def _response(status_code: int, body: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _load_github_app_credentials() -> dict[str, Any]:
    """Load the one Secrets Manager blob backing all caller-auth checks:
    GitHub App credentials (story 2) plus `webhook_secret` and
    `stage_callback_secret` (this story). Called lazily, only from the
    branches that need it, so at most one uncached `get_secret_value` call
    per invocation (zero for a request that never reaches one of those
    branches); no caching added in this story.
    """
    # Imported lazily: boto3 is pre-bundled in the Lambda Python runtime
    # and deliberately not pinned in requirements.txt (see that file's
    # comment), so it's only imported when this function actually runs
    # (i.e. not merely by importing this module, which matters for the
    # local test suite in tests/, which mocks this function out entirely).
    import boto3

    secrets_client = boto3.client("secretsmanager")
    response = secrets_client.get_secret_value(SecretId=_GITHUB_APP_SECRET_NAME)
    return json.loads(response["SecretString"])
