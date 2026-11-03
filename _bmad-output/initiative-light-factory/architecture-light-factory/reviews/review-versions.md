---
name: 'review-versions'
type: review
reviews: '_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md'
created: '2026-11-03'
---

# Review — Technology/Version Claims (architecture-light-factory.md)

Scope: verify every committed decision in the Stack table and the related ADs (AD-2, AD-17, AD-18, AD-20) was web-researched rather than asserted from training data. Checked 2026-11-03 against live web sources.

## Summary of severity

- **CRITICAL (flagged):** The single most load-bearing fact in the spine — that "require PR approval" branch protection works for a private, non-Enterprise repo — is true only on GitHub **Team** or higher. **GitHub Free does not support branch protection on private repos at all.** The spine never states or verifies which GitHub plan this repo/org is on, so the premise is unverified, not confirmed.
- **MEDIUM (flagged):** Lambda Function URL cold start vs. GitHub's strict 10-second webhook response window is a real, current operational risk the spine doesn't mention anywhere (not in AD-17, not in Deferred).
- **LOW (flagged):** GitHub App installation tokens are mid-rollout to a new stateless format (`ghs_APPID_JWT...`) since April 2026 — doesn't break AD-18's design, but worth a footnote since the spine was written/updated in this same window.
- **OK (verified):** AWS Lambda `python3.14` runtime — correct, GA since 2025-11-18, current and non-preview.
- **OK (verified):** Terraform `>=1.16.x` — correct, 1.16.6 is current as of the spine's stated verification date.
- **OK (verified):** React `>=19.x` — major version and minor line (19.2) correct and current; exact patch (19.2.8) not independently confirmed but directionally right.
- **OK (verified):** `workflow_dispatch` returning no run id — still accurate, still a known, unresolved GitHub Actions API gap.
- **OK (verified):** GitHub App installation-token flow — still supported and functioning as described.
- **OK, no material issue found:** DynamoDB on-demand pricing/API model — nothing has shifted that undermines the spine's "control-plane state only" usage.

---

## 1. AWS Lambda Python runtime (`python3.14`)

**Claim:** "`python3.14` (current, non-preview Lambda runtime verified 2026-11-03...)"

**Verdict: OK — verified.**

AWS announced general availability of the `python3.14` Lambda runtime on **2025-11-18** (AWS What's New / Compute Blog). As of 2026-11-03 this is the current, non-preview, generally-available runtime; Amazon Linux 2023-based, with Lambda-side deprecation not expected until mid-2029 per AWS's runtime-support lifecycle. No newer Python runtime (3.15) has shipped for Lambda as of this review.

Sources:
- [AWS Lambda adds support for Python 3.14 — AWS What's New](https://aws.amazon.com/about-aws/whats-new/2025/11/aws-lambda-python-314)
- [Python 3.14 runtime now available in AWS Lambda — AWS Compute Blog](https://aws.amazon.com/pt/blogs/compute/python-3-14-runtime-now-available-in-aws-lambda/)
- [AWS Lambda Runtimes — AWS docs](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)

## 2. DynamoDB — API/pricing model

**Claim:** hosted platform, on-demand capacity, control-plane state only (AD-10/AD-17), no claims about specific pricing or API behavior beyond "on-demand."

**Verdict: OK — nothing material has shifted against the spine's claims.**

DynamoDB on-demand pricing was cut ~50% in Nov 2024 and Database Savings Plans (additional ~18% on top) launched Dec 2025 — both are *cost reductions*, which only make the "DynamoDB for lightweight control-plane rows" choice cheaper, not riskier. No API-shape change affects the spine's usage (a stage/status field + counters, read/written by key) — this is a trivial, stable DynamoDB access pattern regardless of pricing-model churn. No red flags.

Sources:
- [Amazon DynamoDB Pricing — airbyte.com summary of on-demand/provisioned model](https://airbyte.com/data-engineering-resources/dynamodb-pricing)
- [DynamoDB On-Demand vs Provisioned — usage.ai](https://www.usage.ai/blogs/aws/database-savings-plans/dynamodb/on-demand-pricing/)

## 3. Terraform version

**Claim:** "`>=1.16.x` (1.16.6 verified current 2026-11-03)"

**Verdict: OK — verified.**

HashiCorp shipped Terraform 1.16.0 on 2026-08-26; patch releases followed, with 1.16.6 reported as current around mid-October 2026, consistent with the spine's 2026-11-03 verification date. No 1.17 or later major/minor has shipped as of this review. Supported release lines as of mid-October 2026 span 1.7 through 1.16.

Sources:
- [Terraform 1.16: The Changes That Matter Before You Upgrade — aicybr.com](https://aicybr.com/blog/terraform-1-16-upgrade-guide)
- [Latest Stable Version of HashiCorp Terraform — uni-luebeck wiki](https://www.its.uni-luebeck.de/en/coding-agent-help-wiki/latest-stable-version-of-hashicorp-terraform-2026)

## 4. React version

**Claim:** "`>=19.x` (19.2.8 verified current stable major version, 2026-11-03)"

**Verdict: OK (directionally) — major/minor confirmed current; exact patch not independently pinned.**

React 19.2 (Activity component, `useEffectEvent`, React Compiler 1.0 stable) shipped October 2025 and has continued receiving patch releases through 2026 (19.2.4 in Jan 2026, 19.2.6 reported in May 2026, 19.2.7 referenced elsewhere). No React 20 or other major has shipped as of this review, so "≥19.x, current stable major" is correct. I could not independently confirm the specific patch "19.2.8" existed as of 2026-11-03 from search snippets alone (search surfaced .4/.6/.7 but not .8) — low-risk since the spine only commits to the major version range in the Rule; the exact patch number is informational, not load-bearing. Also worth noting: CVE-2025-55182 affected React 19.0.0–19.2.2, patched in 19.2.3+ — any implementation should pin to ≥19.2.3 regardless of exact latest patch, which the spine doesn't currently call out.

Sources:
- [React 19.2 Is Here — digitalthriveai.com](https://digitalthriveai.com/en-ie/resources/web-development/react-19-2-is-here/)
- [React 19.2 deep dive — dev.to](https://dev.to/webtoolshub/react-192-activity-useeffectevent-react-compiler-a-practical-deep-dive-2026-glp)
- [endoflife.date/react](https://endoflife.date/react)

## 5. AWS Secrets Manager / GitHub Apps — installation-token flow

**Claim (AD-18):** GitHub App private key in Secrets Manager; orchestrator mints short-lived installation tokens on demand.

**Verdict: OK, with a timing footnote worth adding.**

The GitHub App installation-access-token flow (JWT signed with the app's private key → `POST /app/installations/{id}/access_tokens` → short-lived installation token) is still fully supported and is exactly the mechanism AD-18 describes. One timing-relevant wrinkle: GitHub began a staged rollout in **April 2026** of a new stateless installation-token format (`ghs_<appid>_<jwt>`-shaped, vs. the older 40-char opaque token). This doesn't change AD-18's design (minting is the same API call either way) but is worth a one-line footnote since the spine was last touched in the same rollout window — an implementer should not hardcode assumptions about token length/format.

Sources:
- [Generating an installation access token for a GitHub App — GitHub docs](https://docs.github.com/en/enterprise-server@3.21/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

## 6. Lambda Function URL for receiving GitHub webhooks

**Claim (AD-17):** Lambda Function URL as HTTPS entry point (not API Gateway); signature verified inside the function; chosen for cost (no separate service, no per-request charge beyond Lambda invocation).

**Verdict: Mechanism OK; one gotcha is real and unaddressed — flagged MEDIUM.**

- **Mechanism works as assumed.** AWS documents this exact pattern (a Lambda Function URL as a webhook receiver, HMAC signature verified in the handler) directly, including a dedicated "Tutorial: Create a webhook endpoint using a Lambda function URL." No API Gateway is required; Function URLs get their own HTTPS endpoint and support `NONE`/`AWS_IAM` auth exactly as AD-17 states.
- **Payload size:** buffered-mode Function URLs cap request/response payload at **6 MB** (same long-standing limit as synchronous Lambda invokes generally); GitHub webhook payloads for PR/review/comment events are far under this, so not a practical risk, but worth naming as the actual number rather than leaving it unstated.
- **Timeout/cold-start — this is the real gotcha the spine misses.** GitHub enforces a strict **10-second** response window for a webhook delivery to return 2xx before it's marked failed (GitHub.com; GitHub Enterprise Server allows longer). A cold-started Python Lambda doing signature verification plus a DynamoDB read/write for idempotency-check-on-entry (AD-20) is very likely fast enough in the common case, but cold start + first DynamoDB SDK init inside the same invocation is a documented source of webhook-delivery timeouts in exactly this kind of architecture (Lambda-behind-Function-URL-as-webhook-receiver). GitHub does retry failed deliveries, so this is not fatal to correctness, but: (a) it's an operational risk the spine doesn't mention in AD-17, AD-20, or Deferred; (b) AD-20's "every Lambda invocation checks actual current state before acting" adds exactly the kind of cold-start-sensitive work (a DynamoDB read) into the hot path of every webhook. Recommend the spine either accept this risk explicitly (e.g., in Deferred, alongside the existing "non-gate failure/retry semantics... Lambda crash/timeout" entry, which already gestures at this but doesn't name cold start specifically) or note a mitigation (provisioned concurrency, memory bump, or "respond 200 immediately, process async" pattern) at implementation time.

Sources:
- [Tutorial: Create a webhook endpoint using a Lambda function URL — AWS docs](https://docs.aws.amazon.com/de_de/lambda/latest/dg/urls-webhook-tutorial.html)
- [Lambda Function URL payload limits discussion — repost.aws](https://repost.aws/questions/QUp138JLIPRG-3oPDWYf7xGw/issues-with-lambda-function-urls)
- [Secure AWS Lambda Webhooks: Signature Verification Guide — kitemetric.com](https://kitemetric.com/blogs/secure-aws-lambda-webhooks-signature-verification-guide)
- [Lambda cold start overhead causing webhook signature verification timeout — community thread](https://forum.sggu.com/t/lambda-cold-start-overhead-causing-gc-webhook-signature-verification-timeout/10145)
- [Troubleshooting webhooks — GitHub docs (10s/30s response window)](https://docs.github.com/en/enterprise-server@3.20/webhooks/testing-and-troubleshooting-webhooks/troubleshooting-webhooks)

## 7. GitHub branch protection "require PR approval" on a private, non-Enterprise repo — THE LOAD-BEARING CLAIM

**Claim (AD-2, Superseded note):** the prior mechanism (GitHub Actions **Environments** + required-reviewers protection rules) "is restricted to GitHub Enterprise or public repos; this repo is private and non-Enterprise, so it was never actually usable here." The replacement (`evidence-approval` = plain native GitHub **branch-protection** "require PR approval" rule, no Environment) is implicitly assumed to not have this restriction.

**Verdict: PARTIALLY FLAGGED — the premise about the old mechanism is correct, but the replacement's own precondition is never verified, and it is NOT true on GitHub Free.**

Two distinct GitHub features are in play here, and the spine is right to distinguish them, but doesn't go far enough:

1. **GitHub Actions Environments + "required reviewers" protection rule** (what the original 2026-10-02 Rule relied on): confirmed Enterprise-only for private/internal repos. "Required reviewers are only available for public repositories on GitHub Free, Pro, or Team. Deployment protection rules such as required reviewers in private or internal repositories require GitHub Enterprise." — this part of the spine's superseded-note reasoning is **correct**.

2. **Plain branch protection "require pull request reviews before merging"** (what AD-2's replacement actually depends on for `evidence-approval`): this is **NOT restricted to Enterprise** — but it is **also not available on GitHub Free for private repositories**. Per GitHub's own pricing page (fetched directly): *"Repository rules" (which include branch protection / require-reviews) shows **Free: Public repositories only**; **Team: Included (all repositories)**; **Enterprise: Included (all repositories)."* The minimum tier for branch protection on a **private** repo is **GitHub Team** ($4/user/month) — or GitHub Pro for an individual-owned private repo (not applicable to an org-owned repo).

**Why this matters:** the spine's framing — "this repo is private and non-Enterprise, so [the old mechanism] was never actually usable here" — correctly rules out Enterprise-dependency for the *old* mechanism, and the *replacement* is correctly not Enterprise-gated either. But the spine never states or confirms **which GitHub plan the actual target repo/org is on**. If light-factory's target repos run on **GitHub Free** (very plausible for a PoC/demo repo, or for an individual's free private repo), branch protection — and therefore the entire `evidence-approval` gate as currently designed — **does not work at all**, Enterprise or not. "Non-Enterprise" is not the same as "any non-Enterprise plan including Free"; the real dividing line is **Free vs. Team-or-above**, a distinction the spine never draws. This is the single most load-bearing fact in the architecture and it is **asserted, not verified** — no plan-tier confirmation appears anywhere in the document (Stack table, AD-2, AD-18, or Deferred).

**Recommendation:** add an explicit line (Stack table or AD-2) naming the required GitHub plan tier (Team or above) for the org/repo this ships into, and confirm the actual target repo meets it — otherwise `evidence-approval` as designed silently cannot be enabled.

Sources:
- [GitHub Pricing — github.com/pricing (fetched directly, feature comparison table)](https://github.com/pricing)
- [Required reviewers / deployment protection rules — Enterprise-only for private repos (community discussion + docs)](https://github.com/orgs/community/discussions/202852)
- [About environments — GitHub docs](https://docs.github.com/actions/reference/environments)
- [Private personal repository branch protection: Pro vs Team — GitHub community discussion](https://github.com/orgs/community/discussions/209198)

## 8. GitHub Actions `workflow_dispatch` — no run id synchronously; concurrency/rate limits (AD-20)

**Claim:** "`workflow_dispatch` itself returns no run id" (correlation-key AD-20's load-bearing premise); idempotent-state-check-on-entry plus the branch-name correlation key carry forward AD-15's concurrency-safety intent.

**Verdict: OK — verified, still accurate.**

- The `workflow_dispatch` REST/GraphQL trigger still returns **no run id** synchronously — this is a long-standing, still-open GitHub Actions API gap, confirmed by an active GitHub community discussion ("Workflow dispatch API doesn't return the run id") and multiple third-party workaround libraries (`return-dispatch`, `workflow-dispatch-sync`) that exist specifically because GitHub has not closed this gap. AD-20's correlation-key design (using the branch name as the matching key instead of a run id) is a reasonable, currently-necessary workaround given this.
- **Rate limits/concurrency relevant to AD-20:** current documented limits are a **1,500 events per 10 seconds** cap on workflow-triggering events per repository, and (where `concurrency: queue:` is used) up to **100 queued runs per concurrency group**. Neither limit is remotely close to being hit by a single-story, human-gated pipeline, so AD-20's design isn't at risk from these limits — noted for completeness, not flagged.

Sources:
- [Workflow dispatch API doesn't return the run id — GitHub community discussion #126578](https://github.com/orgs/community/discussions/126578)
- [return-dispatch — GitHub Action polling workaround](https://github.com/eak12913/return-dispatch)
- [GitHub Actions usage limits — docs.github.com/actions/reference/limits](https://docs.github.com/en/actions/reference/limits)

---

## Items spot-checked but not in the explicit list (brief, FYI only — not separately flagged)

- **GitHub App auth generally (AD-18):** confirmed the installation-token-minting flow is current; see §5 above.
- **DynamoDB control-plane usage pattern:** confirmed stable; see §2.

## Bottom line

Of the eight checks requested, six are solidly verified against current, dated web sources (Lambda `python3.14`, DynamoDB, Terraform, React major/minor, GitHub App installation-token flow, `workflow_dispatch` no-run-id + rate limits). Two are flagged:

1. **CRITICAL — the GitHub branch-protection "require PR approval" premise (§7)** is correct that it's not Enterprise-gated, but the spine never verifies the repo/org is on at least GitHub **Team**, and it does not work at all on GitHub **Free** for a private repo. This is the single most load-bearing fact in the document and it is currently an unverified assumption, not a researched fact.
2. **MEDIUM — Lambda Function URL cold start vs. GitHub's 10-second webhook timeout (§6)** is a real, current, documented failure mode for exactly this architecture shape, and the spine doesn't mention it anywhere.
