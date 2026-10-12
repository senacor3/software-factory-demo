# Read the checks config from the target branch

## Problem

`factory/scripts/run_checks.py` reads the commands for the `build`, `test`, `lint`
and `security` checks from `.github/post-implementation-checks.yml` in the working
tree — that is, from the story's own branch. A story's implementation can therefore
change the checks that judge it: emptying `test` turns it into `skipped`, which the
`checks` job and the fix loop both accept. The only sign is the word `skipped` in
the evidence summary.

## What to build

Make `run_checks.py` take the checks config from the target branch, `origin/main`,
so a change to the config only takes effect for runs that start after it is merged.

- In `load_commands`, read the config text with
  `git show origin/main:.github/post-implementation-checks.yml`, run in `cwd` when
  one is given. Put that call in its own function,
  `_read_target_config(cwd) -> str | None`, which returns `None` when the `git`
  call fails for any reason (no such ref, not a git checkout, `git` missing).
- When `_read_target_config` returns `None`, fall back to the working-tree file,
  exactly as today. This keeps local runs and the unit tests working.
- Name the target branch once, as a module constant `TARGET_BRANCH = "main"`.
- Every evidence file gains a `config_source` key: `"origin/main"` when the config
  came from the target branch, `"working-tree"` on the fallback, and `null` when no
  config could be read at all.
- `factory/scripts/post_evidence_summary.py`: under the Checks list, add one line
  that states the config source, for example `- config: origin/main`. When the
  evidence files disagree or the key is missing, the line says `unknown`.
- Everything else stays as it is: the four check names, the CLI, the `skipped`
  rule, the error handling for a missing or malformed config, and the signatures
  of `run_build`, `run_test`, `run_lint` and `run_security`.

## Tests

- The existing tests in `factory/scripts/tests/test_run_checks.py` mock
  `run_checks.subprocess.run` for the check commands. They must keep passing: add a
  fixture there that makes `_read_target_config` return `None`, and apply it to
  the existing tests, so they keep reading the temporary config file.
- Add tests for: the target-branch config being used when `_read_target_config`
  returns text (and the working-tree file being ignored, even when it differs);
  the fallback when it returns `None`; `config_source` in the evidence for both
  cases and for a missing config; and `_read_target_config` itself returning
  `None` when `git` exits non-zero and when it raises `OSError`.
- Add tests in `factory/scripts/tests/test_post_evidence_summary.py` for the new
  config line: one source, disagreeing sources, and a missing key.

## Documents to update

- The module docstring of `factory/scripts/run_checks.py`.
- The header comment of `.github/post-implementation-checks.yml`: say that a
  change to this file applies to runs started after it is merged.
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md`:
  extend AD-6's addendum with one sentence on where the config is read from and
  why, and update the `post-implementation-checks.yml` line in the file tree.
- Do not edit `.github/workflows/light-factory.yml` — a commit touching that
  directory cannot be pushed by the pipeline's token.

## Why

Recorded as an open finding in
`_bmad-output/initiative-light-factory/deferred-work.md` (a story branch can weaken
its own mechanical checks). Known consequence, accepted: a story that adds or
changes check commands does not run them on its own run, only on later ones.
