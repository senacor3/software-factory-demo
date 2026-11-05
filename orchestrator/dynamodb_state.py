"""dynamodb_state -- the orchestrator's DynamoDB access: conditional writes for the two
state transitions (marking a run terminal when a human posts `/reject` on its PR, AD-2
entry 2; and recording a workflow's own stage-completion status, AD-17's addendum, entry
6), a conditional write for gate-action dedup (this entry, AD-20's addendum), two plain
reads (`get_stage_status`, entry 5; `is_terminal`, this entry), and one atomic counter
claim (AD-19: the bounded merge-conflict-resolution loop's attempt count).

`mark_terminal`/`record_stage_status`/`claim_gate_action` are conditional `UpdateItem`s
that return `bool` -- whether *this* call caused the transition (`True`) or a prior call
already had (`False`, a `ConditionalCheckFailedException`) -- AD-20's addendum: every
orchestrator state transition must report back whether it actually happened, so callers
can skip their side effects (dispatch, comment, file commit) on a duplicate GitHub webhook
redelivery. `UpdateItem`'s scoped `SET` -- never `PutItem` -- so none of these three ever
clobbers unrelated fields already on the same row (e.g. `merge_conflict_attempts`,
`gate_action`) written by a different one of these functions. `get_stage_status`/
`is_terminal` are plain `GetItem`s; `claim_merge_conflict_attempt` is an `UpdateItem` `ADD`
-- all against the control-plane table `light-factory-orchestrator-state` (must match
`local.table_name` in `infra/main.tf`), keyed on the composite partition key
`story_slug#run_id` (AD-17's addendum). That matches the IAM policy already granted to the
Lambda's role (`dynamodb:GetItem`/`dynamodb:PutItem`/`dynamodb:UpdateItem`, see
`infra/main.tf`'s `lambda_dynamodb` policy).

Lazy `import boto3`, mirroring `handler._load_github_app_credentials` --
importing this module never requires boto3 to be installed (useful for
the local test suite, which mocks `boto3.client` out entirely), and a
request that never calls either write below never pays a real AWS SDK import
cost.
"""

from __future__ import annotations

from datetime import UTC, datetime

_TABLE_NAME = "light-factory-orchestrator-state"


def mark_terminal(story_slug: str, run_id: str, reason: str) -> bool:
    """Conditionally write a terminal control-plane row for this story/run via
    `UpdateItem` (AD-20's addendum). `status` is the fixed string `"rejected"` --
    this entry's only caller is `/reject`, always a human-initiated terminal
    rejection; `reason` carries the human-readable detail (e.g. which comment
    triggered it).

    Returns `True` when this call actually wrote the terminal status (status was
    anything else, or the row didn't exist yet), `False` when the row was already
    `"rejected"` (a duplicate `/reject` webhook redelivery, or a race with another
    `/reject`) -- the `ConditionExpression` catches both: no transition, no second
    write.
    """
    import boto3

    client = boto3.client("dynamodb")
    try:
        client.update_item(
            TableName=_TABLE_NAME,
            Key={"story_slug#run_id": {"S": f"{story_slug}#{run_id}"}},
            UpdateExpression="SET #status = :status, reason = :reason, updated = :updated",
            ConditionExpression="attribute_not_exists(#status) OR #status <> :status",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": {"S": "rejected"},
                ":reason": {"S": reason},
                ":updated": {"S": _now()},
            },
        )
    except client.exceptions.ConditionalCheckFailedException:
        return False
    return True


def record_stage_status(story_slug: str, run_id: str, stage: str, status: str) -> bool:
    """Conditionally write a stage-completion control-plane row via `UpdateItem`
    (AD-17's addendum, entry 6, hardened by AD-20's addendum here) -- this entry's
    own write, alongside `mark_terminal`. Same composite partition key shape
    (`story_slug#run_id`); `stage`/`status` are whatever the calling workflow's
    final step reported, not re-validated against AD-10's enum here (that already
    happened when the state file was written).

    Returns `True` when this call actually changed `(stage, status)` from whatever
    the row previously held (or the row didn't exist yet), `False` when a prior
    call already wrote this exact `(stage, status)` pair (a duplicate
    stage-completion callback redelivery) -- the `ConditionExpression`'s first clause
    requires *either* field to differ, so a transition from one real stage/status to
    the next is never blocked, only an exact repeat.

    A second, independent clause (`AND`ed in) guards against a race with
    `mark_terminal`: `/reject` can write `status == "rejected"` (with no `stage`
    attribute at all) for a story/run whose workflow job is still in flight: that
    job's own later `record_stage_status` call would otherwise see
    `attribute_not_exists(stage)` evaluate `True` and win anyway, silently
    un-rejecting an already-terminal run (and making `is_terminal` wrongly report
    `False` afterward). This clause blocks the write -- and this call returns
    `False` -- whenever the row is already `status == "rejected"`, regardless of
    what the first clause would otherwise allow.
    """
    import boto3

    client = boto3.client("dynamodb")
    try:
        client.update_item(
            TableName=_TABLE_NAME,
            Key={"story_slug#run_id": {"S": f"{story_slug}#{run_id}"}},
            UpdateExpression="SET stage = :stage, #status = :status, updated = :updated",
            ConditionExpression=(
                "(attribute_not_exists(stage) OR stage <> :stage OR #status <> :status)"
                " AND (attribute_not_exists(#status) OR #status <> :rejected_guard)"
            ),
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":stage": {"S": stage},
                ":status": {"S": status},
                ":updated": {"S": _now()},
                ":rejected_guard": {"S": "rejected"},
            },
        )
    except client.exceptions.ConditionalCheckFailedException:
        return False
    return True


def claim_gate_action(story_slug: str, run_id: str, stage: str, status: str, action: str) -> bool:
    """Conditionally claim this `(stage, status, action)` gate-action for this
    story/run via `UpdateItem` (this entry, AD-20's addendum) -- the
    orchestrator-owned dedup marker for `/approve`/`/rework`. Keyed on the triple,
    not `action` alone (Design Notes): a legitimate second `/approve` at a *later*
    gate (after a real stage transition moved `stage`/`status` forward) claims a
    different key and is never confused with a duplicate delivery of the first.

    Returns `True` when this call claimed a fresh `(stage, status, action)` key
    (no prior call had it), `False` when another call already claimed it (a
    duplicate `/approve`/`/rework` webhook redelivery, or a concurrent one racing
    this call) -- callers skip their dispatch/comment/file-write on `False`.
    """
    import boto3

    client = boto3.client("dynamodb")
    gate_action = f"{stage}#{status}#{action}"
    try:
        client.update_item(
            TableName=_TABLE_NAME,
            Key={"story_slug#run_id": {"S": f"{story_slug}#{run_id}"}},
            UpdateExpression="SET gate_action = :gate_action",
            ConditionExpression="attribute_not_exists(gate_action) OR gate_action <> :gate_action",
            ExpressionAttributeValues={":gate_action": {"S": gate_action}},
        )
    except client.exceptions.ConditionalCheckFailedException:
        return False
    return True


def claim_merge_conflict_attempt(story_slug: str, run_id: str) -> int:
    """Atomically claim the next merge-conflict-resolution attempt number for this
    story/run via `UpdateItem`'s `ADD` (AD-19) and return the new count.

    `ADD merge_conflict_attempts :one` starts the attribute at 1 when it doesn't
    exist yet -- no `if_not_exists` needed -- so the first claim for a story/run needs
    no separate initialization. This is the orchestrator-owned counter the bounded
    merge-conflict-resolution loop claims before every attempt: never incremented by
    the agent, never a local/in-job variable, so it survives a job retry. Already
    atomic by construction (a DynamoDB `ADD` can't lose a concurrent update) --
    audited for AD-20's addendum and left unchanged.
    """
    import boto3

    client = boto3.client("dynamodb")
    response = client.update_item(
        TableName=_TABLE_NAME,
        Key={"story_slug#run_id": {"S": f"{story_slug}#{run_id}"}},
        UpdateExpression="ADD merge_conflict_attempts :one",
        ExpressionAttributeValues={":one": {"N": "1"}},
        ReturnValues="UPDATED_NEW",
    )
    return int(response["Attributes"]["merge_conflict_attempts"]["N"])


def get_stage_status(story_slug: str, run_id: str) -> dict[str, str] | None:
    """Read back the row `record_stage_status` last wrote for this story/run via
    plain `GetItem` (this entry) -- unwraps DynamoDB's `{"S": ...}` attribute
    shape into a plain `{"stage": ..., "status": ...}` dict. Returns `None` when
    no `Item` key is present in the response (no row has ever been written for
    this story_slug/run_id, e.g. before `analysis.yml`'s first callback), or
    when the item has no `stage`/`status` (a `mark_terminal` row from `/reject`
    -- that row has no current gate by definition) -- callers treat either case
    the same as "no gate is current", not an error.
    """
    import boto3

    client = boto3.client("dynamodb")
    response = client.get_item(
        TableName=_TABLE_NAME,
        Key={"story_slug#run_id": {"S": f"{story_slug}#{run_id}"}},
    )
    item = response.get("Item")
    if item is None or "stage" not in item or "status" not in item:
        return None
    return {"stage": item["stage"]["S"], "status": item["status"]["S"]}


def is_terminal(story_slug: str, run_id: str) -> bool:
    """Whether this story/run's control-plane row is terminal (`/reject`'s
    `mark_terminal` wrote `status == "rejected"`) via plain `GetItem` (this entry)
    -- backs `check-run-terminal` (AD-20's addendum), which
    `open_implementation_pr.py`'s supersession path calls to avoid racing a
    concurrent `/reject` on a prior PR. `False` for a missing item or any
    non-terminal row (never raises on either).
    """
    import boto3

    client = boto3.client("dynamodb")
    response = client.get_item(
        TableName=_TABLE_NAME,
        Key={"story_slug#run_id": {"S": f"{story_slug}#{run_id}"}},
    )
    item = response.get("Item")
    if item is None:
        return False
    return item.get("status", {}).get("S") == "rejected"


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
