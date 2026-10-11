#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""open_implementation_pr -- AD-12's deterministic branch+PR-open step.

Once the analysis job's `run_analysis` (factory/graph/analysis_graph.py) decides to proceed (a
non-halted result), this script -- not the agent -- creates the isolated branch
(`light-factory/<story-slug>/<run-id>`), commits the analysis stage's own just-written
`plan.md`/`decisions.md` as the branch's first real commit, and opens a PR against the
target branch. Mirrors `state_io.py`'s "script writes, not agent" precedent (AD-5).

Idempotent: if an open PR already exists for this exact branch name, its info is
returned instead of recreating anything -- entry 4's clarification rounds re-call
`run_analysis` and must not fail or duplicate work against an already-open PR.

Supersession (AD-15): once this run's PR exists, every *other* open PR whose head branch
starts with `light-factory/<story-slug>/` is closed with a "Superseded by #N" comment and
the new PR gets one "Retry of #M" comment (see `supersede_prior_prs`). Only the PR closes
-- branches and state directories stay. This runs on the idempotent-reuse path too, so a
same-run-id re-run finishes a supersession its first attempt left incomplete. An at-cap PR
that `post_clarification_cap_notice` deliberately left open is superseded like any other
on the next re-trigger; it still counts toward the clarification cap, since
`count_clarification_rounds` queries all states.

All `git`/`gh` subprocess failures raise a single `PROpenError`, carrying the failing
command and its output, so callers can distinguish this failure mode from a CAP-1
judgment halt or a `claude` CLI tooling failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state_io


class PROpenError(RuntimeError):
    """A `git` or `gh` subprocess call failed while opening the implementation PR."""


# AD-13's bounded-rounds cap (ticket 2.1, Option C) and the PR label that makes each
# clarification round countable via AD-15's branch-prefix search. Matches AD-11's
# fix-loop cap (MAX_FIX_CYCLES = 2) by design choice, not by shared code.
CLARIFICATION_CAP = 2
CLARIFICATION_LABEL = "clarification-round"


def _run(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise PROpenError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise PROpenError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout.strip()


def find_open_pr(branch: str, *, cwd: str | os.PathLike | None = None) -> dict | None:
    out = _run(
        ["gh", "pr", "list", "--head", branch, "--state", "open", "--json", "number,url"],
        cwd=cwd,
    )
    import json

    prs = json.loads(out) if out else []
    if not prs:
        return None
    pr = prs[0]
    return {"branch": branch, "pr_number": pr["number"], "pr_url": pr["url"]}


def count_clarification_rounds(
    story_slug: str, run_id: str, *, cwd: str | os.PathLike | None = None
) -> int:
    """Count this story-slug's prior PRs labeled `clarification-round`, in **any** state
    (open or closed) -- AD-13's cap must stay correct even when an at-cap PR is left open,
    so counting only closed PRs would let the cap silently reset.

    Excludes `run_id`'s own branch (`light-factory/<story_slug>/<run_id>`): this is called
    before this run's own PR exists, but a same-run-id retry after a partial failure (e.g.
    `label_clarification_round` already labeled this run's own PR, then a later step
    failed) must not double-count that already-labeled PR as a *prior* round.

    `gh pr list --head` only matches one exact branch name (no prefix/glob mode), so this
    can't reuse `find_open_pr`'s query shape. Instead, lists PRs by `--label` repo-wide
    (`--state all`, `--limit 100`) and filters client-side on the branch-prefix
    `light-factory/<story_slug>/*` -- never another story-slug's PRs (a decoy PR for a
    different slug is excluded by this prefix check). Known PoC-scope limitation,
    consistent with AD-15's own unpaginated search: a repo with more than 100
    `clarification-round`-labeled PRs across *all* story-slugs could undercount a given
    slug's rounds -- not worth solving now, no existing query in this codebase paginates.
    """
    out = _run(
        [
            "gh",
            "pr",
            "list",
            "--label",
            CLARIFICATION_LABEL,
            "--state",
            "all",
            "--limit",
            "100",
            "--json",
            "headRefName",
        ],
        cwd=cwd,
    )
    import json

    prs = json.loads(out) if out else []
    prefix = f"light-factory/{story_slug}/"
    own_branch = f"light-factory/{story_slug}/{run_id}"
    return sum(
        1
        for pr in prs
        if pr.get("headRefName", "").startswith(prefix) and pr.get("headRefName") != own_branch
    )


def clarification_status(
    story_slug: str, run_id: str, *, cwd: str | os.PathLike | None = None
) -> str:
    """Decide `awaiting-clarification` vs `clarification-cap-reached` (AD-13's cap, 2) from
    this story-slug's prior `clarification-round` round count, excluding `run_id`'s own
    branch (see `count_clarification_rounds`). Deterministic -- never the agent -- and must
    run before `plan.md`/`decisions.md` are written so their `status` field reflects the
    decision. Raises PROpenError on any subprocess failure."""
    count = count_clarification_rounds(story_slug, run_id, cwd=cwd)
    return "clarification-cap-reached" if count >= CLARIFICATION_CAP else "awaiting-clarification"


def supersede_prior_prs(
    story_slug: str,
    run_id: str,
    new_pr_number: int,
    *,
    cwd: str | os.PathLike | None = None,
) -> list[int]:
    """AD-15's supersession rule: post one "Retry of #M" comment on `new_pr_number`, then
    close every other open PR for this story-slug with a "Superseded by #N" comment.
    Returns the closed PR numbers in ascending order (empty when there was no predecessor,
    in which case nothing is closed or commented).

    Same query shape as `count_clarification_rounds` -- `gh pr list --head` has no prefix
    mode, so this lists open PRs repo-wide (`--limit 100`, same unpaginated PoC limitation)
    and filters client-side on `light-factory/<story_slug>/` with the trailing slash (so
    slug `foo` never matches `foo-bar`), excluding `run_id`'s own branch.

    Never `--delete-branch` and never touches state directories (AD-10/AD-12/AD-15).
    Comments first, closes second: a failure part-way leaves the back-link complete, and a
    same-run-id re-run closes whatever is still open at worst with a duplicate "Retry of"
    comment -- never a predecessor closed without being named. Raises PROpenError on any
    subprocess failure."""
    out = _run(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,headRefName",
        ],
        cwd=cwd,
    )
    import json

    prs = json.loads(out) if out else []
    prefix = f"light-factory/{story_slug}/"
    own_branch = f"light-factory/{story_slug}/{run_id}"
    prior = sorted(
        pr["number"]
        for pr in prs
        if pr.get("headRefName", "").startswith(prefix)
        and pr.get("headRefName") != own_branch
        and pr["number"] != new_pr_number
    )
    if not prior:
        return []

    retry_of = ", ".join(f"#{number}" for number in prior)
    _run(["gh", "pr", "comment", str(new_pr_number), "--body", f"Retry of {retry_of}"], cwd=cwd)
    for number in prior:
        _run(
            ["gh", "pr", "close", str(number), "--comment", f"Superseded by #{new_pr_number}"],
            cwd=cwd,
        )
    return prior


def open_pr_for_story(
    story_slug: str,
    run_id: str,
    *,
    target_branch: str = "main",
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Create the isolated branch, commit plan.md/decisions.md, push, and open the PR.

    Idempotent: returns the existing open PR's info if one is already open for this
    branch, without creating anything new. Either way, supersedes this story-slug's other
    open PRs (AD-15, `supersede_prior_prs`) before returning. Raises PROpenError on any
    git/gh failure.
    """
    branch = f"light-factory/{story_slug}/{run_id}"

    existing = find_open_pr(branch, cwd=cwd)
    if existing is not None:
        supersede_prior_prs(story_slug, run_id, existing["pr_number"], cwd=cwd)
        return existing

    state_directory = state_io.state_dir(story_slug, run_id, base=state_base)
    plan_path = state_directory / "plan.md"
    decisions_path = state_directory / "decisions.md"

    _run(["git", "checkout", "-b", branch], cwd=cwd)
    _run(["git", "add", str(plan_path), str(decisions_path)], cwd=cwd)
    _run(
        [
            "git",
            "-c",
            "user.name=light-factory-bot",
            "-c",
            "user.email=light-factory-bot@users.noreply.github.com",
            "commit",
            "-m",
            f"Analysis: {story_slug} ({run_id})",
        ],
        cwd=cwd,
    )
    _run(["git", "push", "-u", "origin", branch], cwd=cwd)
    _run(
        [
            "gh",
            "pr",
            "create",
            "--head",
            branch,
            "--base",
            target_branch,
            "--title",
            f"light-factory: {story_slug} ({run_id})",
            "--body",
            f"Automated analysis-stage PR for `{story_slug}` (`{run_id}`). See `plan.md`/`decisions.md`.",
        ],
        cwd=cwd,
    )

    created = find_open_pr(branch, cwd=cwd)
    if created is None:
        raise PROpenError(f"gh pr create reported success but no open PR found for branch {branch!r}")
    supersede_prior_prs(story_slug, run_id, created["pr_number"], cwd=cwd)
    return created


def close_for_clarification(
    pr_number: int,
    open_questions: list[str],
    *,
    cwd: str | os.PathLike | None = None,
) -> None:
    """Post `open_questions` as a comment on `pr_number` and close it in the same call
    (AD-13/AD-15) -- never `--delete-branch`, per AD-10/AD-12/AD-15's audit-trail-over-
    cleanup posture. Raises PROpenError on any subprocess failure."""
    comment = "Open questions from analysis:\n\n" + "\n".join(f"- {q}" for q in open_questions)
    _run(["gh", "pr", "close", str(pr_number), "--comment", comment], cwd=cwd)


def label_clarification_round(pr_number: int, *, cwd: str | os.PathLike | None = None) -> None:
    """Ensure the `clarification-round` label exists (`gh label create ... --force` is
    idempotent -- creates or updates, so a fresh target repo needs no manual one-time
    label setup, unlike the Environments that did need manual creation in epic 1), then
    apply it to `pr_number`. Used by both the below-cap path (alongside
    `close_for_clarification`, which stays unchanged) and `post_clarification_cap_notice`
    (the at-cap path). Raises PROpenError on any subprocess failure."""
    _run(
        [
            "gh",
            "label",
            "create",
            CLARIFICATION_LABEL,
            "--description",
            "AD-13: a clarification round was closed or cap-noticed for this story-slug",
            "--force",
        ],
        cwd=cwd,
    )
    _run(["gh", "pr", "edit", str(pr_number), "--add-label", CLARIFICATION_LABEL], cwd=cwd)


def post_clarification_cap_notice(
    pr_number: int,
    open_questions: list[str],
    *,
    cwd: str | os.PathLike | None = None,
) -> None:
    """The at-cap path (AD-13, user's call 2026-10-11): label `pr_number` and post a
    comment that the clarification budget is spent and it's up to the developer to decide
    how to proceed -- does **not** close the PR (unlike `close_for_clarification`'s
    below-cap path). Raises PROpenError on any subprocess failure."""
    label_clarification_round(pr_number, cwd=cwd)
    comment = (
        f"Clarification budget spent ({CLARIFICATION_CAP}-round cap reached) for this "
        "story-slug. It's up to the developer to decide how to proceed (e.g. rescope or "
        "split the story) -- this PR is left open, not closed automatically.\n\n"
        "Open questions from the latest analysis pass:\n\n"
        + "\n".join(f"- {q}" for q in open_questions)
    )
    _run(["gh", "pr", "comment", str(pr_number), "--body", comment], cwd=cwd)
