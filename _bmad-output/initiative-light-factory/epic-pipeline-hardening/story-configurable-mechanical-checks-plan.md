---
title: 'Configurable mechanical checks'
type: 'feature'
ticket: '1'
created: '2026-10-11'
status: 'built'
baseline_revision: 'a9ececa2ffa920adfffe78fb83e704155aee6fa2'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `factory/scripts/run_checks.py` hard-codes the build, test, and lint commands for this repo's own Python code, so the pipeline cannot check any other project — a story for the freight-tenders app would pass without the app being built or tested.

**Approach:** Move the commands into a per-repo checks config that `run_checks.py` reads. The config is `.github/post-implementation-checks.yml`; each check holds a list of commands and all of them always run. This repo's config reproduces today's commands (the test command gains the YAML parser); a check with no configured command records `"skipped"`.

## Boundaries & Constraints

**Always:**
- Checks stay direct pipeline steps and plain subprocess calls — never a graph node or agent tool call (AD-6).
- Evidence is written to `evidence/checks/<name>.json` before the exit code is decided; a failing check always leaves a record.
- The four check names (`build`, `test`, `lint`, `security`) and the CLI (`run_checks.py <name> --story-slug S --run-id R`) are unchanged, so the workflow's four steps and `post_evidence_summary.py` keep working.
- `run_build` and `run_test` keep their signatures and return shape (`status`, `detail`), since `fix_loop_graph.py` calls them.
- A check with no configured command records `status: "skipped"`, never `"pass"`. In this repo that is `security`, permanently (user's call, 2026-10-11); a project that wants a real security check configures a command for it.
- The config is `.github/post-implementation-checks.yml`, YAML, parsed with PyYAML (user's call, 2026-10-11).
- Each check holds a list of commands; every command runs on every story, in order, with no path filtering (user's call, 2026-10-11). The check passes only when all pass, and stops at the first failure.
- A missing or malformed config is a `"fail"` with a detail naming the problem — never a silent skip of every check.

**Never:**
- No change to which checks exist, to the gates, or to the fix loop's logic.
- No commands for the freight-tenders app — that is `epic-demo-app` entry 7.
- No wiring of a security scanner in this repo.
- No runner toolchain setup (JDK, Node) — `epic-demo-app` entry 7 adds those workflow steps when the app's versions are known (user's call, 2026-10-11).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Configured check passes | config names one or more commands; all exit 0 | evidence `status: "pass"`, exit 0 | No error expected |
| Configured check fails | a command exits non-zero | evidence `status: "fail"` with that command and its stdout+stderr in `detail`, exit 1; later commands do not run | Not raised |
| Command not on PATH | `OSError` from subprocess | evidence `status: "fail"`, `detail` names the command | Caught, not raised |
| Check not configured | no entry for `security`, or an empty command list | evidence `status: "skipped"`, `command: null`, exit 0, no subprocess | No error expected |
| Config file missing | no config in the repo | evidence `status: "fail"`, `detail` names the expected path, exit 1 | Not raised |
| Config malformed | invalid syntax, or a command that is not a list of strings | evidence `status: "fail"`, `detail` names the file and the problem, exit 1 | Not raised |
| Unknown check name in config | e.g. `checks.deploy` | evidence `status: "fail"` for the check being run, `detail` names the unknown key | Not raised |

</frozen-after-approval>

## Code Map

- `factory/scripts/run_checks.py` -- the only file with the hard-coded commands (`run_build`, `run_test`, `run_lint`, `run_security`, `_RUNNERS`, `PLACEHOLDER_DETAIL`). `_run_command_check` and `_write_evidence` are reused as they are. The module docstring lists the commands and must be rewritten.
- `factory/scripts/tests/test_run_checks.py` -- 20 tests; they patch `run_checks.subprocess.run` and pass `state_base=tmp_path`. The command-equality assertions (e.g. line 50) move to a test of this repo's real config.
- `factory/graph/fix_loop_graph.py:111,116` -- calls `run_checks.run_build` / `run_test` with `state_base=` and `cwd=`; do not change these calls. Its tests mock both functions wholesale.
- `factory/scripts/post_evidence_summary.py:35,61,92` -- reads the four evidence files by name and uses `status`; do not change.
- `.github/workflows/light-factory.yml:181-208` -- the four check steps; only the comment and the "Security check (placeholder)" step name need to reflect the config. The config sits beside it in `.github/`, which `GITHUB_TOKEN` can write (only `.github/workflows/` is restricted).
- `factory/graph/fix_loop_graph.py:4` -- inline `dependencies`; change that line only.
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- AD-6 (line 71) gets the addendum; the file tree (line 285) gets the config file.

## Tasks & Acceptance

**Execution:**
- [ ] `.github/post-implementation-checks.yml` -- create it with this repo's three commands and no `security` entry; the test command adds `--with pyyaml` -- reproduces today's behavior
- [ ] `factory/scripts/run_checks.py` -- add `pyyaml` to the script's inline dependencies; load the config, run a check's configured command(s) through `_run_command_check`, record `skipped` when none is configured, report config errors as `fail`; drop the hard-coded commands -- the ticket's goal
- [ ] `factory/graph/fix_loop_graph.py` -- add `pyyaml` to the inline dependencies only -- it imports `run_checks`
- [ ] `factory/scripts/tests/test_run_checks.py` -- cover every matrix row, plus one test that this repo's real config yields today's three commands and no `security` command -- guards "same results as before"
- [ ] `.github/workflows/light-factory.yml` -- update the checks comment and the security step's name -- they describe the old hard-coding
- [ ] `architecture-light-factory.md` -- add an AD-6 addendum (config location, shape, skipped rule) and the file-tree line -- the entry owes it

**Acceptance Criteria:**
- Given this repo's config, when the four checks run locally, then `build`, `test`, and `lint` record `pass` and `security` records `skipped`, as before the change.
- Given the config's `lint` command is edited to a command that exits 1, when `run_checks.py lint` runs, then it records `fail` and exits 1 with no code edit.
- Given a fix cycle, when `fix_loop_graph` rechecks, then `run_build` and `run_test` run the configured commands.

## Implementation Notes

- Implemented directly in the planning session (no implementation subagent). Files: `.github/post-implementation-checks.yml` (new), `factory/scripts/run_checks.py`, `factory/scripts/tests/test_run_checks.py` (rewritten around a temp-dir config), `factory/graph/fix_loop_graph.py` (dependency line only), `.github/workflows/light-factory.yml` (checks comment, security step name), and the architecture doc (AD-6 addendum, file tree).
- `run_check(name, ...)` is the one code path; `run_build`/`run_test`/`run_lint`/`run_security` are thin wrappers with unchanged signatures. `_run_command_check` was split into `_run_command` (runs, writes nothing) so a check with several commands writes one evidence file.
- PyYAML is imported inside `load_commands`, not at module top, mirroring the graphs' deferred `langgraph` import: `fix_loop_graph.py`'s tests still run without it. The configured test command and the test file's own run line carry `--with pyyaml`.
- Evidence gained a `commands` key (every command that ran); `status`, `command`, `returncode`, `detail` are kept on every outcome.
- Verified locally 2026-10-11: 238 tests pass, `ruff check factory/` clean, the four real checks give pass, pass, pass, skipped. Not verified on a live run -- `epic-pipeline-hardening` entry 3 is the first dispatch that will use the config on a runner.

## Plan Change Log

## Review Triage Log

Pass 1 (2026-10-11, lens `quick`): high 0, medium 2, low 2, false 1, maybe-false 0.

| # | Finding | Verdict | Route | Evidence |
|---|---------|---------|-------|----------|
| 1 | `load_commands`: a non-UTF-8 config raises `UnicodeDecodeError` instead of recording `fail` | medium | patch | Real: `read_text()` caught only `OSError`; breaks the matrix's "Config malformed -> fail, not raised". Fixed: `encoding="utf-8"` and `UnicodeDecodeError` caught; test added. |
| 2 | `run_check` docstring says one shape, but `skipped` lacked `returncode` | low | patch | Real, nothing reads the key today. Fixed by adding `returncode: None` to the skipped result; asserted in the skipped test. |
| 3 | An empty-string argument is rejected, stricter than the matrix | low | patch | Real: `""` is a valid argv element. Fixed by deleting the `and arg` condition; test added. |
| 4 | `build`/`test` can now return `skipped`, and the fix loop and `checks` job accept it -- including a config edited on the story branch | medium | defer | Skipping an unconfigured check is the frozen intent, and the plan forbids changing the fix loop. The underlying exposure predates this change: the implementation agent could already edit `run_checks.py` on its branch. Recorded in `deferred-work.md`. |
| 5 | Test gaps: undecodable config untested; skipped exit code asserted for one variant only | false (second half) | patch (first half) | First half covered by finding 1's new test. Second half refuted: `main` maps status to exit code in one line, so the variant tests through `run_check` are sufficient, as the reviewer also concluded. |

## Design Notes

Today's `build` command uses `sys.executable`. A config cannot name that path, so the loader substitutes the token `{python}` in any command argument with `sys.executable`:

```yaml
checks:
  build:
    - ["{python}", "-m", "compileall", "factory", "-q"]
  test:
    - ["uv", "run", "--with", "pytest", "--with", "pyyaml", "pytest", "factory/graph/tests/", "factory/scripts/tests/"]
```

With several commands, the evidence keeps today's keys: `command` and `returncode` are those of the failing command, or of the last one when all pass, and a `commands` list holds every command that ran.

The config is resolved relative to `cwd` when one is passed (the fix loop passes it), else the working directory.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass
- `uv run --with ruff ruff check factory/` -- expected: no findings
- `uv run factory/scripts/run_checks.py build --story-slug tmp-check --run-id local` (and `test`, `lint`, `security`) -- expected: pass, pass, pass, skipped; remove the `.factory/tmp-check/` directory afterwards
