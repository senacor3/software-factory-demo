"""GitHub App authentication and PR-comment posting.

Pure functions with no Lambda-specific coupling (no boto3, no event/context
shapes) -- callers (e.g. `handler.py`) own fetching the App's credentials
from wherever they live (Secrets Manager) and wiring them into these calls.
GitHub App auth only, per AD-18 (not a human-tied PAT).
"""

import json
import time
import urllib.error
import urllib.request
from typing import Any

import jwt

_GITHUB_API_BASE = "https://api.github.com"
_API_VERSION = "2022-11-28"

# Fixed per this story's scope -- the demo app the pipeline is proven
# against (see the story's I/O matrix: post_comment takes only a PR number
# and body, no repo parameter).
_REPO = "senacor3/software-factory-demo"


def mint_jwt(app_id: str, private_key_pem: str) -> str:
    """Mint a short-lived RS256 JWT authenticating as the GitHub App itself.

    Per GitHub's App-auth flow: `iss` is the App ID, and `iat`/`exp` bound
    the JWT's validity window to at most 10 minutes (GitHub rejects a
    longer-lived JWT). `iat` is backdated by 60s to tolerate clock drift
    between this host and GitHub's, per GitHub's own documented guidance.
    """
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + 600,
        "iss": app_id,
    }
    return jwt.encode(payload, private_key_pem, algorithm="RS256")


def get_installation_token(jwt_token: str, installation_id: str) -> str:
    """Exchange an App JWT for a short-lived installation access token.

    Raises RuntimeError with GitHub's error body surfaced clearly if the
    exchange fails (bad JWT, bad installation id, revoked App, etc.).
    """
    url = f"{_GITHUB_API_BASE}/app/installations/{installation_id}/access_tokens"
    request = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": _API_VERSION,
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            body: dict[str, Any] = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub installation-token request failed ({exc.code}): {error_body}"
        ) from exc

    return body["token"]


def post_comment(installation_token: str, pr_number: int, body: str) -> dict[str, Any]:
    """Post a comment on the given PR/issue number using an installation token.

    Raises RuntimeError with GitHub's error body surfaced clearly if the
    post fails (expired/insufficiently-scoped token, missing PR, etc.).
    """
    url = f"{_GITHUB_API_BASE}/repos/{_REPO}/issues/{pr_number}/comments"
    payload = json.dumps({"body": body}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {installation_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": _API_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub post-comment request failed ({exc.code}): {error_body}"
        ) from exc
