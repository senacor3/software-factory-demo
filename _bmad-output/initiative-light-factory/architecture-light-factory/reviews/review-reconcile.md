# Reconciliation review: architecture-light-factory.md vs. brainstorm-quality-gate-alternatives.md

Scope: does the spine (as updated 2026-11-03) accurately and completely reflect the intent doc that drove the update, with no quiet drops/weakenings outside of explicit, deliberate architecture decisions made during the spine's own update session?

Method: read both files in full, plus the spine's `.memlog.md` (the session's own decision log) to distinguish "deliberately refined during this session" from "quietly dropped/changed."

## Overall verdict

Lands cleanly on every structural/functional item the task asked to verify. One genuine quiet drop found: an editorial "why" (Gate 1 judged more critical than Gate 2) that the memlog explicitly captured as adopted from brainstorming, but that never made it into the spine's AD-2 text or anywhere else in the document. Everything else — the Must-haves, the command grammar, the correlation key, idempotency, Gate 2, conflict resolution, DynamoDB, the explicit rejections, and the cost rationale — is present and either correctly carried over or correctly (and traceably) refined.

## Item-by-item

### Must-have: custom orchestrator outside GitHub Actions (Lambda + Lambda Function URL)
**Present, intact.** Design Paradigm section, AD-17, AD-7 (widened dependency list), Stack table. Lambda owns pipeline state/transitions; GitHub Actions demoted to step-runner — matches intent doc exactly.

### Must-have: custom UI dashboard, day one, action semantics
**Present, and correctly reflects the session's own deliberate refinement — not a regression.**
- Intent doc's stated Must-have: UI actions call the GitHub API directly to post a PR comment on the human's behalf ("rather than driving the orchestrator directly").
- During the spine's own update session, this was explicitly refined (memlog line 72: "GitHub-credential boundary clarification (forced by the GitHub-App decision)") because the UI can never hold a GitHub credential once a GitHub App installation token is the orchestrator's auth mechanism (AD-18).
- The spine consistently reflects the REFINED version everywhere it discusses this: AD-18 ("the orchestrator's Lambda is the only thing that ever calls the GitHub API, including to post a PR comment on the developer's behalf from a UI action"), AD-21 ("Its approve/rework/reject actions call the orchestrator's Lambda Function URL, which posts the real PR comment... the SPA never calls the GitHub API directly and never holds a GitHub credential"), Design Paradigm's namespace mapping ("PR-comment actions posted via the orchestrator on the developer's behalf"), and the Structural Seed file tree comment for `ui/src/`.
- No stale "UI posts directly to GitHub" wording was found anywhere in the spine. This is the correct outcome per the task's own instruction — a deliberate, session-documented refinement, not something to flag as a problem.
- "Must-have from day one / not deferred": the UI is not listed in Deferred, and AD-21/the Structural Seed treat it as a fully specified, present-tense component — consistent with "not deferred."
- The "shows per-story pipeline state (analysis/implementation/review/etc.)" framing survives in the Structural Seed file-tree comment: "React SPA: per-story pipeline-state dashboard" (line ~359).
- The "UI is a front end onto that thread, not a parallel state channel" framing survives verbatim in intent (AD-21: "the UI is a front end onto that thread, never a parallel one").

### Gate 1 PR-comment command grammar (/approve, /rework <feedback>, /reject)
**Present, correctly described.** AD-2: `/approve` → `workflow_dispatch` of implementation→checks→review; `/rework (feedback text)` → re-invoke analysis with comment text as new input; `/reject` → cancels the story, closes the PR directly (explicitly superseding AD-16's old trailing reject-cleanup job). Also carried into the Structural Seed state diagram (GateA transitions). Matches intent doc's grammar and semantics exactly, with the mechanism updated to name the concrete `workflow_dispatch` target (a correct elaboration, not a change in meaning).

### Unique branch name as correlation key
**Present.** AD-20 ("the unique branch name AD-12 already creates... doubles as the correlation key"), AD-12's own note, Consistency Conventions table, Structural Seed note block. Matches intent doc's stated reason (`workflow_dispatch` returns no run ID).

### Idempotent state-check-on-entry
**Present.** AD-20: "Every Lambda invocation checks the actual current state (the PR's state and/or its DynamoDB control-plane row)... before acting, rather than trusting the triggering event alone." The intent doc's exact rationale — "makes duplicate/double invocations safe without needing to be prevented outright" — is preserved near-verbatim.

### Gate 2 via native branch-protection PR approval
**Present.** AD-2: "`evidence-approval` is a plain native GitHub branch-protection 'require PR approval' rule (no Environment)." Also in Structural Seed (GateB) and Capability map (CAP-8). Matches intent doc.

Minor, not requested but worth noting: the intent doc's rationale for Gate 2 ("free on any plan, no custom infra needed") is in the memlog (line 74) but doesn't appear in the spine's AD-2 prose the way the Lambda Function URL cost rationale does in AD-17. Since the task's explicit soft-check was only about the Lambda Function URL vs. API Gateway rationale, this is flagged only as a secondary observation, not a gap against the stated checklist.

### Agent-driven merge-conflict resolution + DynamoDB checkpoint state
**Both present.** AD-19 covers the bounded (cap-2) agent-driven conflict-resolution loop, branch-scoped only, same permission shape as the implementation agent (AD-5), surfacing to a human on cap-out — matches intent doc's Should-have exactly, including the "replacing a human in that step" intent (captured via AD-19's "Prevents" clause). DynamoDB control-plane state is covered by AD-17, the AD-10 addendum, and AD-20 — explicitly scoped to control-plane bookkeeping only, never a second copy of content state, matching the intent doc's stated reason ("since the Lambda is stateless between invocations").

### Explicit rejections — checked for quiet reintroduction
- **GitHub's required-reviewers environment-protection feature itself**: correctly treated as rejected/superseded throughout — AD-2's "Superseded 2026-11-03" note states the Enterprise/public-repo restriction as the reason it was never usable here (preserves the intent doc's problem statement almost verbatim), the Stack table marks GitHub Actions "no longer Environments-based," and the Consistency Conventions table states "Neither is backed by a literal GitHub Environment resource any more." No AD, Deferred entry, or diagram node reintroduces it as live behavior.
- **A separate plan-only PR for Gate 1**: correctly not reintroduced. AD-12 is explicit that "This PR is the single artifact for the rest of the run" — plan/decisions updates, both gate summaries, checks, review findings, and fix-loop commits all land on the one PR. The three-way workflow split (analysis.yml / implementation-checks-review.yml / merge.yml) is a GitHub Actions file split, not a second PR — confirmed by AD-12/AD-15/the Structural Seed, which all describe one PR per run.
- **"Nature's Solutions" biomimetic framing**: absent from the spine, as expected and as the task instructs (never meant to land in an architecture doc) — not a gap.

### Lambda Function URL over API Gateway — cost rationale
**Preserved, not just a bare fact.** AD-17's Rule states it explicitly: "fronted by a Lambda Function URL (not API Gateway) as its HTTPS entry point — chosen for run cost: no separate service, no per-request charge beyond the Lambda invocation itself." This reads as a deliberate, reasoned choice to a future reader, not an arbitrary one. The same rationale also appears in the intent doc's own Must-have bullet almost word-for-word, confirming direct lineage.

## Gap found: "Gate 1 judged the more critical of the two gates" — dropped editorial framing

The intent doc states, as part of its Gate 1 Must-have bullet: "**Gate 1 (plan review before implementation)** — judged the more critical of the two gates — implemented as..."

The spine's own memlog (`.memlog.md` line 73) shows this framing was explicitly carried into the update session as an adopted decision: "[ADOPTED from brainstorming, supersedes AD-2's plan-approval half] Gate 1 (plan review before implementation, **judged more critical than Gate 2**) drops the plan-approval GitHub Environment entirely..."

However, this framing does not appear anywhere in the final spine document (`architecture-light-factory.md`) — not in AD-2's Rule, not in AD-2's "Prevents" clause, not in the Design Paradigm narrative, not in the Structural Seed diagram's Gate 1 node label, and not in the Consistency Conventions table. A `grep -i "critical"` across the spine returns nothing.

This is exactly the kind of quiet drop the task asked to watch for: a tone/"why" that is easy for an AD-structured document to lose when prose gets compressed into Binds/Prevents/Rule fields. It's soft in the sense that no functional requirement is attached to it in the intent doc (there's no stated behavioral consequence of Gate 1 being "more critical" — e.g., no asymmetric rigor, no extra reviewer requirement) — but it was captured as a deliberate "adopted from brainstorming" decision in the memlog and then silently didn't make it to the spine text itself. A future reader of the spine alone has no way to know the two gates were ever judged unequal in importance, which was explicitly part of the brainstorming intent.

**Recommendation**: add a short clause to AD-2's Rule or its Design Paradigm cross-reference noting that Gate 1 was judged the more critical of the two gates (hence receiving the richer command-grammar treatment), or drop a one-line note under AD-2 similar to the "Superseded 2026-11-03" note already there. Low severity — doesn't change any Rule's behavior, purely a lost editorial signal.

## Summary table

| Checklist item | Status |
| --- | --- |
| Custom orchestrator (Lambda + Function URL) | Present, intact |
| Custom UI dashboard, day-one, refined posting-via-orchestrator semantics | Present, correctly reflects deliberate in-session refinement |
| Gate 1 PR-comment grammar (/approve, /rework, /reject) | Present, correct |
| Unique branch name as correlation key | Present |
| Idempotent state-check-on-entry | Present, rationale preserved |
| Gate 2 via native branch-protection PR approval | Present |
| Agent-driven merge-conflict resolution | Present |
| DynamoDB checkpoint state | Present, scope correctly limited to control-plane |
| Rejection: required-reviewers Environment feature | Correctly rejected, not reintroduced |
| Rejection: separate plan-only PR for Gate 1 | Correctly rejected, not reintroduced |
| Rejection: "Nature's Solutions" framing | Correctly absent (expected) |
| Lambda Function URL run-cost rationale | Preserved as a reasoned "why," not a bare fact |
| "Gate 1 judged more critical" editorial framing | **Dropped** — adopted in memlog, absent from spine text |
