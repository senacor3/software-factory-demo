# Rubric Review — architecture-light-factory.md

Reviewed against: good-spine checklist (divergence coverage, AD enforceability, Deferred safety, tech currency, spec-capability coverage, dimension ownership). Spec companion: `spec-light-factory.md` (CAP-1..CAP-9). Focus: AD-12 (PR-at-branch-creation) and AD-13 (clarification cap), their consistency with AD-2/AD-4/AD-8/AD-10/AD-11 and the two updated Mermaid diagrams.

## Verdict

Mostly solid — AD-12 and AD-13 are well-integrated with the existing AD set and the diagrams are internally consistent — but AD-12's rule contains a factual error about GitHub's PR-creation API that makes it not literally executable as written, and two spec-driven constraints (checks never agent-delegated; Job 3 merge mechanics) lack an enforcing AD despite appearing only as diagram labels.

## Findings

### 1. [High] AD-12's rule is not executable as written — GitHub rejects PR creation with zero commit diff

AD-12 (lines 107–111) and the Structural Seed (`OpenPR` state, lines 181/186–187) both specify: create the isolated branch, then open the PR, *before any commits*. GitHub's PR-creation API (REST and the `gh` CLI) returns a hard error — "No commits between `<base>` and `<branch>`" — when head and base are identical, i.e. when the branch has zero divergent commits. This is a long-standing, still-open GitHub limitation (see `cli/cli#9112`, `cli/cli#2691`, `octokit.net#879`). A branch created and pushed with no new commits cannot have a PR opened against it.

This means Job 2 cannot literally do "create branch → open PR → first commit" in that order; there must be at least one commit (even a trivial placeholder/empty commit) between branch creation and PR creation. As written, the rule would make the "level below" (whoever implements Job 2) discover this only at execution time, and different implementers would likely patch around it differently (empty commit vs. stub-file commit vs. reordering to "first real commit, then PR") — reintroducing exactly the ambiguity AD-12 was added to close.

**Fix direction:** amend AD-12's Rule to require an initial placeholder commit (e.g., an empty commit, or a commit adding a minimal marker file) immediately after branch creation and before PR creation, so "before any [implementation] commits" is the actual invariant, not "before any commits" literally.

### 2. [Medium] CAP-5's "checks never agent-delegated" constraint has no enforcing AD

The spec's Constraints section is explicit: "Deterministic checks (build, test, lint, security) run as direct pipeline steps, **never delegated to an agent**" (spec line 59, also CAP-5 lines 33–35). This is a hard constraint, not a preference. In the architecture, it appears only as a diagram label — the Structural Seed's `Checks` state is annotated "direct pipeline steps: build/test/lint/security" (line 183) and sits outside the `LG2a`/`LG2b` LangGraph subflow — and as a comment in the repo-tree block (line 214). No AD's Rule actually fixes this.

AD-6 (lines 71–75) only says the orchestration graph is Python/LangGraph; it doesn't prohibit a future implementer from wiring build/test/lint/security as LangGraph tool-calling nodes delegated to an agent, which the diagram alone can't stop since diagrams aren't enforceable the way an AD's Rule is. This is exactly the class of real divergence point the spine exists to close (two teams could legitimately read the diagram as illustrative rather than binding). Recommend promoting this to its own AD (or folding into AD-6) with an explicit Rule.

### 3. [Medium] Job 3 (Merge) has no AD — mechanics left fully undefined

CAP-9's success criterion is "the branch can merge to the target branch." Job 3 appears in the Structural Seed only as an opaque state (`Job3_Merge`, lines 206–207) with no AD behind it. Undefined and left to the implementer: which actor performs the merge (an automated pipeline step vs. the human clicking "Merge" on the PR UI after approving `evidence-approval`), what merge strategy (squash/merge-commit/rebase), what token/permissions Job 3's job needs under AD-5's per-job scoping, and whether the source branch is deleted afterward. AD-5 does establish "no agent invocation ever holds merge/admin tools," which rules out an *agent* performing the merge, but doesn't say whether a *non-agent* pipeline step does it automatically or whether Job 3 is just a human-driven no-op. This is also exactly what the spec's own Open Questions flags and leaves unresolved ("resolution path for CAP-9... merge conflict against a moved target branch," spec line 92) — the architecture doesn't carry this forward as a Deferred item or Open Question either; it's simply silent. Recommend either a thin AD-14 pinning the merge mechanism, or explicitly listing it under Deferred/Open Questions so it's a visible gap rather than a silent one.

### 4. [Low–Medium] Operational/environmental envelope: non-gate failure and retry semantics are silent

AD-2's "reject is terminal, re-trigger as new run" pattern (and AD-13's analogous cap-out pattern) only covers *human-gate-driven* termination. Nothing in the spine addresses what happens when a job fails for an infrastructure/execution reason unrelated to a gate — a LangGraph node throwing an uncaught exception, a runner crash, a transient GitHub API failure. GitHub Actions' "re-run failed jobs" feature interacts non-trivially with AD-8's "slug computed once in the first job, threaded via `needs:` outputs" — whether a re-run preserves earlier jobs' outputs or forces the whole run (and slug derivation) to restart is unaddressed. Runner type (GitHub-hosted vs. self-hosted) is also never named, which matters given AD-5's security model (ephemeral vs. persistent execution environment for agent-written code). Given this is explicitly initiative-level and PoC-scoped, an explicit "out of scope for v1" Deferred entry would be sufficient — but right now this dimension isn't decided, deferred, or flagged as open; it's just absent.

### 5. [Low] AD-13 cites AD-4 for a case AD-4's own Rule doesn't cover

AD-4's Rule (lines 59–63) is scoped to "every stage **ending in a human gate**" and its Binds line names only the two gates. AD-13's cap-out path explicitly *skips* the gate (diagram: "run ends here, no GateA") yet still cites "(AD-4)" as the basis for posting the commit-comment summary (line 117). The commit-comment *mechanism* is clearly the same pattern, but AD-4's Rule as literally scoped doesn't license a non-gate-ending stage to use it. Minor precision gap — either loosen AD-4's Rule text to "every stage boundary that produces a summary" or stop citing AD-4 specifically for the cap-out path and treat it as an independent (but mechanically identical) convention.

### 6. [Nitpick] Stack table's Python currency claim has a same-day timing wrinkle

Verified via web search: Python 3.13's bugfix-support window ends 2026-10-01 (today, per devguide.python.org), and Python 3.14 remains well-supported (EOL 2030-10-31) — so "target 3.14 for new work" is sound advice independent of exact dates. However, Python 3.15.0's first stable release is also scheduled for 2026-10-01 — the same day this document is dated — so the claim "3.14 is current stable" may already be superseded by the time this is read. Not a real problem (3.14 remains a fine, well-supported choice either way), but worth a quick "revisit this line" note since it was written right at the version's expiry point.

## Checklist walk-through

- **Divergence points fixed for the level below:** mostly yes; gaps are #2 (checks-as-agent) and #3 (Job 3 merge mechanics) — both real divergence risks currently resolved only by diagram convention, not by an enforceable Rule.
- **Every AD's Rule enforceable and prevents its stated divergence:** AD-1 through AD-11, AD-13 all check out. AD-12 fails this test concretely (#1) — its Rule describes a sequence GitHub's API won't allow.
- **Nothing under Deferred could let two units diverge:** confirmed clean — all eight Deferred items are unambiguous "not in v1" scope cuts tied to a brief/AD citation, none leaves an active decision unmade.
- **Named tech verified-current:** LangGraph (Python) 1.2.12 confirmed as latest (PyPI, released 2026-09-21). Claude Code CLI `@anthropic-ai/claude-code` latest is 2.1.286; Node ≥22 requirement since v2.1.198 confirmed accurate. AD-9's claim that `/install-github-app`'s token expires in hours-to-a-day with no auto-refresh vs. `claude setup-token`'s long-lived (~1 year) token is confirmed accurate (matches `anthropics/claude-code#11016` and current Claude Code docs) — AD-9 is well-grounded. GitHub Environment required-reviewers' 30-day native wait (AD-2) confirmed accurate per GitHub's own docs. Only wrinkle: #6 above (Python 3.14/3.15 timing).
- **Spec capability coverage (CAP-1..CAP-9):** CAP-1 (intake) is the one capability with no explicit AD — it's reasonably left to the analysis skill's prompt content rather than an architectural decision, so not flagging it as a defect, but note it's also not mentioned in Deferred/Open Questions despite the spec itself flagging "what defines complete/in-scope" as an open question (spec line 87). CAP-2 through CAP-4, CAP-6 through CAP-8 are each covered by a clear AD. CAP-5 and CAP-9 have the gaps in findings #2 and #3.
- **Dimension ownership (operational/environmental envelope):** deployment-of-the-product-itself is covered (AD-1, template-copy model); infra/provider choice is covered (AD-7, AD-9, GitHub Actions in Stack). Operations — failure/retry semantics distinct from gate-reject, and runner type — is silent (finding #4).
- **AD-12/AD-13 internal consistency with AD-2, AD-4, AD-8, AD-10, AD-11 and the two updated diagrams:** strong overall. AD-13 correctly reuses AD-10's pre-existing `awaiting-clarification` enum value (no new status invented), correctly mirrors AD-11's counter-ownership pattern (graph-only increment), and correctly follows AD-2's reject-is-terminal/re-trigger convention for its cap-out path. The stateDiagram-v2 changes (OpenPR state in Job 2; clarification-cap exit path in Job 1) match both ADs' prose exactly. The two issues found are #1 (AD-12 vs. GitHub's actual API behavior) and #5 (AD-13's citation of AD-4 for a case AD-4's Binds line doesn't name).

## Sources consulted (live verification)

- LangGraph PyPI page (version/date) — https://pypi.org/project/langgraph/
- Python 3.13/3.14/3.15 release and support schedule — devguide.python.org, endoflife.ai
- `@anthropic-ai/claude-code` npm package version and Node 22 requirement
- GitHub Actions environment protection rules / required-reviewers 30-day timeout — GitHub Docs
- GitHub PR-creation "No commits between" limitation — `cli/cli#9112`, `cli/cli#2691`, `octokit.net#879`
- `claude setup-token` vs. `/install-github-app` token lifetime — `anthropics/claude-code#11016`, Claude Code docs
