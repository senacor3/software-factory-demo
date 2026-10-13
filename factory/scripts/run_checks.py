#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml>=6,<7"]
# ///
"""run_checks -- CAP-5's deterministic mechanical-checks script (AD-6).

Five checks -- `build`, `test`, `lint`, `security`, `static_analysis` -- every one a
plain subprocess call from this single script, never a LangGraph node or agent tool
call (AD-6). Wired into the `checks` job's workflow as 5 direct steps, each invoking
one subcommand here right after "Checkout implementation branch".

The commands are not written here: they come from the repo's own
`.github/post-implementation-checks.yml` (AD-6 addendum), so the same script checks
whatever project the repo holds. The config is read from `origin/main`, not from the
story branch's working tree, so a story cannot change the commands by editing the
config (this script itself still runs from the story branch); only when
`origin/main` cannot be read does it fall back to the working tree. Where it came from
is recorded as `config_source` in every evidence file. Each check holds a list of commands; all of them
run, in order, and the check stops at the first failure. A check with no commands
records `status: "skipped"`, never `"pass"` -- in this repo that is `security` and
`static_analysis`, by decision (user's call, 2026-10-11 and 2026-10-12). A missing or
malformed config is a `"fail"` that names the problem, never a silent skip of every
check.

Evidence is written to `evidence/checks/<name>.json` via `state_io.write_atomic`
*before* `main()` inspects the result's status to decide the exit code -- a failing
check always leaves a record, never just a non-zero exit with nothing on disk.

Usage (each `--story-slug S --run-id R`): run_checks.py build | test | lint | security | static_analysis

Exits 1 only when the written result's status is `"fail"`; 0 for `"pass"` or
`"skipped"`.

A sixth subcommand, `toolchains` (no flags), reads the same config's `toolchains:`
mapping and prints `java=`/`node=` lines shaped for `>> "$GITHUB_OUTPUT"` -- the
`checks` job's workflow steps use it to set up the Java/Node versions the configured
build/test/lint commands need, before any of the five checks above run. It writes no
evidence and exits 2 only on a missing/unreadable/malformed config.

Two more subcommands serve the `checks` job around its five check steps (AD-6 and
AD-10 addenda, backlog bug 5). `setup` (`--story-slug S --run-id R`) runs the config's
optional top-level `setup:` commands -- what prepares the checkout for the checks, e.g.
a dependency install -- so a check never relies on an earlier check having run; both
fix loops call the same `run_setup()` before each re-check. Its result goes to
`evidence/checks/setup.json`, beside the five checks' own, so a failed setup is on
record for the job that follows; it exits 1 when a command fails. `reconcile` (`--story-slug S --run-id R`) resets a stale
`checks.md` an earlier attempt's fix loop left behind, once every check has passed or
been skipped; it exits 0 whether or not it wrote anything.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state_io

CHECK_NAMES = ("build", "test", "lint", "security", "static_analysis")

TOOLCHAIN_NAMES = ("java", "node")

CONFIG_RELPATH = Path(".github") / "post-implementation-checks.yml"

PYTHON_TOKEN = "{python}"

NOT_CONFIGURED_DETAIL = f"no command configured for this check in {CONFIG_RELPATH}"

SETUP_KEY = "setup"

NO_SETUP_DETAIL = f"no `{SETUP_KEY}` command configured in {CONFIG_RELPATH}"

# Return codes a shell gives when a command could not be started at all -- 126 "found
# but not executable", 127 "not found" -- as opposed to a tool that ran and reported.
TOOLING_RETURNCODES = (126, 127)

RESOLVED_CHECKS_BODY = "## Failing checks\n\n_none_"


TARGET_BRANCH = "main"

SOURCE_TARGET = f"origin/{TARGET_BRANCH}"
SOURCE_WORKING_TREE = "working-tree"


class ChecksConfigError(Exception):
    """The checks config is missing, unreadable, or not in the expected shape.

    `source` says where the config came from (`origin/main`, `working-tree`), or is
    None when it could not be read at all.
    """

    def __init__(self, message: str, source: str | None = None):
        super().__init__(message)
        self.source = source


def _read_target_config(cwd: str | os.PathLike | None = None) -> str | None:
    """Return the checks config as it is on `origin/<TARGET_BRANCH>`, or None.

    None covers every way the read can fail -- a missing ref, a non-git directory, a
    missing git binary -- so the caller can fall back to the working tree.
    """
    try:
        proc = subprocess.run(
            ["git", "show", f"{SOURCE_TARGET}:{CONFIG_RELPATH.as_posix()}"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def load_commands(name: str, *, cwd: str | os.PathLike | None = None) -> list[list[str]]:
    """Return the commands configured for check `name`; an empty list means none.

    See `_load_config` for where the config is read from and what raises.
    """
    return _load_config(name, cwd)[0]


def _read_config_text(cwd: str | os.PathLike | None = None) -> tuple[str, str, object]:
    """Return `(text, source, path)` for the checks config, origin/main-first.

    Shared read step for `_load_config` and `load_toolchains`, so both read the same
    config the same way: from `origin/<TARGET_BRANCH>` when that can be read, else
    falling back to the working tree under `cwd`, else the working directory. Raises
    `ChecksConfigError` (with `source` left at its default, None) when neither can be
    read.
    """
    text = _read_target_config(cwd)
    if text is not None:
        return text, SOURCE_TARGET, f"{SOURCE_TARGET}:{CONFIG_RELPATH.as_posix()}"
    path = Path(cwd or ".") / CONFIG_RELPATH
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ChecksConfigError(f"checks config not found: {path}") from None
    except (OSError, UnicodeDecodeError) as e:
        raise ChecksConfigError(f"cannot read checks config {path}: {e}") from e
    return text, SOURCE_WORKING_TREE, path


def _load_config(name: str, cwd: str | os.PathLike | None = None) -> tuple[list[list[str]], str | None]:
    """Return `(commands, source)` for check `name`; no commands means none configured.

    The config is read from `origin/<TARGET_BRANCH>` so a story cannot change the
    commands by editing the config; only when that cannot be read does it fall back to the working tree under
    `cwd` (the fix loop passes the checkout it works in), else the working directory.
    Raises `ChecksConfigError` (carrying `source`) for a missing file, invalid YAML, a
    check name outside `CHECK_NAMES`, or a command that is not a non-empty list of
    strings.
    """
    # Imported here, not at module top, so importing this module (fix_loop_graph.py
    # does) needs no third-party package until a config is actually read -- mirrors
    # the graphs' own deferred `langgraph` import.
    import yaml

    text, source, path = _read_config_text(cwd)

    try:
        return _parse_commands(name, text, path, yaml), source
    except ChecksConfigError as e:
        e.source = source
        raise


def _parse_commands(name: str, text: str, path: object, yaml) -> list[list[str]]:
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ChecksConfigError(f"{path} is not valid YAML: {e}") from e

    checks = data.get("checks") if isinstance(data, dict) else None
    if not isinstance(checks, dict):
        raise ChecksConfigError(f"{path} must hold a top-level `checks` mapping")

    unknown = sorted(str(key) for key in checks if key not in CHECK_NAMES)
    if unknown:
        raise ChecksConfigError(
            f"{path} names unknown check(s) {', '.join(unknown)}; allowed: {', '.join(CHECK_NAMES)}"
        )

    return _command_list(name, checks.get(name), path)


def _command_list(name: str, commands: object, path: object) -> list[list[str]]:
    """Validate one list of commands from the config; None means none configured."""
    if commands is None:
        return []
    if not isinstance(commands, list):
        raise ChecksConfigError(f"{path}: `{name}` must be a list of commands")
    for cmd in commands:
        if not isinstance(cmd, list) or not cmd or not all(isinstance(arg, str) for arg in cmd):
            raise ChecksConfigError(
                f"{path}: every `{name}` command must be a non-empty list of strings, got {cmd!r}"
            )
    return [[arg.replace(PYTHON_TOKEN, sys.executable) for arg in cmd] for cmd in commands]


def load_setup_commands(*, cwd: str | os.PathLike | None = None) -> list[list[str]]:
    """Return the config's top-level `setup:` commands; an empty list means none.

    Read the same way `checks:` is (`_read_config_text`), and each command has the same
    shape as a check's. The key is optional -- a config without it prepares nothing.
    Raises `ChecksConfigError` (carrying `source`) for a missing/unreadable config,
    invalid YAML, or a `setup:` value that is not a list of commands.
    """
    import yaml

    text, source, path = _read_config_text(cwd)
    try:
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError as e:
            raise ChecksConfigError(f"{path} is not valid YAML: {e}") from e
        if not isinstance(data, dict):
            raise ChecksConfigError(f"{path} must hold a top-level mapping")
        return _command_list(SETUP_KEY, data.get(SETUP_KEY), path)
    except ChecksConfigError as e:
        e.source = source
        raise


def _parse_toolchains(text: str, path: object, yaml) -> dict[str, str]:
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ChecksConfigError(f"{path} is not valid YAML: {e}") from e

    toolchains = data.get("toolchains") if isinstance(data, dict) else None
    if toolchains is None:
        toolchains = {}
    if not isinstance(toolchains, dict):
        raise ChecksConfigError(f"{path}: `toolchains` must be a mapping")

    unknown = sorted(str(key) for key in toolchains if key not in TOOLCHAIN_NAMES)
    if unknown:
        raise ChecksConfigError(
            f"{path} names unknown toolchain(s) {', '.join(unknown)}; allowed: {', '.join(TOOLCHAIN_NAMES)}"
        )

    result: dict[str, str] = {}
    for name in TOOLCHAIN_NAMES:
        value = toolchains.get(name)
        if value is None:
            result[name] = ""
        elif isinstance(value, str):
            result[name] = value
        else:
            raise ChecksConfigError(f"{path}: `toolchains.{name}` must be a string, got {value!r}")
    return result


def load_toolchains(*, cwd: str | os.PathLike | None = None) -> dict[str, str]:
    """Return `{"java": ..., "node": ...}` from the config's `toolchains:` mapping.

    Reuses `_load_config`'s own origin/main-with-working-tree-fallback read (via
    `_read_config_text`), so this reads the exact same config `checks:` does. A
    missing `toolchains:` key, or a missing key within it, maps to `""` rather than
    raising -- the workflow's `if:` gates treat an empty string as "no setup needed",
    mirroring `state_io.py`'s `cmd_derive` output convention rather than
    `_parse_commands`'s "absent means fail" posture for `checks:` itself. Raises
    `ChecksConfigError` (carrying `source`) for a missing/unreadable config, invalid
    YAML, a `toolchains:` value that isn't a mapping, an unknown toolchain name, or a
    version value that isn't a string -- same "fail loud on malformed, never a silent
    skip" posture `_parse_commands` already applies to `checks:`.
    """
    import yaml

    text, source, path = _read_config_text(cwd)
    try:
        return _parse_toolchains(text, path, yaml)
    except ChecksConfigError as e:
        e.source = source
        raise


def _write_evidence(
    name: str,
    story_slug: str,
    run_id: str,
    result: dict,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
) -> Path:
    path = (
        state_io.state_dir(story_slug, run_id, base=state_base)
        / "evidence"
        / "checks"
        / f"{name}.json"
    )
    state_io.write_atomic(path, json.dumps(result, indent=2) + "\n")
    return path


def _run_command(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> dict:
    """Run `cmd` and return its result dict, writing nothing.

    A non-zero exit is a legitimate `status: "fail"` result, not a script error --
    this never raises for that. Only an OSError (e.g. the command isn't on PATH) is
    caught and folded into the same fail shape, so a missing tool is reported the
    same way a real failure is, not conflated with an uncaught crash.
    """
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        return {
            "status": "fail",
            "command": cmd,
            "returncode": None,
            "detail": f"failed to run {cmd!r}: {e}",
        }
    status = "pass" if proc.returncode == 0 else "fail"
    # Concatenate both streams rather than preferring stderr -- a command run via
    # `uv run --with X X ...` (lint's `ruff`, test's `pytest`) writes uv's own
    # download/install banner to stderr and the wrapped tool's real findings to
    # stdout; picking stderr-first (the previous behavior) silently discarded the
    # actionable output and surfaced only uv's noise. Discovered live during
    # ticket 13's end-to-end run.
    detail = "" if status == "pass" else "\n".join(p for p in (proc.stdout.strip(), proc.stderr.strip()) if p)
    return {"status": status, "command": cmd, "returncode": proc.returncode, "detail": detail}


def run_check(
    name: str,
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Run check `name`'s configured commands, write its evidence, return the result.

    The result keeps one shape whatever the outcome: `status`, `command`,
    `returncode`, `detail` are those of the failing command, or of the last one when
    all pass, and `commands` lists every command that ran.
    """
    try:
        commands, source = _load_config(name, cwd)
    except ChecksConfigError as e:
        result = {"status": "fail", "command": None, "returncode": None, "detail": str(e), "commands": []}
        source = e.source
    else:
        if not commands:
            result = {"status": "skipped", "command": None, "returncode": None, "detail": NOT_CONFIGURED_DETAIL, "commands": []}
        else:
            ran = []
            for cmd in commands:
                result = _run_command(cmd, cwd=cwd)
                ran.append(cmd)
                if result["status"] == "fail":
                    break
            result["commands"] = ran
    result["config_source"] = source

    _write_evidence(name, story_slug, run_id, result, state_base=state_base)
    return result


def run_setup(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Run the config's `setup:` commands in order, stopping at the first failure.

    Returns the same result shape `run_check` does (`skipped` when no command is
    configured) and writes it to `evidence/checks/setup.json`. Setup is not one of the
    five checks -- it is what they all rely on -- but its result has to outlive the job
    that ran it the same way theirs does, so a failed setup can be named afterwards
    instead of read off the checks that then failed for want of it. A config that
    cannot be read is a `"fail"`, never raised.
    """
    try:
        commands = load_setup_commands(cwd=cwd)
    except ChecksConfigError as e:
        result = {"status": "fail", "command": None, "returncode": None, "detail": str(e), "commands": []}
    else:
        if not commands:
            result = {"status": "skipped", "command": None, "returncode": None, "detail": NO_SETUP_DETAIL, "commands": []}
        else:
            ran = []
            for cmd in commands:
                result = _run_command(cmd, cwd=cwd)
                ran.append(cmd)
                if result["status"] == "fail":
                    break
            result["commands"] = ran

    _write_evidence(SETUP_KEY, story_slug, run_id, result, state_base=state_base)
    return result


def read_setup_result(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
) -> dict | None:
    """Return the last recorded setup result, or None when there is none to read.

    None is not a failure: a config without `setup:` commands still records `skipped`,
    but a run started before setup existed has no file at all.
    """
    path = state_io.state_dir(story_slug, run_id, base=state_base) / "evidence" / "checks" / f"{SETUP_KEY}.json"
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    return result if isinstance(result, dict) else None


def is_tooling_failure(result: dict) -> bool:
    """True when a failed result's command could not be started at all.

    That is a shell's 126/127, or no return code because spawning it raised (see
    `_run_command`) -- a broken runner, not a finding in the code under check. A
    result that names no command (missing evidence, an unreadable config) is not one.
    """
    return (
        result.get("status") == "fail"
        and result.get("command") is not None
        and (result.get("returncode") is None or result.get("returncode") in TOOLING_RETURNCODES)
    )


def reconcile_checks_state(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
) -> bool:
    """Reset a stale `checks.md` once every check has passed or been skipped.

    `checks.md` is written by the checks fix loop, which only runs when the `checks`
    job failed -- so when a later attempt of that job goes green, nothing else would
    correct what an earlier attempt's loop stamped. This is the one case the `checks`
    job writes the file: it must already exist with a status other than `resolved`,
    all five evidence files must read `pass` or `skipped`, and the recorded setup must
    not have failed. The `fix_cycle` count is carried over, never reset. Returns
    whether the file was rewritten.
    """
    directory = state_io.state_dir(story_slug, run_id, base=state_base)
    checks_path = directory / "checks.md"
    try:
        meta, _ = state_io.read_state(checks_path)
    except (FileNotFoundError, ValueError):
        return False
    if meta.get("status") == "resolved":
        return False
    setup = read_setup_result(story_slug, run_id, state_base=state_base)
    if setup is not None and setup.get("status") == "fail":
        return False
    for name in CHECK_NAMES:
        try:
            evidence = json.loads((directory / "evidence" / "checks" / f"{name}.json").read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return False
        if not isinstance(evidence, dict) or evidence.get("status") not in ("pass", "skipped"):
            return False
    state_io.write_state(
        checks_path,
        story_slug=story_slug,
        stage="checks",
        status="resolved",
        body=RESOLVED_CHECKS_BODY,
        extra={"fix_cycle": meta.get("fix_cycle", 0)},
    )
    return True


def run_build(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    return run_check("build", story_slug, run_id, state_base=state_base, cwd=cwd)


def run_test(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    return run_check("test", story_slug, run_id, state_base=state_base, cwd=cwd)


def run_lint(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    return run_check("lint", story_slug, run_id, state_base=state_base, cwd=cwd)


def run_security(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    return run_check("security", story_slug, run_id, state_base=state_base, cwd=cwd)


def run_static_analysis(
    story_slug: str,
    run_id: str,
    *,
    state_base: str | os.PathLike = state_io.FACTORY_DIR,
    cwd: str | os.PathLike | None = None,
) -> dict:
    return run_check("static_analysis", story_slug, run_id, state_base=state_base, cwd=cwd)


# --- CLI ---------------------------------------------------------------------


def _add_check_subparser(sub, name: str):
    pc = sub.add_parser(name, help=f"run the {name} check")
    pc.add_argument("--story-slug", required=True)
    pc.add_argument("--run-id", required=True)
    pc.set_defaults(check=name)
    return pc


def cmd_toolchains(args) -> int:
    """Print the config's `toolchains:` versions as `java=`/`node=` lines.

    Shaped for direct `>> "$GITHUB_OUTPUT"` redirection, mirroring `state_io.py`'s
    `cmd_derive`. A key absent from the config prints as an empty value (`java=`),
    never raises -- only a missing/unreadable/malformed config is an error.
    """
    try:
        toolchains = load_toolchains()
    except ChecksConfigError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    for name in TOOLCHAIN_NAMES:
        print(f"{name}={toolchains[name]}")
    return 0


def cmd_setup(args) -> int:
    """Run the config's `setup:` commands; exit 1 when one fails, 0 otherwise."""
    result = run_setup(args.story_slug, args.run_id)
    print(json.dumps(result))
    return 1 if result["status"] == "fail" else 0


def cmd_reconcile(args) -> int:
    """Reset a stale `checks.md` when every check passed; exit 0 either way."""
    reconciled = reconcile_checks_state(args.story_slug, args.run_id)
    print(json.dumps({"ok": True, "reconciled": reconciled}))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in CHECK_NAMES:
        _add_check_subparser(sub, name)
    sub.add_parser("toolchains", help="print configured runner toolchain versions (java=/node=)")
    ps = sub.add_parser(SETUP_KEY, help="run the configured setup commands that prepare the checkout for the checks")
    ps.add_argument("--story-slug", required=True)
    ps.add_argument("--run-id", required=True)
    pr = sub.add_parser("reconcile", help="reset a stale checks.md once every check passed or was skipped")
    pr.add_argument("--story-slug", required=True)
    pr.add_argument("--run-id", required=True)

    args = p.parse_args(argv)

    if args.cmd == "toolchains":
        return cmd_toolchains(args)
    if args.cmd == SETUP_KEY:
        return cmd_setup(args)
    if args.cmd == "reconcile":
        return cmd_reconcile(args)

    result = run_check(args.check, args.story_slug, args.run_id)
    print(json.dumps(result))
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())
