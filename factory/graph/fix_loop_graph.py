#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["langgraph>=1.2.12,<2"]
# ///
"""fix_loop_graph -- the review job's bounded fix loop (CAP-7, AD-11).

Orchestrates: review (ticket 9's `review_graph.run_review`, unchanged) -> while
findings remain and the cycle count is under 2 -> re-engage the *same*
`light-factory-implementation` skill (via its optional `review_path` argument, ticket
7) with the review findings as added context, re-run only `build`/`test` (the two
checks with real pass/fail signal -- `lint`/`security` are inert placeholders, ticket
8's Design Notes), then review again.

A hard cap of 2 fix cycles (AD-11): if still unresolved after the second cycle's
review, stop -- no third fix cycle -- and stamp `review.md`'s status
`unresolved-after-cap` instead of looping again just to relabel.

The fix-cycle counter is incremented and stamped only by this module's own code
(AD-11) -- never derived from or trusted to either agent's output. It lives in
`review.md`'s frontmatter as an `extra` field (`state_io.write_state`'s new optional
kwarg, ticket 10), written exactly once, after the loop: this module re-reads the body
`review_graph.run_review` already wrote (its last invocation) and re-stamps the same
file once, rather than extending `review_graph.run_review` itself with a counter
param -- see the plan's Design Notes. `review_graph.py`'s own write logic is untouched.

A `build`/`test` regression introduced by a fix cycle is not tolerated as "just
another finding" -- it immediately raises `CheckRegressionError`, the same hard-stop
policy ticket 8 already established for AD-6 (a check failure stops the job), now
extended into the loop: no further review invocation, no final re-stamp attempted
(the exception propagates straight out).

Per AD-6, deterministic checks (build/test) are invoked here as plain function calls,
never as graph nodes or agent tool calls -- this graph's one node is pure judgment
work (looping over the review/implementation agent invocations).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import checkout_branch
import commit_push_implementation
import run_checks
import state_io

sys.path.insert(0, str(Path(__file__).resolve().parent))
import implementation_graph
import review_graph

MAX_FIX_CYCLES = 2


class CheckRegressionError(RuntimeError):
    """A fix cycle's `build` or `test` recheck came back `"fail"` -- a regression, not
    another finding. The loop stops immediately: no further review invocation, no
    final re-stamp of `review.md`."""


# --- the loop -------------------------------------------------------------------


def run_review_with_fix_loop(
    story_slug: str,
    run_id: str,
    *,
    claude_bin: str = "claude",
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Review -> bounded fix loop (cap 2 cycles, AD-11) -> final status stamp.

    Returns `{"status": str, "fix_cycle": int, "review": dict}` where `status` is the
    stamped final status (`resolved` or `unresolved-after-cap`) and `review` is the
    frontmatter dict actually (re-)written.

    Raises `review_graph.ReviewInvocationError` or
    `implementation_graph.ImplementationInvocationError` if either agent's tooling
    call fails, `checkout_branch.CheckoutError` /
    `commit_push_implementation.CommitPushError` if a fix cycle's deterministic
    checkout/commit step fails, or `CheckRegressionError` if a fix cycle's recheck
    regresses `build`/`test` -- each stops the loop immediately with nothing further
    attempted (no final re-stamp), per the I/O & Edge-Case Matrix.
    """
    outcome = review_graph.run_review(
        story_slug, run_id, claude_bin=claude_bin, state_base=state_base, cwd=cwd
    )
    status = outcome["status"]

    state_directory = state_io.state_dir(story_slug, run_id, base=state_base)
    review_path = str(state_directory / "review.md")

    cycle = 0
    while status == "findings-open" and cycle < MAX_FIX_CYCLES:
        cycle += 1

        implementation_graph.run_implementation(
            story_slug,
            run_id,
            claude_bin=claude_bin,
            state_base=state_base,
            cwd=cwd,
            review_path=review_path,
        )

        build_result = run_checks.run_build(story_slug, run_id, state_base=state_base, cwd=cwd)
        if build_result["status"] == "fail":
            raise CheckRegressionError(
                f"fix cycle {cycle} regressed the build check: {build_result.get('detail', '')}"
            )
        test_result = run_checks.run_test(story_slug, run_id, state_base=state_base, cwd=cwd)
        if test_result["status"] == "fail":
            raise CheckRegressionError(
                f"fix cycle {cycle} regressed the test check: {test_result.get('detail', '')}"
            )

        outcome = review_graph.run_review(
            story_slug, run_id, claude_bin=claude_bin, state_base=state_base, cwd=cwd
        )
        status = outcome["status"]

    final_status = "unresolved-after-cap" if status == "findings-open" else status
    _, body = state_io.read_state(review_path)
    review_meta = state_io.write_state(
        review_path,
        story_slug=story_slug,
        stage="review",
        status=final_status,
        body=body,
        extra={"fix_cycle": cycle},
    )

    return {"status": final_status, "fix_cycle": cycle, "review": review_meta}


# --- LangGraph wiring (AD-6: judgment work only; this ticket's single node) -------------


def build_graph():
    """A minimal single-node LangGraph graph wrapping run_review_with_fix_loop -- kept
    separate so the looping logic above stays reusable and testable without going
    through the graph (mirrors review_graph.py's build_graph)."""
    from langgraph.graph import END, StateGraph
    from typing_extensions import TypedDict

    class FixLoopState(TypedDict, total=False):
        story_slug: str
        run_id: str
        claude_bin: str
        state_base: str
        outcome: dict

    def fix_loop_node(state: FixLoopState) -> FixLoopState:
        outcome = run_review_with_fix_loop(
            state["story_slug"],
            state["run_id"],
            claude_bin=state.get("claude_bin", "claude"),
            state_base=state.get("state_base", state_io.FACTORY_DIR),
        )
        return {"outcome": outcome}

    graph = StateGraph(FixLoopState)
    graph.add_node("fix_loop", fix_loop_node)
    graph.set_entry_point("fix_loop")
    graph.add_edge("fix_loop", END)
    return graph.compile()


# --- CLI ---------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--claude-bin", default="claude", help="override for testing; defaults to the claude CLI on PATH")
    args = p.parse_args(argv)

    try:
        outcome = run_review_with_fix_loop(args.story_slug, args.run_id, claude_bin=args.claude_bin)
    except review_graph.ReviewInvocationError as e:
        print(f"review tooling failure: {e}", file=sys.stderr)
        return 3
    except implementation_graph.ImplementationInvocationError as e:
        print(f"implementation tooling failure: {e}", file=sys.stderr)
        return 4
    except (checkout_branch.CheckoutError, commit_push_implementation.CommitPushError) as e:
        print(f"fix-cycle git step failed: {e}", file=sys.stderr)
        return 5
    except CheckRegressionError as e:
        print(f"check regression: {e}", file=sys.stderr)
        return 6

    print(json.dumps({"ok": True, "status": outcome["status"], "fix_cycle": outcome["fix_cycle"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
