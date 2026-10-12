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
    ],
)
def test_named_runners_run_their_own_check(repo, runner, name):
    with patch("run_checks.subprocess.run", return_value=_ok()):
        result = runner("foo-bar", "run-1", state_base=repo, cwd=repo)

    assert result["status"] == ("skipped" if name == "security" else "pass")
    assert _evidence(repo, name)["status"] == result["status"]


# --- this repo's own config ------------------------------------------------------


def test_repo_config_holds_the_commands_the_script_used_to_hard_code():
    # Each list's first entry is still factory/'s own original command, untouched;
    # the freight-tenders backend/frontend commands are appended after it.
    assert run_checks.load_commands("build", cwd=REPO_ROOT) == [
        [sys.executable, "-m", "compileall", "factory", "-q"],
        ["bash", "-c", 'JAVA_HOME="$JAVA_HOME_25_X64" mvn -B -f freight-tenders/backend/pom.xml compile'],
        ["npm", "--prefix", "freight-tenders/frontend", "ci"],
        ["npm", "--prefix", "freight-tenders/frontend", "run", "build"],
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
