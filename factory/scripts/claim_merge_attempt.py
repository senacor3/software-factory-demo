#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""claim_merge_attempt -- `merge_conflict_graph.py`'s bounded resolution loop's call
into the orchestrator's `claim-merge-conflict-attempt` action (AD-19), claiming the
next attempt count for a story/run before every agent invocation.

Plain `urllib.request` POST -- mirrors `post_stage_callback.py`'s stdlib-only,
POST-with-shared-secret shape exactly, same `X-Stage-Callback-Secret` header. The
orchestrator's `handler.py` routes a body carrying an `"action"` key to
`_handle_claim_merge_conflict_attempt`, which calls `dynamodb_state.
claim_merge_conflict_attempt`'s atomic `UpdateItem` ADD and returns the new count in
the response body's `attempt` field.

Raises ClaimMergeAttemptError on any non-2xx response or transport failure, carrying
the response body / error detail, so a loop iteration fails loudly rather than
silently -- same posture as `post_stage_callback.StageCallbackError`.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class ClaimMergeAttemptError(RuntimeError):
    """The claim POST itself failed -- a non-2xx response or a transport error --
    distinct from the attempt count it reports."""


def claim(url: str, secret: str, story_slug: str, run_id: str) -> int:
    """POST a `claim-merge-conflict-attempt` request and return the new attempt
    count. Raises ClaimMergeAttemptError on any non-2xx response or transport
    failure."""
    payload = json.dumps(
        {
            "action": "claim-merge-conflict-attempt",
            "story-slug": story_slug,
            "run-id": run_id,
        }
    ).encode("utf-8")

    try:
        request = urllib.request.Request(
            url,
            data=payload,
            method="POST",
            headers={
                "X-Stage-Callback-Secret": secret,
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(request) as response:
            body = json.loads(response.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise ClaimMergeAttemptError(
            f"claim-merge-conflict-attempt POST failed ({e.code}): {error_body}"
        ) from e
    except (urllib.error.URLError, ValueError) as e:
        # ValueError: raised by Request.__init__/urlopen itself for a
        # malformed/empty `url` (mirrors post_stage_callback.post), and also by
        # json.loads on a non-JSON response body.
        raise ClaimMergeAttemptError(f"claim-merge-conflict-attempt POST failed: {e}") from e

    return body["attempt"]
