#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["langgraph>=1.2.12,<2"]
# ///
"""implementation_graph -- Job 2's implementation stage (CAP-4 scoped implementation).

Sequences three steps around the agent invocation (see
story-implementation-agent-plan.md's I/O & Edge-Case Matrix):

  1. `factory/scripts/checkout_branch.py` checks out the exact branch Job 1's
     `open_implementation_pr.py` already opened (AD-12) -- never creates one.
  2. The read/write-scoped `.claude/skills/light-factory-implementation/` skill
     implements `plan.md`'s subtasks against that checkout, via `--allowedTools`
     (Read Write Edit Grep Glob -- no Bash/git/gh/merge tool) plus a `--settings`
     inline deny rule excluding `plan.md`/`decisions.md`/`review.md` from Edit --
     AD-5's two independent enforcement layers.
  3. `factory/scripts/commit_push_implementation.py` commits and pushes the result
     on that same branch -- a no-op, not an error, if the agent made no changes.

Unlike `analysis_graph.py`, there is no `--json-schema`/structured-output parsing
here: the implementation agent reports no judgment verdict for the graph to branch
on (success is "the CLI exited 0"; committed-vs-no-op is decided from `git status`,
not the agent's report -- see the plan's Design Notes).

Per AD-6, deterministic checkout/commit/push never become graph nodes or agent tool
calls -- this graph's one node is pure judgment work (shelling out to the
implementation skill), nothing else.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import checkout_branch
import commit_push_implementation
import state_io

# AD-5's second enforcement layer: even though the implementation agent's branch
# checkout holds plan.md/decisions.md/review.md alongside the files it may edit, it
# must never Edit those three -- they are owned by the analysis/review stages
# (AD-10). Scoped per-invocation via `--settings`, not a committed project-wide
# .claude/settings.json (see the plan's Design Notes).
DENY_SETTINGS = {
    "permissions": {
        "deny": [
            "Edit(.factory/**/plan.md)",
            "Edit(.factory/**/decisions.md)",
            "Edit(.factory/**/review.md)",
        ]
    }
}


class ImplementationInvocationError(RuntimeError):
    """The `claude` CLI invocation itself failed -- a tooling failure (process error
    or non-zero exit). Distinct from `checkout_branch.CheckoutError` (before the
    agent runs) and `commit_push_implementation.CommitPushError` (after it
    succeeds)."""


# --- the single invocation ----------------------------------------------------------


def _build_command(
    plan_path: str,
    decisions_path: str,
    claude_bin: str,
    review_path: str | None = None,
) -> list[str]:
    prompt = f"/light-factory-implementation {plan_path} {decisions_path}"
    if review_path:
        prompt += f" {review_path}"
    return [
        claude_bin,
        "-p",
        prompt,
        "--allowedTools",
        "Read Write Edit Grep Glob",
        "--permission-prompts",
        "none",
        "--settings",
        json.dumps(DENY_SETTINGS),
    ]


def invoke_skill(
    plan_path: str,
    decisions_path: str,
    *,
    claude_bin: str = "claude",
    cwd: str | os.PathLike | None = None,
    review_path: str | None = None,
) -> str:
    """Shell out to the `claude` CLI with the implementation skill and return its raw
    stdout text. No JSON schema -- there is no judgment verdict to parse here, unlike
    `analysis_graph.invoke_skill`. Raises ImplementationInvocationError on any tooling
    failure.

    `review_path`, when given (a fix cycle, AD-11), is appended as the skill's third
    argument so the agent re-engages with the review findings as added context."""
    cmd = _build_command(plan_path, decisions_path, claude_bin, review_path)
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise ImplementationInvocationError(f"failed to invoke {claude_bin!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise ImplementationInvocationError(f"`claude` exited {proc.returncode}: {detail}")

    return proc.stdout


def run_implementation(
    story_slug: str,
    run_id: str,
    *,
    claude_bin: str = "claude",
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
    review_path: str | None = None,
) -> dict:
    """Sequence checkout -> agent invocation -> commit/push.

    Returns `{"branch": str, "output": str, "committed": bool}`. Raises
    `checkout_branch.CheckoutError` before the agent is ever invoked,
    `ImplementationInvocationError` if the `claude` CLI call itself fails (no commit
    attempted), or `commit_push_implementation.CommitPushError` if the post-agent
    commit/push step fails (the agent's edits remain on disk uncommitted) -- each
    distinct, per the I/O & Edge-Case Matrix.

    `review_path`, when given, is a fix cycle (AD-11/`fix_loop_graph.py`): the same
    implementation skill is re-engaged with the review findings as added context,
    rather than a fresh invocation of plan/decisions alone.
    """
    branch = checkout_branch.checkout_branch(story_slug, run_id, cwd=cwd)

    state_directory = state_io.state_dir(story_slug, run_id, base=state_base)
    plan_path = str(state_directory / "plan.md")
    decisions_path = str(state_directory / "decisions.md")

    output = invoke_skill(
        plan_path, decisions_path, claude_bin=claude_bin, cwd=cwd, review_path=review_path
    )

    commit_result = commit_push_implementation.commit_and_push(
        branch, story_slug, run_id, cwd=cwd
    )

    return {"branch": branch, "output": output, "committed": commit_result["committed"]}


# --- LangGraph wiring (AD-6: judgment work only; this ticket's single node) -------------


def build_graph():
    """A minimal single-node LangGraph graph wrapping run_implementation -- kept
    separate so the subprocess/sequencing logic above stays reusable and testable
    without going through the graph (mirrors analysis_graph.py's build_graph)."""
    from langgraph.graph import END, StateGraph
    from typing_extensions import TypedDict

    class ImplementationState(TypedDict, total=False):
        story_slug: str
        run_id: str
        claude_bin: str
        state_base: str
        outcome: dict

    def implement_node(state: ImplementationState) -> ImplementationState:
        outcome = run_implementation(
            state["story_slug"],
            state["run_id"],
            claude_bin=state.get("claude_bin", "claude"),
            state_base=state.get("state_base", state_io.FACTORY_DIR),
        )
        return {"outcome": outcome}

    graph = StateGraph(ImplementationState)
    graph.add_node("implement", implement_node)
    graph.set_entry_point("implement")
    graph.add_edge("implement", END)
    return graph.compile()


# --- CLI ---------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--claude-bin", default="claude", help="override for testing; defaults to the claude CLI on PATH")
    args = p.parse_args(argv)

    try:
        outcome = run_implementation(args.story_slug, args.run_id, claude_bin=args.claude_bin)
    except checkout_branch.CheckoutError as e:
        print(f"branch checkout failed: {e}", file=sys.stderr)
        return 2
    except ImplementationInvocationError as e:
        print(f"implementation tooling failure: {e}", file=sys.stderr)
        return 3
    except commit_push_implementation.CommitPushError as e:
        print(f"commit/push failed: {e}", file=sys.stderr)
        return 4

    print(json.dumps({"ok": True, "committed": outcome["committed"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
