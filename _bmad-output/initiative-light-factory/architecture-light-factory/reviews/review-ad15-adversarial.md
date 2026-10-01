# Adversarial Review — AD-15 (Run-level isolation on re-trigger)

**Method:** constructed pairs of implementers who each follow an AD's text to the letter but make a different, individually-defensible choice on something the text leaves open, then checked whether their outputs still compose.

## Verdict

AD-15 closes the *naming* collision (branch/PR/state-dir keyed only by story-slug) but does not close the *concurrency* collision it implicitly assumes exists — it never says whether two runs for the same story can be in flight at once, and the one shared, cross-run artifact it introduces (`CURRENT_RUN`) has no defined git location, so two compliant implementations of "the same script writes/overwrites CURRENT_RUN" produce incompatible storage shapes. Four concrete findings below, roughly in order of severity.

---

## Finding 1 (high) — `CURRENT_RUN`'s git location is undefined; two compliant implementations can't talk to each other

AD-15's rule text: *"`.light-factory/<story-slug>/CURRENT_RUN` is written/overwritten by the same script with the current `run-id`."* "The same script" = AD-12's `open_implementation_pr.py`. Neither AD-8, AD-10, AD-12, nor AD-15 ever states which git ref/branch the `.light-factory/<story-slug>/` *parent* directory (the one above `<run-id>/`, shared across every run of that story) is committed to.

- **Unit A ("branch-local" reading):** AD-12 calls the branch "isolated" and AD-5 scopes edit tools "both to its isolated branch (git-ref boundary) and to the state-file paths." Unit A's implementer reasonably concludes all `.light-factory/` writes — `CURRENT_RUN` included — land on the *current run's own branch*, freshly forked from the target branch. To the letter, this satisfies AD-15: the script writes `CURRENT_RUN`, on the branch it already has write access to.
- **Unit B ("shared-state" reading):** AD-15's own supersession logic requires the *new* run's script to find and close *prior* runs' PRs and to overwrite a pointer that must already exist before this run started. That's only possible if `.light-factory/<story-slug>/` lives somewhere every run can see *before* branching — i.e. on `main` or a dedicated persistent ref, not on any one run's isolated branch. Unit B's implementer pushes `CURRENT_RUN` (and the story-level directory) to such a shared location. This also satisfies AD-15's text — it never forbids it.

**Collision:** Unit A's `CURRENT_RUN` is branch-local and fragments — every run has its own copy, none authoritative, and a fresh run's branch (forked from `main`) never even contains the prior run's pointer to overwrite, since it was never merged. Unit B's `CURRENT_RUN` is a single global file, but writing it requires either a direct push to `main` (which AD-5's second enforcement layer explicitly blocks: *"branch protection blocks direct push to main"*) or a new persistent branch/ref that no AD names, with an unspecified token-permission scope (AD-5's "each job's token permissions match only that stage's needs" has nothing to match against, since this ref isn't tied to any stage). Both units are individually AD-compliant; composed, there is no single answer to "where does Job 3 or a human actually look to resolve which run is current" — which is the exact problem AD-15 claims to solve.

**Close with:** an AD (or a tightened AD-15) naming the concrete git location of the per-story shared directory/pointer — e.g. "committed directly to `main` by a dedicated, narrowly-scoped bot token used only by this one script, as the sole exception to AD-5's no-direct-push rule" — or drop the shared-pointer design in favor of something that doesn't require a write location outside any run's own branch (e.g., resolving "current run" purely via the GitHub PR API's open/closed state, which needs no file at all).

## Finding 2 (high) — no concurrency guard, so a superseded run can still be waiting at a gate when its PR is closed out from under it ("zombie run")

No AD — not AD-2, not AD-15, not the workflow sketch — states whether GitHub Actions is configured to prevent two runs of the same story from being in flight simultaneously (a `concurrency:` group keyed by story-slug is the standard mechanism; it's absent from every AD and from the `.github/workflows/light-factory.yml` sketch in Structural Seed). AD-15's own existence (solving branch/PR/state-dir collisions on re-trigger) implies concurrent runs are expected to happen, yet nothing stops a human from re-triggering Job 1 for a story while an earlier run for that same story is still *paused at `evidence-approval`*, not rejected — AD-2's "reject is terminal" only covers an explicit reject, never an in-flight pause.

- **Unit A (Job 3 implementer):** follows AD-14 literally — *"Job 3 executes the merge ... triggered automatically on evidence-approval's approval."* No AD requires Job 3 to re-check that its PR is still open before merging, so Unit A's merge step trusts the gate approval unconditionally.
- **Unit B (AD-12/AD-15 script implementer):** follows AD-15 literally — on a new run, close every other open PR for the story-slug prefix, unconditionally, regardless of whether that PR's run is sitting at a human gate mid-review.

**Collision:** Run A is paused at `evidence-approval` (gate open, up to 30 days per AD-2). Someone re-triggers the story as Run B (nothing forbids this). Run B's script (Unit B) closes Run A's PR with "superseded by #N." Run A's GitHub Environment deployment review is untouched by the PR closing — a reviewer can still click Approve on Run A's stale review page. That resumes Run A's workflow into Job 3 (Unit A), which attempts to merge a PR that is now closed. Nothing in AD-14, AD-2, or AD-15 says what Job 3 does in that case (this isn't the already-deferred "non-gate failure/retry semantics" — it's a designed, reachable consequence of AD-15 interacting with AD-2/AD-14, not a transient infra fault).

**Close with:** either (a) an explicit `concurrency:` group in the workflow (name it in AD-15 or a new AD) that cancels/blocks a new trigger while a prior run for the same story is still active past Job 1, closing the hole at the source, or (b) if concurrent in-flight runs are intentionally allowed, a Rule making Job 3 check `CURRENT_RUN` (or the PR's open/closed state) before merging and abort cleanly if it's been superseded.

## Finding 3 (medium) — `CURRENT_RUN` is silently never written (and stays stale) for any story whose latest run caps out in clarification (AD-13)

AD-15 ties the `CURRENT_RUN` write to "the same script" as AD-12's PR-opening step. AD-13's clarification-cap path *never reaches Job 2*, so AD-12's script never runs, so `CURRENT_RUN` is never written for that run — even though that run produced a real, legitimate state directory (`decisions.md` with `status: awaiting-clarification`) that a human or Job 3 might need to find. Two sub-cases:

- If this is the story's *first-ever* run and it caps out, `CURRENT_RUN` never exists at all — a reader following AD-15's advice ("without listing and sorting `run-id` directories") has nothing to read and must fall back to exactly the directory-listing AD-15 says it's avoiding.
- If a later run caps out in clarification after an earlier run reached Job 2, `CURRENT_RUN` is left pointing at the *older* run, even though the newer (clarification-capped) run is the one with the current unanswered question. A human landing on `CURRENT_RUN`'s target would see an outdated plan, not the live blocker.

This is distinct from the review's question 4 framing (does the *supersession search* need a special case for AD-13's cap-out) — the search itself is fine, since a cap-out run never opened a PR, so there's nothing to find-and-close and no special case is needed there. The actual gap is `CURRENT_RUN` going stale/missing, which is a real regression against AD-15's own stated purpose for exactly the stories that hit AD-13's cap.

**Close with:** make `CURRENT_RUN`-writing a Job 1 responsibility that fires on *every* run completion (normal path and AD-13 cap-out alike), not something bolted only onto AD-12's Job 2 script.

## Finding 4 (medium) — the Structural Seed diagram actively hides Findings 1–3 behind clean terminal states

The `stateDiagram-v2` still shows `RunEndsClarify`, `RunEndsA`, and `RunEndsB` as simple dead-end states captioned "Human re-triggers Job 1 as a NEW run" — with no `run-id`, no `CURRENT_RUN`, no PR-supersession/closing, and (most importantly for Finding 2) no indication that a prior run might still be alive and waiting at a gate when the new one starts. A reader building Job 3 or the re-trigger path from this diagram alone — which is the document's intended "structural seed" for implementation — would never learn AD-15 exists, let alone that re-triggering can orphan an in-flight gate approval. This is exactly the gap that let Units A and B in Finding 2 diverge without either side knowing about the other's assumption.

**Close with:** update the diagram to show `run-id` threading, the supersession/close-PR edge on re-trigger, and ideally an explicit guard/state showing what happens to a prior run that's still paused at a gate when a new one starts (even if that guard is "not yet decided" — make the open question visible in the diagram, not just absent from it).

## Minor note — AD-4 / evidence-approval comment on a since-closed PR

Once Run A's PR is closed (Finding 2's scenario, or even a clean re-trigger after explicit reject), its `evidence-approval` PR-comment summary (AD-4) remains readable on the closed PR — GitHub doesn't delete comments on close — so this isn't data loss. The only real consequence is the Finding 2 failure mode (a reviewer still being able to approve a gate whose PR is gone); AD-4 itself doesn't need a tightening, it's AD-2/AD-14/AD-15's interaction that does.

---

**File:** `/Users/Andreas.Guenzel/dev/workspaces/light-factory/_bmad-output/initiative-light-factory/architecture-light-factory/reviews/review-ad15-adversarial.md`
