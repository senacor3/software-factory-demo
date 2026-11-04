#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""post_stage_callback -- the shared deterministic step each of the three pipeline
workflow files' (analysis.yml, implementation-checks-review.yml, merge.yml) final job
step calls to report its own concrete stage status to the orchestrator's Function URL
(AD-17's addendum, caller type c), authenticated via entry 3's shared stage-callback
secret.

Plain `urllib.request` POST -- no new pip dependency, mirrors post_summary.py's and
open_implementation_pr.py's stdlib-only posture. `orchestrator/handler.py`'s
`stage-callback` branch records the status in DynamoDB and, only for the `analysis`
workflow's `ready-for-review` status, renders and posts the AD-4 plan-approval summary
itself -- this script's only job is to report the status; it never decides what to do
with it.

Raises StageCallbackError on any non-2xx response or transport failure, carrying the
response body / error detail, so a workflow step fails loudly rather than silently.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state_io


class StageCallbackError(RuntimeError):
    """The callback POST itself failed -- a non-2xx response or a transport error --
    distinct from the stage status being reported, which this script never judges."""


def post(url: str, secret: str, stage: str, story_slug: str, run_id: str, status: str) -> None:
    """POST this stage's status to the orchestrator's Function URL, authenticated via
    the `X-Stage-Callback-Secret` header. Raises StageCallbackError on any non-2xx
    response or transport failure."""
    payload = json.dumps(
        {"stage": stage, "story-slug": story_slug, "run-id": run_id, "status": status}
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
            response.read()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise StageCallbackError(
            f"stage-callback POST failed ({e.code}): {error_body}"
        ) from e
    except (urllib.error.URLError, ValueError) as e:
        # ValueError: raised by Request.__init__/urlopen itself for a
        # malformed/empty --url (e.g. "unknown url type") -- caught here too so a
        # bad URL fails cleanly like any other transport error, instead of an
        # unhandled traceback.
        raise StageCallbackError(f"stage-callback POST failed: {e}") from e


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--url", required=True, help="the orchestrator's Function URL")
    p.add_argument("--secret", required=True, help="the shared stage-callback secret")
    p.add_argument("--stage", required=True)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    status_source = p.add_mutually_exclusive_group(required=True)
    status_source.add_argument("--status-file", help="a state file to read `status` from (e.g. plan.md)")
    status_source.add_argument("--status", help="a literal status value (e.g. 'merged')")
    args = p.parse_args(argv)

    if args.status_file:
        meta, _ = state_io.read_state(args.status_file)
        status = meta["status"]
    else:
        status = args.status

    try:
        post(args.url, args.secret, args.stage, args.story_slug, args.run_id, status)
    except StageCallbackError as e:
        print(f"stage-callback failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "stage": args.stage, "status": status}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
