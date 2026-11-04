#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""attempt_target_merge -- the deterministic merge-conflict probe + marker-resolution
check shared by `merge.yml`'s `detect-conflict` job and `merge_conflict_graph.py`'s
bounded resolution loop (CAP-11, AD-19).

`attempt_merge` checks out the exact branch the analysis stage opened (AD-12, reusing
`checkout_branch.checkout_branch`), fetches the target branch, then runs a real
`git merge --no-commit --no-ff origin/<target>` -- left staged, uncommitted, on a clean
merge (`(False, [])`) or on a real conflict (`(True, conflicted_paths)`, the conflicted
paths captured once, right here, via `git diff --name-only --diff-filter=U`). That list
never changes afterward -- only `git add` would clear a path's unmerged-index state, and
nothing in this pipeline ever runs it -- so it is the one list every later fix-cycle
attempt resolves against. Raises `MergeAttemptError` if the fetch or the merge itself
fails for a reason other than a real conflict (its combined stdout/stderr must contain
`"CONFLICT"` for a merge failure to be treated as one), e.g. a missing target ref.

`has_unresolved_markers` is the only trustworthy "is it still conflicted" signal (see
`merge_conflict_graph.py`'s module docstring for why re-running `git merge` can't be):
it reads each given path and checks for a literal `<<<<<<< ` line left over from the
merge.

The CLI is `detect-conflict`'s only caller: it always runs `git merge --abort` afterward
regardless of outcome (a pure probe, never left staged) and prints a single
`has-conflict=true|false` line, shaped for direct `>> "$GITHUB_OUTPUT"` redirection --
mirroring `state_io.py`'s `cmd_derive` and `run_checks.py`'s `cmd_any_check_failed`
convention exactly (no JSON mixed into that same stdout, which would corrupt the
GITHUB_OUTPUT file).
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checkout_branch


class MergeAttemptError(RuntimeError):
    """The fetch or the merge subprocess call itself failed for a reason other than a
    real conflict -- e.g. a missing target ref -- distinct from `checkout_branch.
    CheckoutError` (before the merge is ever attempted)."""


def _run(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise MergeAttemptError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise MergeAttemptError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout


def attempt_merge(
    story_slug: str,
    run_id: str,
    target: str,
    *,
    cwd: str | os.PathLike | None = None,
) -> tuple[bool, list[str]]:
    """Check out the branch, fetch `target`, and attempt a real, uncommitted merge.

    Returns `(False, [])` on a clean merge (left staged, uncommitted) or
    `(True, conflicted_paths)` on a real conflict. Raises `checkout_branch.
    CheckoutError` if the checkout itself fails, or `MergeAttemptError` if the fetch
    or merge subprocess call fails for any reason other than a real conflict.
    """
    checkout_branch.checkout_branch(story_slug, run_id, cwd=cwd)
    _run(["git", "fetch", "origin", target], cwd=cwd)

    try:
        proc = subprocess.run(
            ["git", "merge", "--no-commit", "--no-ff", f"origin/{target}"],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as e:
        raise MergeAttemptError(f"failed to run git merge: {e}") from e

    if proc.returncode == 0:
        return False, []

    combined = "\n".join(part for part in (proc.stdout, proc.stderr) if part)
    if "CONFLICT" not in combined:
        raise MergeAttemptError(
            f"git merge --no-commit --no-ff origin/{target} exited {proc.returncode}: "
            f"{combined.strip()}"
        )

    conflicted_output = _run(["git", "diff", "--name-only", "--diff-filter=U"], cwd=cwd)
    conflicted_paths = [line for line in conflicted_output.splitlines() if line]
    return True, conflicted_paths


def has_unresolved_markers(paths: list[str], *, cwd: str | os.PathLike | None = None) -> bool:
    """True if any of `paths` still contains a leftover `<<<<<<< ` conflict-marker line.

    The only trustworthy "still conflicted" signal (see `merge_conflict_graph.py`'s
    module docstring) -- never re-running `git merge`, which would always report clean
    the instant the first conflict is staged.
    """
    base = Path(cwd) if cwd else Path(".")
    for rel_path in paths:
        text = (base / rel_path).read_text(encoding="utf-8")
        if any(line.startswith("<<<<<<< ") for line in text.splitlines()):
            return True
    return False


def abort_merge(*, cwd: str | os.PathLike | None = None) -> None:
    """Abort whatever merge is currently staged, leaving a clean working tree.

    A no-op (never raises) when no merge is in progress -- used both by the CLI below
    (a pure probe, always left clean) and by `merge_conflict_graph.py` once the
    attempt cap is reached (AD-19).
    """
    subprocess.run(["git", "merge", "--abort"], cwd=cwd, capture_output=True, text=True, check=False)


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--target", default="main")
    args = p.parse_args(argv)

    try:
        has_conflict, _ = attempt_merge(args.story_slug, args.run_id, args.target)
    except checkout_branch.CheckoutError as e:
        print(f"branch checkout failed: {e}", file=sys.stderr)
        abort_merge()
        return 1
    except MergeAttemptError as e:
        print(f"merge probe failed: {e}", file=sys.stderr)
        abort_merge()
        return 2

    abort_merge()
    print(f"has-conflict={'true' if has_conflict else 'false'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
