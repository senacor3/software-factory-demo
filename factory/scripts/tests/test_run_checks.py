# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0", "pyyaml>=6,<7"]
# ///
"""Tests for run_checks.py. Run:
uv run --with pytest --with pyyaml pytest factory/scripts/tests/test_run_checks.py

Covers the I/O & Edge-Case Matrix in story-configurable-mechanical-checks-plan.md:
a configured check passing and failing (status, exit code, evidence content), a
command missing from PATH, a check with no command (skipped, never "pass", no
subprocess), a missing or malformed config and an unknown check name (all "fail",
never raised), several commands per check, and that this repo's real config yields
the commands the script used to hard-code. `subprocess.run` is mocked throughout --
no real `compileall`/`pytest`/`ruff` subprocess in the committed suite (mirrors
test_commit_push_implementation.py).
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import run_checks
import state_io

REPO_ROOT = Path(__file__).resolve().parents[3]

# The autouse fixture below replaces `run_checks._read_target_config`; keep the real one.
_real_read_target_config = run_checks._read_target_config

CONFIG = """\
checks:
  build:
    - ["{python}", "-m", "compileall", "src", "-q"]
  test:
    - ["run-tests", "backend"]
    - ["run-tests", "frontend"]
  lint:
    - ["run-lint"]
"""


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(returncode=1, stderr="boom", stdout=""):
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


def _write_config(repo: Path, text: str = CONFIG) -> Path:
    path = repo / run_checks.CONFIG_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


@pytest.fixture(autouse=True)
def no_target_config():
    """Default every test to the working-tree config; target-branch tests re-patch."""
    with patch("run_checks._read_target_config", return_value=None) as mock:
        yield mock


@pytest.fixture
def repo(tmp_path):
    """A checkout holding a checks config; also used as the state base."""
    _write_config(tmp_path)
    return tmp_path


def _evidence(repo, name):
    path = state_io.state_dir("foo-bar", "run-1", base=repo) / "evidence" / "checks" / f"{name}.json"
    return json.loads(path.read_text())


def _run(name, repo):
    return run_checks.run_check(name, "foo-bar", "run-1", state_base=repo, cwd=repo)


# --- configured check: pass ----------------------------------------------------


def test_configured_check_pass_runs_the_configured_command(repo):
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = _run("lint", repo)

    assert result["status"] == "pass"
    assert mock_run.call_args.args[0] == ["run-lint"]
    assert mock_run.call_args.kwargs["cwd"] == repo
    assert result["commands"] == [["run-lint"]]
    assert _evidence(repo, "lint")["status"] == "pass"


def test_python_token_is_replaced_with_the_running_interpreter(repo):
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        _run("build", repo)

    assert mock_run.call_args.args[0] == [sys.executable, "-m", "compileall", "src", "-q"]


def test_all_commands_of_a_check_run_in_order(repo):
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = _run("test", repo)

    assert [c.args[0] for c in mock_run.call_args_list] == [["run-tests", "backend"], ["run-tests", "frontend"]]
    assert result["status"] == "pass"
    assert result["command"] == ["run-tests", "frontend"]
    assert _evidence(repo, "test")["commands"] == [["run-tests", "backend"], ["run-tests", "frontend"]]


# --- configured check: fail ----------------------------------------------------


def test_configured_check_fail_captures_both_streams(repo):
    findings = "src/x.py:1:1: F401 `os` imported but unused"
    with patch("run_checks.subprocess.run", return_value=_fail(stdout=findings, stderr="Installed 1 package")):
        result = _run("lint", repo)

    assert result["status"] == "fail"
    assert "F401" in result["detail"]
    assert "Installed 1 package" in result["detail"]
    written = _evidence(repo, "lint")
    assert written["status"] == "fail"
    assert written["returncode"] == 1
    assert "F401" in written["detail"]


def test_check_stops_at_the_first_failing_command(repo):
    with patch("run_checks.subprocess.run", return_value=_fail(stderr="1 failed")) as mock_run:
        result = _run("test", repo)

    assert mock_run.call_count == 1
    assert result["status"] == "fail"
    assert result["command"] == ["run-tests", "backend"]
    assert result["commands"] == [["run-tests", "backend"]]
    assert "1 failed" in _evidence(repo, "test")["detail"]


def test_command_not_on_path_is_reported_as_fail_not_raised(repo):
    with patch("run_checks.subprocess.run", side_effect=OSError("run-lint not found")):
        result = _run("lint", repo)

    assert result["status"] == "fail"
    assert "run-lint" in result["detail"]
    assert "not found" in result["detail"]
    assert _evidence(repo, "lint")["status"] == "fail"


# --- check not configured: skipped, never pass -----------------------------------


@pytest.mark.parametrize(
    "config",
    [CONFIG, CONFIG + "  security: []\n", CONFIG + "  security:\n"],
    ids=["no entry", "empty list", "null"],
)
def test_unconfigured_check_is_skipped_and_runs_no_command(tmp_path, config):
    _write_config(tmp_path, config)
    with patch("run_checks.subprocess.run") as mock_run:
        result = _run("security", tmp_path)

    mock_run.assert_not_called()
    assert result["status"] == "skipped"
    assert result["command"] is None
    written = _evidence(tmp_path, "security")
    assert written["status"] == "skipped"
    assert written["command"] is None
    assert written["returncode"] is None


def test_configured_security_command_runs_like_any_other(tmp_path):
    _write_config(tmp_path, CONFIG + '  security:\n    - ["scan", "src"]\n')
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = _run("security", tmp_path)

    assert mock_run.call_args.args[0] == ["scan", "src"]
    assert result["status"] == "pass"


# --- config errors: fail with a reason, never raised, never a silent skip --------


def test_missing_config_is_a_fail_naming_the_expected_path(tmp_path):
    with patch("run_checks.subprocess.run") as mock_run:
        result = _run("build", tmp_path)

    mock_run.assert_not_called()
    assert result["status"] == "fail"
    assert str(run_checks.CONFIG_RELPATH) in result["detail"]
    assert _evidence(tmp_path, "build")["status"] == "fail"


@pytest.mark.parametrize(
    ("config", "expected"),
    [
        ("checks: [unclosed", "not valid YAML"),
        ("- just\n- a list\n", "top-level `checks` mapping"),
        ("checks:\n  build: compile\n", "must be a list of commands"),
        ("checks:\n  build:\n    - compile everything\n", "non-empty list of strings"),
        ("checks:\n  build:\n    - [compile, 3]\n", "non-empty list of strings"),
        ("checks:\n  build:\n    - []\n", "non-empty list of strings"),
    ],
    ids=["bad syntax", "no checks mapping", "command not a list", "command a string", "non-string arg", "empty command"],
)
def test_malformed_config_is_a_fail_naming_the_file_and_problem(tmp_path, config, expected):
    _write_config(tmp_path, config)
    with patch("run_checks.subprocess.run") as mock_run:
        result = _run("build", tmp_path)

    mock_run.assert_not_called()
    assert result["status"] == "fail"
    assert str(run_checks.CONFIG_RELPATH) in result["detail"]
    assert expected in result["detail"]
    assert _evidence(tmp_path, "build")["status"] == "fail"


def test_undecodable_config_is_a_fail_not_raised(tmp_path):
    _write_config(tmp_path).write_bytes(b"checks:\n  build:\n    - [caf\xe9]\n")
    with patch("run_checks.subprocess.run") as mock_run:
        result = _run("build", tmp_path)

    mock_run.assert_not_called()
    assert result["status"] == "fail"
    assert str(run_checks.CONFIG_RELPATH) in result["detail"]
    assert _evidence(tmp_path, "build")["status"] == "fail"


def test_empty_string_argument_is_a_valid_argument(tmp_path):
    _write_config(tmp_path, 'checks:\n  lint:\n    - ["grep", "", "file"]\n')
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = _run("lint", tmp_path)

    assert mock_run.call_args.args[0] == ["grep", "", "file"]
    assert result["status"] == "pass"


def test_unknown_check_name_fails_the_check_being_run(tmp_path):
    _write_config(tmp_path, CONFIG + '  deploy:\n    - ["ship-it"]\n')
    with patch("run_checks.subprocess.run") as mock_run:
        result = _run("build", tmp_path)

    mock_run.assert_not_called()
    assert result["status"] == "fail"
    assert "deploy" in result["detail"]
    assert _evidence(tmp_path, "build")["status"] == "fail"


# --- the per-check functions fix_loop_graph.py calls ------------------------------


@pytest.mark.parametrize(
    ("runner", "name"),
    [
        (run_checks.run_build, "build"),
        (run_checks.run_test, "test"),
        (run_checks.run_lint, "lint"),
        (run_checks.run_security, "security"),
        (run_checks.run_static_analysis, "static_analysis"),
    ],
)
def test_named_runners_run_their_own_check(repo, runner, name):
    with patch("run_checks.subprocess.run", return_value=_ok()):
        result = runner("foo-bar", "run-1", state_base=repo, cwd=repo)

    assert result["status"] == ("skipped" if name in ("security", "static_analysis") else "pass")
    assert _evidence(repo, name)["status"] == result["status"]


# --- this repo's own config ------------------------------------------------------


def test_repo_config_holds_the_commands_the_script_used_to_hard_code():
    # Each list's first entry is still factory/'s own original command, untouched;
    # the freight-tenders backend/frontend commands are appended after it.
    assert run_checks.load_commands("build", cwd=REPO_ROOT) == [
        [sys.executable, "-m", "compileall", "factory", "-q"],
        ["bash", "-c", 'JAVA_HOME="$JAVA_HOME_25_X64" mvn -B -f freight-tenders/backend/pom.xml compile'],
        ["npm", "--prefix", "freight-tenders/frontend", "run", "build"],
    ]
    # The dependency install every frontend command relies on is setup, not part of
    # `build` -- the checks fix loop re-runs only the failed checks (backlog bug 5).
    assert run_checks.load_setup_commands(cwd=REPO_ROOT) == [
        ["npm", "--prefix", "freight-tenders/frontend", "ci"],
    ]
    # Unchanged apart from `--with pyyaml`, which this module's own tests now need.
    assert run_checks.load_commands("test", cwd=REPO_ROOT) == [
        ["uv", "run", "--with", "pytest", "--with", "pyyaml", "pytest", "factory/graph/tests/", "factory/scripts/tests/"],
        ["bash", "-c", 'JAVA_HOME="$JAVA_HOME_25_X64" mvn -B -f freight-tenders/backend/pom.xml test'],
        ["npm", "--prefix", "freight-tenders/frontend", "test", "--", "--watch=false"],
    ]
    assert run_checks.load_commands("lint", cwd=REPO_ROOT) == [
        ["uv", "run", "--with", "ruff", "ruff", "check", "factory/"],
        ["bash", "-c", 'JAVA_HOME="$JAVA_HOME_25_X64" mvn -B -f freight-tenders/backend/pom.xml spotless:check'],
        ["npm", "--prefix", "freight-tenders/frontend", "run", "lint"],
    ]
    assert run_checks.load_commands("security", cwd=REPO_ROOT) == []
    # The toolchain versions those appended mvn/npm commands need (AD-6 addendum).
    assert run_checks.load_toolchains(cwd=REPO_ROOT) == {"java": "25", "node": "26"}


# --- config read from the target branch -------------------------------------------------


TARGET_CONFIG = """\
checks:
  lint:
    - ["target-lint"]
"""


def test_target_config_is_used_and_working_tree_ignored(repo, no_target_config):
    no_target_config.return_value = TARGET_CONFIG
    with patch("run_checks.subprocess.run", return_value=_ok()) as mock_run:
        result = _run("lint", repo)

    assert mock_run.call_args.args[0] == ["target-lint"]
    assert result["status"] == "pass"
    assert result["config_source"] == "origin/main"
    assert _evidence(repo, "lint")["config_source"] == "origin/main"


def test_working_tree_is_used_when_target_config_unreadable(repo):
    with patch("run_checks.subprocess.run", return_value=_ok()):
        result = _run("lint", repo)

    assert result["config_source"] == "working-tree"
    assert _evidence(repo, "lint")["config_source"] == "working-tree"


def test_missing_config_everywhere_fails_with_null_source(tmp_path):
    result = _run("lint", tmp_path)

    assert result["status"] == "fail"
    assert result["config_source"] is None
    assert _evidence(tmp_path, "lint")["config_source"] is None


def test_target_config_disabling_a_check_skips_it_despite_working_tree(repo, no_target_config):
    no_target_config.return_value = "checks:\n  test: []\n"
    with patch("run_checks.subprocess.run") as mock_run:
        result = _run("test", repo)

    mock_run.assert_not_called()
    assert result["status"] == "skipped"
    assert result["config_source"] == "origin/main"


def test_malformed_target_config_is_a_fail_with_target_source(repo, no_target_config):
    no_target_config.return_value = "checks: [unclosed"
    result = _run("lint", repo)

    assert result["status"] == "fail"
    assert "not valid YAML" in result["detail"]
    assert result["config_source"] == "origin/main"


def test_read_target_config_returns_stdout_and_runs_git_show(tmp_path):
    with patch("run_checks.subprocess.run", return_value=_ok("checks: {}\n")) as mock_run:
        text = _real_read_target_config(tmp_path)

    assert text == "checks: {}\n"
    assert mock_run.call_args.args[0] == ["git", "show", "origin/main:.github/post-implementation-checks.yml"]
    assert mock_run.call_args.kwargs["cwd"] == tmp_path


def test_read_target_config_returns_none_on_nonzero_exit(tmp_path):
    with patch("run_checks.subprocess.run", return_value=_fail(returncode=128)):
        assert _real_read_target_config(tmp_path) is None


def test_read_target_config_returns_none_on_oserror(tmp_path):
    with patch("run_checks.subprocess.run", side_effect=FileNotFoundError("git")):
        assert _real_read_target_config(tmp_path) is None


# --- CLI: exit codes ---------------------------------------------------------------


def test_cli_exits_zero_on_pass(repo, monkeypatch):
    monkeypatch.chdir(repo)
    with patch("run_checks.subprocess.run", return_value=_ok()):
        rc = run_checks.main(["build", "--story-slug", "foo-bar", "--run-id", "run-1"])

    assert rc == 0


def test_cli_exits_nonzero_on_fail_after_writing_evidence(repo, monkeypatch):
    monkeypatch.chdir(repo)
    with patch("run_checks.subprocess.run", return_value=_fail()):
        rc = run_checks.main(["test", "--story-slug", "foo-bar", "--run-id", "run-1"])

    assert rc == 1
    assert _evidence(repo / state_io.FACTORY_DIR, "test")["status"] == "fail"


def test_cli_exits_zero_on_skipped(repo, monkeypatch):
    monkeypatch.chdir(repo)
    rc = run_checks.main(["security", "--story-slug", "foo-bar", "--run-id", "run-1"])

    assert rc == 0


def test_cli_exits_nonzero_when_the_config_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rc = run_checks.main(["lint", "--story-slug", "foo-bar", "--run-id", "run-1"])

    assert rc == 1
    assert _evidence(tmp_path / state_io.FACTORY_DIR, "lint")["status"] == "fail"


def test_cli_requires_story_slug_and_run_id():
    with pytest.raises(SystemExit):
        run_checks.main(["build"])


# --- toolchains: present, absent, malformed ---------------------------------------

TOOLCHAIN_CONFIG = CONFIG + "toolchains:\n  java: '25'\n  node: '26'\n"


def test_load_toolchains_returns_configured_versions(tmp_path):
    _write_config(tmp_path, TOOLCHAIN_CONFIG)
    assert run_checks.load_toolchains(cwd=tmp_path) == {"java": "25", "node": "26"}


def test_load_toolchains_missing_key_is_empty_string(tmp_path):
    _write_config(tmp_path, CONFIG + "toolchains:\n  java: '25'\n")
    assert run_checks.load_toolchains(cwd=tmp_path) == {"java": "25", "node": ""}


def test_load_toolchains_absent_mapping_is_all_empty(repo):
    assert run_checks.load_toolchains(cwd=repo) == {"java": "", "node": ""}


def test_load_toolchains_null_mapping_is_all_empty(tmp_path):
    _write_config(tmp_path, CONFIG + "toolchains:\n")
    assert run_checks.load_toolchains(cwd=tmp_path) == {"java": "", "node": ""}


def test_load_toolchains_rejects_non_mapping(tmp_path):
    _write_config(tmp_path, CONFIG + "toolchains:\n  - java\n  - node\n")
    with pytest.raises(run_checks.ChecksConfigError, match="must be a mapping"):
        run_checks.load_toolchains(cwd=tmp_path)


def test_load_toolchains_rejects_unknown_toolchain(tmp_path):
    _write_config(tmp_path, CONFIG + "toolchains:\n  python: '3.13'\n")
    with pytest.raises(run_checks.ChecksConfigError, match="python"):
        run_checks.load_toolchains(cwd=tmp_path)


def test_load_toolchains_rejects_non_string_version(tmp_path):
    _write_config(tmp_path, CONFIG + "toolchains:\n  java: 25\n")
    with pytest.raises(run_checks.ChecksConfigError, match="must be a string"):
        run_checks.load_toolchains(cwd=tmp_path)


def test_load_toolchains_missing_config_raises(tmp_path):
    with pytest.raises(run_checks.ChecksConfigError, match=str(run_checks.CONFIG_RELPATH)):
        run_checks.load_toolchains(cwd=tmp_path)


def test_load_toolchains_malformed_yaml_raises(tmp_path):
    _write_config(tmp_path, "toolchains: [unclosed")
    with pytest.raises(run_checks.ChecksConfigError, match="not valid YAML"):
        run_checks.load_toolchains(cwd=tmp_path)


def test_load_toolchains_reads_from_target_branch(repo, no_target_config):
    no_target_config.return_value = CONFIG + "toolchains:\n  java: '21'\n"
    assert run_checks.load_toolchains(cwd=repo) == {"java": "21", "node": ""}


# --- CLI: toolchains subcommand ----------------------------------------------------


def test_cmd_toolchains_prints_java_and_node_lines(tmp_path, monkeypatch, capsys):
    _write_config(tmp_path, TOOLCHAIN_CONFIG)
    monkeypatch.chdir(tmp_path)
    rc = run_checks.main(["toolchains"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "java=25" in out
    assert "node=26" in out


def test_cmd_toolchains_prints_empty_values_when_absent(repo, monkeypatch, capsys):
    monkeypatch.chdir(repo)
    rc = run_checks.main(["toolchains"])

    assert rc == 0
    out = capsys.readouterr().out
    assert "java=\n" in out
    assert "node=\n" in out


def test_cmd_toolchains_exits_nonzero_on_malformed_config(tmp_path, monkeypatch, capsys):
    _write_config(tmp_path, CONFIG + "toolchains:\n  python: '3.13'\n")
    monkeypatch.chdir(tmp_path)
    rc = run_checks.main(["toolchains"])

    assert rc == 2
    assert "python" in capsys.readouterr().err


# --- setup: commands that prepare the checkout for the checks (backlog bug 5) ----------


SETUP_CONFIG = CONFIG + """\
setup:
  - ["install-deps", "backend"]
  - ["{python}", "-m", "install", "frontend"]
"""


def test_load_setup_commands_returns_the_configured_commands(tmp_path):
    _write_config(tmp_path, SETUP_CONFIG)
    assert run_checks.load_setup_commands(cwd=tmp_path) == [
        ["install-deps", "backend"],
        [sys.executable, "-m", "install", "frontend"],
    ]


def test_load_setup_commands_absent_key_is_empty(repo):
    assert run_checks.load_setup_commands(cwd=repo) == []


def test_load_setup_commands_needs_no_checks_mapping(tmp_path):
    _write_config(tmp_path, 'setup:\n  - ["install-deps"]\n')
    assert run_checks.load_setup_commands(cwd=tmp_path) == [["install-deps"]]


@pytest.mark.parametrize(
    "config, expected",
    [
        ("setup: install-deps\n", "`setup` must be a list of commands"),
        ("setup:\n  - install-deps\n", "every `setup` command must be a non-empty list of strings"),
        ("setup:\n  - []\n", "every `setup` command must be a non-empty list of strings"),
        ("setup: [unclosed\n", "is not valid YAML"),
        # Not a mapping at the top level: never read as "no setup configured".
        ("", "must hold a top-level mapping"),
        ("- setup\n", "must hold a top-level mapping"),
    ],
)
def test_load_setup_commands_rejects_a_malformed_value(tmp_path, config, expected):
    _write_config(tmp_path, config)
    with pytest.raises(run_checks.ChecksConfigError, match=expected) as excinfo:
        run_checks.load_setup_commands(cwd=tmp_path)
    assert excinfo.value.source == run_checks.SOURCE_WORKING_TREE


def test_load_setup_commands_reads_from_target_branch(repo, no_target_config):
    no_target_config.return_value = 'setup:\n  - ["target-install"]\n'
    assert run_checks.load_setup_commands(cwd=repo) == [["target-install"]]


def _setup(repo):
    return run_checks.run_setup("foo-bar", "run-1", state_base=repo, cwd=repo)


def test_run_setup_runs_every_command_in_order_and_records_the_result(tmp_path):
    _write_config(tmp_path, SETUP_CONFIG)
    with patch("subprocess.run", return_value=_ok()) as mock_run:
        result = _setup(tmp_path)

    assert result["status"] == "pass"
    assert [c.args[0] for c in mock_run.call_args_list] == [
        ["install-deps", "backend"],
        [sys.executable, "-m", "install", "frontend"],
    ]
    assert result["commands"] == [c.args[0] for c in mock_run.call_args_list]
    assert all(c.kwargs["cwd"] == tmp_path for c in mock_run.call_args_list)
    # recorded beside the five checks' evidence, so the next job can read it
    assert _evidence(tmp_path, "setup") == result
    assert run_checks.read_setup_result("foo-bar", "run-1", state_base=tmp_path) == result


def test_run_setup_stops_at_the_first_failing_command(tmp_path):
    _write_config(tmp_path, SETUP_CONFIG)
    with patch("subprocess.run", return_value=_fail(returncode=1, stderr="registry down")) as mock_run:
        result = _setup(tmp_path)

    assert result["status"] == "fail"
    assert result["command"] == ["install-deps", "backend"]
    assert "registry down" in result["detail"]
    mock_run.assert_called_once()
    assert _evidence(tmp_path, "setup")["status"] == "fail"


def test_run_setup_with_no_command_is_skipped_and_runs_nothing(repo):
    with patch("subprocess.run") as mock_run:
        result = _setup(repo)

    assert result["status"] == "skipped"
    assert result["commands"] == []
    mock_run.assert_not_called()
    assert _evidence(repo, "setup")["status"] == "skipped"


def test_run_setup_missing_config_is_a_fail_not_raised(tmp_path):
    with patch("subprocess.run") as mock_run:
        result = _setup(tmp_path)

    assert result["status"] == "fail"
    assert result["command"] is None
    assert "checks config not found" in result["detail"]
    mock_run.assert_not_called()
    assert _evidence(tmp_path, "setup")["status"] == "fail"


def test_read_setup_result_is_none_when_nothing_was_recorded(tmp_path):
    assert run_checks.read_setup_result("foo-bar", "run-1", state_base=tmp_path) is None


SETUP_ARGS = ["setup", "--story-slug", "foo-bar", "--run-id", "run-1"]


def test_cli_setup_exits_zero_on_pass_and_on_skipped(tmp_path, repo, monkeypatch, capsys):
    monkeypatch.chdir(repo)
    assert run_checks.main(SETUP_ARGS) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "skipped"

    _write_config(repo, SETUP_CONFIG)
    with patch("subprocess.run", return_value=_ok()):
        assert run_checks.main(SETUP_ARGS) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "pass"
    assert _evidence(repo / state_io.FACTORY_DIR, "setup")["status"] == "pass"


def test_cli_setup_exits_nonzero_when_a_command_fails(tmp_path, monkeypatch, capsys):
    _write_config(tmp_path, SETUP_CONFIG)
    monkeypatch.chdir(tmp_path)
    with patch("subprocess.run", return_value=_fail(returncode=127, stderr="install-deps: not found")):
        assert run_checks.main(SETUP_ARGS) == 1
    assert json.loads(capsys.readouterr().out)["returncode"] == 127


def test_cli_setup_requires_story_slug_and_run_id():
    with pytest.raises(SystemExit):
        run_checks.main(["setup"])


# --- tooling failure: the command could not be started at all ---------------------------


@pytest.mark.parametrize(
    "result, expected",
    [
        ({"status": "fail", "command": ["npm", "run", "lint"], "returncode": 127, "detail": "ng: not found"}, True),
        ({"status": "fail", "command": ["./gradlew"], "returncode": 126, "detail": "Permission denied"}, True),
        # `_run_command`'s shape when spawning the command raised OSError.
        ({"status": "fail", "command": ["mvn"], "returncode": None, "detail": "failed to run"}, True),
        # A tool that ran and reported a finding.
        ({"status": "fail", "command": ["npm", "run", "lint"], "returncode": 1, "detail": "1 error"}, False),
        ({"status": "fail", "command": ["mvn"], "returncode": 2, "detail": "usage"}, False),
        # No command named: missing evidence or an unreadable config, not a tool that would not start.
        ({"status": "fail", "command": None, "returncode": None, "detail": "no evidence found"}, False),
        ({"status": "pass", "command": ["x"], "returncode": 0, "detail": ""}, False),
        ({"status": "skipped", "command": None, "returncode": None, "detail": ""}, False),
    ],
)
def test_is_tooling_failure(result, expected):
    assert run_checks.is_tooling_failure(result) is expected


def test_command_not_on_path_result_is_a_tooling_failure(repo):
    with patch("subprocess.run", side_effect=FileNotFoundError("run-lint")):
        result = _run("lint", repo)
    assert run_checks.is_tooling_failure(result)


# --- reconcile: a later passing attempt corrects a stale checks.md ----------------------


def _write_all_evidence(base, statuses=None):
    statuses = statuses or {}
    directory = state_io.state_dir("foo-bar", "run-1", base=base) / "evidence" / "checks"
    directory.mkdir(parents=True, exist_ok=True)
    for name in run_checks.CHECK_NAMES:
        status = statuses.get(name, "skipped" if name == "security" else "pass")
        (directory / f"{name}.json").write_text(json.dumps({"status": status, "command": ["x"], "returncode": 0, "detail": ""}))


def _write_checks_md(base, status, fix_cycle=2, body="## Failing checks\n\n- **lint**: sh: 1: ng: not found"):
    path = state_io.state_dir("foo-bar", "run-1", base=base) / "checks.md"
    state_io.write_state(path, story_slug="foo-bar", stage="checks", status=status, body=body, extra={"fix_cycle": fix_cycle})
    return path


@pytest.mark.parametrize("stale_status", ["unresolved-after-cap", "tooling-failure", "findings-open"])
def test_reconcile_resets_a_stale_checks_md_when_every_check_passed_or_skipped(tmp_path, stale_status):
    _write_all_evidence(tmp_path)
    path = _write_checks_md(tmp_path, stale_status, fix_cycle=2)

    assert run_checks.reconcile_checks_state("foo-bar", "run-1", state_base=tmp_path) is True

    meta, body = state_io.read_state(path)
    assert meta["status"] == "resolved"
    assert meta["stage"] == "checks"
    assert meta["story_slug"] == "foo-bar"
    assert meta["fix_cycle"] == "2"  # how many fix cycles the run used is kept, never reset
    assert "_none_" in body
    assert "lint" not in body and "ng: not found" not in body


def test_reconcile_leaves_checks_md_alone_while_any_check_still_fails(tmp_path):
    _write_all_evidence(tmp_path, {"lint": "fail"})
    path = _write_checks_md(tmp_path, "unresolved-after-cap")
    before = path.read_text()

    assert run_checks.reconcile_checks_state("foo-bar", "run-1", state_base=tmp_path) is False
    assert path.read_text() == before


def test_reconcile_leaves_checks_md_alone_when_a_check_has_no_evidence(tmp_path):
    _write_all_evidence(tmp_path)
    (state_io.state_dir("foo-bar", "run-1", base=tmp_path) / "evidence" / "checks" / "test.json").unlink()
    path = _write_checks_md(tmp_path, "unresolved-after-cap")
    before = path.read_text()

    assert run_checks.reconcile_checks_state("foo-bar", "run-1", state_base=tmp_path) is False
    assert path.read_text() == before


def test_reconcile_leaves_checks_md_alone_when_setup_failed_though_every_check_passed(tmp_path):
    """Checks that pass on a checkout setup could not prepare do not make the attempt green."""
    _write_all_evidence(tmp_path)
    directory = state_io.state_dir("foo-bar", "run-1", base=tmp_path) / "evidence" / "checks"
    (directory / "setup.json").write_text(json.dumps({"status": "fail", "command": ["install-deps"], "returncode": 1, "detail": "registry down"}))
    path = _write_checks_md(tmp_path, "tooling-failure")
    before = path.read_text()

    assert run_checks.reconcile_checks_state("foo-bar", "run-1", state_base=tmp_path) is False
    assert path.read_text() == before


def test_reconcile_never_creates_checks_md(tmp_path):
    _write_all_evidence(tmp_path)

    assert run_checks.reconcile_checks_state("foo-bar", "run-1", state_base=tmp_path) is False
    assert not (state_io.state_dir("foo-bar", "run-1", base=tmp_path) / "checks.md").exists()


def test_reconcile_does_not_rewrite_an_already_resolved_checks_md(tmp_path):
    _write_all_evidence(tmp_path)
    path = _write_checks_md(tmp_path, "resolved", fix_cycle=1, body="## Failing checks\n\n_none_")
    before = path.read_text()

    assert run_checks.reconcile_checks_state("foo-bar", "run-1", state_base=tmp_path) is False
    assert path.read_text() == before


def test_cli_reconcile_exits_zero_and_reports_whether_it_wrote(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    args = ["reconcile", "--story-slug", "foo-bar", "--run-id", "run-1"]

    assert run_checks.main(args) == 0  # nothing there at all
    assert json.loads(capsys.readouterr().out) == {"ok": True, "reconciled": False}

    _write_all_evidence(tmp_path / state_io.FACTORY_DIR)
    path = _write_checks_md(tmp_path / state_io.FACTORY_DIR, "unresolved-after-cap")
    assert run_checks.main(args) == 0
    assert json.loads(capsys.readouterr().out) == {"ok": True, "reconciled": True}
    assert state_io.read_state(path)[0]["status"] == "resolved"


# --- any-check-failed: the checks job's signal to the fix loop (backlog bug 4) ----------


@pytest.mark.parametrize(
    "outcomes, expected",
    [
        (["success"] * 5, False),
        (["success", "failure", "success", "success", "success"], True),
        (["failure"] * 5, True),
        # A step is skipped/cancelled only when something else already ended the job.
        (["skipped"] * 5, False),
        (["success", "skipped", "cancelled", "success", "success"], False),
        (["success", "failure", "skipped", "skipped", "skipped"], True),
    ],
)
def test_any_check_failed_is_true_only_for_a_failure_outcome(outcomes, expected):
    assert run_checks.any_check_failed(outcomes) is expected


@pytest.mark.parametrize(
    "outcomes, named",
    [
        (["success", "", "success"], "''"),  # a mistyped step id evaluates to an empty string
        (["success", "failed"], "'failed'"),
        (["true"], "'true'"),
        ([], "no step outcome"),
    ],
)
def test_any_check_failed_rejects_what_is_not_a_step_outcome(outcomes, named):
    with pytest.raises(ValueError, match=named):
        run_checks.any_check_failed(outcomes)


@pytest.mark.parametrize(
    "outcomes, line",
    [
        (["success", "success", "success", "success", "success"], "any-check-failed=false"),
        (["success", "success", "failure", "success", "failure"], "any-check-failed=true"),
        (["skipped", "skipped", "skipped", "skipped", "skipped"], "any-check-failed=false"),
    ],
)
def test_cmd_any_check_failed_prints_the_output_line(capsys, outcomes, line):
    rc = run_checks.main(["any-check-failed", *outcomes])

    assert rc == 0
    assert capsys.readouterr().out == line + "\n"  # exactly one line, for >> "$GITHUB_OUTPUT"


@pytest.mark.parametrize("outcomes", [["success", "", "success", "success", "success"], ["success", "bogus"], []])
def test_cmd_any_check_failed_exits_2_and_prints_no_line_for_an_unknown_outcome(capsys, outcomes):
    rc = run_checks.main(["any-check-failed", *outcomes])

    captured = capsys.readouterr()
    assert rc == 2
    assert captured.out == ""  # never a line the workflow could read as "nothing failed"
    assert "error:" in captured.err
