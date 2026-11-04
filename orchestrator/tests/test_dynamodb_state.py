"""Unit tests for the orchestrator's DynamoDB access
(orchestrator/dynamodb_state.py): the two writes, `mark_terminal` and
`record_stage_status`, each issuing the expected `PutItem` call; and (this
entry) the one read, `get_stage_status`, issuing the expected `GetItem` call.

No real AWS call, and no real boto3 import either: both functions only
`import boto3`s lazily inside the function (mirroring
`handler._load_github_app_credentials`), and boto3 isn't installed in this
story's own verification environment (`uv run --with pytest pytest tests/
-v` -- no boto3 in that `--with` list, deliberately, per
`requirements.txt`'s "pre-bundled in the Lambda runtime" comment). So a
fake `boto3` module is injected into `sys.modules` for the duration of the
call, rather than patching `boto3.client` directly (which would require
the real package to be importable first).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dynamodb_state import (  # noqa: E402
    claim_merge_conflict_attempt,
    get_stage_status,
    mark_terminal,
    record_stage_status,
)


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


class TestRecordStageStatus:
    def test_issues_put_item_with_composite_key_stage_and_status(self):
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            record_stage_status("my-story-slug", "run-123", "analysis", "ready-for-review")

        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.put_item.assert_called_once()
        _, kwargs = mock_client.put_item.call_args

        assert kwargs["TableName"] == "light-factory-orchestrator-state"
        item = kwargs["Item"]
        assert item["story_slug#run_id"] == {"S": "my-story-slug#run-123"}
        assert item["stage"] == {"S": "analysis"}
        assert item["status"] == {"S": "ready-for-review"}
        assert "updated" in item


class TestClaimMergeConflictAttempt:
    def test_issues_update_item_add_and_returns_new_count(self):
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client
        mock_client.update_item.return_value = {
            "Attributes": {"merge_conflict_attempts": {"N": "1"}}
        }

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = claim_merge_conflict_attempt("my-story-slug", "run-123")

        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.update_item.assert_called_once_with(
            TableName="light-factory-orchestrator-state",
            Key={"story_slug#run_id": {"S": "my-story-slug#run-123"}},
            UpdateExpression="ADD merge_conflict_attempts :one",
            ExpressionAttributeValues={":one": {"N": "1"}},
            ReturnValues="UPDATED_NEW",
        )
        assert result == 1

    def test_second_claim_returns_the_next_incremented_count(self):
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client
        mock_client.update_item.return_value = {
            "Attributes": {"merge_conflict_attempts": {"N": "2"}}
        }

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = claim_merge_conflict_attempt("my-story-slug", "run-123")

        assert result == 2


class TestGetStageStatus:
    def test_row_found_returns_unwrapped_stage_and_status(self):
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client
        mock_client.get_item.return_value = {
            "Item": {
                "story_slug#run_id": {"S": "my-story-slug#run-123"},
                "stage": {"S": "analysis"},
                "status": {"S": "ready-for-review"},
                "updated": {"S": "2026-11-04T00:00:00Z"},
            }
        }

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = get_stage_status("my-story-slug", "run-123")

        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.get_item.assert_called_once_with(
            TableName="light-factory-orchestrator-state",
            Key={"story_slug#run_id": {"S": "my-story-slug#run-123"}},
        )
        assert result == {"stage": "analysis", "status": "ready-for-review"}

    def test_no_row_returns_none(self):
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client
        mock_client.get_item.return_value = {}

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = get_stage_status("my-story-slug", "run-123")

        assert result is None

    def test_terminal_row_with_no_stage_or_status_returns_none(self):
        # A `mark_terminal` row (written once `/reject` has run) has no
        # `stage`/`status` keys at all -- that row has no current gate by
        # definition, same as no row at all, not a KeyError.
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client
        mock_client.get_item.return_value = {
            "Item": {
                "story_slug#run_id": {"S": "my-story-slug#run-123"},
                "status": {"S": "rejected"},
                "reason": {"S": "rejected via /reject PR comment"},
                "updated": {"S": "2026-11-04T00:00:00Z"},
            }
        }

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = get_stage_status("my-story-slug", "run-123")

        assert result is None
