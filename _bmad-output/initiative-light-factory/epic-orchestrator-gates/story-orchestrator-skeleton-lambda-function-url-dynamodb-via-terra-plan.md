---
title: 'Orchestrator skeleton: Lambda, Function URL, DynamoDB via Terraform'
type: 'feature'
ticket: '1'
created: '2026-11-03'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 2
context: ['{project-root}/AGENTS.md']
baseline_revision: 'd95c34ae146e2e302658336e48b125a5ea6a78dc'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** GitHub's required-reviewers-on-environments gate is Enterprise/public-repo-restricted, and the replacement orchestrator design (AD-17) has no AWS infrastructure at all yet in this repo.

**Approach:** Stand up the AWS side from scratch via Terraform — a stateless Lambda behind a Lambda Function URL (not API Gateway, chosen for run cost) and a DynamoDB table keyed on the composite partition key `story_slug#run_id` — as the tracer bullet proving every layer (Terraform → AWS → Function URL → Lambda → DynamoDB) connects, before any real gate logic is built on top.

## Boundaries & Constraints

**Always:** Terraform only, single AWS environment/account, applied from a developer's local machine (no CI/CD deploy pipeline for this infra yet, per AD-22). Target AWS account `830495964081` ("DAI-CST"), region `eu-central-1` (matches every existing local profile's region) — no local AWS profile targets this account yet, so the developer sets one up (e.g. `aws configure sso`) before the first `terraform apply` (hitl). DynamoDB holds orchestrator control-plane state only — never a copy of git-committed content state. Lambda Function URL, not API Gateway. Terraform's own state is local (`*.tfstate`), never committed.

**Never:** No caller-type auth dispatch, webhook signature verification, or GitHub App calls — that's stories 2/3/5/6. No changes to `.github/workflows/` — untouched by this story. No DynamoDB attributes beyond the partition key, and no IAM policy beyond least-privilege for this one Lambda's own execution + table access.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Function URL invoked | Any HTTP request to the deployed Function URL | Handler returns 200 + minimal JSON body | No error expected |
| DynamoDB round trip | An item manually put with key `story_slug#run_id` | A read by that key returns the identical item | No error expected |
| `terraform apply` from clean state | No prior infra exists | Lambda, Function URL, DynamoDB table created with no manual console steps | Provider auth failure surfaces clearly in `plan`/`apply` output |

</frozen-after-approval>

## Code Map

- `orchestrator/handler.py` -- new: stub Lambda entry point, returns 200 + minimal JSON, no auth/FSM logic yet
- `orchestrator/requirements.txt` -- new: pinned deps for the deployed package (see Design Notes — deliberately not PEP 723)
- `orchestrator/tests/test_handler.py` -- new: local unit test of the handler's response shape
- `infra/variables.tf` -- new: `aws_region` variable defaulting to `eu-central-1`, `aws_profile` as a required variable with no default (account `830495964081` targeted via whichever local profile the developer points at it)
- `infra/main.tf` -- new: `aws_lambda_function` (zipped from `orchestrator/` via `archive_file`), `aws_lambda_function_url` (`authorization_type = "NONE"`), `aws_dynamodb_table` (hash key `story_slug#run_id`, `PAY_PER_REQUEST` billing), minimal IAM execution role
- `infra/outputs.tf` -- new: Function URL and table name, for the manual verify step and later stories
- `.gitignore` -- add `.terraform/`, `*.tfstate`, `*.tfstate.backup`, `infra/build/`, `infra/lambda_package.zip` (currently absent). `.terraform.lock.hcl` is deliberately NOT ignored -- Terraform's own convention is to commit it, pinning provider versions (`~> 5.0` aws, `~> 2.4` archive) reproducibly across machines/runs. `infra/build/` and `infra/lambda_package.zip` are `main.tf`'s own packaging-step outputs (the unzipped build dir and the deployable zip) -- reproducible from `orchestrator/` on every `apply`, never deliverables
- `factory/scripts/state_io.py` -- reference only, for contrast: this repo's existing PEP-723 convention that `orchestrator/` deliberately does not follow

## Tasks & Acceptance

**Execution:**
- [ ] `orchestrator/handler.py` -- stub handler returning 200 + JSON -- proves the Function URL round-trips
- [ ] `orchestrator/requirements.txt` -- minimal pinned deps -- Lambda packaging, distinct from `factory/`'s inline-deps convention
- [ ] `orchestrator/tests/test_handler.py` -- unit test the response shape -- local verification before any deploy
- [ ] `infra/variables.tf` -- `aws_region` defaults to `eu-central-1`, `aws_profile` required with no default -- keeps account-targeting explicit, not silently baked in
- [ ] `infra/main.tf` -- Lambda + Function URL + DynamoDB + IAM role -- the tracer-bullet infra
- [ ] `infra/outputs.tf` -- Function URL + table name -- needed for verification and later stories
- [ ] `.gitignore` -- add `.terraform/`, `*.tfstate`, `*.tfstate.backup`, `infra/build/`, `infra/lambda_package.zip` -- prevents committing local state and `main.tf`'s own packaging-step outputs, while leaving `.terraform.lock.hcl` committable per Terraform's own reproducibility convention

**Acceptance Criteria:**
- Given a clean `infra/` with no prior state, when `terraform apply` runs with a valid AWS profile/region, then the Lambda, its Function URL, and the DynamoDB table are created with no manual console steps.
- Given the deployed Function URL, when it receives any HTTP request, then it returns a 200 response with a minimal JSON body.
- Given the deployed DynamoDB table, when an item keyed `story_slug#run_id` is put and then read, then the read returns the identical item.
- Given `.gitignore`, when `terraform apply` runs locally, then `git status` shows no `.terraform/`, `.tfstate`, or lock file as untracked-but-stageable.

## Implementation Notes

## Plan Change Log

**2026-11-03, review pass 1, bad_plan:** Triggering finding: `.gitignore` ignoring `.terraform.lock.hcl` per this plan's own original Code Map/Tasks instruction undermines Terraform's provider-version reproducibility across machines/runs (medium). Amended: Code Map and Tasks now instruct `.gitignore` to add only `.terraform/`, `*.tfstate`, `*.tfstate.backup` -- `.terraform.lock.hcl` stays committable, matching Terraform's own convention. Known-bad state avoided: a second developer's `terraform init` silently resolving a different `aws`/`archive` provider patch version than whoever applies first. KEEP: everything else in the prior implementation verified correct and must survive re-derivation unchanged -- `orchestrator/handler.py`, `orchestrator/tests/test_handler.py`, `orchestrator/requirements.txt` (empty is correct, not a bug -- a separate `patch`-routed low finding on `infra/main.tf`'s IAM log-group ARN wildcarding the account segment is deferred to the next review pass, not blocking this loopback), `infra/variables.tf`, `infra/outputs.tf`, and `infra/main.tf`'s resource structure (Lambda, Function URL with `authorization_type = "NONE"`, DynamoDB table with hash key `story_slug#run_id` and `PAY_PER_REQUEST` billing, the `null_resource`/`archive_file` packaging pattern, `runtime = "python3.13"` -- confirmed correct against the installed `hashicorp/aws` provider's actual enum, not the architecture doc's unverified `python3.14` claim), and the `aws_lambda_permission` resource added beyond the literal Code Map (required for `authorization_type = "NONE"` to actually permit invocation, verified against the provider's real schema).

**2026-11-03, review pass 2, bad_plan:** Triggering finding: `.gitignore` never accounted for `main.tf`'s own packaging-step outputs (`infra/build/`, `infra/lambda_package.zip`) -- a real `terraform apply` leaves both untracked-but-stageable, violating acceptance criterion 4's intent (medium). Amended: Code Map and Tasks now instruct `.gitignore` to also add `infra/build/` and `infra/lambda_package.zip`. Known-bad state avoided: the deployed Lambda zip and its unzipped build directory being one `git add -A` away from landing in history. KEEP: everything from pass 1's KEEP list, unchanged, plus `infra/main.tf`'s exact `local.build_dir`/zip `output_path` values (`${path.module}/build`, `${path.module}/lambda_package.zip`) -- the new `.gitignore` patterns must match these literal paths, not be invented independently.

## Review Triage Log

**Pass 1 (quick lens, 2026-11-03):** 1 high/medium/low-bearing finding routed, 1 low routed, 1 false. Verdict counts: medium=1, low=1, false=1.

- `infra/.gitignore` ignoring `.terraform.lock.hcl` (plan's own Code Map/Tasks instruction) — **medium, bad_plan.** Verified: `terraform init` itself advises committing this lock file for reproducible provider-version pinning across machines/runs; ignoring it lets a second developer's `terraform init` silently resolve a different `~> 5.0`/`~> 2.4` provider patch version. Root cause is in the plan's Code Map/Tasks (non-frozen), not a deviation by the implementer — the diff correctly did what the plan said.
- `infra/main.tf`'s CloudWatch log-group ARN wildcarding the account-id segment (`*`) instead of `830495964081` — **low, patch.** Verified: no real security loosening (an IAM identity-based policy can't grant cross-account access this way regardless), but slightly looser than the plan's own "least privilege" framing given it names a single target account. Trivial direct fix (`data.aws_caller_identity.current.account_id`), no new public surface.
- `orchestrator/requirements.txt` reading as "minimal pinned deps" (Code Map) while holding zero actual pins — **false.** Refuted: the file's own inline comments and the plan's Design Notes already establish the stub handler needs no third-party deps (stdlib-only, boto3 pre-bundled); no bad outcome occurs, only the Code Map's one-line gloss undersold "possibly zero."

**Pass 2 (quick lens, 2026-11-03):** 1 finding routed. Verdict counts: medium=1.

- `.gitignore`'s Terraform patterns (`.terraform/`, `*.tfstate`, `*.tfstate.backup`) don't cover `infra/main.tf`'s own packaging-step outputs — **medium, bad_plan.** Verified directly against the diff: `main.tf` writes its build directory to `${path.module}/build` (i.e. `infra/build/`) and its zip to `${path.module}/lambda_package.zip` (i.e. `infra/lambda_package.zip`); neither path is matched by any `.gitignore` pattern added. A real `terraform apply` leaves both as untracked-but-stageable, directly undermining acceptance criterion 4's intent. Root cause is the plan's Code Map/Tasks `.gitignore` enumeration, written before `main.tf`'s packaging approach was decided and never reconciled against it — not an implementer deviation (the implementer built exactly what both tasks specified, which simply never intersected).

**Pass 3 (quick lens, 2026-11-03):** 0 new findings. All acceptance criteria and boundaries independently re-verified clean. The one outstanding item from pass 1 (IAM log-group ARN account-id wildcard, low/patch) was deliberately not re-reported per instruction and is actioned now below, since no intent_gap/bad_plan this pass left it moot no longer.

- `infra/main.tf`'s CloudWatch log-group ARN wildcarding the account-id segment — **low, patch** (verdict carried from pass 1, now actioned). Fix applied: added `data "aws_caller_identity" "current" {}`, replaced `*` with `data.aws_caller_identity.current.account_id` in the ARN. Re-verified: `terraform fmt`/`validate` clean, 3/3 handler tests still pass (untouched by this file).

## Design Notes

PEP 723 vs. Lambda packaging: `factory/`'s scripts resolve dependencies inline at `uv run` time; AWS Lambda's runtime has no `uv` and can't read that metadata. `orchestrator/` therefore gets its own `requirements.txt`, pip-installed into a build directory and zipped via Terraform's `archive_file` data source — a deliberate, scoped deviation from AGENTS.md's convention, limited to Lambda-deployed code. Local dev/test tooling for `orchestrator/` still uses `uv run --with pytest pytest ...`, matching `factory/`'s test-running style even though the deployed artifact differs.

DynamoDB billing mode: `PAY_PER_REQUEST`, not provisioned capacity — low, unpredictable PoC traffic with no capacity planning needed; reversible later if usage patterns justify provisioned throughput.

## Verification

**Commands:**
- `cd orchestrator && uv run --with pytest pytest tests/ -v` -- expected: all tests pass
- `cd infra && terraform fmt -check && terraform validate` -- expected: no formatting diffs, config is valid
- `cd infra && terraform plan` -- expected: shows exactly the planned Lambda, Function URL, DynamoDB table, IAM role, no errors

**Manual checks (if no CLI):**
- Human runs `terraform apply` (hitl, per the ticket), then curls the output Function URL and confirms a 200 + JSON response
- Human runs `aws dynamodb put-item` / `get-item` against the output table name to confirm a round-trip
