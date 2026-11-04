# Adversarial Review — AD-18 (PAT model), AD-17 (orchestrator/webhook), AD-5 (defense-in-depth)

**Reviewer stance:** attacker/future-implementer. For each finding: what the Rule actually says, what a literal-minded implementer would build from it, and what breaks.

**Scope note:** this review is confined to the four attack vectors requested (rotation/expiry, single point of identity, webhook-secret wiring, human-account scope) plus one structural issue (stale cross-references) that surfaced directly while tracing those four vectors through the rest of the document. It is not a general-purpose line edit of the spine.

---

## Verdict

AD-18's new PAT Rule is internally coherent on its own, but the rewrite was not propagated to the rest of the spine: at least six other locations (Stack table, file-tree, AD-22, AD-23, Deferred) still describe the superseded GitHub-App mechanics as if current, and three genuine new gaps — no rotation/alerting path for an expiry AD-18 itself mandates, no specified storage location for the webhook HMAC secret, and no offboarding/succession story for a credential now tied to one human's GitHub account — are real enough that a from-the-letter implementation would either silently stop working or quietly regress the security posture the superseded Rule had.

---

## Finding 1 — Stale "GitHub App" references left standing after AD-18's rewrite (High, structural)

AD-18's Superseded note (2026-11-04) is explicit: the GitHub App is gone, "that machinery is removed, not just unused." But the rewrite did not touch the rest of the document, which still instructs a future implementer to build GitHub-App plumbing:

- **Stack table** (line 238): `GitHub Apps — ... the orchestrator's GitHub identity, AD-18 — ... Installation tokens are mid-rollout to a new stateless format...` — this row directly contradicts AD-18's current Rule. A reader who hits the Stack table before AD-18's prose would go provision a GitHub App — reintroducing the exact org-owner-rights blocker (`senacor3` org, no reachable admin) that caused AD-18 to be superseded in the first place.
- **Structural Seed file tree** (`orchestrator/github_app.py`, line 382): `"GitHub App installation-token minting from the Secrets-Manager-held private key (AD-18); verifies the issue_comment webhook signature"`. AD-18's own text says installation-token minting machinery is removed. This file's stated responsibility is exactly the removed machinery, plus it conflates "mint installation token" and "verify webhook signature" into one file/AD citation when AD-17's addendum now attributes the HMAC check to caller-type-(a) handling generically, not to a GitHub-App-specific module.
- **AD-23's Rule** (line 205, not itself superseded or addended): "a GitHub OAuth App, a separate GitHub-side registration from **the GitHub App installation AD-18 defines**..." and "...holding the OAuth App's client secret in Secrets Manager, alongside **the GitHub App's private key (AD-18)**." Both clauses describe AD-18 mechanics that no longer exist. AD-23 was never revised when AD-18 was, so it now actively misdescribes its own cross-reference.
- **AD-22's Binds line** (line 195): "...the AWS resources backing the orchestrator (...) **and the GitHub App installation config**." No GitHub App installation exists to configure.
- **Deferred, line 417**: "(The DynamoDB composite key and **the GitHub App's granular permission scopes** themselves are now decided — AD-17, AD-18...)" — should read "the PAT's granular permission scopes."

**Why it matters:** this is precisely the "future implementer, obeying [a] Rule to the letter, builds something incompatible" scenario — except the incompatible Rule is one of these *other* five locations, each individually plausible as the thing someone implements from (especially the file-tree, which is the part people copy literally when scaffolding `orchestrator/`). Any one of them alone reintroduces the org-owner-approval blocker AD-18 exists to route around.

**Recommendation:** sweep for "GitHub App" outside AD-18's own Superseded note and AD-7 (which was correctly updated — see line 96) and rewrite each occurrence to PAT-based language, or explicitly mark each as historical/stale pending a cleanup pass.

---

## Finding 2 — PAT expiry is mandated with no rotation process and no alerting anywhere in the spine (High, operational)

AD-18's Rule: "Set with an expiry, not 'No expiration'." No AD — not AD-18, not AD-17, not AD-20, not the Deferred bucket — says who rotates it, when, or how the orchestrator (or a human) learns it is about to expire or already has.

- AD-20 (idempotent state-check-on-entry) only guards against duplicate/out-of-order *events*; it says nothing about an auth failure from GitHub's API becoming a *terminal* condition rather than a retryable one.
- The Deferred bucket's "Observability for the new AWS stack" (line 419) explicitly lists "the GitHub App token-minting path" as an example of what's undecided — stale wording aside (Finding 1), this framing assumes the *old* short-lived-token-minting failure mode (a per-call mint that can fail and retry), not the *new* failure mode: a single long-lived credential that goes from 100% working to 100% failing at one fixed instant, deterministically, pipeline-wide, across every one of the three caller-type auth paths that depend on it (webhook-triggered actions still need the PAT to act on GitHub even though the webhook itself is HMAC-verified, not PAT-verified).
- Nothing distinguishes "PAT expired" from the generic "transient GitHub API failure" bucket already deferred (line 414) as undecided retry/alerting semantics — but PAT expiry is not transient and not a crash; it is scheduled, predictable, and 100%-reproducing, which is a materially different failure class that deserves its own line, not folding into "revisit if real runs surface reliability gaps."

**Why it matters:** AD-18 *requires* an expiry to exist (closing the old "no expiry requirement" gap), which means the orchestrator calling GitHub as its sole mechanism for every post-webhook, post-UI-action, and post-stage-completion action **will** go dark on a known date, pipeline-wide, with nothing in this spine describing how anyone notices before every PR comment, workflow_dispatch, and merge silently starts failing. The old GitHub-App Rule didn't have this exposure in the same way: an installation token is minted fresh per use from a private key, so the *key* could in principle live indefinitely (GitHub App private keys have no forced expiry), meaning there was no scheduled, guaranteed outage date baked into the design.

**Recommendation:** add either (a) an explicit AD or Deferred-bucket entry naming PAT-expiry monitoring/alerting as a named, tracked gap (distinct from the generic transient-failure bucket), or (b) a rotation procedure (who, how often, calendar reminder vs. automated check via GitHub's PAT-expiration API) before this ships even as a PoC.

---

## Finding 3 — No AD specifies where the webhook HMAC secret lives or who keeps GitHub's copy and the orchestrator's copy in sync (High, concrete gap confirmed by grep)

Grepped the full document for `webhook_secret` / "webhook secret" / HMAC: the **only** two hits are in AD-17's caller-type addendum (line 166): "(b) UI calls ... (the SPA holds no webhook secret)" and "(c) stage-completion callbacks ... authenticated via a distinct shared secret stored as a GitHub Actions secret." Caller type (a) — the actual GitHub webhook — is verified "via GitHub's `X-Hub-Signature-256` HMAC signature," full stop. No AD says:

- what Secrets Manager field holds the Lambda's copy of that HMAC secret (AD-18's Rule explicitly says the credentials blob holds "**one field**, `github_pat`" — leaving no stated home for a second, HMAC-verification secret in that same blob, and no other blob is named anywhere);
- who creates the webhook's secret value on the GitHub side (repo Settings → Webhooks is a manual UI action per AD-17's addendum — note it says "not a GitHub App's own webhook config," i.e., there is no org-level App installer who could have set this centrally anymore; it now falls to whoever has repo-admin rights, which per AD-18's Superseded note is a different population than the org-owner rights the removed GitHub App needed);
- how that value is round-tripped into Secrets Manager consistently (`infra/main.tf`'s resource list, line 385, names "Lambda, Lambda Function URL, DynamoDB table, Secrets Manager secret, S3 UI bucket" — no GitHub webhook resource, so Terraform isn't shown as the single source of truth for both sides either).

**Why it matters:** this is exactly the "future implementer wires GitHub's webhook secret and the Lambda's verification secret inconsistently" scenario the task asked me to hunt for, and it's real: two independent setup steps (GitHub repo-admin configuring the webhook; whoever provisions Secrets Manager) have no architectural tie-breaker telling them to use the same value, nor a single script/Terraform resource generating one value and pushing it to both places. A mismatch fails closed (signature check fails, webhook rejected) rather than open, which limits blast radius, but it is an availability gap with no diagnosis path named anywhere (ties back to Finding 2's observability gap).

Separately, AD-18's claim that the PAT's storage "blob/ARN/IAM-policy shape" was "already established" by AD-5 does not hold up: AD-5's full Rule (lines 75–80) only covers Claude Code tool-allowlists and per-job GitHub Actions token/branch-protection scoping — it never mentions Secrets Manager, blobs, ARNs, or IAM policies. So the "shape" AD-18 cites as precedent does not actually exist in this document; Secrets Manager's structure for *any* GitHub-related credential (PAT or webhook secret) is architecturally unspecified.

**Recommendation:** name an explicit Secrets Manager field (e.g., `webhook_secret`) alongside `github_pat` in AD-18 or AD-17, and either (a) make webhook creation/secret-sync a Terraform-managed step (the `github` Terraform provider supports `github_repository_webhook` with a `secret` argument sourced from the same value written to Secrets Manager) or (b) explicitly document the manual two-sided setup as a deploy runbook step. Also correct or remove AD-18's "AD-5 already established" citation.

---

## Finding 4 — No AD addresses PAT-owner account disablement, 2FA lockout, or offboarding (Medium, acknowledged but incompletely)

AD-18's Superseded note partially anticipates this: "every orchestrator action now attributes to the PAT owner's personal GitHub identity, not a distinct bot identity — accepted for this PoC's current scale (one maintainer), **revisit if a second maintainer joins** or a real GitHub App installation becomes available." This names the bus-factor/audit-trail tradeoff but only in terms of a *second maintainer joining* — it does not address:

- the PAT owner's GitHub account being disabled, suspended, or 2FA-locked (fine-grained PATs are revoked immediately if the owning account loses access or is removed from the org);
- what "rotation" even means operationally when the credential is tied to one person's account settings — it is necessarily a manual action by that specific human, with no backup owner named;
- org-level fine-grained-PAT approval policies (many GitHub orgs require an admin to approve fine-grained PATs before they can access org repos) — if `senacor3` has or later enables this policy, the PAT could be revoked or fail to renew independently of the "expiry" field AD-18 already names, and nothing in this spine's Deferred bucket or AD-18 flags this as a distinct risk from ordinary expiry.

**Why it matters:** this compounds Finding 2 — rotation isn't just "undescribed," it is tied to a single named individual with no documented successor, so an unplanned account issue (not just a calendar expiry) can take down the same single point of failure, and the spine gives no indication anyone should plan for it beyond "revisit if a second maintainer joins."

**Recommendation:** add this to the Deferred bucket explicitly (it currently is not — the closest existing entry, line 414's failure/retry bucket, only covers transient technical failures, not credential/identity continuity), naming it as a known PoC-scale risk the same way the Superseded note already frames the bot-identity tradeoff.

---

## Finding 5 — AD-5's defense-in-depth model never actually extends to the orchestrator's own PAT (Medium)

AD-5 binds "all agent invocations" and describes two layers: (1) Claude Code tool-allowlists, (2) per-job GitHub Actions token scoping. Both layers are about the GitHub Actions jobs' own tokens and the Claude Code agents' own tool access — neither layer says anything about the Lambda orchestrator's own credential. AD-18's PAT is a single, broadly-scoped (`Pull requests`, `Issues`, `Actions`, `Contents`, all read/write) credential used uniformly for every orchestrator action regardless of stage or gate — there is no per-stage scoping of the orchestrator's own GitHub calls analogous to AD-5's per-job GHA token scoping. The only thing standing between a leaked PAT and full read/write control of PRs/issues/Actions/Contents on the target repo is Secrets Manager IAM + whatever the Lambda's own input validation does — a single layer, not the two independent layers AD-5 champions elsewhere in this same spine for every other credential in the system.

**Why it matters:** this isn't necessarily wrong for a one-Lambda PoC, but it is an asymmetry worth naming rather than leaving implicit: AD-5's "neither sufficient alone" framing reads as a spine-wide principle, but the orchestrator's single highest-privilege GitHub credential is the one credential in the system it doesn't actually cover.

**Recommendation:** either note explicitly in AD-18 or AD-5 that the orchestrator's PAT is a deliberately-accepted single-layer exception to AD-5's defense-in-depth principle (consistent with how AD-19's addendum explicitly calls out where it follows AD-5's *philosophy* but not its *letter*), or scope the PAT down further / add a second check (e.g., Lambda-side allow-list of which PR/story the given action is permitted to touch, keyed off AD-20's correlation key) as a second layer.

---

## Minor/supporting observations (not scored as standalone findings)

- AD-7 (line 96) *was* correctly updated to PAT language and is the one place that correctly notes the OAuth App (AD-23) is unaffected by AD-18's change — useful as a model for how the other stale locations (Finding 1) should read once fixed.
- The webhook's required rights changed from org-owner (GitHub App install) to repo-admin (classic webhook) per AD-17's addendum — this is a real, positive side effect of AD-18's supersession (lower privilege bar to configure), but it's never cross-referenced from AD-18 itself, only from AD-17's addendum, so a reader of AD-18 alone wouldn't know the webhook-configuration rights model changed too.
