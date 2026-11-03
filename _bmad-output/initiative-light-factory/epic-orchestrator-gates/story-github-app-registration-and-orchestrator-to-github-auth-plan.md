---
title: 'GitHub App registration and orchestrator-to-GitHub auth'
type: 'feature'
ticket: '2'
created: '2026-11-03'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: 'd46956e2936c363a5ab165e0c0ab2039a391f3fb'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The orchestrator Lambda (built in entry 1) has no way to authenticate to GitHub yet — nothing can call the GitHub API on the human's behalf, which every later gate mechanism depends on.

**Approach:** Register a dedicated GitHub App (human-driven, scoped permissions, no admin), store its private key in AWS Secrets Manager, and wire the Lambda to mint a JWT, exchange it for a short-lived installation access token, and call the GitHub REST API — verified by the Lambda actually posting a comment on a real test PR.

## Boundaries & Constraints

**Always:** GitHub App only (not a human-tied PAT, per AD-18). Permissions: `pull_requests: write`, `issues: write`, `actions: write` — no admin; human confirms these exact scopes before install. Private key lives only in Secrets Manager, never committed. IAM grants the Lambda `secretsmanager:GetSecretValue` on only this one secret's ARN. `PyJWT[crypto]` is the one new pip dependency; GitHub API calls use stdlib `urllib.request`, not `requests`. The packaging step must target `manylinux2014_x86_64` explicitly (Lambda defaults to x86_64; a bare local `pip install` on this dev machine would otherwise fetch an incompatible macOS wheel for `cryptography`).

**Never:** No webhook signature verification or caller-type auth dispatch (story 3). No `/approve`/`/rework`/`/reject` parsing (story 5). No changes to `.github/workflows/`. No attempt to create the GitHub App itself via Terraform (not possible — confirmed no provider can do this; App creation is GitHub-UI-only).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| JWT minted | App ID + private key from Secrets Manager | A valid RS256 JWT with `iss`/`iat`/`exp` claims | N/A (local signing, no network) |
| Installation token requested | Valid JWT, real installation id | GitHub returns a short-lived installation access token | A JWT/App auth failure surfaces GitHub's error body clearly |
| Real PR comment posted | Valid installation token, real PR number | GitHub returns 201, comment appears on the PR | A token/permission failure surfaces GitHub's error body clearly |

</frozen-after-approval>

## Code Map

- `orchestrator/github_app.py` -- new: `mint_jwt()` (PyJWT, RS256), `get_installation_token()` (POST to `/app/installations/{id}/access_tokens`), `post_comment()` (POST to `/repos/senacor3/software-factory-demo/issues/{n}/comments` via `urllib.request`) — pure functions, no Lambda-specific coupling
- `orchestrator/handler.py` -- extend minimally: recognize an optional `_verify_post_comment: {pr_number, body}` key in the event for THIS story's own live verification only (temporary diagnostic path, not real caller-type routing — stories 3/5/6 own that); everything else still returns entry 1's stub 200
- `orchestrator/requirements.txt` -- add `PyJWT[crypto]` (the first real pin; currently empty)
- `orchestrator/tests/test_github_app.py` -- new: unit tests for `mint_jwt`/`get_installation_token`/`post_comment` with mocked `boto3`/`urllib` — no real network calls in automated tests
- `infra/main.tf` -- add `aws_secretsmanager_secret` + `aws_secretsmanager_secret_version` (one secret, a JSON blob: app_id, installation_id, private_key_pem — supplied via new sensitive variables, never hardcoded), a scoped `aws_iam_role_policy` for `secretsmanager:GetSecretValue` on just that ARN, and fix `null_resource.install_dependencies`'s pip command to add `--platform manylinux2014_x86_64 --implementation cp --python-version 3.13 --only-binary=:all:`
- `infra/variables.tf` -- add `github_app_id` (string), `github_app_installation_id` (string), `github_app_private_key_pem` (string, `sensitive = true`, no default)
- `aws_lambda_function.orchestrator`, `aws_iam_role.lambda_exec`, `aws_dynamodb_table.orchestrator_state` (entry 1, unchanged) -- referenced, not modified beyond the one IAM policy addition and the packaging-command fix

## Tasks & Acceptance

**Execution:**
- [ ] `orchestrator/github_app.py` -- JWT mint + installation-token exchange + post_comment -- the actual GitHub-auth capability
- [ ] `orchestrator/requirements.txt` -- add `PyJWT[crypto]` -- needed for RS256 signing (stdlib can't do it)
- [ ] `orchestrator/handler.py` -- recognize `_verify_post_comment` test key -- lets this story's verify run inside the real Lambda
- [ ] `orchestrator/tests/test_github_app.py` -- unit test all three functions with mocks -- local verification before any deploy
- [ ] `infra/variables.tf` -- 3 new required variables for App id/installation id/private key -- keeps the credential explicit, never baked in
- [ ] `infra/main.tf` -- Secrets Manager secret + scoped IAM read policy + packaging-command platform fix -- the deployable credential path and the x86_64 wheel-compatibility fix
- [ ] `infra/outputs.tf` -- no change needed (secret ARN not required by any consumer yet)

**Acceptance Criteria:**
- Given the GitHub App is created and installed (human step, App ID/installation ID/private key supplied as Terraform variables), when `terraform apply` runs, then the private key is stored in Secrets Manager and the Lambda's role can read only that one secret.
- Given a real installation id and private key in Secrets Manager, when the orchestrator mints a JWT and exchanges it for an installation token, then GitHub returns a valid short-lived token via a real call (not mocked).
- Given a valid installation token and a real test PR number, when `post_comment` runs, then GitHub returns 201 and the comment is visible on the PR.
- Given the packaging step, when dependencies are installed, then `cryptography`'s wheel in the build dir is tagged `manylinux2014_x86_64`, not a macOS build.

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-03):** 3 findings routed. Verdict counts: medium=2, low=1, all patch.

- `orchestrator/tests/test_handler.py`'s own docstring documents running tests via plain `uv run --with pytest pytest tests/ -v` (no PyJWT) — now stale, since `handler.py` unconditionally imports `github_app.py`, which unconditionally imports `jwt` — **low, patch.** Verified: that exact documented command now fails at collection with `ModuleNotFoundError: No module named 'jwt'`. The story's own prescribed Verification command already includes `--with "PyJWT[crypto]"` and works; only the pre-existing docstring is wrong now. Fix: update the docstring to the real current command, and fix the `_load_github_app_credentials` comment's misleading framing (it protects only against `boto3`, not the dependency this story actually added).
- `infra/variables.tf`'s `github_app_private_key_pem` description claims a `.tfvars` file is "excluded from git" — **medium, patch.** Verified: no `.gitignore` anywhere in the repo excludes `*.tfvars`/`terraform.tfvars`/`*.auto.tfvars`. A human following this story's own documented guidance has no actual guard against committing the private key. Fix: add those patterns to `.gitignore`.
- `aws_secretsmanager_secret.github_app` has no `recovery_window_in_days` set, defaulting to AWS's 30-day soft-delete — **medium, patch.** A `terraform destroy`+re-`apply` cycle (plausible during early local-machine iteration per AD-22) would fail on the same secret name until the window elapses or someone force-deletes it out-of-band. Fix: set `recovery_window_in_days = 0` -- no data-loss risk here since the secret's content is always re-suppliable from the same GitHub App credentials.

All three patches applied and re-verified: 9/9 tests pass, `.gitignore` now excludes `*.tfvars`/`*.tfvars.json`/`*.auto.tfvars`/`*.auto.tfvars.json`, `recovery_window_in_days = 0` present, `terraform fmt`/`validate` clean.

## Design Notes

Why `urllib.request` over `requests`: avoids a second pip dependency when a single Bearer-header POST is all that's needed, consistent with `requirements.txt`'s existing "pin only what's actually imported" philosophy from entry 1.

Why `PyJWT[crypto]` is unavoidable: GitHub App auth requires RS256-signed JWTs; Python's stdlib has no RSA-signing primitive suitable for this without a crypto backend, and `cryptography` is PyJWT's standard one.

Packaging risk (confirmed by investigation): `aws_lambda_function.orchestrator` has no `architectures` set, so it defaults to x86_64. The existing `pip install -t <build_dir>` (no platform flags) running on this macOS dev machine would otherwise fetch a `cryptography` wheel built for macOS, which cannot run on Lambda's Linux x86_64 runtime. Fixed by adding explicit `--platform manylinux2014_x86_64 --implementation cp --python-version 3.13 --only-binary=:all:` to the pip command — `cryptography` publishes manylinux x86_64 wheels, so no Docker/Lambda build container is needed.

GitHub App creation itself cannot be automated (no Terraform provider creates the App resource) — human creates it via GitHub's web UI (Settings → Developer settings → GitHub Apps → New GitHub App), sets permissions `pull_requests: write`/`issues: write`/`actions: write` (no admin, confirmed with the human first per the ticket's own note), leaves the webhook disabled/placeholder (story 3's concern, not this one), installs it on `senacor3/software-factory-demo`, and supplies the App ID, installation ID, and downloaded private key PEM as Terraform variables.

## Verification

**Commands:**
- `cd orchestrator && uv run --with pytest --with PyJWT[crypto] pytest tests/ -v` -- expected: all tests pass
- `cd infra && terraform fmt -check && terraform validate` -- expected: no diff, config valid

**Manual checks (if no CLI):**
- Human creates and installs the GitHub App, supplies App ID/installation ID/private key as `terraform apply -var` values, and applies
- Human creates a disposable test PR on `senacor3/software-factory-demo`
- Human invokes the Lambda (`aws lambda invoke` with a `_verify_post_comment` test payload naming that PR's number) and confirms the comment actually appears on the PR
- Human inspects `infra/build/`'s installed `cryptography` wheel metadata to confirm the `manylinux2014_x86_64` platform tag
