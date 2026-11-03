"""Stub Lambda entry point for the orchestrator skeleton.

Proves the Terraform -> AWS -> Function URL -> Lambda chain connects end to
end. Deliberately minimal: no caller-type auth dispatch, webhook signature
verification, or GitHub App calls -- that's stories 2/3/5/6.
"""

import json
from typing import Any


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Return a minimal 200 JSON response for any Function URL request."""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"status": "ok"}),
    }
