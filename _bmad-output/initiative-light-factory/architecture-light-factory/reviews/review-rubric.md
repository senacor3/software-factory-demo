# Rubric Review — architecture-light-factory.md (orchestrator/UI update, 2026-11-03)

Reviewed against: good-spine checklist (divergence coverage, AD enforceability, Deferred safety, tech
currency, brownfield-codebase ratification, spec-capability coverage, dimension ownership, internal
consistency). Scope: this review supersedes the prior `review-rubric.md` (which covered AD-12/AD-13 in
isolation). Focus here is the 2026-11-03 update that replaces the GitHub-Environment gate mechanism with
an external Lambda orchestrator, a React SPA, PR-comment approval (Gate 1), and native branch-protection
PR approval (Gate 2) — i.e. AD-17 through AD-22, and the amendments to AD-2, AD-4, AD-5, AD-7, AD-8, AD-10,
AD-11, AD-12, AD-13, AD-14, AD-15, AD-16.

## Verdict

The update is well-reasoned and mostly internally consistent, but it ships with two critical, independently
verified defects — pervasive stale "light-factory" naming that contradicts the already-renamed live
codebase, and a new agent invocation (AD-19) with no defined execution substrate — plus a high-severity
authentication gap on the UI's gate actions and a now-contradicted companion spec, so this spine is not yet
safe to build against as-is.

## Findings

### 1. [Critical] Spine still uses "light-factory" naming; the live codebase was renamed to "software-factory"

Commit `9ec75aa` ("Rename light-factory to software-factory") already renamed the project on disk. The
*current* workflow file is `.github/workflows/software-factory.yml`; its concurrency group is
`software-factory-${{ github.event.inputs.story_file }}`; `factory/scripts/open_implementation_pr.py`
hardcodes the branch prefix as `software-factory/{story_slug}/{run_id}` and the git-commit identity as
`software-factory-bot`; `factory/scripts/state_io.py` defines
`STORY_PROJECTS = ("software-factory", "freight-tenders")`; and the skill folders on disk are
`.claude/skills/software-factory-analysis/`, `-implementation/`, `-review/`.

The spine's text — written and touched again in this very update — still says the opposite throughout:
AD-8/AD-15 define `<project>` as "`light-factory` or `freight-tenders`"; AD-12/AD-15/Consistency Conventions
give the branch pattern as `light-factory/<story-slug>/<run-id>`; the Namespace mapping and Structural Seed
source tree name the skills `light-factory-analysis/-implementation/-review/`; AD-15's memlog-era
concurrency group is `light-factory-<story-slug>`.

This is not cosmetic: AD-15's PR-supersession search is defined as "search by branch-name prefix
`light-factory/<story-slug>/`" — if an implementer builds the new orchestrator's correlation-key logic
(AD-20) or re-implements `open_implementation_pr.py`'s search off the spine's literal string, it will not
match the already-live `software-factory/...` branches, silently breaking supersession-closing and the
correlation key the whole Gate-1/Gate-2 webhook-matching design (AD-20) depends on. This is exactly the
"two independently built units diverge incompatibly" failure the checklist asks to catch, and it's fully
verifiable on disk today, not speculative.

**Fix direction:** global find/replace `light-factory` → `software-factory` across the spine's prose, ADs,
Consistency Conventions, Structural Seed (both diagrams and the source tree), everywhere it denotes the
on-disk branch prefix, concurrency group, or skill folder names — distinct from the *initiative* name
`light-factory`, which can stay as the doc's own identity if that's intentional.

### 2. [Critical] AD-19's new conflict-resolution agent has no defined execution substrate

AD-19 introduces a new Claude-Code agent invocation ("an agent is invoked scoped ONLY to the feature
branch... to reconcile the conflicts and push a clean branch") but never says *where* it runs. The
Structural Seed's source-tree comment for `merge.yml` states it is "workflow_dispatch'd by the orchestrator
**after** the conflict-resolution loop" — i.e. the loop runs *before* `merge.yml` is even dispatched. The
`stateDiagram-v2` confirms this: `ConflictCheck` is drawn as a bare state between `GateB` and
`MergeWorkflow`, never nested inside any of the three named workflow-file composite states the way
`ImplJob`/`ChecksJobS`/`ReviewJobS` are nested inside `implementation-checks-review.yml`.

But the Design Paradigm, AD-1's Binds, the Namespace mapping, and the Consistency Conventions all assert
exactly "three separate workflow files" (analysis / implementation→checks→review / merge) with no fourth
ever named anywhere. So where does this agent actually execute?
- If it's meant to be a step inside `merge.yml` itself, the source-tree comment and diagram both say
  otherwise ("after the conflict-resolution loop" / drawn outside the box).
- If it's meant to be a 4th dispatched workflow, it is never named in the source tree, the Namespace
  mapping, or anywhere the "three workflow files" invariant is stated — a real omission, not a stylistic one.
- If it's meant to run *inside the Lambda itself*, that contradicts every other agent-invocation AD in this
  spine (AD-5, AD-9), which assume a GitHub-Actions-job-hosted Claude Code CLI with a scoped per-job GitHub
  token — a model the stateless Lambda (no Claude Code CLI, no git tooling, a much shorter execution-time
  ceiling, AD-9's OAuth-token wiring never extended to it) cannot satisfy as described.

Two implementers would plausibly land on two different, incompatible answers here — this is a genuine
divergence point the checklist specifically asks to catch, left completely open.

**Fix direction:** AD-19 needs an explicit Rule clause naming which workflow file (existing or a newly
declared 4th one) hosts this agent invocation, and the source tree / Namespace mapping / "three workflow
files" invariant need to be updated to match whichever answer is chosen.

### 3. [High] UI gate-actions and GitHub's webhook share one unauthenticated Function URL

AD-17 sets the Lambda Function URL's auth type to `NONE`, with GitHub's own webhook signature verified
inside the function as the only described access control. AD-21 then has the React SPA call **the same
Function URL** to carry out `/approve`, `/rework`, and `/reject` on the human's behalf. Nothing in AD-17,
AD-18, or AD-21 describes any authentication or authorization for a UI-originated call — no session, no
shared secret, no verification that the caller is the requesting developer (or any authorized human) at
all. AD-18 carefully specifies the orchestrator-to-GitHub credential boundary ("the UI never holds a GitHub
credential") but that's the wrong half of the problem: the open question is who/what is allowed to *call
the orchestrator* to take a gate action, not what the orchestrator uses once called.

As written, anyone who obtains the (public, by design) Function URL could POST a forged `/approve` or
`/reject` for any story with zero credentials, directly undermining CAP-3/CAP-8's single-human-gate model
that the entire v1 is organized around. This dimension — UI-call authentication/authorization — is not
decided, not deferred, and not raised as an open question; it is simply silent, despite being exactly the
kind of thing this altitude owns.

### 4. [High] Companion spec (`spec-light-factory.md`) is now stale and directly contradicts this spine

The spec's frontmatter calls itself, together with its companions, "the complete, preservation-validated
contract for what to build" — i.e. canonical. Its Constraints section (unchanged by this update) still
asserts: "GitHub Environment + required-reviewers protection rules... own the two human-wait gates as job
boundaries"; "The pipeline is one GitHub Actions workflow, one triggered run, jobs chained by `needs:`";
and "v1 external dependencies are GitHub... and Anthropic/Claude Code only" (no AWS). CAP-3's success
criterion still reads "the same run resumes on approval via GitHub Environment protection rules." All three
are now false per AD-2, AD-7, and the three-workflow-file split this exact update made. An implementer
handed the spec as the canonical contract (as its own frontmatter instructs) would build the precise
mechanism this update replaced. This spine update should not land without a matching spec update, or at
minimum an explicit note flagging the spec as pending revision.

### 5. [Medium] AD-2's Rule never states the Gate-2 reject path

AD-2's Rule paragraph for `evidence-approval` only describes the approval path: "the orchestrator is
notified via the PR-review-submitted webhook, then runs... AD-19... before... AD-14... runs." It never
states what happens when the PR review is submitted as "changes requested" (Gate 2's reject). That path
only appears in the Structural Seed diagram (`GateB --> RunEndsReject2`), not as an enforceable Rule clause
in the AD it's supposedly formalizing. An implementer reading AD-2's prose alone — which is what an AD's
Rule is supposed to make unnecessary — would not know this path exists or how it's meant to behave.

### 6. [Medium] Operations (observability/alerting) for the new AWS stack is a silent dimension

AD-22 decides deployment/IaC (Terraform, single environment, local-machine deploy) but nothing in the
spine says how an operator would notice or diagnose a stuck pipeline, a failing Lambda invocation, a
DynamoDB write error, or a GitHub App token-minting failure in production. This is distinct from the
existing "non-gate failure/retry semantics... undecided" Deferred entry, which covers failure *behavior*,
not observability. Given the checklist's explicit instruction to scrutinize the operational/environmental
envelope closely, and given that this update newly introduces an always-on serverless control plane that
didn't exist before (the old design's "pause state" lived entirely and durably inside GitHub itself),
leaving monitoring/alerting completely unaddressed — not decided, not deferred, not an open question — is
a real gap at this altitude.

### 7. [Medium] The orchestrator split introduces a new split-brain failure mode, folded into an existing Deferred line without being named

Under the old design, GitHub's own Environment durably held "paused" state with no other moving part
required. Under the new design, a single gate transition requires two separate durable writes to succeed
together: the orchestrator's DynamoDB control-plane update and the `workflow_dispatch` API call to GitHub.
A failure between those two (DynamoDB says "dispatched," GitHub never received the dispatch, or vice versa)
is a new risk this exact update introduces, not one that existed before it. It's currently absorbed,
unnamed, into the pre-existing "Non-gate failure/retry semantics... undecided... sufficient as an explicit
v1 cut" Deferred entry. That entry was written before AD-17-22 existed and doesn't call out that this
specific new failure mode is a direct consequence of today's change — worth a one-line addition so a future
reader knows it's a known, accepted new risk rather than an oversight.

### 8. [Low] Stack table's three newest rows lack the verification audit trail the rest of the doc keeps

The LangGraph, Python, and Claude Code CLI rows each have a matching `.memlog.md` "(version)" entry citing
a source URL. The three rows added by this update — AWS Lambda's `python3.14` runtime, Terraform `1.16.6`,
and React `19.2.8` — say "verified current... 2026-11-03" in the Stack table but have no corresponding
memlog entry or cited source. Spot-checking the first of these independently: AWS Lambda's Python 3.14
runtime did in fact reach general availability on 2025-11-18 (AWS Compute Blog,
`aws.amazon.com/blogs/compute/python-3-14-runtime-now-available-in-aws-lambda`), so the claim holds — but
the process gap (asserted-looking text with no citation trail, unlike this document's own established
convention) is still worth closing for the other two rows and for future audits.

### 9. [Low] Structural Seed's source tree silently drops `close_rejected_pr.py` with no removal note

Consistent with AD-16 being superseded, the script no longer appears in the forward-looking source tree —
but the file still exists on disk today, and nothing in the spine says it's now dead code to be deleted as
part of implementing this update. A one-line note ("remove `close_rejected_pr.py`; its mechanism is
superseded by AD-2's direct webhook handling") would prevent an implementer from wondering whether to keep
invoking it.

## Checklist walk-through

- **Divergence points fixed for the level below, none missed:** largely yes, but findings #1 and #2 are
  exactly the kind of "level below" divergence point the spine exists to close, and both are currently
  open.
- **Every AD's Rule enforceable and actually prevents its divergence:** AD-17/18/20/21/22 and the amended
  AD-5/AD-10/AD-11 check out well. AD-2 fails this partially for the Gate-2 reject path (#5). AD-19 fails it
  for its own execution substrate (#2).
- **Nothing under Deferred could let two units diverge incompatibly:** the named Deferred entries
  themselves are fine (merge mechanics, DynamoDB/IAM/CloudFront specifics are genuinely non-load-bearing at
  this altitude). The real problem is what's *not* in Deferred at all and should be: UI-call
  authentication (#3) and the new split-brain failure mode (#7, partially addressed but not named).
- **Named tech verified-current:** mostly solid; AWS Lambda's python3.14 claim independently confirmed
  accurate. Process gap noted in #8 rather than a factual error.
- **Ratifies rather than contradicts the brownfield codebase:** this is where the update is weakest — #1 is
  a concrete, disk-verified contradiction (`light-factory` vs. the already-live `software-factory` naming).
  Everything else checked against disk (AD-5's per-job token scopes, AD-6's addenda re: `static_analysis`,
  `setup:`, `toolchains:`, the Capability→Architecture Map) matched the live `.github/workflows/software-factory.yml`
  and `.github/post-implementation-checks.yml` exactly.
- **Spec capability coverage:** the Capability → Architecture Map covers all nine CAPs. The gap is the
  *companion spec itself* being stale (#4), not missing capability coverage in the spine.
- **Every dimension this altitude owns is decided/deferred/open, especially the operational envelope:**
  deployment & environments (AD-22) and infra/provider strategy (AD-7, AD-17/18/21/22) are explicitly
  decided. Operations/observability (#6) and UI-call auth (#3) are the two dimensions left genuinely
  silent.
- **Internal consistency (AD-17..22 vs. amended ADs vs. unaffected ADs vs. Structural Seed):** strong
  overall — AD-19's permission shape correctly mirrors AD-5; AD-20's correlation key and AD-15's
  concurrency-safety handoff are consistent; AD-13's clarification-loop citation and AD-11/AD-19's
  bounded-loop pattern all line up with the Consistency Conventions table. The two real breaks are #2
  (AD-19 vs. the "three workflow files" invariant) and #5 (AD-2's prose vs. the diagram's reject path).
</content>
