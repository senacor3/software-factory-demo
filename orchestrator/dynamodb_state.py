"""dynamodb_state -- the orchestrator's DynamoDB access: two writes (marking a
run terminal when a human posts `/reject` on its PR, AD-2 entry 2; and
recording a workflow's own stage-completion status, AD-17's addendum, entry 6)
plus one read (this entry: which gate, if any, is current for a story/run).

The two writes are plain `PutItem`s; the read is a plain `GetItem` -- all
against the control-plane table `light-factory-orchestrator-state` (must
match `local.table_name` in `infra/main.tf`), keyed on the composite
partition key `story_slug#run_id` (AD-17's addendum) -- not yet AD-20's
atomic conditional write (entry 9's scope). That matches the IAM policy
already granted to the Lambda's role (`dynamodb:GetItem`/`dynamodb:PutItem`
only, see `infra/main.tf`'s `lambda_dynamodb` policy).

Lazy `import boto3`, mirroring `handler._load_github_app_credentials` --
importing this module never requires boto3 to be installed (useful for
the local test suite, which mocks `boto3.client` out entirely), and a
request that never calls either write below never pays a real AWS SDK import
cost.
"""

from __future__ import annotations

from datetime import UTC, datetime

_TABLE_NAME = "light-factory-orchestrator-state"


def mark_terminal(story_slug: str, run_id: str, reason: str) -> None:
    """Write a terminal control-plane row for this story/run via PutItem.

    `status` is the fixed string `"rejected"` -- this entry's only caller
    is `/reject`, always a human-initiated terminal rejection; `reason`
    carries the human-readable detail (e.g. which comment triggered it).
    """
    import boto3

    client = boto3.client("dynamodb")
    client.put_item(
        TableName=_TABLE_NAME,
        Item={
            "story_slug#run_id": {"S": f"{story_slug}#{run_id}"},
            "status": {"S": "rejected"},
            "reason": {"S": reason},
            "updated": {"S": _now()},
        },
    )


def record_stage_status(story_slug: str, run_id: str, stage: str, status: str) -> None:
    """Write a stage-completion control-plane row via PutItem (AD-17's addendum,
    entry 6) -- this entry's own write, alongside `mark_terminal`. Same composite
    partition key shape (`story_slug#run_id`); `stage`/`status` are whatever the
    calling workflow's final step reported, not re-validated against AD-10's enum
    here (that already happened when the state file was written).

    Not yet AD-20's atomic conditional write (entry 9's scope) -- a second callback
    for the same story_slug/run_id just overwrites the row, same posture as
    `mark_terminal`.
    """
    import boto3

    client = boto3.client("dynamodb")
    client.put_item(
        TableName=_TABLE_NAME,
        Item={
            "story_slug#run_id": {"S": f"{story_slug}#{run_id}"},
            "stage": {"S": stage},
            "status": {"S": status},
            "updated": {"S": _now()},
        },
    )


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


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
