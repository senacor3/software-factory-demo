# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for claim_merge_attempt.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_claim_merge_attempt.py

Covers `claim`'s request shape (URL, header, JSON body), its parsing of the `attempt`
field from a successful response, and non-2xx/transport-failure handling -- mirrors
test_post_stage_callback.py's `TestPost` exactly. No real network call:
`urllib.request.urlopen` is mocked throughout.
"""

import json
import sys
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import claim_merge_attempt


def _fake_http_response(body: bytes = b'{"status": "accepted", "caller": "stage-callback", "attempt": 1}') -> MagicMock:
    response = MagicMock()
    response.read.return_value = body
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


@patch("claim_merge_attempt.urllib.request.urlopen")
def test_posts_expected_url_header_and_body(mock_urlopen):
    mock_urlopen.return_value = _fake_http_response()

    claim_merge_attempt.claim(
        "https://orchestrator.example/callback", "the-shared-secret", "my-story-slug", "run-7"
    )

    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://orchestrator.example/callback"
    assert request.get_method() == "POST"
    assert request.get_header("X-stage-callback-secret") == "the-shared-secret"
    assert json.loads(request.data.decode("utf-8")) == {
        "action": "claim-merge-conflict-attempt",
        "story-slug": "my-story-slug",
        "run-id": "run-7",
    }


@patch("claim_merge_attempt.urllib.request.urlopen")
def test_returns_the_attempt_count_from_the_response_body(mock_urlopen):
    mock_urlopen.return_value = _fake_http_response(
        b'{"status": "accepted", "caller": "stage-callback", "attempt": 2}'
    )

    attempt = claim_merge_attempt.claim(
        "https://orchestrator.example/callback", "the-shared-secret", "my-story-slug", "run-7"
    )

    assert attempt == 2


@patch("claim_merge_attempt.urllib.request.urlopen")
def test_surfaces_http_error_body_on_non_2xx(mock_urlopen):
    error_body = json.dumps({"status": "rejected", "reason": "bad secret"}).encode("utf-8")
    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://orchestrator.example/callback",
        code=401,
        msg="Unauthorized",
        hdrs=None,
        fp=BytesIO(error_body),
    )

    with pytest.raises(claim_merge_attempt.ClaimMergeAttemptError, match="bad secret"):
        claim_merge_attempt.claim(
            "https://orchestrator.example/callback", "wrong-secret", "my-story-slug", "run-7"
        )


@patch("claim_merge_attempt.urllib.request.urlopen")
def test_surfaces_transport_failure(mock_urlopen):
    mock_urlopen.side_effect = urllib.error.URLError("connection refused")

    with pytest.raises(claim_merge_attempt.ClaimMergeAttemptError, match="connection refused"):
        claim_merge_attempt.claim(
            "https://orchestrator.example/callback", "the-shared-secret", "my-story-slug", "run-7"
        )
