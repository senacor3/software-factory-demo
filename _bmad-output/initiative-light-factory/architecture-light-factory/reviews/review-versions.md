# Versions Lens Review — architecture-light-factory.md

**Scope:** Fresh verification pass focused on (1) whether AD-12/AD-13 (newly added) introduce or imply any version-sensitive or API-behavior claim that needs reality-checking, and (2) a spot-re-check of the existing Stack table (LangGraph, Python, Claude Code CLI, Node.js), given AD-1–AD-11 and the Stack table already had a versions-lens pass applied earlier today and AD-12/13 added no new technology/stack entries.

**Date of check:** 2026-10-01 (web searches run live against current sources).

---

## Verdict

One real, actionable finding: **AD-12's core sequencing claim ("open the PR... immediately after creating the isolated branch and before any commits") is not reality-checked against how GitHub's PR-creation API actually behaves, and is likely to fail as literally written.** Everything else checked — the Stack table's four version-sensitive rows, and AD-9's `CLAUDE_CODE_OAUTH_TOKEN` approach — holds up against current sources, with one immaterial date nit and one forward-looking watch item.

---

## Findings

### 1. [HIGH] AD-12: opening a PR "before any commits" is not how GitHub's PR-creation API behaves

AD-12's rule (line 111): *"the implementation agent's first action in Job 2 is to open the PR against the target branch, immediately after creating the isolated branch and before any commits."*

This was asserted, not reality-checked, and the check fails it. GitHub's pull-request creation (REST API, GraphQL, and `gh pr create` alike) requires the head branch to have at least one commit that differs from the base branch. A branch created directly from the base with zero new commits is identical to base (same commit SHA), and GitHub rejects the PR-creation call outright. This is well-documented, reproducible behavior — the underlying GraphQL error is literally `No commits between <base> and <head>` (see e.g. [cli/cli#10238](https://github.com/cli/cli/issues/10238), [octokit.net#879](https://github.com/octokit/octokit.net/issues/879), [cli/cli#2691](https://github.com/cli/cli/issues/2691)). GitHub's official REST API reference doesn't spell this out explicitly, but the consistent, independently-reported error text across multiple GitHub API clients corroborates it.

**Why this matters for the spine:** AD-12 is a deliberate, reasoned decision (good) — it pins the PR as "the single artifact for the rest of the run" and makes AD-4's commit-comment/PR-comment split temporal. That reasoning is sound. But the literal mechanic described ("before any commits") is not achievable via a plain `git checkout -b` + immediate PR-open. The implementation agent will hit a creation failure on its very first action in Job 2 unless the sequence actually includes a commit first.

**Fix options** (pick one, doesn't require re-opening the AD's intent):
- Cheapest: amend the rule to "immediately after creating the isolated branch **and an initial empty commit** (`git commit --allow-empty`), before any content commits" — this preserves "PR exists before real work lands" while being achievable.
- Alternative: have the branch-creation step itself commit a trivial scaffold (e.g., a `.light-factory/<story-slug>/` placeholder) as its first commit, then open the PR — folds naturally into AD-8's state-directory creation.

Either way, the Structural Seed diagram's `OpenPR` state (line 181) and the `light-factory.yml` comment (line 214) should get the same one-line correction once the AD text is fixed, so they don't silently re-assert the unachievable version.

### 2. [confirmed, no issue] AD-9 `CLAUDE_CODE_OAUTH_TOKEN` / `claude setup-token` — still the sanctioned, current CI path

This wasn't touched by AD-12/13 but is worth flagging as checked, since the topic is genuinely live right now: Anthropic ran a crackdown (Jan–Mar 2026) on subscription OAuth tokens being used in *unofficial third-party tools* (OpenCode, Zed, Cline, Aider, etc.) bypassing the Claude Code CLI itself. That could read as a risk to AD-9. It isn't: the live Claude Code docs (fetched today, `code.claude.com/docs/en/authentication`) explicitly document `claude setup-token` → `CLAUDE_CODE_OAUTH_TOKEN` as the one-year, CI-intended credential, officially supported and unaffected by that crackdown — the crackdown targeted non-Anthropic tooling reusing the OAuth flow outside Claude Code, not this documented in-CLI CI path. AD-9's rejection of the `/install-github-app` short-lived token in favor of `claude setup-token` also still matches current docs (that flow's token is not positioned for long-lived CI use). No change needed.

### 3. [confirmed] Stack table spot-re-check

| Stack row | Checked against | Result |
| --- | --- | --- |
| LangGraph (Python) 1.2.12 | PyPI release history | Confirmed current — 1.2.12 released 2026-09-21, no newer release as of 2026-10-01. |
| Claude Code CLI `>=2.1.x`, `@latest`, Node 22+ since v2.1.198 | npm package page | Confirmed — latest published version is 2.1.286; Node 22 floor since v2.1.198 still holds. |
| Node.js `>=22` | Node release/EOL trackers | Confirmed compatible; as of today Node 22 is in Maintenance LTS (Active LTS passed to Node 24 in Oct 2026), EOL April 2027 — doesn't contradict the AD's `>=22` floor, just worth knowing Node 22 itself is no longer the newest LTS. |
| Python `>=3.13` targeting 3.14 | EOL trackers | Directionally confirmed, one date nit (below). |

### 4. [LOW, cosmetic] Python 3.13 active-support-end date is off by ~5 days

Stack table (line 136) states Python 3.13 "exits active support 2026-10-01." Multiple independent EOL trackers give **2026-10-06** as the actual active-support cutoff (3.13 was released 2024-10-07; full support runs 2 years). The conclusion (target 3.14 for new work, 3.13 becomes security-only) is unaffected either way — this is a one-sentence date correction, not a reasoning problem.

### 5. [LOW, forward-looking watch item, out of this update's scope] GitHub's 30-day Environment-wait ceiling may shrink

AD-2 (unchanged by this update, so not re-litigated here) relies on "GitHub pauses and resumes that same run natively, up to 30 days." That's still accurate today — confirmed via GitHub Community discussions and docs. But GitHub has publicly announced a planned change reducing the *default* wait timeout to 5 days, configurable up to 15 days, down from the current fixed 30-day ceiling. No shipped date found in this pass. Not an AD-12/13 concern and not asserted incorrectly today, but worth a note for whoever next revisits AD-2/AD-4, since a shortened default could matter for the gate-wait story if it ships before v1 goes live.

---

## Non-findings (checked, nothing wrong)

- AD-13's clarification-loop cap mechanics make no new technology or API claims beyond what AD-11/AD-10 already established — nothing version-sensitive to check there beyond the shared `status: awaiting-clarification` enum reuse, which is an internal convention, not an external fact.
- GitHub Actions Environment + required-reviewers protection-rule behavior generally (pause/resume, reviewer approval semantics) matches current GitHub docs and community reporting.
