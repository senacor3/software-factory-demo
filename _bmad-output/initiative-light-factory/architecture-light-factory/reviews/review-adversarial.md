# Adversarial Divergence Review — architecture-light-factory.md (AD-12/AD-13 pass)

**Lens:** construct two independent, spec-compliant units one level down that each obey every AD to the letter yet build incompatibly. Scope: AD-12 (PR opened at Job 2 branch creation) and AD-13 (clarification loop capped at 2 rounds), their interaction with the unchanged AD-1..AD-11, and internal consistency of the updated Structural Seed `stateDiagram-v2`. AD-1..AD-11 themselves are out of scope except where AD-12/AD-13 newly stress them; see `review-adversarial.md`'s prior pass (git history / project memory) for the AD-1..AD-11-only findings, not restated here.

**Verdict:** AD-12 and AD-13 close the two gaps they were written for (PR-existence timing, unbounded clarification spend) but each opens a new, narrower gap of the same shape as the ones already fixed elsewhere in the spine: AD-12 hands the implementation agent a brand-new write capability (branch/PR creation) that AD-5's least-privilege enumeration never names, and leaves PR lifecycle across the reject-and-re-trigger path (AD-2) completely unspecified; AD-13 claims parity with AD-11's bounded-loop pattern (the Consistency Conventions table says so explicitly) but its trigger wording and persistence requirements are measurably looser than AD-11's, so two to-the-letter-compliant implementations of the two loops would behave asymmetrically despite the claimed symmetry.

---

## Divergent pairs constructed

### Pair 1 — PR lifecycle across the reject/re-trigger path is unspecified (HIGH)

**Binds:** AD-12, AD-2.

AD-12's Rule describes exactly one PR, created unconditionally as "the implementation agent's first action in Job 2." AD-2 separately establishes that a reviewer **reject** at either gate is terminal for that run, and the human "re-triggers the pipeline's first job as a new run." Nothing in AD-12 says what happens to the PR from a rejected run when a new run starts, or whether the new run's Job 2 is allowed to find and resume a prior run's PR instead of opening a fresh one.

- **Unit A — literal AD-12 reading:** every Job 2 execution, including Job 2 of a re-triggered run after an `evidence-approval` reject, performs "open the PR" as its unconditional first action with no existence check. Each reject-and-retry cycle for the same story leaves the previous run's PR open and orphaned (never closed, AD-12 gives no closing instruction) and creates a new one — a story that gets rejected twice now has three open PRs, one of which Job 3 must correctly ignore.
- **Unit B — idempotent/reuse reading:** also AD-12-compliant (AD-12 never forbids reuse, it only describes the sequence for a fresh instantiation) — the implementation agent checks whether a PR already exists for this story-slug's branch before creating one, reusing/reopening it if so, to avoid PR accumulation.

Both satisfy AD-12's text. They produce incompatible repo states: N open PRs per story vs. exactly one. This matters operationally — AD-12 itself calls the PR "the single artifact for the rest of the run," but "the run" is scoped to one attempt, while AD-2's re-trigger pattern is the spine's own designed mechanism for a story to span multiple runs. Job 3 (`Job3_Merge`) has no documented way to know which of several open PRs is current if Unit A's behavior is what ships.

**Close with:** state explicitly in AD-12 (or a cross-reference to AD-2) whether a re-triggered run's Job 2 must reuse an existing open PR/branch for the same story-slug or close out the prior one before opening a new one, and who/what is responsible for that cleanup.

---

### Pair 2 — Branch/PR-creation is a new permission surface AD-5 never enumerates (HIGH)

**Binds:** AD-12, AD-5.

AD-5's two-layer least-privilege model names exactly two kinds of agent capability: a Claude Code tool-allowlist for *edits*, scoped to the isolated branch and specific state-file paths, and GitHub token/branch-protection scoping. It never mentions branch creation or PR creation as a capability any agent holds. AD-12 now requires *something* to create a branch and open a PR as literally the first action of Job 2 — a git/GitHub-API write operation categorically different from editing a file inside an already-existing branch.

- **Unit A:** reads AD-12's "the implementation agent's first action" loosely — a deterministic Actions workflow step (not an LLM tool call) creates the branch and opens the PR via `gh pr create` before the LangGraph implementation agent is ever invoked. The agent's tool-allowlist stays exactly as AD-5 describes it: edit tools scoped to files, no git-push or PR-create capability granted to the model at all.
- **Unit B:** reads AD-12 literally — "the implementation agent's first action" means the LLM agent itself issues the branch-creation and `gh pr create` calls via a Bash/git tool in its allowlist, since AD-12 names the *agent*, not a pipeline script, as the actor. This requires granting the agent push and PR-creation capability, which is strictly broader than anything AD-5 scopes or excludes.

Both are faithful readings of AD-12's actor ("the implementation agent"). They produce materially different attack surfaces: in Unit A the LLM never holds git-push/PR-create tools; in Unit B it does, and AD-5's "defense-in-depth, neither sufficient alone" framing was written without this capability in view, so there's no stated restriction on it (e.g., nothing says the agent's PR-create capability is limited to one call, to the target branch only, or can't be reused mid-run to open additional PRs).

**Close with:** state explicitly whether branch/PR creation in AD-12 is performed by a deterministic workflow/script step or by the LLM agent's own tool call, and if the latter, extend AD-5 to scope that capability (one-shot, target-branch-only, no re-use) the same way it scopes edit tools.

---

### Pair 3 — AD-13's cap-trigger wording is looser than AD-11's, despite claimed parity (MEDIUM)

**Binds:** AD-13, AD-11, Consistency Conventions ("State & cross-cutting (bounded loops)" row).

The Consistency Conventions table asserts: "Both agent loops are hard-capped and counted the same way." But the two ADs don't actually use the same trigger phrasing:

- AD-11: "hard cap of 2 fix cycles: **on the second unresolved review**, it must not loop again." This pins the exact event (the 2nd cycle completing unresolved) that halts the loop — unambiguous, allows exactly 2 cycles, never a 3rd.
- AD-13: "hard-capped at 2 rounds... **on exceeding the cap**, the graph halts intake." "Exceeding 2" is satisfied only once the count reaches 3 — a literal reading permits a 3rd round to be *attempted* before the halt fires, since round 2 alone (count = 2) does not yet "exceed" a cap of 2.

- **Unit A** implements AD-13 by analogy to AD-11's precise pattern: halts after the 2nd round is still unresolved, never starts a 3rd round. Matches the diagram's "cap 2 rounds" annotation and AD-11's sibling behavior.
- **Unit B** implements AD-13's literal text: increments the counter, and only halts once the counter's value *exceeds* 2 — i.e., after a 3rd round is reached. Equally defensible from AD-13's wording alone, and nothing in AD-13 cross-references AD-11's "on the second X" phrasing to disambiguate.

Both claim compliance with "counted the same way." One spends one full extra agent-turn round-trip (a real-human-wait round, not a cheap retry) before halting — directly undermining AD-13's own stated purpose ("Prevents: an unbounded pre-approval loop burning agent turns waiting on a slow or unavailable human").

**Close with:** reword AD-13's halt condition to mirror AD-11's exactly — e.g., "on the second unresolved clarification round, the graph must not loop again" — removing "exceeding the cap" as the trigger phrase.

---

### Pair 4 — Clarification-round counter has no mandated persisted field, unlike the fix-cycle counter (MEDIUM)

**Binds:** AD-13, AD-11, AD-10.

AD-11 is explicit about where its counter lives durably: "`review.md`'s frontmatter tracks a fix-cycle counter." AD-10's shared-frontmatter-field list and status enum are written with this in mind. AD-13 describes the *ownership* of its counter in the same terms ("the round counter lives in the orchestration graph's own loop-control node, never incremented by the analysis agent itself") but never states that the count is written into `plan.md`/`decisions.md` frontmatter at all — it only specifies what gets written *at cap-out* (`status: awaiting-clarification`), not per-round.

- **Unit A:** persists a `clarification_round` field in `plan.md`/`decisions.md` frontmatter after every round, symmetric with AD-11's `review.md` counter — durable, auditable, survives a job crash mid-loop.
- **Unit B:** keeps the round counter purely as in-process LangGraph graph state (a field in the graph's internal state schema), exactly as AD-13's literal text permits — since Job 1's graph "lives and dies within that job's own runner process" (Design Paradigm) and AD-13 never requires writing it to disk. `plan.md`'s frontmatter never records how many rounds occurred, in the resolved case or the cap-out case; the only place that information surfaces is the (non-git, non-durable) PostSummaryCapA comment at the moment of cap-out, and nowhere in the resolved-case path.

Both are AD-13-compliant. The asymmetry breaks the parity the Consistency Conventions table claims, and more concretely: a `resolved` `plan.md` in Unit B carries no audit trail of whether it took 0, 1, or 2 clarification rounds to reach `ready-for-review` — a strictly weaker record than `review.md` ever has for the fix loop, for no stated reason.

**Close with:** either name a `clarification_round` frontmatter field in AD-13 (and register it as a shared field alongside AD-10's list, since AD-10 says "no stage invents its own naming for the same concept"), or state explicitly that the clarification loop's counter is intentionally ephemeral/in-memory-only and that this is an accepted asymmetry with AD-11, not an oversight.

---

### Pair 5 — AD-12 doesn't pin the branch name to AD-8's propagated slug (LOW/MEDIUM)

**Binds:** AD-12, AD-8.

AD-8 requires the story-slug be "derived exactly once, in the workflow's first job," exposed as a job output, and consumed (never re-derived) by every downstream job — but its Rule only binds this explicitly to the `.light-factory/<story-slug>/` state directory. AD-12 introduces a second artifact that plausibly needs the same identifier — the isolated branch name — but never cross-references AD-8's propagation requirement for it.

- **Unit A:** names the branch from `needs.<job1>.outputs.story-slug` (the same propagated value AD-8 mandates for the state directory), so branch name and state directory always agree.
- **Unit B:** equally AD-12-compliant — the Job 2 implementation agent derives the branch name by re-slugifying the triggering story file's name itself (AD-12 never says the branch name must come from the AD-8 output), which can diverge from the propagated slug on any edge case where two slugification implementations disagree (unicode, length truncation, punctuation).

If Unit B ships, the PR's branch name and the `.light-factory/<story-slug>/` directory it's meant to report on can silently drift apart — the same class of hole the prior adversarial pass already flagged for the state directory (slug computation/propagation), now reopened by AD-12 in a second place AD-8 doesn't cover.

**Close with:** add one clause to AD-12 (or AD-8): the branch name is derived from the same AD-8-propagated `story-slug` job output, not independently recomputed.

---

## Diagram-internal-consistency check

The updated `stateDiagram-v2` is internally consistent with the AD text on the points it labels explicitly (status values used — `ready-for-review`, `awaiting-clarification`, `unresolved-after-cap` — all match AD-10's enum; "no PR yet" / "commit comment" vs. "PR comment" placement matches AD-12's temporal split; `FixLoop --> Checks: re-run affected checks` matches AD-11's "only the checks relevant to the finding(s)"). Two softer issues:

- The three terminal-state labels (`RunEndsA`, `RunEndsB`, `RunEndsClarify`) use inconsistent phrasing for the same re-trigger action — "re-triggers Job 1 as a NEW run," "re-triggers pipeline as a NEW run," "re-triggers Job 1 as a NEW run" — cosmetic, but a diagram meant to be the canonical structural reference for three near-identical terminal paths should use one wording so a reader doesn't go looking for a meaningful difference between "Job 1" and "pipeline" as re-trigger targets.
- `Job1_Analysis`'s two internal exits (`PostSummary1`, `PostSummaryCapA`) both flow to the same internal `[*]`, with the branch to `GateA` vs. `RunEndsClarify` expressed only via edge labels on the two *external* transitions out of the composite state. This is standard Mermaid shorthand and not a defect, but it means the diagram's graph structure alone (stripped of prose labels) cannot distinguish the two exits — worth a one-line note if the diagram is ever used as a codegen source rather than documentation.

---

## Severity-ranked summary

1. **HIGH** — Pair 1: PR lifecycle across AD-2's reject/re-trigger path is unspecified; literal AD-12 compliance accumulates orphaned PRs per story.
2. **HIGH** — Pair 2: AD-12's branch/PR-creation actor is ambiguous (script vs. agent tool call), and AD-5's least-privilege model never scopes this capability either way.
3. **MEDIUM** — Pair 3: AD-13's "on exceeding the cap" is an off-by-one looser trigger than AD-11's "on the second unresolved review," contradicting the Consistency Conventions table's claimed parity.
4. **MEDIUM** — Pair 4: AD-13 never mandates a persisted round-counter field (unlike AD-11's explicit `review.md` counter), leaving the clarification loop's audit trail strictly weaker with no stated justification.
5. **LOW/MEDIUM** — Pair 5: AD-12 doesn't tie the new branch name to AD-8's propagated story-slug output, reopening the slug-propagation gap in a second location.
