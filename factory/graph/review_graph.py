#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["langgraph>=1.2.12,<2"]
# ///
"""review_graph -- the review job's independent review stage (CAP-6 independent agent review).

Invokes the read-only `.claude/skills/software-factory-review/` skill via the `claude`
CLI, parses its schema-validated structured output, and writes the one outcome the
I/O & Edge-Case Matrix defines (see
story-independent-review-agent-plan.md):

  1. `findings` is empty -- the implementation satisfies the plan. Writes `review.md`
     with status `resolved` (AD-10's existing enum) and `evidence/review/findings.json`
     with an empty `findings` array (AD-8).
  2. `findings` is non-empty -- a legitimate outcome, not a failure. Writes `review.md`
     with status `findings-open`, listing each finding, and the same raw findings to
     `evidence/review/findings.json`.

A third case -- the `claude` CLI invocation itself failing (non-zero exit, malformed
or schema-invalid JSON) -- is a tooling failure, not a legitimate verdict, and is
raised as `ReviewInvocationError`, distinct from both outcomes above. Nothing is
written on this path.

No fix-loop or counter logic lives here (ticket 10's scope); this module only ever
writes `review.md` + `evidence/review/`, never `plan.md`/`decisions.md` (AD-10).

Per AD-6, deterministic checks never become graph nodes -- this graph's one node is
pure judgment work (shelling out to the review skill), nothing else.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import state_io

SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "review_result.schema.json"
RESULT_FIELDS = ("findings",)


class ReviewInvocationError(RuntimeError):
    """The `claude` CLI invocation itself failed -- a tooling failure (process error,
    non-zero exit, malformed JSON, or a structured_output missing a required field).
    Distinct from a legitimate review verdict (clean pass or findings) -- only this
    path leaves no review.md/evidence written."""


# --- the single invocation ----------------------------------------------------------


def _build_command(plan_path: str, decisions_path: str, schema_text: str, claude_bin: str) -> list[str]:
    # Mirrors analysis_graph.py's _build_command: no `--bare` (skips skill
    # auto-discovery and would require ANTHROPIC_API_KEY, contradicting AD-9).
    return [
        claude_bin,
        "-p",
        f"/software-factory-review {plan_path} {decisions_path}",
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
        raise ReviewInvocationError(f"claude CLI output was not valid JSON: {e}") from e

    try:
        result = payload["structured_output"]
    except (KeyError, TypeError) as e:
        raise ReviewInvocationError(
            f"claude CLI output missing 'structured_output': {payload!r}"
        ) from e

    if not isinstance(result, dict):
        raise ReviewInvocationError(f"structured_output is not an object: {result!r}")

    missing = [f for f in RESULT_FIELDS if f not in result]
    if missing:
        raise ReviewInvocationError(f"structured_output missing required field(s): {missing}")

    return result


def invoke_skill(
    plan_path: str,
    decisions_path: str,
    *,
    claude_bin: str = "claude",
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Shell out to the `claude` CLI with the review skill and return the parsed,
    schema-validated result dict. Raises ReviewInvocationError on any tooling failure."""
    schema_text = SCHEMA_PATH.read_text(encoding="utf-8")
    cmd = _build_command(plan_path, decisions_path, schema_text, claude_bin)
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise ReviewInvocationError(f"failed to invoke {claude_bin!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise ReviewInvocationError(f"`claude` exited {proc.returncode}: {detail}")

    return _parse_structured_output(proc.stdout)


def _render_review_body(result: dict) -> str:
    findings = result.get("findings") or []
    lines = ["## Findings", ""]
    if not findings:
        lines.append("_none_")
    else:
        for f in findings:
            location = f.get("location", "")
            description = f.get("description", "")
            lines.append(f"- **{location}**: {description}")
    return "\n".join(lines)


def run_review(
    story_slug: str,
    run_id: str,
    *,
    claude_bin: str = "claude",
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Run the single review invocation and write its outcome.

    Returns `{"status": str, "result": dict, "review": dict}` on success -- either
    legitimate verdict (`resolved` or `findings-open`). Raises ReviewInvocationError
    (tooling failure) otherwise -- nothing is written on that path.
    """
    state_directory = state_io.state_dir(story_slug, run_id, base=state_base)
    plan_path = str(state_directory / "plan.md")
    decisions_path = str(state_directory / "decisions.md")

    result = invoke_skill(plan_path, decisions_path, claude_bin=claude_bin, cwd=cwd)

    findings = result["findings"]
    status = "findings-open" if findings else "resolved"

    review_meta = state_io.write_state(
        state_directory / "review.md",
        story_slug=story_slug,
        stage="review",
        status=status,
        body=_render_review_body(result),
    )
    state_io.write_atomic(
        state_directory / "evidence" / "review" / "findings.json",
        json.dumps({"findings": findings}, indent=2) + "\n",
    )

    return {"status": status, "result": result, "review": review_meta}


# --- LangGraph wiring (AD-6: judgment work only; this ticket's single node) -------------


def build_graph():
    """A minimal single-node LangGraph graph wrapping run_review -- kept separate from
    run_review itself so the subprocess/parse logic above stays reusable and testable
    without going through the graph (mirrors analysis_graph.py's build_graph)."""
    from langgraph.graph import END, StateGraph
    from typing_extensions import TypedDict

    class ReviewState(TypedDict, total=False):
        story_slug: str
        run_id: str
        claude_bin: str
        state_base: str
        outcome: dict

    def review_node(state: ReviewState) -> ReviewState:
        outcome = run_review(
            state["story_slug"],
            state["run_id"],
            claude_bin=state.get("claude_bin", "claude"),
            state_base=state.get("state_base", state_io.FACTORY_DIR),
        )
        return {"outcome": outcome}

    graph = StateGraph(ReviewState)
    graph.add_node("review", review_node)
    graph.set_entry_point("review")
    graph.add_edge("review", END)
    return graph.compile()


# --- CLI ---------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--claude-bin", default="claude", help="override for testing; defaults to the claude CLI on PATH")
    args = p.parse_args(argv)

    try:
        outcome = run_review(args.story_slug, args.run_id, claude_bin=args.claude_bin)
    except ReviewInvocationError as e:
        print(f"review tooling failure: {e}", file=sys.stderr)
        return 3

    print(json.dumps({"ok": True, "status": outcome["status"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
