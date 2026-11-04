"""Lambda entry point for the orchestrator: caller-type auth dispatch, and
(this entry) the `plan-approval` gate's PR-comment command grammar (AD-2).

Three recognized caller types, checked in this order, each header checked
only once and -- when present -- resolved immediately (either accepted or
rejected) rather than falling through to a later check:

1. GitHub webhook -- `X-Hub-Signature-256` present: verified via
   HMAC-SHA256 over the exact raw body bytes (base64-decoded first when the
   Function URL delivered a base64-encoded body). A present-but-wrong
   signature is rejected immediately as forged; it never falls through to
   a different caller type. Once verified, the body is parsed as an
   `issue_comment` event and acted on -- see `_handle_github_comment`.
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

No DynamoDB-backed stage-tracking or idempotency hardening here (entries
6/9 own that; this entry's only DynamoDB write is `/reject`'s plain
`PutItem` via `dynamodb_state.mark_terminal`) -- a successful dispatch
returns 200 naming the recognized caller type. The old `_verify_post_comment`
diagnostic backdoor (entry 2) is gone: leaving an unauthenticated path
reachable alongside real caller-type auth would contradict this story's own
"unrecognized caller is rejected" criterion.
"""

import base64
import json
from typing import Any

import comment_commands
import dynamodb_state
import github_app
from auth import verify_github_webhook_signature, verify_stage_callback_secret

# `software-factory/<story-slug>/<run-id>` (AD-8/AD-12/AD-15/AD-20) -- the PR's
# head branch parses directly into both identifiers, so `/approve`/`/reject`
# need no DynamoDB read at all.
_BRANCH_PREFIX = "software-factory"

# This entry's two dispatch targets -- both on `main` (AD-2, entry 4's live
# finding: `workflow_dispatch` only resolves a workflow file present on the
# default branch regardless of `ref`).
_IMPLEMENTATION_CHECKS_REVIEW_WORKFLOW = "implementation-checks-review.yml"
_ANALYSIS_WORKFLOW = "analysis.yml"
_TARGET_REF = "main"

# AD-8/AD-15's two story project subfolders, in the order `/rework`'s path
# resolution tries them -- the real repo's own folder (`light-factory`)
# first, per this story's Design Notes (ratifying the live repo over AD-8's
# prose, which still names `software-factory`).
_STORY_PROJECTS = ("light-factory", "freight-tenders")

# Must match the `name` of `aws_secretsmanager_secret.github_app` in
# infra/main.tf -- the Lambda's IAM role is scoped to read only this one
# secret's ARN (AD-18), so the name is fixed rather than configurable. The
# same blob also carries `webhook_secret` and `stage_callback_secret`
# (story 3) alongside the fine-grained GitHub PAT (AD-18) -- one secret,
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
            _handle_github_comment(raw_body, credentials)
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


def _handle_github_comment(raw_body: bytes, credentials: dict[str, Any]) -> None:
    """Parse the signature-verified webhook body as an `issue_comment`
    event and act on a recognized gate command (AD-2).

    Guards, in order: valid JSON object; `action == "created"`;
    `issue.pull_request` present (ignores a comment on a plain issue);
    comment author not a bot (`comment.user.type == "Bot"`). A comment
    matching none of the three commands -- including `/rework` with no
    feedback text -- is `comment_commands.parse_gate_command`'s `"none"`
    kind and is silently ignored here too: this function simply returns,
    making no GitHub API call and sending no reply. A human chatting
    normally on the PR must never get a bot reply.

    Any GitHub API failure past that point (a `RuntimeError` from
    `github_app.*`) is left to propagate out of this function and out of
    `handler()` itself -- surfacing in Lambda logs, never silently
    swallowed.
    """
    try:
        payload = json.loads(raw_body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return
    if not isinstance(payload, dict) or payload.get("action") != "created":
        return

    issue = payload.get("issue")
    if not isinstance(issue, dict) or "pull_request" not in issue:
        return

    comment = payload.get("comment")
    if not isinstance(comment, dict):
        return
    author = comment.get("user") or {}
    if author.get("type") == "Bot":
        return

    command = comment_commands.parse_gate_command(comment.get("body") or "")
    if command.kind == "none":
        return

    pr_number = issue.get("number")
    if pr_number is None:
        return

    token = credentials["github_pat"]

    if command.kind == "approve":
        _handle_approve(token, pr_number)
    elif command.kind == "reject":
        _handle_reject(token, pr_number)
    elif command.kind == "rework":
        _handle_rework(token, pr_number, command.feedback or "")


def _parse_branch(head_ref: str) -> tuple[str, str] | None:
    """Parse `software-factory/<story-slug>/<run-id>` into (slug, run-id).

    Defensive only: a PR this pipeline opened always has this shape
    (AD-12/AD-20). Returns None (never raises) on anything else, so a
    comment on an unrelated PR is a no-op rather than a crash.
    """
    parts = head_ref.split("/")
    if len(parts) != 3 or parts[0] != _BRANCH_PREFIX or not parts[1] or not parts[2]:
        return None
    return parts[1], parts[2]


def _handle_approve(token: str, pr_number: int) -> None:
    """`/approve`: dispatch `implementation-checks-review.yml` with the
    story-slug/run-id parsed from the PR's own head branch -- no
    DynamoDB read needed -- then post a confirmation comment.
    """
    pr = github_app.get_pull_request(token, pr_number)
    parsed = _parse_branch(pr["head"]["ref"])
    if parsed is None:
        return
    story_slug, run_id = parsed

    github_app.dispatch_workflow(
        token,
        _IMPLEMENTATION_CHECKS_REVIEW_WORKFLOW,
        _TARGET_REF,
        {"story-slug": story_slug, "run-id": run_id},
    )
    github_app.post_comment(
        token,
        pr_number,
        f"Approved via `/approve`. Dispatching `{_IMPLEMENTATION_CHECKS_REVIEW_WORKFLOW}` "
        f"for `{story_slug}` (`{run_id}`).",
    )


def _handle_reject(token: str, pr_number: int) -> None:
    """`/reject`: mark the run terminal in DynamoDB (PutItem only, matching
    the IAM policy already granted), close the PR, and post an
    explanatory comment. Terminal for this run -- no re-dispatch.

    Same guard as `_handle_approve`/`_handle_rework`: a PR whose head
    branch doesn't match this pipeline's own naming scheme (AD-12/AD-20)
    is not one this pipeline opened, so `/reject` must not close or
    comment on it either -- closing/commenting only ever happens once the
    branch is confirmed to be one of ours.
    """
    pr = github_app.get_pull_request(token, pr_number)
    parsed = _parse_branch(pr["head"]["ref"])
    if parsed is None:
        return
    story_slug, run_id = parsed

    dynamodb_state.mark_terminal(
        story_slug, run_id, "rejected via /reject PR comment on plan-approval"
    )
    github_app.close_pull_request(token, pr_number)
    github_app.post_comment(
        token,
        pr_number,
        "Rejected via `/reject`. This run is now terminal; closing the PR.",
    )


def _handle_rework(token: str, pr_number: int, feedback: str) -> None:
    """`/rework <feedback>`: append the feedback as a new commit to the
    resolved story file on `main`, then re-dispatch `analysis.yml` with
    that file's path. No DynamoDB read/write (stage-tracking and
    idempotency hardening are entries 6/9's).

    Story-file path resolution (AD-8's slug carries no project subfolder):
    tries `stories/light-factory/<slug>.md` then
    `stories/freight-tenders/<slug>.md` via the Contents API and uses
    whichever responds -- deterministic, since slugs are globally unique
    and the other path must 404. Not found under either -> a rejected
    response naming the problem, per this story's own I/O matrix.
    """
    pr = github_app.get_pull_request(token, pr_number)
    parsed = _parse_branch(pr["head"]["ref"])
    if parsed is None:
        return
    story_slug, _run_id = parsed

    resolved = _resolve_story_file(token, story_slug)
    if resolved is None:
        tried = ", ".join(f"`stories/{project}/{story_slug}.md`" for project in _STORY_PROJECTS)
        github_app.post_comment(
            token,
            pr_number,
            f"Rework requested via `/rework`, but no story file for `{story_slug}` "
            f"was found (tried {tried}). Nothing was changed; no workflow was re-dispatched.",
        )
        return
    story_path, content, sha = resolved

    new_content = content.rstrip("\n") + "\n\n" + feedback + "\n"
    github_app.update_file_content(
        token,
        story_path,
        _TARGET_REF,
        new_content,
        sha,
        f"Append /rework feedback for {story_slug}",
    )
    github_app.dispatch_workflow(
        token, _ANALYSIS_WORKFLOW, _TARGET_REF, {"story_file": story_path}
    )
    github_app.post_comment(
        token,
        pr_number,
        f"Rework requested via `/rework`. Feedback appended to `{story_path}`; "
        f"re-dispatching `{_ANALYSIS_WORKFLOW}`.",
    )


def _resolve_story_file(token: str, story_slug: str) -> tuple[str, str, str] | None:
    """Try each of `_STORY_PROJECTS` in order, returning the first
    `(path, content, sha)` that exists on `main`. A 404 on a candidate
    path means "try the next one"; any other GitHub API failure still
    propagates (never swallowed) -- only "not found" is expected here.
    """
    for project in _STORY_PROJECTS:
        path = f"stories/{project}/{story_slug}.md"
        try:
            content, sha = github_app.get_file_content(token, path, _TARGET_REF)
        except RuntimeError as exc:
            if "(404)" in str(exc):
                continue
            raise
        return path, content, sha
    return None


def _load_github_app_credentials() -> dict[str, Any]:
    """Load the one Secrets Manager blob backing all caller-auth checks:
    the fine-grained GitHub PAT (AD-18) plus `webhook_secret` and
    `stage_callback_secret`. Called lazily, only from the branches that
    need it, so at most one uncached `get_secret_value` call per
    invocation (zero for a request that never reaches one of those
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
