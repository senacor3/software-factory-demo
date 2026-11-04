"""GitHub REST API surface the `/approve`/`/rework`/`/reject` comment-command
grammar (AD-2) needs: posting a PR comment, reading a PR's head branch,
dispatching a workflow, reading/writing a file's content on a branch, and
closing a PR.

Pure functions with no Lambda-specific coupling (no boto3, no event/context
shapes) -- callers (e.g. `handler.py`) own fetching the token from wherever
it lives (Secrets Manager) and passing it into these calls. Fine-grained,
repo-scoped PAT auth, per AD-18 (superseded from the original GitHub App
design: no JWT-minting or installation-token exchange, the token is used
directly as the Bearer credential). Same error style throughout: every call
raises `RuntimeError` with GitHub's error body surfaced clearly on an
`HTTPError`, never swallowed.
"""

import base64
import json
import urllib.error
import urllib.request
from typing import Any

_GITHUB_API_BASE = "https://api.github.com"
_API_VERSION = "2022-11-28"

# Fixed per this story's scope -- the demo app the pipeline is proven
# against (see the story's I/O matrix: post_comment takes only a PR number
# and body, no repo parameter).
_REPO = "senacor3/software-factory-demo"


def post_comment(token: str, pr_number: int, body: str) -> dict[str, Any]:
    """Post a comment on the given PR/issue number.

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
            "Authorization": f"Bearer {token}",
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


def get_pull_request(token: str, pr_number: int) -> dict[str, Any]:
    """Fetch a PR's full resource, notably `head.ref` -- the branch name
    that doubles as the story-slug/run-id correlation key (AD-20) for
    `/approve`/`/reject`, which need neither a DynamoDB read.

    Raises RuntimeError with GitHub's error body surfaced clearly if the
    PR can't be read (missing PR, insufficiently-scoped token, etc.).
    """
    url = f"{_GITHUB_API_BASE}/repos/{_REPO}/pulls/{pr_number}"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": _API_VERSION,
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub get-pull-request request failed ({exc.code}): {error_body}"
        ) from exc


def dispatch_workflow(
    token: str, workflow_file: str, ref: str, inputs: dict[str, str]
) -> None:
    """Trigger a `workflow_dispatch` run of `workflow_file` at `ref` with
    the given `inputs` (e.g. `implementation-checks-review.yml` for
    `/approve`, `analysis.yml` for `/rework`).

    `workflow_dispatch` only resolves a workflow file present on the
    default branch regardless of `ref` (entry 4's live finding) -- `ref`
    only selects which commit's code runs, matching this story's choice of
    `main` for both. Raises RuntimeError with GitHub's error body surfaced
    clearly on failure (bad ref, unknown workflow file, etc.).
    """
    url = f"{_GITHUB_API_BASE}/repos/{_REPO}/actions/workflows/{workflow_file}/dispatches"
    payload = json.dumps({"ref": ref, "inputs": inputs}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": _API_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub workflow-dispatch request failed ({exc.code}): {error_body}"
        ) from exc


def get_file_content(token: str, path: str, ref: str) -> tuple[str, str]:
    """Fetch a file's decoded text content and blob `sha` at `ref`, via the
    Contents API. The `sha` is required by `update_file_content` below to
    commit a new version of the same file without a stale-write race.

    Raises RuntimeError with GitHub's error body surfaced clearly on
    failure -- including a 404 when the path doesn't exist at `ref`, which
    callers resolving a story file's project folder (AD-8's two candidate
    paths) distinguish by checking for `"(404)"` in the message.
    """
    url = f"{_GITHUB_API_BASE}/repos/{_REPO}/contents/{path}?ref={ref}"
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
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
            f"GitHub get-file-content request failed ({exc.code}): {error_body}"
        ) from exc

    # GitHub's Contents API returns `content` as base64 split into
    # newline-delimited chunks -- base64.b64decode's default
    # validate=False discards those embedded newlines before decoding, so
    # no manual strip is needed.
    content = base64.b64decode(body["content"]).decode("utf-8")
    return content, body["sha"]


def update_file_content(
    token: str, path: str, branch: str, content: str, sha: str, message: str
) -> None:
    """Commit a new version of `path` on `branch` via the Contents API's
    PUT endpoint -- a plain new commit, not a force-push -- using `sha`
    (from a prior `get_file_content` call) to target the exact version
    being replaced.

    Raises RuntimeError with GitHub's error body surfaced clearly on
    failure (stale `sha`, protected branch, etc.).
    """
    url = f"{_GITHUB_API_BASE}/repos/{_REPO}/contents/{path}"
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("ascii")
    payload = json.dumps(
        {"message": message, "content": encoded_content, "sha": sha, "branch": branch}
    ).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": _API_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub update-file-content request failed ({exc.code}): {error_body}"
        ) from exc


def close_pull_request(token: str, pr_number: int) -> None:
    """Close a PR (`state: closed`) via the Pulls API's PATCH endpoint --
    used by `/reject`. Never merges, never deletes the branch.

    Raises RuntimeError with GitHub's error body surfaced clearly on
    failure (missing PR, already closed, etc. -- GitHub itself treats
    closing an already-closed PR as a no-op success, not an error).
    """
    url = f"{_GITHUB_API_BASE}/repos/{_REPO}/pulls/{pr_number}"
    payload = json.dumps({"state": "closed"}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        method="PATCH",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": _API_VERSION,
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8")
        raise RuntimeError(
            f"GitHub close-pull-request request failed ({exc.code}): {error_body}"
        ) from exc
