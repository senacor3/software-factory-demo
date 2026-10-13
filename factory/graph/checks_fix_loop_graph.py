#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = ["langgraph>=1.2.12,<2"]
# ///
"""checks_fix_loop_graph -- the checks-fix-loop job's bounded fix loop (AD-10, new
stage mirroring AD-11's existing review fix loop).

Runs only when the `checks` job reported a failed check -- its `any-check-failed`
output, not its conclusion: that job ends `success` on a failed check, so a run this
loop recovers is not left red (wired via the workflow's `checks-fix-loop` job `if:`,
backlog bug 4). Unlike `fix_loop_graph.py`, the *initial* check run
already happened in the `checks` job itself (CAP-5, AD-6) -- this module never
re-invokes `run_checks.py`'s commands speculatively, it only reads the evidence that
job already wrote (`evidence/checks/<name>.json`, committed before this job starts)
to learn which check(s) actually failed.

Then: while any check is still failing and the cycle count is under
`MAX_FIX_CYCLES` -- re-engage the implementation skill (via its optional
`review_path` argument, reused as-is) with a `checks.md` state file naming the
failing check(s) and their output, re-run *only* those check(s) (never the full
suite, mirrors AD-11), and check again. Multiple simultaneous check failures are
passed together as one cycle's context, not split into separate cycles.

A hard cap of 2 fix cycles (`MAX_FIX_CYCLES`, duplicated from `fix_loop_graph.py`
rather than imported -- the two fix-loop stages are independently owned, see the
plan's Code Map): if still failing after the second cycle's recheck, stop -- no
third fix cycle -- and stamp `checks.md`'s status `unresolved-after-cap` instead of
looping again just to relabel. Cap-out fails this job (via this module's CLI exit
code), and with it the run -- no silent success, no auto-merge.

A re-check runs under the conditions the `checks` job's first run had: the job
sets up the same toolchains (the workflow's shared `checks-toolchain` action), and
this module runs the config's `setup:` commands (`run_checks.run_setup`, e.g. a
dependency install) before every re-check -- after the agent's edits, since a fix may
change what there is to install -- because re-running only the failed check(s) means
no earlier check has prepared the checkout.

A check whose command could not be started at all (`run_checks.is_tooling_failure`),
or a failing setup command, is a tooling failure, not a finding in the code: the loop
stops without engaging the implementation agent for it, stamps `checks.md`'s status
`tooling-failure` naming the check and command, and this module's CLI exits 6. That
holds for the evidence the loop starts from -- the checks' and the setup's
(`evidence/checks/setup.json`) -- as well as for a re-check. Checks that still hold a
real finding at that point stay listed in `checks.md` beside the tooling failure.

A tooling failure in the evidence the loop starts from is verified once before it is
believed: setup and the failing check(s) are run again, with no agent call and no fix
cycle counted. That evidence may be this job's own from an earlier attempt -- "Re-run
failed jobs" re-runs this job alone, since the `checks` job is not a failed one -- and
a runner problem that has since gone (a registry that was down) must not fail every
re-run from the record of it.

`checks.md`'s `fix_cycle` counter is incremented and stamped only by this module's
own code -- never derived from or trusted to the implementation agent's output.

Per AD-6, deterministic checks (build/test/lint/security) are invoked here as plain
function calls (`run_checks.run_check`), never as graph nodes or agent tool calls --
this graph's one node is pure judgment work (looping over the implementation agent
invocation).
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import checkout_branch
import commit_push_implementation
import run_checks
import state_io

sys.path.insert(0, str(Path(__file__).resolve().parent))
import implementation_graph

MAX_FIX_CYCLES = 2

_NO_EVIDENCE_DETAIL = (
    "no evidence found for check {name!r} -- the checks job may have failed before "
    "running it (e.g. a toolchain/checkout crash)"
)


# --- reading which checks failed -------------------------------------------------


def _read_check_result(
    name: str, story_slug: str, run_id: str, *, state_base: str | os.PathLike
) -> dict:
    """Return the evidence `run_checks.py` already wrote for check `name`.

    A missing evidence file (the checks job crashed before that check ever ran) is
    treated conservatively as a failure, so this stage is never silently skipped
    over a check we have no result for -- see the plan's I/O & Edge-Case Matrix row
    on a non-check `checks` job error.
    """
    path = (
        state_io.state_dir(story_slug, run_id, base=state_base)
        / "evidence"
        / "checks"
        / f"{name}.json"
    )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {"status": "fail", "command": None, "returncode": None, "detail": _NO_EVIDENCE_DETAIL.format(name=name)}


def _failing_checks(names, story_slug: str, run_id: str, *, state_base: str | os.PathLike) -> dict[str, dict]:
    """Return `{name: result}` for every check in `names` whose result is `"fail"`."""
    return {
        name: result
        for name in names
        if (result := _read_check_result(name, story_slug, run_id, state_base=state_base))["status"] == "fail"
    }


def _rerun_checks(
    names, story_slug: str, run_id: str, *, state_base: str | os.PathLike, cwd
) -> dict[str, dict]:
    """Re-run exactly the checks named in `names` (never the full suite) and return
    `{name: result}` for those still `"fail"` afterward. Writes fresh evidence for
    each one re-run, same as the `checks` job's own steps do."""
    return {
        name: result
        for name in names
        if (result := run_checks.run_check(name, story_slug, run_id, state_base=state_base, cwd=cwd))["status"]
        == "fail"
    }


def _tooling_failures(failing: dict[str, dict]) -> dict[str, dict]:
    """Return the subset of `failing` whose command could not be started at all."""
    return {name: result for name, result in failing.items() if run_checks.is_tooling_failure(result)}


def _describe_tooling_failure(name: str, result: dict) -> str:
    command = result.get("command")
    what = f"`{shlex.join(command)}`" if command else "its configuration"
    returncode = result.get("returncode")
    code = "" if returncode is None else f" (return code {returncode})"
    return f"{name}: {what} could not be run{code}: {result.get('detail', '')}"


def _render_tooling_body(tooling: dict[str, dict], failing: dict[str, dict]) -> str:
    """Name what could not be run, then whatever still holds a real finding beside it."""
    lines = ["## Tooling failures", ""]
    lines += [f"- {_describe_tooling_failure(name, tooling[name])}" for name in sorted(tooling)]
    findings = {name: result for name, result in failing.items() if name not in tooling}
    if findings:
        lines += ["", _render_checks_body(findings)]
    return "\n".join(lines)


def _render_checks_body(failing: dict[str, dict]) -> str:
    lines = ["## Failing checks", ""]
    if not failing:
        lines.append("_none_")
    else:
        for name in sorted(failing):
            lines.append(f"- **{name}**: {failing[name].get('detail', '')}")
    return "\n".join(lines)


# --- the loop ----------------------------------------------------------------------


def run_checks_with_fix_loop(
    story_slug: str,
    run_id: str,
    *,
    claude_bin: str = "claude",
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Bounded checks fix loop (cap 2 cycles, AD-10) -> final status stamp.

    Returns `{"status": str, "fix_cycle": int, "failing": list[str], "tooling": dict,
    "checks": dict}` where `status` is the stamped final status (`resolved`,
    `unresolved-after-cap` or `tooling-failure`), `failing` the still-failing check
    names (empty when resolved), `tooling` the `{name: result}` of whatever could not
    be run (`setup` for a failing setup command; empty unless the status is
    `tooling-failure`), and `checks` the frontmatter dict actually written to
    `checks.md`.

    Raises `implementation_graph.ImplementationInvocationError` if the implementation
    agent's tooling call fails, or `checkout_branch.CheckoutError` /
    `commit_push_implementation.CommitPushError` if a fix cycle's deterministic
    checkout/commit step fails -- each stops the loop immediately with nothing
    further attempted (no final re-stamp), mirroring `fix_loop_graph.py`.
    """
    state_directory = state_io.state_dir(story_slug, run_id, base=state_base)
    checks_path = str(state_directory / "checks.md")

    failing = _failing_checks(run_checks.CHECK_NAMES, story_slug, run_id, state_base=state_base)

    cycle = 0
    setup = run_checks.read_setup_result(story_slug, run_id, state_base=state_base)
    setup_failed = setup is not None and setup.get("status") == "fail"
    tooling = _tooling_failures(failing)
    if setup_failed or tooling:
        # The evidence on the branch says something could not be run. Verify that
        # once before believing it -- see the module docstring -- with setup first:
        # where it failed, whatever the checks then reported says nothing about the
        # code.
        setup = run_checks.run_setup(story_slug, run_id, state_base=state_base, cwd=cwd)
        if setup["status"] == "fail":
            tooling = {run_checks.SETUP_KEY: setup}
        else:
            failing = _rerun_checks(sorted(failing), story_slug, run_id, state_base=state_base, cwd=cwd)
            tooling = _tooling_failures(failing)
    while failing and not tooling and cycle < MAX_FIX_CYCLES:
        cycle += 1

        state_io.write_state(
            checks_path,
            story_slug=story_slug,
            stage="checks",
            status="findings-open",
            body=_render_checks_body(failing),
            extra={"fix_cycle": cycle},
        )

        implementation_graph.run_implementation(
            story_slug,
            run_id,
            claude_bin=claude_bin,
            state_base=state_base,
            cwd=cwd,
            review_path=checks_path,
        )

        setup = run_checks.run_setup(story_slug, run_id, state_base=state_base, cwd=cwd)
        if setup["status"] == "fail":
            tooling = {run_checks.SETUP_KEY: setup}
            break

        failing = _rerun_checks(sorted(failing), story_slug, run_id, state_base=state_base, cwd=cwd)
        tooling = _tooling_failures(failing)

    if tooling:
        final_status, body = "tooling-failure", _render_tooling_body(tooling, failing)
    else:
        final_status = "unresolved-after-cap" if failing else "resolved"
        body = _render_checks_body(failing)
    checks_meta = state_io.write_state(
        checks_path,
        story_slug=story_slug,
        stage="checks",
        status=final_status,
        body=body,
        extra={"fix_cycle": cycle},
    )

    return {
        "status": final_status,
        "fix_cycle": cycle,
        "failing": sorted(failing),
        "tooling": tooling,
        "checks": checks_meta,
    }


# --- LangGraph wiring (AD-6: judgment work only; this ticket's single node) -------------


def build_graph():
    """A minimal single-node LangGraph graph wrapping run_checks_with_fix_loop --
    kept separate so the looping logic above stays reusable and testable without
    going through the graph (mirrors fix_loop_graph.py's build_graph)."""
    from langgraph.graph import END, StateGraph
    from typing_extensions import TypedDict

    class ChecksFixLoopState(TypedDict, total=False):
        story_slug: str
        run_id: str
        claude_bin: str
        state_base: str
        outcome: dict

    def fix_loop_node(state: ChecksFixLoopState) -> ChecksFixLoopState:
        outcome = run_checks_with_fix_loop(
            state["story_slug"],
            state["run_id"],
            claude_bin=state.get("claude_bin", "claude"),
            state_base=state.get("state_base", state_io.FACTORY_DIR),
        )
        return {"outcome": outcome}

    graph = StateGraph(ChecksFixLoopState)
    graph.add_node("checks_fix_loop", fix_loop_node)
    graph.set_entry_point("checks_fix_loop")
    graph.add_edge("checks_fix_loop", END)
    return graph.compile()


# --- CLI ---------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--claude-bin", default="claude", help="override for testing; defaults to the claude CLI on PATH")
    args = p.parse_args(argv)

    try:
        outcome = run_checks_with_fix_loop(args.story_slug, args.run_id, claude_bin=args.claude_bin)
    except implementation_graph.ImplementationInvocationError as e:
        print(f"implementation tooling failure: {e}", file=sys.stderr)
        return 4
    except (checkout_branch.CheckoutError, commit_push_implementation.CommitPushError) as e:
        print(f"fix-cycle git step failed: {e}", file=sys.stderr)
        return 5

    if outcome["status"] == "tooling-failure":
        for name in sorted(outcome["tooling"]):
            print(f"tooling failure: {_describe_tooling_failure(name, outcome['tooling'][name])}", file=sys.stderr)
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": outcome["status"],
                    "fix_cycle": outcome["fix_cycle"],
                    "tooling": sorted(outcome["tooling"]),
                }
            )
        )
        return 6

    print(json.dumps({"ok": True, "status": outcome["status"], "fix_cycle": outcome["fix_cycle"]}))
    return 1 if outcome["status"] == "unresolved-after-cap" else 0


if __name__ == "__main__":
    sys.exit(main())
