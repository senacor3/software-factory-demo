---
name: 'review-adversarial'
type: review
reviews: '_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md'
reviewed-ads: 'AD-1 through AD-22, Design Paradigm, Consistency Conventions, Structural Seed, Deferred'
posture: adversarial — each pair below is constructed to obey every binding AD to the letter while still producing an incompatible build
created: '2026-11-03'
---

# Adversarial Review — architecture-light-factory.md

## Verdict

The spine pins the *shape* of the orchestrator confidently (one Lambda, one Function URL, DynamoDB control-plane, GitHub App, hand-rolled FSM, three dispatched workflows, two gate mechanisms, a bounded conflict loop) but leaves almost every *wire format* at the new serverless/webhook boundary unpinned — DynamoDB item/key schema, the stage-completion webhook's event type and payload, the GitHub App's granular permission set, the UI→orchestrator auth story, and the conflict-resolution agent's exact write-scope are all asserted in prose and then explicitly or implicitly deferred — so two engineers can each satisfy every AD that binds them and still hand back incompatible systems. Eight concrete adversarial pairs are documented below, two of them (the DynamoDB key-schema mismatch and the UI-vs-webhook auth contradiction) severe enough to silently defeat AD-19's hard cap or AD-21's entire feature respectively.

## Findings

### 1. [CRITICAL] DynamoDB item/key schema is asserted, never specified — AD-19's hard cap can silently become unbounded

**Pair:** the engineer implementing the `/approve` · `/reject` stage-transition handling in `orchestrator/handler.py` vs. the engineer implementing AD-19's merge-conflict-resolution attempt counter in the same file.

- AD-17 says DynamoDB holds "current stage/status, branch name, retry/cycle counters." AD-10's addendum repeats the same prose. AD-19 says the conflict-loop's attempt counter is "owned solely by the orchestrator's own control-plane state (AD-17), never by the agent." None of these — nor the Consistency Conventions table, nor the Structural Seed — gives a partition key, sort key, attribute name, or item-per-entity vs. item-per-counter shape. The Deferred section confirms this explicitly: *"DynamoDB table schema specifics... none of these were decided at this altitude; left for implementation (AD-17...)."*
- Engineer A, building the gate-transition logic, reasonably keys the table by `story_slug` alone (AD-15 guarantees at most one run in flight per story, so one row per story is a defensible reading) and stores `{stage, status, branch}` on it, overwriting on every transition.
- Engineer B, building AD-19's bounded loop, needs a counter scoped to *this run* specifically (a new run must start the conflict-attempt count back at zero — this is the entire point of AD-15's run isolation) and therefore keys by `story_slug#run_id` composite, writing `{conflict_attempts: int}` under that key.
- Both engineers satisfy their own AD to the letter. But Engineer B's reads against `story_slug#run_id` never find a row Engineer A never wrote under that key shape — the GetItem comes back empty every time, `conflict_attempts` is always treated as 0/absent, and AD-19's hard cap of 2 never actually trips. The defect is invisible in isolation: each engineer's unit tests (against their own schema) pass.
- **Close with:** a new AD pinning the DynamoDB table's exact key schema (partition/sort key, one item per `story_slug#run_id`, explicit attribute names for stage, status, branch, and each of the three counters) before any orchestrator code is written — not left as an implementation detail.

### 2. [CRITICAL] The UI's direct calls to the Function URL are not GitHub webhooks — AD-17's literal signature-verification rule, applied uniformly, rejects every legitimate UI action

**Pair:** the engineer implementing AD-17's Lambda entry point (`handler.py`'s request-validation front door) vs. the engineer implementing AD-21's React SPA actions.

- AD-17: "GitHub's webhook signature is verified inside the function itself **before any action is taken**." Read literally and uniformly — the natural way to implement a single shared Lambda entry point — every inbound request to the one Function URL must carry a valid `X-Hub-Signature-256` HMAC before the function does anything.
- AD-21: the SPA's approve/rework/reject buttons "call the orchestrator's Lambda Function URL" directly, and by AD-18 "the UI never holds any GitHub credential of any kind." The SPA therefore has no webhook secret and cannot produce that signature.
- AD-17's Function URL auth type is `NONE` and nothing in AD-17, AD-18, or AD-21 defines a *second* authentication mechanism for the non-GitHub caller (no API key, no session token, no shared secret for the UI path specifically). Two implementers reading only their own AD build mutually exclusive things: the handler-side engineer, following AD-17 to the letter, rejects every UI request as an invalid/missing signature; the UI-side engineer, following AD-21 to the letter, never attempts to sign anything because AD-18/AD-21 told them the SPA holds no credential at all. One of them is wrong, but nothing in the spine says which, and both are individually AD-compliant.
- **Close with:** a new AD (or a tightened AD-17/AD-21) defining the *second* authentication path for UI-originated calls to the shared Function URL — e.g. a per-developer bearer token, Cognito/IAM-authenticated Function URL mode for the UI path only, or a dedicated `ui/` route distinguished from the webhook route with its own auth — and state explicitly that AD-17's signature check applies only to the GitHub-sourced path.

### 3. [HIGH] "New input" to a re-invoked analysis stage means two different things in AD-2 and AD-13

**Pair:** the engineer implementing `/rework`'s workflow_dispatch in `handler.py` + `analysis.yml`'s `inputs:` block vs. the engineer implementing `analysis_graph.py`'s clarification loop per AD-13.

- AD-2: `/rework (feedback text)` "loops back to re-invoke the analysis stage **with the comment text as new input**."
- AD-13: "the developer answers by editing the story file itself (**the only input `run_analysis` ever reads**) and re-triggers the pipeline as a new run."
- These are two different data paths into the same function. Engineer A (gate/dispatch side) adds a `feedback_text` `workflow_dispatch` input and threads it as an argument into `run_analysis`. Engineer B (graph side), implementing AD-13's explicit constraint that the story file is "the only input `run_analysis` ever reads," gives `run_analysis` no such parameter at all. Both are individually faithful to the AD that binds their unit. The result: `/rework`'s feedback text is dispatched into a function signature that has nowhere to put it — either dropped silently, or `analysis.yml` (built by whichever of the two, or a third, owns the workflow YAML) never declares the input in the first place and the dispatch call itself fails.
- **Close with:** reconcile AD-2 and AD-13 — either `/rework` must append the feedback text into the story file (or a sibling file) deterministically before re-dispatch, matching AD-13's "file is the only input" invariant, or AD-13 must be amended to admit a second, dispatch-input-sourced form of new input, with `run_analysis`'s signature pinned accordingly.

### 4. [HIGH] Stage-completion "webhook" — event type and payload shape never pinned; a generic `workflow_run` conclusion cannot carry the status AD-13 requires

**Pair:** the engineer implementing each workflow file's final step (`analysis.yml`, `implementation-checks-review.yml`) vs. the engineer implementing the Lambda's completion-event handler.

- The Structural Seed labels every exit edge "webhook to orchestrator" (e.g. "analysis complete," "clarification halt," "clarification cap reached" — three *different* outcomes). AD-20 binds "every webhook/completion event the orchestrator receives" but never names the GitHub event type or payload.
- A `workflow_run` (or `check_run`) completion webhook only reports the *job/workflow's* own exit conclusion (`success`/`failure`/`cancelled`) — in all three of analysis's outcomes above, the job itself exits 0 and the conclusion is `success`. A generic workflow-completion webhook cannot by itself distinguish "ready-for-review" from "awaiting-clarification" from "clarification-cap-reached" — that distinction lives only in `plan.md`'s frontmatter `status` field (AD-10), committed to the branch.
- Engineer A (workflow-file owner), taking "webhook to orchestrator" literally, relies on GitHub's native `workflow_run` webhook and does nothing else — no custom callback step.
- Engineer B (Lambda owner), needing to actually distinguish the three outcomes, assumes the *workflow* will tell it directly — e.g. a final `curl` step posting `{status: ...}` to the Function URL — and writes handler logic keyed off a JSON field that engineer A's workflow never sends.
- Neither engineer is wrong per the text they were given; "webhook to orchestrator" was never pinned to a concrete event + payload, so whichever of (native GitHub event + Lambda re-reads `.factory/.../plan.md` via the GitHub Contents API) vs. (custom callback step with an explicit status payload) was intended is genuinely ambiguous, and the two implementations are not interoperable.
- **Close with:** pin the completion signal explicitly — either "every dispatched workflow's final step POSTs `{story_slug, run_id, stage, status}` to the Function URL" (custom callback, needs its own lightweight auth — ties to Finding 2) or "the orchestrator subscribes to `workflow_run` and re-reads the relevant `.factory/<slug>/<run-id>/*.md` frontmatter via the GitHub Contents API to learn `status`" — and state it as a Rule, not an inference from a diagram label.

### 5. [HIGH] Duplicate-webhook race: AD-20's idempotency claim depends on an atomic check-and-set that is never mandated

**Pair:** the engineer implementing the `/approve` → dispatch-implementation path vs. the engineer implementing the Gate-2-approved → dispatch-conflict-check path.

- AD-20: "checks the actual current state... before acting, rather than trusting the triggering event alone — this makes a duplicate or double invocation safe without needing to be prevented outright." This is true only if the read-check-then-write is a single atomic operation (e.g., a DynamoDB `ConditionExpression` on the expected prior stage). GitHub explicitly delivers webhooks at-least-once and can redeliver.
- Nothing in AD-20 (or anywhere else) requires the state transition to be an atomic conditional write. Engineer A implements `/approve` handling with a plain `GetItem` → business logic → `PutItem` (the natural, simpler reading of "check state, then act"). Engineer B, working the other transition, independently implements theirs with a proper `UpdateItem`+`ConditionExpression` guard. Both satisfy AD-20's prose ("checks actual current state before acting"); only one is actually race-safe. Two near-simultaneous duplicate `/approve` deliveries hitting Engineer A's path both read "plan-approval, not yet dispatched" before either write lands, and both call `workflow_dispatch` — two concurrent `implementation-checks-review.yml` runs against the same branch, racing each other's commits and evidence files (which AD-10 assumes are written by exactly one live job).
- **Close with:** tighten AD-20 to require the state-check-and-transition to be a single atomic conditional write (name the DynamoDB mechanism explicitly: conditional `PutItem`/`UpdateItem` with `ConditionExpression` on expected prior stage), not merely "check before acting."

### 6. [MEDIUM] GitHub App permission scope omits the scope PR *comments* actually require

**Pair:** the engineer writing `infra/main.tf`'s GitHub App resource (AD-22) vs. the engineer writing `orchestrator/github_app.py` / the comment-posting code path (AD-18, AD-2, AD-4).

- AD-18: "The App's permissions are scoped (PR read/write, Actions write — no admin)." This maps naturally to GitHub's `pull_requests` and `actions` granular permissions. But every comment this pipeline posts or reads — the `/approve`/`/rework`/`/reject` command grammar (AD-2) and both gate summaries (AD-4) — goes through the Issue Comments API, which is gated by GitHub's `issues` permission, not `pull_requests` (a PR *review* is `pull_requests`; a PR *comment* is `issues` in GitHub's App permission model).
- Engineer A (Terraform), reading AD-18's "PR read/write" literally, provisions only `pull_requests: write` + `actions: write`. Engineer B (orchestrator code), assuming the App can already read/post comments because AD-18 said "PR read/write" covers it, writes `/approve`-reading and comment-posting code with no additional check. The integration only fails at runtime (403 from GitHub) — exactly the kind of mismatch that two implementers working from the same under-specified AD would not catch at review time, since each unit is internally consistent with the text they were given.
- **Close with:** list the exact granular GitHub App permissions by name in AD-18 or AD-22: `pull_requests: write` (for branch-protection/review state, PR close), `issues: write` (for comment read/post — the actual mechanism behind AD-2's command grammar and AD-4's summaries), `actions: write` (dispatch), `contents: read` (if the orchestrator ever reads repo content directly) — plus the webhook event subscriptions (`issue_comment`, `pull_request_review`, `workflow_run`/`check_run`, `pull_request`) that must be enabled on the App for AD-2/AD-20 to receive anything at all.

### 7. [MEDIUM] Two independent PR-close code paths, two credentials, no shared lock — AD-20's idempotency guard does not reach one of them

**Pair:** the engineer implementing the orchestrator's `/reject`-webhook handler (AD-2, runs as a Lambda invocation, GitHub-App-credentialed) vs. the engineer implementing `open_implementation_pr.py`'s supersession-close logic (AD-12/AD-15, runs as a step inside the `analysis` GitHub Actions job, job-token-credentialed).

- Both paths can close the same PR for the same story-slug. AD-20 explicitly scopes its idempotent-state-check-on-entry to "every Lambda invocation" — `open_implementation_pr.py` is not a Lambda invocation, it runs inside a dispatched GitHub Actions job, so AD-20's guard does not cover it at all.
- Concrete race: a human posts `/reject` on the currently-open PR for story X at the same moment a re-trigger for story X has already been dispatched (its `analysis.yml` run is mid-flight, about to reach `open_implementation_pr.py`'s supersession search). The Lambda closes the PR with a "rejected" comment and (per Finding 1's schema ambiguity) marks the DynamoDB row terminal. Seconds later, the in-flight analysis job's supersession script finds that same PR (by branch-prefix search, AD-15) and closes it again with a "superseded by #N" comment — leaving a self-contradictory comment trail (rejected and superseded), and now the DynamoDB control-plane row (terminal/rejected) disagrees with git reality (a new branch/PR/run now exists and is proceeding). Each engineer's own code is correct per the AD that binds their own unit (AD-2 for the Lambda path, AD-12/AD-15 for the script path); neither AD requires the two to coordinate, and AD-20's text makes it easy to believe (wrongly) that this race is already closed.
- **Close with:** extend AD-20's idempotency/correlation-key coverage explicitly to non-Lambda deterministic scripts that mutate PR state (name `open_implementation_pr.py`'s close/supersede action specifically), or centralize all PR-closing mutations behind the orchestrator so there is exactly one writer of "this PR is closed."

### 8. [MEDIUM] "Identical permission shape" for the conflict-resolution agent is ambiguous between two very different scopes

**Pair:** the engineer implementing AD-19's conflict-resolution agent invocation vs. the engineer implementing the pre-existing implementation agent's AD-5 tool-allowlist, read as the template to copy.

- AD-19: the conflict agent is "scoped ONLY to the feature branch — no `main` access, no merge/admin tool, identical permission shape to the existing implementation agent under AD-5."
- AD-5's actual implementation-agent scoping is two-dimensional: a git-ref boundary (the branch) **and** a specific state-file-path allowlist (that story's own implementation subtask files, explicitly excluding `plan.md`/`decisions.md`/`review.md`). "Identical permission shape" is ambiguous about which dimension travels: Engineer A reads it as "same two-layer *philosophy*" and gives the conflict agent Edit/Write across the whole branch (any file, since a merge conflict can land in any file touched by a concurrent change to the target branch — including files the original implementation subtask never touched). Engineer B reads "identical" literally and reuses the *same narrow path allowlist* computed for the implementation agent's own subtask — which means the conflict agent is unable to edit any conflicting file outside that original subtask's file list, i.e. it cannot resolve a large class of real conflicts (any conflict in a file the implementation agent didn't itself write), silently failing or cycling to cap-out on conflicts it was never permissioned to touch.
- Both are defensible readings of "identical permission shape," and they produce agents with very different (and differently risky) blast radii — Engineer A's is branch-wide write (broader, matches what the task actually needs, but wider than "implementation agent" literally was scoped); Engineer B's is narrower but functionally broken for its stated purpose.
- **Close with:** state explicitly in AD-19 whether the conflict agent's write scope is "the whole feature branch, any path" (functionally required) or "only the paths already touched by this story's own commits" (AD-5's literal template) — these are not the same guarantee and AD-19 currently reads as both.

## Supporting observation (not a pair, pre-existing inconsistency)

AD-10's Rule pins the content-state `stage` field enum to exactly `analysis | implementation | review`, yet AD-10's own 2026-10-13 addendum calls `checks.md` "the state file of stage `checks`" — a fourth value the Rule's own enum doesn't list. This self-contradiction already exists in the document independent of this update, but it is exactly the pattern that invites Findings 1 and 8 above: nothing stops two implementers of the new `merge` stage / conflict-resolution sub-stage from independently inventing yet more stage-name strings (`merge`, `conflict-resolution`, `merge-conflict-check`, …) for the DynamoDB control-plane `stage` field, none of them reconciled against AD-10's enum or each other.

## File

Review written to `/Users/Andreas.Guenzel/dev/workspaces/light-factory/_bmad-output/initiative-light-factory/architecture-light-factory/reviews/review-adversarial.md`.
