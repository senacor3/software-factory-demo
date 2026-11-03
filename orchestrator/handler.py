"""Lambda entry point for the orchestrator.

Still deliberately minimal: no caller-type auth dispatch or webhook
signature verification (story 3), and no /approve//rework//reject parsing
(story 5). The only addition in this story is a temporary diagnostic path --
an optional `_verify_post_comment` event key -- that lets this story's own
live GitHub-auth verification run inside the real deployed Lambda. It is
not real caller-type routing; stories 3/5/6 own that. Every other request
shape still returns entry 1's stub 200.
"""

import json
from typing import Any

from github_app import get_installation_token, mint_jwt, post_comment

# Must match the `name` of `aws_secretsmanager_secret.github_app` in
# infra/main.tf -- the Lambda's IAM role is scoped to read only this one
# secret's ARN (AD-18), so the name is fixed rather than configurable.
_GITHUB_APP_SECRET_NAME = "light-factory-orchestrator-github-app"


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Return a minimal 200 JSON response for any Function URL request."""
    verify_request = event.get("_verify_post_comment")
    if verify_request:
        _verify_post_comment(verify_request)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"status": "ok"}),
    }


def _verify_post_comment(verify_request: dict[str, Any]) -> None:
    """Live diagnostic path for this story only: mint a JWT, exchange it for
    an installation token, and post a real comment on a real PR -- proving
    the orchestrator can actually authenticate to and call the GitHub API.
    """
    pr_number = verify_request["pr_number"]
    body = verify_request["body"]

    credentials = _load_github_app_credentials()
    jwt_token = mint_jwt(credentials["app_id"], credentials["private_key_pem"])
    installation_token = get_installation_token(jwt_token, credentials["installation_id"])
    post_comment(installation_token, pr_number, body)


def _load_github_app_credentials() -> dict[str, Any]:
    # Imported lazily: boto3 is pre-bundled in the Lambda Python runtime
    # and deliberately not pinned in requirements.txt (see that file's
    # comment), so it's only imported when this diagnostic
    # `_verify_post_comment` path actually runs. This does NOT shield local
    # test runs from needing extra deps -- `github_app.py`'s own top-level
    # `import jwt` already requires `PyJWT[crypto]` to be installed just to
    # import handler.py at all (see tests/test_handler.py's docstring).
    import boto3

    secrets_client = boto3.client("secretsmanager")
    response = secrets_client.get_secret_value(SecretId=_GITHUB_APP_SECRET_NAME)
    return json.loads(response["SecretString"])
