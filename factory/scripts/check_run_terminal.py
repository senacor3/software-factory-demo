#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""check_run_terminal -- `open_implementation_pr.py`'s supersession path's call into the
orchestrator's `check-run-terminal` action (AD-20's addendum), checking whether a prior
PR's own story-slug/run-id has already been marked terminal in the orchestrator's
control plane before closing/commenting on it -- so this script's job doesn't race the
orchestrator's own `/reject` handler deciding the same PR independently.

Plain `urllib.request` POST -- mirrors `claim_merge_attempt.py`'s stdlib-only,
POST-with-shared-secret shape exactly, same `X-Stage-Callback-Secret` header. The
orchestrator's `handler.py` routes a body carrying `{"action": "check-run-terminal", ...}`
to `_handle_check_run_terminal`, which calls `dynamodb_state.is_terminal` and returns the
verdict in the response body's `terminal` field.

Raises CheckRunTerminalError on any non-2xx response or transport failure, carrying the
response body / error detail, so a supersession call fails loudly rather than silently --
same posture as claim_merge_attempt.ClaimMergeAttemptError.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class CheckRunTerminalError(RuntimeError):
    """The check-run-terminal POST itself failed -- a non-2xx response or a transport
    error -- distinct from the terminal verdict it reports."""


def is_terminal(url: str, secret: str, story_slug: str, run_id: str) -> bool:
    """POST a `check-run-terminal` request and return whether that story/run is already
    terminal. Raises CheckRunTerminalError on any non-2xx response or transport
    failure."""
    payload = json.dumps(
        {
            "action": "check-run-terminal",
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
        raise CheckRunTerminalError(
            f"check-run-terminal POST failed ({e.code}): {error_body}"
        ) from e
    except (urllib.error.URLError, ValueError) as e:
        # ValueError: raised by Request.__init__/urlopen itself for a
        # malformed/empty `url` (mirrors claim_merge_attempt.claim), and also by
        # json.loads on a non-JSON response body.
        raise CheckRunTerminalError(f"check-run-terminal POST failed: {e}") from e

    return body["terminal"]
