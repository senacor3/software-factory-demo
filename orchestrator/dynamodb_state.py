"""dynamodb_state -- the only DynamoDB write this entry owns: marking a
run terminal when a human posts `/reject` on its PR (AD-2).

`mark_terminal` is a plain `PutItem` against the control-plane table
`light-factory-orchestrator-state` (must match `local.table_name` in
`infra/main.tf`), keyed on the composite partition key `story_slug#run_id`
(AD-17's addendum) -- not yet AD-20's atomic conditional write. That
matches the IAM policy already granted to the Lambda's role
(`dynamodb:GetItem`/`dynamodb:PutItem` only, see `infra/main.tf`'s
`lambda_dynamodb` policy) and keeps this entry's scope to "/reject marks
the run terminal" without pulling in entry 9's idempotency hardening.

Lazy `import boto3`, mirroring `handler._load_github_app_credentials` --
importing this module never requires boto3 to be installed (useful for
the local test suite, which mocks `boto3.client` out entirely), and a
request that never calls `mark_terminal` never pays a real AWS SDK import
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


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
