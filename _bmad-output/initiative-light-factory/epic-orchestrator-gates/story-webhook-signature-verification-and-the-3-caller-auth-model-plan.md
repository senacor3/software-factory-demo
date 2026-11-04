---
title: 'Webhook-signature verification and the 3-caller auth model'
type: 'feature'
ticket: '3'
created: '2026-11-03'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: 'e72505984d24b3a940f4d32a95bd342187a8f787'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The Function URL has zero auth right now — any caller, including a forged request, hits the same unauthenticated path, and entry 2 left behind an explicit unauthenticated backdoor (`_verify_post_comment`) that can trigger a real GitHub API call from anyone who knows the key name.

**Approach:** Add a caller-type dispatch layer: verify GitHub webhook HMAC signatures, authenticate stage-completion callbacks via a distinct shared secret, reserve a stub branch for the future UI OAuth caller (AD-23), reject everything else with a clear reason — and remove the old unauthenticated diagnostic shortcut now that real auth exists.

## Boundaries & Constraints

**Always:** Verify only `X-Hub-Signature-256` (HMAC-SHA256 over the exact raw body bytes, constant-time compare via `hmac.compare_digest`); ignore the legacy `X-Hub-Signature` (SHA-1) header entirely. Decode `isBase64Encoded` bodies to raw bytes *before* hashing, never hash a re-parsed/re-serialized form. `webhook_secret` and `stage_callback_secret` both live as new fields in the existing `aws_secretsmanager_secret.github_app` blob (same ARN, same IAM policy — no new Secrets Manager call, no new policy resource). The UI OAuth caller type is a reserved stub only — no real session-token validation in this story (epic-pipeline-dashboard's job). Stdlib only (`hmac`, `hashlib`, `base64`) — no new pip dependency.

**Never:** No DynamoDB state transitions or FSM logic (entries 5/6/9). No real OAuth implementation. No changes to `.github/workflows/` (the split workflows don't exist in dispatched form yet). The old `_verify_post_comment` path is removed, not left reachable — an unauthenticated backdoor existing alongside real auth would directly contradict this story's own "unrecognized caller is rejected" criterion.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Correctly-signed GitHub webhook | Valid `X-Hub-Signature-256` matching the configured secret, computed over the exact raw body | Accepted, dispatched to the webhook-caller branch | N/A |
| Forged/unsigned webhook | Missing, malformed, or incorrect `X-Hub-Signature-256` | Rejected with a clear reason, no downstream call attempted | Clear-reason response body, no GitHub API call |
| Correctly-authenticated stage-completion callback | Correct shared-secret header value | Accepted, dispatched to the stage-callback branch | N/A |
| Unrecognized caller | Matches none of the three types | Rejected with a clear reason, distinguishable from a signature failure | Clear-reason response body |

</frozen-after-approval>

## Code Map

- `orchestrator/auth.py` -- new: `verify_github_webhook_signature(raw_body: bytes, signature_header: str | None, secret: str) -> bool` (HMAC-SHA256, constant-time); `verify_stage_callback_secret(provided: str | None, expected: str) -> bool` (constant-time compare, not a plain `==`)
- `orchestrator/handler.py` -- rewrite: extract raw body (base64-decode if `isBase64Encoded`) and lowercase-keyed headers; dispatch in order: GitHub webhook signature -> stage-callback secret -> UI-OAuth stub heuristic (an `Authorization` header present but neither other check matched -> "not yet implemented", distinct from generic rejection) -> else reject as unrecognized with a clear reason. On a successful match, return 200 naming the recognized caller type -- no further processing (that's entries 5/6/9). REMOVE `_verify_post_comment` entirely (entry 2's own docstring called it explicitly temporary). `_load_github_app_credentials()` becomes the shared secret-loader for all three fields in the one blob (still one `get_secret_value` call, no caching added in this story)
- `orchestrator/requirements.txt` -- unchanged (stdlib only)
- `orchestrator/tests/test_auth.py` -- new: valid signature, forged signature, missing header, base64-encoded-body signature, stage-callback secret valid/invalid
- `orchestrator/tests/test_handler.py` -- rewrite the dispatch-level tests: webhook accepted, forged rejected, stage-callback accepted, UI-stub-heuristic rejected-as-not-implemented, fully unrecognized rejected -- replacing entry 2's now-removed `_verify_post_comment` tests
- `infra/main.tf` -- extend `aws_secretsmanager_secret_version.github_app`'s JSON blob with `webhook_secret`/`stage_callback_secret` (from new variables); no new secret resource, no new IAM policy
- `infra/variables.tf` -- add `github_webhook_secret` (string, `sensitive = true`, no default), `stage_callback_secret` (string, `sensitive = true`, no default)

## Tasks & Acceptance

**Execution:**
- [ ] `orchestrator/auth.py` -- HMAC signature verification + stage-callback secret check -- the actual auth primitives
- [ ] `orchestrator/handler.py` -- 3-branch dispatch, `_verify_post_comment` removed -- closes the unauthenticated backdoor
- [ ] `orchestrator/tests/test_auth.py` -- unit test both primitives, including a deliberate forged-signature attempt -- the ticket's own named check
- [ ] `orchestrator/tests/test_handler.py` -- dispatch-level tests for all four outcomes -- proves the full routing, not just the primitives
- [ ] `infra/variables.tf` -- 2 new required sensitive variables -- keeps both secrets explicit, never baked in
- [ ] `infra/main.tf` -- extend the existing secret blob -- no new Secrets Manager resource or IAM policy needed

**Acceptance Criteria:**
- Given a request with a valid `X-Hub-Signature-256` computed from the configured webhook secret over the exact raw body, when the handler processes it, then it is accepted and dispatched to the webhook-caller branch.
- Given a request with a missing, malformed, or incorrect `X-Hub-Signature-256`, when the handler processes it, then it is rejected with a clear reason and no downstream call is attempted.
- Given a request with the correct stage-callback shared-secret header, when the handler processes it, then it is accepted and dispatched to the stage-callback branch.
- Given a request matching none of the three caller types, when the handler processes it, then it is rejected with a clear reason distinguishable from a signature failure.
- Given a base64-encoded Function URL event body, when signature verification runs, then it operates on the decoded raw bytes, never a re-serialized form.

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-03):** 2 findings routed. Verdict counts: high=1, low=1, both patch.

- `handler()` calls `_load_github_app_credentials()` unconditionally at the top, before any dispatch branch, even though the UI-stub and fully-unrecognized branches never read `credentials` at all — **high, patch.** Verified: `aws_lambda_function_url.orchestrator` has `authorization_type = "NONE"` (public internet), so any unauthenticated garbage/scanner request triggers a billed `secretsmanager:GetSecretValue` call for no reason, and an unhandled Secrets Manager failure would crash a request that was always going to be cleanly rejected -- violating the plan's own "rejected with a clear reason" acceptance criterion for exactly the two branches that need no credentials at all. The plan's Design Notes only justify one shared blob/call for the branches that DO need it (webhook, stage-callback); it never justifies fetching for the other two. Fix: move the credential load inside the webhook/stage-callback branches only, so it's fetched lazily, only when the request actually presents one of those headers.
- `orchestrator/tests/test_handler.py`'s module docstring gives a self-contradictory reason for needing `PyJWT[crypto]` (claims it's because `handler.py` imports `auth`, then notes `auth` is stdlib-only) — **low, patch.** Verified: the real reason is that `pytest tests/` also collects `test_github_app.py`, which imports `jwt` -- unrelated to `handler.py`'s own (now stdlib-only) import chain. Fix: correct the docstring's stated reason.

Both patches applied and re-verified: 25/25 tests pass; `_load_github_app_credentials()` now called only inside the webhook and stage-callback branches (confirmed via direct grep), never unconditionally.

## Design Notes

Secret storage: extending the existing `aws_secretsmanager_secret.github_app` blob rather than adding new secrets, because `_load_github_app_credentials()` already does one uncached `get_secret_value` call per invocation -- a second secret would double that call on literally every request (webhook verification runs before any other work), and the existing IAM policy is already scoped to exactly this one ARN. Blast radius is unchanged either way: one Lambda role already reads this secret; splitting fields across secrets wouldn't add real isolation.

`_verify_post_comment` removal: it was an unauthenticated diagnostic backdoor (any caller triggering a real GitHub API post by including a magic key). Leaving it reachable once real caller-type auth exists would contradict this story's own "unrecognized caller is rejected" criterion outright.

Only `X-Hub-Signature-256` (SHA-256) is checked. GitHub still sends the legacy `X-Hub-Signature` (SHA-1) for backward compatibility on older configs, but SHA-1 is deprecated/weak and must not be relied on even as a fallback.

The real GitHub-side webhook hookup (enabling the App's webhook, pointing it at the real deployed Function URL, entering the same secret value in GitHub's UI) is explicitly NOT part of this story's Done -- it's a live-hookup step that can happen whenever is convenient, since a self-signed synthetic test request exercises identical HMAC logic to a real GitHub delivery. This is why the ticket itself is `hitl: false`.

UI-OAuth stub heuristic: an `Authorization` header present with neither the webhook signature nor the stage-callback secret matching routes to a distinct "UI auth not yet implemented" response, rather than the generic "unrecognized caller" rejection -- reserving the branch's shape (per AD-17/AD-23) so `epic-pipeline-dashboard` only has to fill in real validation, not restructure this dispatch.

## Verification

**Commands:**
- `cd orchestrator && uv run --with pytest --with "PyJWT[crypto]" pytest tests/ -v` -- expected: all tests pass, including the deliberate forged-signature case
- `cd infra && terraform fmt -check && terraform validate` -- expected: no diff, config valid

**Manual checks (if no CLI):**
- None required -- this story's full Verify is satisfiable via the automated test suite's synthetic signed/forged requests, per the ticket's own `hitl: false`.
