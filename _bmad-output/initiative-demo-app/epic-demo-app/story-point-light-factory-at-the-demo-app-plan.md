---
title: 'Point light-factory at the demo app'
type: 'chore'
ticket: '7'
created: '2026-10-12'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '9e2da55616364480886dd282ae77293fb0d8da5b'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The pipeline's checks config (`.github/post-implementation-checks.yml`) only ran `factory/`'s own Python build/test/lint commands. Adding the demo app's own commands to it isn't enough on its own: the `checks` job's runner needs Java 25 and a compatible Node version to run them, and a first attempt at this story wrongly assumed the runner already provides both implicitly. Architecture decision AD-6's addendum (`architecture-light-factory.md:76`) and ticket 7's own description ("...and any runner toolchain setup they need") both say toolchain setup belongs to a workflow step, not an assumption.

**Approach:** Keep the backend/frontend commands already appended to `.github/post-implementation-checks.yml`'s `build`/`test`/`lint`. Add a `toolchains:` mapping to that same file (`java: '25'`, `node: '26'`, matching `freight-tenders.yml`'s own CI) naming the versions those commands need — config-driven, like `checks:`, rather than hard-coded into the shared workflow (human's call, 2026-10-12). A new `run_checks.py toolchains` subcommand reads it (reusing the existing `origin/main`-with-working-tree-fallback path) and prints `java=...`/`node=...` lines shaped for `>> "$GITHUB_OUTPUT"`, mirroring `state_io.py`'s `derive`. The `checks` job in `.github/workflows/light-factory.yml` gains 3 steps before its check steps: run that subcommand, then `actions/setup-java@v6`/`actions/setup-node@v7`, each gated `if: steps.toolchain.outputs.<name> != ''` — so a repo/config with no `toolchains:` entry runs exactly as today, unaffected.

## Boundaries & Constraints

**Always:** `security` stays unset/skipped. `factory/`'s existing three commands stay first and untouched in each check's list. The new workflow steps are no-ops (skipped, never failing) when `toolchains:` is absent or empty.

**Never:** Do not generalize toolchain setup beyond `java`/`node` — only what this story needs. Do not touch `.github/workflows/freight-tenders.yml` (the demo app's own independent CI).

</frozen-after-approval>

## Code Map

- `.github/post-implementation-checks.yml` -- the checks config (CAP-5/AD-6); already has freight-tenders backend/frontend commands appended under `build`/`test`/`lint`; needs a new top-level `toolchains:` mapping alongside `checks:`.
- `factory/scripts/run_checks.py` -- `_load_config`/`_parse_commands`/`_read_target_config` (lines 95-165) is the pattern to mirror for a new `load_toolchains()` + `cmd_toolchains()` reading the `toolchains:` key, and a new `toolchains` subparser in `main()` (lines 290-315). Reuses `_read_target_config` as-is (no changes needed there).
- `factory/scripts/state_io.py` -- `cmd_derive` (lines 264-271) is the exact output-shape precedent: `print(f"key=value")` lines meant for `>> "$GITHUB_OUTPUT"`.
- `.github/workflows/light-factory.yml` -- the `checks` job (lines 168-234): `Checkout implementation branch` then 4 check steps. Insert 3 new steps before "Build check": read toolchains into `$GITHUB_OUTPUT` (`id: toolchain`), then `actions/setup-java@v6` and `actions/setup-node@v7`, each `if:`-gated on that step's outputs. `.github/workflows/freight-tenders.yml` lines 26-31/49-54 show the exact `uses:`/`with:` shape for both actions already working in this repo.
- `factory/scripts/tests/test_run_checks.py` -- `test_repo_config_holds_the_commands_the_script_used_to_hard_code` (line 276) now fails against the real edited config (verified locally); update its expected lists and add a `toolchains` assertion. The `CONFIG`/`_write_config`/`no_target_config` fixtures (lines 35-73) are the pattern for new tests covering the toolchains subcommand (present, absent, malformed).
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- AD-6 (line 76) currently states toolchain setup is never config-driven; append a second, dated addendum (after the existing 2026-10-11 one) documenting the `toolchains:` mechanism, same append-only pattern already used there.

## Tasks & Acceptance

**Execution:**
- [x] `.github/post-implementation-checks.yml` -- append freight-tenders backend/frontend commands to `build`/`test`/`lint` -- already done and verified standalone (see Implementation Notes)
- [x] `.github/post-implementation-checks.yml` -- add `toolchains: {java: '25', node: '26'}` -- names the versions the new commands need
- [x] `factory/scripts/run_checks.py` -- add `load_toolchains()` + `cmd_toolchains()` + a `toolchains` CLI subcommand -- reads the new section via the existing config-read path; prints `java=`/`node=` (empty string when a key is absent), shaped for `>> "$GITHUB_OUTPUT"`
- [x] `.github/workflows/light-factory.yml` -- insert 3 steps in the `checks` job before "Build check": run the new subcommand into `$GITHUB_OUTPUT` (`id: toolchain`), then `actions/setup-java@v6` and `actions/setup-node@v7`, each `if: steps.toolchain.outputs.<name> != ''`
- [x] `factory/scripts/tests/test_run_checks.py` -- fix the now-failing repo-config test and add tests for the toolchains function/subcommand (present, absent, malformed config)
- [x] `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- append a dated addendum to AD-6 documenting the `toolchains:` mechanism

**Acceptance Criteria:**
- Given the edited `.github/post-implementation-checks.yml`, when `run_checks.py toolchains` runs against it, then it prints `java=25` and `node=26`.
- Given a config with no `toolchains:` key, when the same subcommand runs, then it prints `java=` and `node=` (both empty), so the workflow's `if:` gates skip both setup steps and nothing regresses for a config with no toolchain needs.
- Given the `checks` job runs on a story touching `freight-tenders/`, when the build/test/lint steps execute, then `mvn`/`npm` resolve to Java 25/Node 26, and `evidence/checks/*.json` records `pass` for each (backend and frontend commands).
- Given `factory/scripts/tests/test_run_checks.py`, when run, then every test passes, including the updated repo-config assertion and the new toolchains tests.

## Implementation Notes

Oneshot attempt 1 (superseded): a single-file, mechanical config edit assumed the `ubuntu-latest` runner's implicit toolchains (Java 25 cached as `JAVA_HOME_25_X64`, Node 22.23.3 "system-wide", per the `actions/runner-images` docs) were enough, avoiding any `.github/workflows/light-factory.yml` edit. A `quick` review (below) found this contradicted AD-6's addendum and ticket 7's own scope text, and flagged that `freight-tenders.yml`'s own CI doesn't rely on anything implicit either (it explicitly sets up Java 25 and Node **26**, not 22 — Angular's `engines` field requires `^22.22.3 || ^24.15.0 || >=26.0.0`, so the "system-wide" Node was an unverified gamble). Asked the human; chose a generic, config-driven toolchain mechanism over hard-coding this app's versions into the shared workflow. Reopened to `full` to design and build that mechanism.

Also discovered (not in the original plan): `factory/scripts/tests/test_run_checks.py::test_repo_config_holds_the_commands_the_script_used_to_hard_code` asserts the config's exact pre-edit command lists and now fails against the real, already-edited `.github/post-implementation-checks.yml` — the original oneshot plan never ran the Python test suite. Folded into this plan's Tasks.

Implementation (2026-10-12): all remaining tasks built. `_load_config`'s read step (origin/main-with-working-tree-fallback) was factored out into `_read_config_text()` so `load_toolchains()` reuses it unchanged rather than duplicating the read logic. `load_toolchains()`/`_parse_toolchains()` mirror `_parse_commands`'s "fail loud, never a silent skip" posture for a malformed config (non-mapping `toolchains:`, an unknown key beyond `java`/`node`, a non-string version), but return `""` rather than raising when a known key or the whole mapping is simply absent, matching `cmd_derive`'s always-print-the-key convention. The existing freight-tenders `mvn` commands' `JAVA_HOME="$JAVA_HOME_25_X64"` override was left untouched (per the Approach) — it still resolves correctly because `actions/setup-java@v6` with `java-version: '25'` also exports `JAVA_HOME_25_X64`, the same variable name the runner's own pre-cached JDK used, so the new explicit step and the pre-existing commands agree with no further edit needed.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 1, medium: 0, low: 0, false: 0, maybe-false: 0

- `.github/workflows/light-factory.yml`'s `checks` job has no Java/Node toolchain setup for the newly-added `mvn`/`npm` commands — **high**, confirmed. Verified both citations verbatim: AD-6's addendum (`architecture-light-factory.md:76`, "Runner toolchain setup ... is not part of the config; it is a workflow step added with the project that needs it") and ticket 7's own description (`tickets.toml:77`, "...and any runner toolchain setup they need"). Route: HALT — asked the human rather than patching unilaterally, since the fix crosses the epic's "not light-factory's own pipeline logic" Boundary and ticket 7's pre-authorization only covers *a* workflow edit, not which shape. The human chose a generic/config-driven toolchain mechanism; plan reopened to `full` (see Implementation Notes).

### Review pass 2 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 0, medium: 0, low: 1, false: 1, maybe-false: 0

- `.github/workflows/light-factory.yml`'s "Set up Node" step omits `cache: 'npm'` / `cache-dependency-path: freight-tenders/frontend/package-lock.json`, unlike the "Set up Java" step right above it (which copies `freight-tenders.yml`'s shape exactly) and unlike `freight-tenders.yml`'s own `actions/setup-node@v7` step — **low**, confirmed (verified both files side by side). No functional defect (npm just reinstalls without a cache), but it's an inconsistent application of the plan's own cited precedent (Code Map, `freight-tenders.yml` lines 26-31/49-54). Route: patch — trivial, two-line addition, no new public surface.
- The plan's Verification section's `run_checks.py toolchains` command, and acceptance criterion 3, read as if achievable against this story's own PR/branch before merge — but `run_checks.py` always reads `origin/main` first, which doesn't have this story's edits yet, so both print/evaluate empty until merge — **false**, rejected. This is the pre-existing, documented `origin/main`-read design (AD-6's addendum, and the config file's own header comment: "a change here applies to runs started after it is merged"), not a defect this diff introduced; every existing `checks:` command already has the identical property, never previously called out in a Verification section either.

## Design Notes

The new `toolchains:` reader mirrors `state_io.py`'s `cmd_derive` output convention — stable `key=value` lines, printed even when the value is empty — rather than inventing a new shape, so the workflow step's `>> "$GITHUB_OUTPUT"` redirection and the later `if:` checks read the same way AD-8's slug/run-id derivation already does.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/scripts/tests/` -- expected: all tests pass
- `uv run --with pyyaml python factory/scripts/run_checks.py toolchains` (from repo root, once the subcommand exists) -- expected: prints `java=25` and `node=26`
- `python3 -c "import yaml; yaml.safe_load(open('.github/post-implementation-checks.yml'))"` -- expected: valid YAML
- `cd freight-tenders/backend && mvn -B verify && mvn -B spotless:check` -- expected: `BUILD SUCCESS`, no violations
- `cd freight-tenders/frontend && npm ci && npm run build && npm test -- --watch=false && npm run lint` -- expected: all pass

**Manual checks (if no CLI):**
- Re-read the edited `.github/workflows/light-factory.yml` `checks` job and confirm the 3 new steps are placed before "Build check" and each is `if:`-gated on the toolchain subcommand's own outputs.
