# Rubric Review — architecture-light-factory.md (AD-18 GitHub-App-to-PAT rewrite, 2026-11-04)

Reviewed against the good-spine checklist for this specific update: AD-18 rewritten from a GitHub App
installation model to a fine-grained, repo-scoped PAT model (with a "Superseded 2026-11-04" note), with
AD-7's dependency list and AD-17's addendum (caller-type (a), webhook config) amended to match. Scope: this
review supersedes the prior `review-rubric.md` (which covered the 2026-11-03 orchestrator/UI update in
general). Verified against the live git diff (`git diff HEAD -- .../architecture-light-factory.md`) and the
`.memlog.md` entries for this same update.

## Verdict

The core AD-18 rewrite (Binds/Prevents/Rule/Superseded) is well-constructed and internally consistent, and
the three cross-references it explicitly touched (AD-7, AD-17's addendum, the webhook-config consequence)
were updated correctly — but the update is **incomplete and currently self-admitted as partial** (the
document's own `.memlog.md` says so: "Partial update applied to spine text (usage-limit interruption)"),
leaving several other "GitHub App" / "installation token" references elsewhere in the spine stale and now
actively contradicting the rewritten AD-18, plus one fabricated cross-reference to AD-5 and a frontmatter
date that was never bumped. Not safe to treat as finished/final as currently staged.

## Findings

### 1. [Critical] AD-18's Rule cites AD-5 for a token-storage shape AD-5 never defines

AD-18's new Rule says the PAT "lives in AWS Secrets Manager (one field, `github_pat`, **in the same
blob/ARN/IAM-policy shape AD-5 already established**)". This sentence is new in this rewrite — the git diff
shows the old Rule merely said "Its private key lives in AWS Secrets Manager," with no AD-5 citation at all.

AD-5 (lines 75–80) is exclusively about (1) Claude Code tool-allowlists scoped to branch + state-file paths,
and (2) per-job GitHub Actions token/branch-protection scoping (`contents: write`, `pull-requests: write`
per job). It says nothing anywhere about Secrets Manager, IAM policies, ARNs, or a secret's blob shape. The
citation is simply wrong — there is no "shape AD-5 already established" to match.

This is exactly the kind of divergence-point failure the checklist is probing for, except self-inflicted by
the rewrite: an implementer building the Secrets Manager resource and an implementer building the Lambda's
secret-read code would each go looking in AD-5 for the referenced shape, find nothing, and have to
independently invent one — the opposite of what this cross-reference was supposed to prevent.

**Fix direction:** either remove the AD-5 citation and just state the field name/structure directly, or
replace it with a real source if one exists (none currently does in this spine).

### 2. [Critical] Stack table's "GitHub Apps" and "AWS Secrets Manager" rows were not updated and now contradict AD-18

The `## Stack` table (lines 224–238) still carries:
- A **"GitHub Apps"** row: "the orchestrator's GitHub identity, AD-18 ... Installation tokens are mid-rollout
  to a new stateless format since April 2026 — minting is the same API call either way..." — this entire row
  describes the exact mechanism AD-18's Superseded note says was removed ("no JWT minting, no
  installation-token exchange (that machinery is removed, not just unused)").
- The **"AWS Secrets Manager"** row: "holds the **GitHub App private key** and the GitHub OAuth App's client
  secret, AD-18/AD-23" — directly contradicts the new AD-18 Rule, which stores a PAT (field `github_pat`),
  not an App private key.

Neither row was touched by this update (confirmed: the git diff only touches AD-7, AD-17's addendum, and
AD-18 itself) and neither is mentioned in `.memlog.md`'s own list of what was amended ("AD-7's stack row
amended" refers to the AD-7 *Rule* text, not this separate Stack table). This is a clean miss, not a
judgment call — the checklist's "grep-style check across the whole document" explicitly asks for this.

**Fix direction:** delete the "GitHub Apps" Stack row (or replace with a "Fine-grained PAT" row referencing
AD-18), and fix the Secrets Manager row to say it holds the PAT (`github_pat`) and the OAuth client secret.

### 3. [Critical] AD-23's own Rule text still asserts a GitHub App installation that AD-18 no longer defines

AD-23's Rule (line 205) says developers log in via "a GitHub OAuth App, a separate GitHub-side registration
from **the GitHub App installation AD-18 defines**" and that the orchestrator holds the OAuth secret "in
Secrets Manager, alongside **the GitHub App's private key (AD-18)**." Both clauses are now false: AD-18 no
longer defines any GitHub App installation or private key.

AD-7's amended text claims AD-23 is "unaffected by AD-18's PAT change since a GitHub OAuth App is a distinct
GitHub product from a GitHub App" — true at the conceptual level (the OAuth App itself doesn't change), but
AD-23's own prose still textually cross-references the now-removed GitHub App mechanics, so "unaffected" is
not actually correct as a claim about the document text. This is confirmed as a known gap by the update's
own `.memlog.md`, which lists "AD-23 cross-reference note" explicitly under "NOT yet done."

**Fix direction:** update AD-23's Rule to say "the fine-grained PAT AD-18 defines" and "alongside the GitHub
PAT (AD-18)".

### 4. [High] Other "GitHub App"/installation-token references left stale across the document

None of these were touched by the diff and all now contradict AD-18's supersession:
- Design Paradigm namespace mapping (line 27): `orchestrator/` — "...**GitHub App auth**, DynamoDB
  control-plane reads/writes (AD-17, AD-18)."
- Design Paradigm namespace mapping (line 28): `infra/` — "...and **the GitHub App installation config**
  (AD-22)."
- AD-22's own **Binds** line (line 197): "...and **the GitHub App installation config**."
- Structural Seed source tree (line 382): `orchestrator/github_app.py` — "**GitHub App
  installation-token minting** from the Secrets-Manager-held private key (AD-18); verifies the
  `issue_comment` webhook signature (caller type a)."
- Deferred section (line 417): "(The DynamoDB composite key and **the GitHub App's granular permission
  scopes** themselves are now decided — AD-17, AD-18 — ...)."

These are not edge cases — `github_app.py`'s own description in the Structural Seed directly describes
"installation-token minting," which the new AD-18 Rule explicitly says is "removed, not just unused." A
later implementer following the Structural Seed literally would rebuild exactly the mechanism this update
discarded.

**Fix direction:** sweep these five locations; rename/rewrite `github_app.py`'s row (e.g. to describe using
the Secrets-Manager-held PAT directly as a Bearer token), and replace "GitHub App installation config" /
"GitHub App auth" / "GitHub App's granular permission scopes" with PAT-appropriate language everywhere.

### 5. [Medium] Update is explicitly unfinished per the document's own memlog, and frontmatter was never bumped

`.memlog.md`'s last entry, verbatim: "Partial update applied to spine text (usage-limit interruption): ...
NOT yet done: Reviewer Gate (rubric/versions/adversarial/reconcile lenses), lint_spine.py pass, frontmatter
updated/status/updated date, AD-23 cross-reference note, and the downstream code change itself..." The
spine's own frontmatter `updated:` field (line 10) still reads `'2026-11-03'`, despite AD-18's Superseded
note being dated 2026-11-04 — so the document's metadata doesn't even reflect that a dated change landed
after the frontmatter's last bump. Treating this spine as ready to build against right now (rather than as
an admittedly incomplete in-flight edit) would be premature.

### 6. [Low] Superseded-note convention deviation: no cited source, unlike every other dated note in the spine

Every other dated Superseded/Changed note in this document cites a traceable source in parentheses — AD-2's
two notes cite `(`brainstorm-quality-gate-alternatives`)`, AD-15's "Changed" note cites the same, AD-16's
Superseded note cites the same, AD-6's addenda cite specific ticket numbers (e.g. "backlog bug 5"). AD-18's
new `**Superseded 2026-11-04:**` note cites no source document or ticket at all — its only traceability is
the `.memlog.md`'s own `(direction)`/`(decision)` entries, which aren't referenced from the AD itself. This
breaks the spine's own established traceability convention for dated changes.

### 7. [Low] Prevents bullet quietly drops the original human-tied-credential concern without flagging it as an accepted risk

The old Prevents bullet named the exact problem the GitHub App was chosen to avoid: "a human-tied personal
access token... (expiry tied to a person, over-broad scope, **no audit trail distinct from a human's own
actions**)." The new Prevents bullet only prevents "a classic, unscoped personal access token" — the
human-tied-credential/audit-trail-separation concern is dropped from Prevents entirely. That concern hasn't
gone away; it's now a knowingly *accepted* tradeoff, but it only survives in the Superseded note's prose
("every orchestrator action now attributes to the PAT owner's personal GitHub identity... accepted for this
PoC's current scale"). A reader who scans only Binds/Prevents/Rule (the pattern used throughout this spine)
would get no signal that this known risk exists or was deliberately accepted — it's not a contradiction, but
it is a loss of the at-a-glance legibility the Binds/Prevents/Rule structure is meant to provide.

## Checklist-by-checklist summary

- **Does the Rule fix real divergence points (permission scope, token storage, token source)?** Mostly yes
  — permission scope (Pull requests/Issues/Actions/Contents) and token source ("used directly as the Bearer
  token — no JWT minting, no installation-token exchange") are both stated unambiguously. Token *storage* is
  undermined by the broken AD-5 citation (Finding 1).
- **Internally consistent Binds/Prevents/Rule?** Yes for AD-18 in isolation — Prevents matches what the Rule
  now forbids (classic unscoped PAT) — but see Finding 7 for a softer legibility concern.
- **Superseded note preserves old rationale, per AD-2's convention?** Mostly yes in substance, but deviates
  from the sourcing convention (Finding 6).
- **Other stale GitHub-App language elsewhere?** Yes, extensively — Findings 2, 3, 4.
- **AD-23 "unaffected" — correct?** No, not as a claim about AD-23's own text — Finding 3; the memlog admits
  this itself.
- **Permission list (Pull requests, Issues, Actions, Contents) complete and justified?** Yes against the
  behaviors described elsewhere (AD-2, AD-12, AD-14/19, AD-15) — no missing GitHub API permission found,
  modulo the still-undecided question of who/what provisions the classic repo-level webhook now that
  AD-22's "GitHub App installation config" line (itself stale, Finding 4) no longer describes anything real.
