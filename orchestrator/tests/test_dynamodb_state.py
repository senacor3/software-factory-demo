"""Unit tests for the orchestrator's DynamoDB access
(orchestrator/dynamodb_state.py): the three conditional writes, `mark_terminal`,
`record_stage_status`, and `claim_gate_action`, each issuing the expected conditional
`UpdateItem` call and returning `True`/`False` for whether this call caused the
transition (AD-20's addendum); the two plain reads, `get_stage_status` and
`is_terminal`, each issuing the expected `GetItem` call; and `claim_merge_conflict_attempt`'s
`UpdateItem` `ADD`.

No real AWS call, and no real boto3 import either: every function only `import
boto3`s lazily inside the function (mirroring `handler._load_github_app_credentials`),
and boto3 isn't installed in this story's own verification environment (`uv run
--with pytest pytest tests/ -v` -- no boto3 in that `--with` list, deliberately, per
`requirements.txt`'s "pre-bundled in the Lambda runtime" comment). So a fake `boto3`
module is injected into `sys.modules` for the duration of the call, rather than
patching `boto3.client` directly (which would require the real package to be
importable first). A `ConditionalCheckFailedException` is simulated the same way real
boto3 clients expose it -- as an attribute on `client.exceptions`, a genuine exception
subclass -- so `except client.exceptions.ConditionalCheckFailedException:` in the
production code resolves to it correctly.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dynamodb_state import (  # noqa: E402
    claim_gate_action,
    claim_merge_conflict_attempt,
    get_stage_status,
    is_terminal,
    mark_terminal,
    record_stage_status,
)


class _FakeConditionalCheckFailedException(Exception):
    pass


def _fake_boto3_client(*, conditional_check_fails: bool = False):
    """A fake `boto3.client("dynamodb")` whose `update_item` either succeeds (default)
    or raises a `ConditionalCheckFailedException` -- mirroring how a real boto3
    client exposes its exception classes on `client.exceptions`."""
    fake_boto3 = MagicMock()
    mock_client = MagicMock()
    fake_boto3.client.return_value = mock_client
    mock_client.exceptions.ConditionalCheckFailedException = _FakeConditionalCheckFailedException
    if conditional_check_fails:
        mock_client.update_item.side_effect = _FakeConditionalCheckFailedException()
    return fake_boto3, mock_client


class TestMarkTerminal:
    def test_issues_conditional_update_item_and_returns_true_on_fresh_transition(self):
        fake_boto3, mock_client = _fake_boto3_client()

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = mark_terminal("my-story-slug", "run-123", "rejected via /reject PR comment")

        assert result is True
        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.update_item.assert_called_once()
        _, kwargs = mock_client.update_item.call_args

        assert kwargs["TableName"] == "light-factory-orchestrator-state"
        assert kwargs["Key"] == {"story_slug#run_id": {"S": "my-story-slug#run-123"}}
        assert kwargs["ConditionExpression"] == "attribute_not_exists(#status) OR #status <> :status"
        assert kwargs["ExpressionAttributeNames"] == {"#status": "status"}
        values = kwargs["ExpressionAttributeValues"]
        assert values[":status"] == {"S": "rejected"}
        assert values[":reason"] == {"S": "rejected via /reject PR comment"}
        assert ":updated" in values

    def test_second_call_for_the_same_transition_returns_false_writes_nothing_new(self):
        fake_boto3, mock_client = _fake_boto3_client(conditional_check_fails=True)

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = mark_terminal("my-story-slug", "run-123", "rejected via /reject PR comment")

        assert result is False
        mock_client.update_item.assert_called_once()


class TestRecordStageStatus:
    def test_issues_conditional_update_item_and_returns_true_on_fresh_transition(self):
        fake_boto3, mock_client = _fake_boto3_client()

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = record_stage_status("my-story-slug", "run-123", "analysis", "ready-for-review")

        assert result is True
        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.update_item.assert_called_once()
        _, kwargs = mock_client.update_item.call_args

        assert kwargs["TableName"] == "light-factory-orchestrator-state"
        assert kwargs["Key"] == {"story_slug#run_id": {"S": "my-story-slug#run-123"}}
        assert kwargs["ConditionExpression"] == (
            "(attribute_not_exists(stage) OR stage <> :stage OR #status <> :status)"
            " AND (attribute_not_exists(#status) OR #status <> :rejected_guard)"
        )
        assert kwargs["ExpressionAttributeNames"] == {"#status": "status"}
        values = kwargs["ExpressionAttributeValues"]
        assert values[":stage"] == {"S": "analysis"}
        assert values[":status"] == {"S": "ready-for-review"}
        assert values[":rejected_guard"] == {"S": "rejected"}
        assert ":updated" in values

    def test_second_call_for_the_same_transition_returns_false_writes_nothing_new(self):
        fake_boto3, mock_client = _fake_boto3_client(conditional_check_fails=True)

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = record_stage_status("my-story-slug", "run-123", "analysis", "ready-for-review")

        assert result is False
        mock_client.update_item.assert_called_once()

    def test_cannot_overwrite_a_row_mark_terminal_already_rejected(self):
        # /reject can write status == "rejected" (no `stage` at all) for a story/run
        # whose workflow job is still in flight -- that job's own later
        # record_stage_status call must not win just because attribute_not_exists(stage)
        # is True on that row; it must see the real ConditionalCheckFailedException
        # DynamoDB would raise once the row already holds status == "rejected", and
        # report False -- status must not be un-rejected.
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client
        mock_client.exceptions.ConditionalCheckFailedException = _FakeConditionalCheckFailedException
        # First call: mark_terminal (/reject) succeeds and writes the terminal row.
        # Second call: record_stage_status for the same story/run, racing in after --
        # DynamoDB itself would raise ConditionalCheckFailedException because the row
        # already holds status == "rejected", which this guard clause exists to block.
        mock_client.update_item.side_effect = [None, _FakeConditionalCheckFailedException()]

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            mark_terminal_result = mark_terminal(
                "my-story-slug", "run-123", "rejected via /reject PR comment"
            )
            record_stage_status_result = record_stage_status(
                "my-story-slug", "run-123", "implementation-checks-review", "resolved"
            )

        assert mark_terminal_result is True
        assert record_stage_status_result is False
        assert mock_client.update_item.call_count == 2
        _, second_call_kwargs = mock_client.update_item.call_args_list[1]
        assert second_call_kwargs["ExpressionAttributeValues"][":rejected_guard"] == {"S": "rejected"}


class TestClaimGateAction:
    def test_issues_conditional_update_item_keyed_on_stage_status_action_and_returns_true(self):
        fake_boto3, mock_client = _fake_boto3_client()

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = claim_gate_action(
                "my-story-slug", "run-123", "analysis", "ready-for-review", "approve"
            )

        assert result is True
        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.update_item.assert_called_once()
        _, kwargs = mock_client.update_item.call_args

        assert kwargs["TableName"] == "light-factory-orchestrator-state"
        assert kwargs["Key"] == {"story_slug#run_id": {"S": "my-story-slug#run-123"}}
        assert kwargs["ConditionExpression"] == (
            "attribute_not_exists(gate_action) OR gate_action <> :gate_action"
        )
        assert kwargs["ExpressionAttributeValues"] == {
            ":gate_action": {"S": "analysis#ready-for-review#approve"}
        }

    def test_duplicate_claim_for_the_same_stage_status_action_returns_false(self):
        fake_boto3, mock_client = _fake_boto3_client(conditional_check_fails=True)

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = claim_gate_action(
                "my-story-slug", "run-123", "analysis", "ready-for-review", "approve"
            )

        assert result is False
        mock_client.update_item.assert_called_once()

    def test_a_later_gate_claims_a_different_key_even_with_the_same_action(self):
        # A legitimate second /approve at a LATER gate (after a real stage transition
        # moved stage/status forward) claims a different (stage, status, action) key --
        # never confused with a duplicate delivery of the first.
        fake_boto3, mock_client = _fake_boto3_client()

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = claim_gate_action(
                "my-story-slug",
                "run-123",
                "implementation-checks-review",
                "resolved",
                "approve",
            )

        assert result is True
        _, kwargs = mock_client.update_item.call_args
        assert kwargs["ExpressionAttributeValues"] == {
            ":gate_action": {"S": "implementation-checks-review#resolved#approve"}
        }


class TestIsTerminal:
    def test_terminal_row_returns_true(self):
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
            result = is_terminal("my-story-slug", "run-123")

        fake_boto3.client.assert_called_once_with("dynamodb")
        mock_client.get_item.assert_called_once_with(
            TableName="light-factory-orchestrator-state",
            Key={"story_slug#run_id": {"S": "my-story-slug#run-123"}},
        )
        assert result is True

    def test_non_terminal_row_returns_false(self):
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
            result = is_terminal("my-story-slug", "run-123")

        assert result is False

    def test_no_row_returns_false(self):
        fake_boto3 = MagicMock()
        mock_client = MagicMock()
        fake_boto3.client.return_value = mock_client
        mock_client.get_item.return_value = {}

        with patch.dict(sys.modules, {"boto3": fake_boto3}):
            result = is_terminal("my-story-slug", "run-123")

        assert result is False


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
