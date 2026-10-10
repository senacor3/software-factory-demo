# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for checkout_branch.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_checkout_branch.py

Covers the I/O & Edge-Case Matrix's checkout-success and checkout-failure rows, with
`subprocess.run` mocked throughout -- no real `git` process in the committed suite
(mirrors test_open_implementation_pr.py).
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import checkout_branch


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stderr="boom"):
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


# --- checkout success ----------------------------------------------------------------


def test_checkout_fetches_and_checks_out_the_exact_branch_name():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        return _ok()

    with patch("checkout_branch.subprocess.run", side_effect=fake_run):
        branch = checkout_branch.checkout_branch("foo", "run-1")

    assert branch == "light-factory/foo/run-1"
    assert calls == [
        ["git", "fetch", "origin", "light-factory/foo/run-1"],
        ["git", "checkout", "light-factory/foo/run-1"],
    ]


def test_checkout_never_creates_a_branch():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        return _ok()

    with patch("checkout_branch.subprocess.run", side_effect=fake_run):
        checkout_branch.checkout_branch("foo", "run-1")

    assert all("-b" not in c for c in calls)


def test_checkout_forwards_cwd():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cwd)
        return _ok()

    with patch("checkout_branch.subprocess.run", side_effect=fake_run):
        checkout_branch.checkout_branch("foo", "run-1", cwd="/some/repo")

    assert calls == ["/some/repo", "/some/repo"]


# --- checkout failure raises CheckoutError, distinct from other exceptions -----------


def test_fetch_failure_raises_checkout_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[:2] == ["git", "fetch"]:
            return _fail(stderr="fatal: couldn't find remote ref light-factory/foo/run-1")
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("checkout_branch.subprocess.run", side_effect=fake_run):
        with pytest.raises(checkout_branch.CheckoutError, match="couldn't find remote ref"):
            checkout_branch.checkout_branch("foo", "run-1")


def test_checkout_failure_raises_checkout_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[:2] == ["git", "fetch"]:
            return _ok()
        if cmd[:2] == ["git", "checkout"]:
            return _fail(stderr="fatal: pathspec did not match any file(s)")
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("checkout_branch.subprocess.run", side_effect=fake_run):
        with pytest.raises(checkout_branch.CheckoutError, match="pathspec"):
            checkout_branch.checkout_branch("foo", "run-1")


def test_subprocess_oserror_raises_checkout_error():
    with patch("checkout_branch.subprocess.run", side_effect=OSError("git not found")):
        with pytest.raises(checkout_branch.CheckoutError, match="git not found"):
            checkout_branch.checkout_branch("foo", "run-1")
