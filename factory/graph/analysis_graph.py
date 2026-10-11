#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["langgraph>=1.2.12,<2"]
# ///
"""analysis_graph -- the analysis job's stage (CAP-1 intake judgment, CAP-2 solution proposal).

Invokes the read-only `.claude/skills/light-factory-analysis/` skill via the `claude` CLI,
parses its schema-validated structured output, and routes to one of three outcomes (see
story-job-1-intake-analysis-plan.md's I/O & Edge-Case Matrix):

  1. Incomplete or out-of-scope -- halt, no state file written, reason on stderr.
  2. Complete, in-scope, no open questions -- write plan.md + decisions.md via
     factory/scripts/state_io.py, status `ready-for-review`; then open the branch+PR
     (AD-12) via factory/scripts/open_implementation_pr.py and post the gate-summary PR
     comment (AD-4) via factory/scripts/post_summary.py.
  3. Complete, in-scope, open questions remain -- a deterministic round-count decides
     `awaiting-clarification` (below AD-13's 2-round cap) or `clarification-cap-reached`
     (at the cap), counted from this story-slug's prior `clarification-round`-labeled PRs
     (any state) via factory/scripts/open_implementation_pr.py's `clarification_status`;
     write both state files with that status; branch+PR opened the same as outcome 2; then
     below cap the PR is labeled, commented with the open question(s), and closed
     (unchanged from v1's single-pass behavior), while at cap the PR is labeled and
     commented that the clarification budget is spent but is left open for the developer
     to decide how to proceed (ticket 2.1's Option C, 2026-10-10/11).

A fourth case -- the `claude` CLI invocation itself failing (non-zero exit, malformed or
schema-invalid JSON) -- is a tooling failure, not a legitimate verdict, and is raised as a
distinct exception type (`AnalysisInvocationError` vs. `AnalysisHalted`) so callers can
tell the two apart.

A fifth case -- plan.md/decisions.md wrote successfully but a deterministic post-analysis
step itself fails (`git`/`gh` subprocess error, whether from opening the branch/PR (AD-12),
superseding this story-slug's prior open PRs inside that same step (AD-15), posting the
gate-summary comment (AD-4), or from the clarification label/comment/close or cap-notice
call (AD-13/AD-15)) -- raises `AnalysisPROpenError`, distinct from both of the
above (per the `change-pr-at-intake` amendment, AD-12). A sixth, earlier failure point --
the round-count query itself (`clarification_status`), which now runs *before* the state
write -- also raises `AnalysisPROpenError`, but in that case plan.md/decisions.md are not
yet written.

The single-invocation call (`run_analysis`) is kept isolated from the LangGraph wiring
(`build_graph`) for reuse and testability -- callers can invoke the subprocess/parse logic
directly without going through the graph.

Per AD-6, deterministic checks never become graph nodes -- this graph's one node is pure
judgment work (shelling out to the analysis skill), nothing else.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import open_implementation_pr
import post_summary
import state_io

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "analysis_result.schema.json"
RESULT_FIELDS = ("complete", "in_scope", "reason", "proposal", "subtasks", "tests", "open_questions")


class AnalysisInvocationError(RuntimeError):
    """The `claude` CLI invocation itself failed -- a tooling failure, distinct from a
    legitimate incomplete/out-of-scope verdict (process error, non-zero exit, malformed
    JSON, or a structured_output missing a required field)."""


class AnalysisHalted(RuntimeError):
    """The skill judged the story incomplete or out-of-scope. Carries the reason surfaced
    to the human; no state file is written for this outcome."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class AnalysisPROpenError(RuntimeError):
    """A deterministic step around the analysis itself failed -- the round-count query
    (`clarification_status`), the branch/PR-open step (AD-12) including its supersession
    of this story-slug's prior open PRs (AD-15), or the clarification label/comment/close
    or cap-notice step (AD-13/AD-15) -- distinct from AnalysisHalted (a
    CAP-1 judgment) and AnalysisInvocationError (a `claude` CLI tooling failure).

    Whether plan.md/decisions.md exist yet depends on which step raised this: the
    round-count query now runs *before* the state write, so a failure there leaves no
    state files; a failure in any later step (PR-open, supersession, labeling, closing,
    commenting) leaves plan.md/decisions.md already written."""


# --- the single invocation (one per run; clarification rounds are re-triggers, AD-13) ---


def _build_command(story_file: str, schema_text: str, claude_bin: str) -> list[str]:
    # See story-job-1-intake-analysis-plan.md's Design Notes: `--bare` is never used here
    # (it skips skill auto-discovery and would require ANTHROPIC_API_KEY, contradicting
    # AD-9's subscription-OAuth requirement). Skill invocation is by literal `/skill-name`
    # text in the prompt -- there is no separate CLI flag for it.
    return [
        claude_bin,
        "-p",
        f"/light-factory-analysis {story_file}",
        "--output-format",
        "json",
        "--json-schema",
        schema_text,
        "--allowedTools",
        "Read Grep Glob",
        "--permission-prompts",
        "none",
    ]


def _parse_structured_output(stdout: str) -> dict:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as e:
        raise AnalysisInvocationError(f"claude CLI output was not valid JSON: {e}") from e

    try:
        result = payload["structured_output"]
    except (KeyError, TypeError) as e:
        raise AnalysisInvocationError(
            f"claude CLI output missing 'structured_output': {payload!r}"
        ) from e

    if not isinstance(result, dict):
        raise AnalysisInvocationError(f"structured_output is not an object: {result!r}")

    missing = [f for f in RESULT_FIELDS if f not in result]
    if missing:
        raise AnalysisInvocationError(f"structured_output missing required field(s): {missing}")

    return result


def invoke_skill(
    story_file: str,
    *,
    claude_bin: str = "claude",
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Shell out to the `claude` CLI with the analysis skill and return the parsed,
    schema-validated result dict. Raises AnalysisInvocationError on any tooling failure."""
    schema_text = SCHEMA_PATH.read_text(encoding="utf-8")
    cmd = _build_command(story_file, schema_text, claude_bin)
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise AnalysisInvocationError(f"failed to invoke {claude_bin!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise AnalysisInvocationError(f"`claude` exited {proc.returncode}: {detail}")

    return _parse_structured_output(proc.stdout)


def _render_plan_body(result: dict) -> str:
    lines = ["## Proposal", "", (result.get("proposal") or "").strip() or "_none_", "", "## Subtasks", ""]
    subtasks = result.get("subtasks") or []
    lines += [f"- {s}" for s in subtasks] if subtasks else ["_none_"]
    lines += ["", "## Tests", ""]
    tests = result.get("tests") or []
    lines += [f"- {t}" for t in tests] if tests else ["_none_"]
    return "\n".join(lines)


def _render_decisions_body(result: dict) -> str:
    questions = result.get("open_questions") or []
    lines = ["## Open Questions", ""]
    lines += [f"- {q}" for q in questions] if questions else ["_none_"]
    return "\n".join(lines)


def _render_plan_summary(result: dict) -> str:
    """AD-4's gate-summary comment for the `plan-approval` gate: the proposal,
    subtask/test counts, and a pointer to the full-detail files -- not their contents."""
    subtasks = result.get("subtasks") or []
    tests = result.get("tests") or []
    lines = [
        "## Plan ready for review",
        "",
        "### Proposal",
        "",
        (result.get("proposal") or "").strip() or "_none_",
        "",
        f"- Subtasks: {len(subtasks)}",
        f"- Tests: {len(tests)}",
        "",
        "See `plan.md`/`decisions.md` for full detail.",
    ]
    return "\n".join(lines)


def run_analysis(
    story_file: str,
    story_slug: str,
    run_id: str,
    *,
    claude_bin: str = "claude",
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Run the single analysis invocation and route to one of the three I/O Matrix
    outcomes. Returns the written state on the two write outcomes. Raises AnalysisHalted
    (incomplete/out-of-scope, carries `.reason`) or AnalysisInvocationError (tooling
    failure) otherwise -- neither writes a state file."""
    result = invoke_skill(story_file, claude_bin=claude_bin, cwd=cwd)

    if not result["complete"] or not result["in_scope"]:
        raise AnalysisHalted(
            result.get("reason") or "analysis judged the story incomplete or out of scope (no reason given)"
        )

    if result.get("open_questions"):
        try:
            status = open_implementation_pr.clarification_status(story_slug, run_id, cwd=cwd)
        except open_implementation_pr.PROpenError as e:
            raise AnalysisPROpenError(str(e)) from e
    else:
        status = "ready-for-review"

    state_dir = state_io.ensure_layout(story_slug, run_id, base=state_base)
    plan_meta = state_io.write_state(
        state_dir / "plan.md",
        story_slug=story_slug,
        stage="analysis",
        status=status,
        body=_render_plan_body(result),
    )
    decisions_meta = state_io.write_state(
        state_dir / "decisions.md",
        story_slug=story_slug,
        stage="analysis",
        status=status,
        body=_render_decisions_body(result),
    )

    try:
        pr = open_implementation_pr.open_pr_for_story(
            story_slug, run_id, state_base=state_base, cwd=cwd
        )
        if status == "awaiting-clarification":
            open_implementation_pr.label_clarification_round(pr["pr_number"], cwd=cwd)
            open_implementation_pr.close_for_clarification(
                pr["pr_number"], result["open_questions"], cwd=cwd
            )
        elif status == "clarification-cap-reached":
            open_implementation_pr.post_clarification_cap_notice(
                pr["pr_number"], result["open_questions"], cwd=cwd
            )
        else:
            post_summary.post_comment(
                pr["pr_number"], _render_plan_summary(result), cwd=cwd
            )
    except (open_implementation_pr.PROpenError, post_summary.PostCommentError) as e:
        raise AnalysisPROpenError(str(e)) from e

    return {
        "status": status,
        "result": result,
        "plan": plan_meta,
        "decisions": decisions_meta,
        "pr": pr,
    }


# --- LangGraph wiring (AD-6: judgment work only; this ticket's single node) -------------


def build_graph():
    """A minimal single-node LangGraph graph wrapping run_analysis -- kept separate from
    run_analysis itself so the subprocess/parse logic above stays reusable and testable
    without going through the graph."""
    from langgraph.graph import END, StateGraph
    from typing_extensions import TypedDict

    class AnalysisState(TypedDict, total=False):
        story_file: str
        story_slug: str
        run_id: str
        claude_bin: str
        state_base: str
        outcome: dict

    def analyze_node(state: AnalysisState) -> AnalysisState:
        outcome = run_analysis(
            state["story_file"],
            state["story_slug"],
            state["run_id"],
            claude_bin=state.get("claude_bin", "claude"),
            state_base=state.get("state_base", state_io.FACTORY_DIR),
        )
        return {"outcome": outcome}

    graph = StateGraph(AnalysisState)
    graph.add_node("analyze", analyze_node)
    graph.set_entry_point("analyze")
    graph.add_edge("analyze", END)
    return graph.compile()


# --- CLI ---------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-file", required=True, help="path to the triggering story file")
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--claude-bin", default="claude", help="override for testing; defaults to the claude CLI on PATH")
    args = p.parse_args(argv)

    try:
        outcome = run_analysis(args.story_file, args.story_slug, args.run_id, claude_bin=args.claude_bin)
    except AnalysisHalted as e:
        print(f"analysis halted: {e.reason}", file=sys.stderr)
        return 1
    except AnalysisInvocationError as e:
        print(f"analysis tooling failure: {e}", file=sys.stderr)
        return 3
    except AnalysisPROpenError as e:
        print(f"branch/PR-open step failed: {e}", file=sys.stderr)
        return 4

    print(json.dumps({"ok": True, "status": outcome["status"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
