"""Unit tests for the orchestrator's only DynamoDB write this entry owns
(orchestrator/dynamodb_state.py): `mark_terminal` issues the expected
`PutItem` call.

No real AWS call, and no real boto3 import either: `mark_terminal` only
`import boto3`s lazily inside the function (mirroring
`handler._load_github_app_credentials`), and boto3 isn't installed in this
story's own verification environment (`uv run --with pytest --with
"PyJWT[crypto]" pytest tests/ -v` -- no boto3 in that `--with` list,
deliberately, per `requirements.txt`'s "pre-bundled in the Lambda runtime"
comment). So a fake `boto3` module is injected into `sys.modules` for the
duration of the call, rather than patching `boto3.client` directly (which
would require the real package to be importable first).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dynamodb_state import mark_terminal  # noqa: E402


class TestMarkTerminal:
    def test_issues_put_item_with_composite_key_and_rejected_status(self):
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            mark_terminal("my-story-slug", "run-123", "rejected via /reject PR comment")

        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.put_item.assert_called_once()
        _, kwargs = mock_client.put_item.call_args

        assert kwargs["TableName"] == "light-factory-orchestrator-state"
        item = kwargs["Item"]
        assert item["story_slug#run_id"] == {"S": "my-story-slug#run-123"}
        assert item["status"] == {"S": "rejected"}
        assert item["reason"] == {"S": "rejected via /reject PR comment"}
        assert "updated" in item
