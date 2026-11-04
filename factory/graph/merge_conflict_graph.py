#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["langgraph>=1.2.12,<2"]
# ///
"""merge_conflict_graph -- the `merge.yml` pipeline's bounded merge-conflict-resolution
loop (CAP-11, AD-19), mirroring `fix_loop_graph.py`'s/`checks_fix_loop_graph.py`'s shape.

Runs only when `detect-conflict`'s own probe (`factory/scripts/attempt_target_merge.py`)
already found a real conflict against the target branch (wired via the workflow's
`resolve-conflict` job `if:`). This module repeats that same, now-staged merge attempt
once for itself (handling the rare case where the target moved between the probe and
this job's own check): clean -> commit/push immediately, no loop. Still conflicted ->
loop -- claim the next attempt count from the orchestrator's DynamoDB-backed counter
(AD-19; a GitHub Actions job retry must never reset a local variable back to zero), cap
out at 2, otherwise re-engage the read/write-scoped
`software-factory-merge-conflict-resolution` skill with the conflicted paths, then
re-check.

"Still conflicted" is decided by scanning the conflicted files' own content for leftover
`<<<<<<<`-style marker lines (`attempt_target_merge.has_unresolved_markers`) -- never by
re-running `git merge`, which would always report clean the instant the first conflict
is staged (`--no-commit` leaves it staged in the index regardless of whether the agent
actually finished), so it can never distinguish "agent fixed it" from "agent did
nothing". The conflicted-path list is captured exactly once, from this module's own
initial `attempt_target_merge.attempt_merge` call, and never re-derived -- only `git add`
would clear a path's unmerged-index state, and nothing here ever runs it.

The attempt counter lives in DynamoDB (AD-19), claimed via `claim_merge_attempt.claim`
against the orchestrator's `claim-merge-conflict-attempt` action -- never incremented by
the agent, never a local/in-job variable -- so it survives a job retry. A claimed count
exceeding `MAX_MERGE_CONFLICT_ATTEMPTS` aborts the merge (leaving a clean working tree)
and raises `ConflictCapReachedError`, failing this job and surfacing to the developer --
no silent stop, no auto-merge of an unresolved conflict.

Per AD-6, deterministic checkout/fetch/merge/commit/push/abort never become graph nodes
or agent tool calls -- this graph's one node is pure judgment work (looping over the
merge-conflict-resolution skill invocation).

AD-5's second enforcement layer (the `--settings` deny rule excluding
plan.md/decisions.md/review.md/checks.md from `Edit`, named in root AGENTS.md's Policy
section) applies here too, reused verbatim from `implementation_graph.py`'s own
`DENY_SETTINGS` -- AD-19's wider path scope for this agent is about which paths it may
touch, never an exemption from that rule.

A conflicted path with no content-marker conflict at all (e.g. a delete/modify
conflict) is checked for and rejected before any attempt is claimed or the agent is
ever invoked (`UnsupportedConflictTypeError`) -- this skill has no tool to meaningfully
resolve that shape of conflict, and AD-19's fail-safe bias means failing and surfacing
it, never silently treating an un-looked-at path as resolved.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import attempt_target_merge
import checkout_branch
import claim_merge_attempt
import commit_push_implementation

MAX_MERGE_CONFLICT_ATTEMPTS = 2


class MergeConflictInvocationError(RuntimeError):
    """The `claude` CLI invocation of the merge-conflict-resolution skill itself
    failed -- a tooling failure (process error or non-zero exit). Distinct from
    `checkout_branch.CheckoutError`/`attempt_target_merge.MergeAttemptError` (before
    the agent runs) and `commit_push_implementation.CommitPushError` (after it
    succeeds)."""


class ConflictCapReachedError(RuntimeError):
    """The claimed attempt count exceeds `MAX_MERGE_CONFLICT_ATTEMPTS` (AD-19) -- the
    merge has been aborted (clean working tree left behind); this stops the loop
    immediately, with no further agent invocation or commit attempted."""


class UnsupportedConflictTypeError(RuntimeError):
    """One or more of the conflicted paths has no content-marker conflict at all --
    e.g. a delete/modify conflict, which this skill has no tool to meaningfully
    resolve. AD-19's fail-safe bias: fail and surface instead of silently treating an
    un-looked-at path as resolved. The merge has been aborted (clean working tree left
    behind); no attempt is claimed and no agent invoked."""


# --- the agent invocation -----------------------------------------------------------

# AD-5's second enforcement layer (named in root AGENTS.md's Policy section), reused
# verbatim from implementation_graph.py's own DENY_SETTINGS: AD-19's wider path scope
# for this agent (any path in the conflict list, not a subtask-file list) is about
# *which* paths it may touch, never an exemption from the rule that no stage's agent
# may Edit another stage's owned state file.
DENY_SETTINGS = {
    "permissions": {
        "deny": [
            "Edit(.factory/**/plan.md)",
            "Edit(.factory/**/decisions.md)",
            "Edit(.factory/**/review.md)",
            "Edit(.factory/**/checks.md)",
        ]
    }
}


def _build_command(conflicted_paths: list[str], claude_bin: str) -> list[str]:
    prompt = "/software-factory-merge-conflict-resolution " + " ".join(conflicted_paths)
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
    conflicted_paths: list[str],
    *,
    claude_bin: str = "claude",
    cwd: str | os.PathLike | None = None,
) -> str:
    """Shell out to the `claude` CLI with the merge-conflict-resolution skill and
    return its raw stdout text. No JSON schema -- there is no judgment verdict to
    parse here, unlike the analysis stage. Raises MergeConflictInvocationError on any
    tooling failure."""
    cmd = _build_command(conflicted_paths, claude_bin)
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise MergeConflictInvocationError(f"failed to invoke {claude_bin!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise MergeConflictInvocationError(f"`claude` exited {proc.returncode}: {detail}")

    return proc.stdout


# --- the loop -------------------------------------------------------------------


def _paths_without_markers(paths: list[str], *, cwd: str | os.PathLike | None = None) -> list[str]:
    """Return the subset of `paths` with no content-marker conflict at all -- e.g. a
    delete/modify conflict, which leaves the surviving side's content with zero
    marker lines. A missing path (some non-content conflict shapes leave nothing to
    read) counts the same way: no markers found."""
    unsupported = []
    for path in paths:
        try:
            has_marker = attempt_target_merge.has_unresolved_markers([path], cwd=cwd)
        except FileNotFoundError:
            has_marker = False
        if not has_marker:
            unsupported.append(path)
    return unsupported


def run_conflict_resolution(
    story_slug: str,
    run_id: str,
    *,
    target: str = "main",
    claude_bin: str = "claude",
    orchestrator_url: str,
    stage_callback_secret: str,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Attempt the merge once; clean -> commit/push, done. Conflicted -> bounded loop
    (cap `MAX_MERGE_CONFLICT_ATTEMPTS`, AD-19): claim the next attempt count, cap out
    aborting the merge, otherwise re-engage the resolution skill and re-check the
    same conflicted paths for leftover markers.

    Returns `{"resolved": True, "attempts": int}`. Raises `checkout_branch.
    CheckoutError`/`attempt_target_merge.MergeAttemptError` if the initial merge
    attempt's deterministic git step fails, `UnsupportedConflictTypeError` if any
    conflicted path has no content-marker conflict at all (a delete/modify or similar
    non-content conflict this skill cannot resolve -- the merge is aborted and no
    attempt is ever claimed), `claim_merge_attempt.ClaimMergeAttemptError`/
    `MergeConflictInvocationError` if the orchestrator claim or the agent's tooling
    call fails, `commit_push_implementation.CommitPushError` if the final commit/push
    step fails, or `ConflictCapReachedError` once the cap is reached -- each stops
    immediately with nothing further attempted, per the plan's I/O & Edge-Case Matrix.
    """
    branch = f"software-factory/{story_slug}/{run_id}"
    has_conflict, conflicted_paths = attempt_target_merge.attempt_merge(
        story_slug, run_id, target, cwd=cwd
    )

    if not has_conflict:
        commit_push_implementation.commit_and_push(
            branch, story_slug, run_id, cwd=cwd, label="Conflict Resolution"
        )
        return {"resolved": True, "attempts": 0}

    # AD-19's fail-safe bias: before claiming any attempt or invoking the agent,
    # verify every conflicted path is actually a content-marker conflict -- never
    # silently treat an un-looked-at delete/modify (or similar) conflict as resolved.
    unsupported_paths = _paths_without_markers(conflicted_paths, cwd=cwd)
    if unsupported_paths:
        attempt_target_merge.abort_merge(cwd=cwd)
        raise UnsupportedConflictTypeError(
            "conflicted path(s) have no content-marker conflict (e.g. a delete/modify "
            "conflict), which this skill cannot resolve: " + ", ".join(sorted(unsupported_paths))
        )

    # `attempt` tracks the count this execution has itself already claimed -- the
    # cap check below runs *before* claiming the next attempt, so reaching the cap
    # after exactly MAX_MERGE_CONFLICT_ATTEMPTS real agent attempts costs no further
    # claim() call (and so leaves the DynamoDB counter at exactly that cap, not one
    # past it). The claimed count is still re-checked right after claim() too, for
    # the separate case where a prior, crashed job attempt already spent some of the
    # budget and this execution's own first claim comes back already over the cap.
    attempt = 0
    while True:
        if attempt >= MAX_MERGE_CONFLICT_ATTEMPTS:
            attempt_target_merge.abort_merge(cwd=cwd)
            raise ConflictCapReachedError(
                f"merge-conflict attempt cap of {MAX_MERGE_CONFLICT_ATTEMPTS} reached "
                f"after {attempt} attempt(s) for {story_slug}/{run_id}"
            )

        attempt = claim_merge_attempt.claim(
            orchestrator_url, stage_callback_secret, story_slug, run_id
        )
        if attempt > MAX_MERGE_CONFLICT_ATTEMPTS:
            attempt_target_merge.abort_merge(cwd=cwd)
            raise ConflictCapReachedError(
                f"merge-conflict attempt {attempt} exceeds the cap of "
                f"{MAX_MERGE_CONFLICT_ATTEMPTS} for {story_slug}/{run_id}"
            )

        invoke_skill(conflicted_paths, claude_bin=claude_bin, cwd=cwd)

        if not attempt_target_merge.has_unresolved_markers(conflicted_paths, cwd=cwd):
            commit_push_implementation.commit_and_push(
                branch, story_slug, run_id, cwd=cwd, label="Conflict Resolution"
            )
            return {"resolved": True, "attempts": attempt}


# --- LangGraph wiring (AD-6: judgment work only; this ticket's single node) -------------


def build_graph():
    """A minimal single-node LangGraph graph wrapping run_conflict_resolution -- kept
    separate so the looping logic above stays reusable and testable without going
    through the graph (mirrors fix_loop_graph.py's build_graph)."""
    from langgraph.graph import END, StateGraph
    from typing_extensions import TypedDict

    class MergeConflictState(TypedDict, total=False):
        story_slug: str
        run_id: str
        target: str
        claude_bin: str
        orchestrator_url: str
        stage_callback_secret: str
        outcome: dict

    def merge_conflict_node(state: MergeConflictState) -> MergeConflictState:
        outcome = run_conflict_resolution(
            state["story_slug"],
            state["run_id"],
            target=state.get("target", "main"),
            claude_bin=state.get("claude_bin", "claude"),
            orchestrator_url=state["orchestrator_url"],
            stage_callback_secret=state["stage_callback_secret"],
        )
        return {"outcome": outcome}

    graph = StateGraph(MergeConflictState)
    graph.add_node("merge_conflict", merge_conflict_node)
    graph.set_entry_point("merge_conflict")
    graph.add_edge("merge_conflict", END)
    return graph.compile()


# --- CLI ---------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--target", default="main")
    p.add_argument("--claude-bin", default="claude", help="override for testing; defaults to the claude CLI on PATH")
    p.add_argument("--orchestrator-url", required=True, help="the orchestrator's Function URL")
    p.add_argument("--stage-callback-secret", required=True, help="the shared stage-callback secret")
    args = p.parse_args(argv)

    try:
        outcome = run_conflict_resolution(
            args.story_slug,
            args.run_id,
            target=args.target,
            claude_bin=args.claude_bin,
            orchestrator_url=args.orchestrator_url,
            stage_callback_secret=args.stage_callback_secret,
        )
    except (MergeConflictInvocationError, claim_merge_attempt.ClaimMergeAttemptError) as e:
        print(f"merge-conflict-resolution tooling failure: {e}", file=sys.stderr)
        return 3
    except (checkout_branch.CheckoutError, attempt_target_merge.MergeAttemptError) as e:
        print(f"merge-conflict git step failed: {e}", file=sys.stderr)
        return 4
    except commit_push_implementation.CommitPushError as e:
        print(f"commit/push failed: {e}", file=sys.stderr)
        return 5
    except ConflictCapReachedError as e:
        print(f"merge-conflict attempt cap reached: {e}", file=sys.stderr)
        return 6
    except UnsupportedConflictTypeError as e:
        print(f"unsupported conflict type: {e}", file=sys.stderr)
        return 7

    print(json.dumps({"ok": True, "resolved": outcome["resolved"], "attempts": outcome["attempts"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
