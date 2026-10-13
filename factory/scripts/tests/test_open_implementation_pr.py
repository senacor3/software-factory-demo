# /// script
# requires-python = ">=3.13"
# dependencies = ["pytest>=8.0"]
# ///
"""Tests for open_implementation_pr.py. Run:
uv run --with pytest pytest factory/scripts/tests/test_open_implementation_pr.py

Covers the amendment's Acceptance Criterion 3 (idempotent-reuse) plus fresh-create,
subprocess-failure, and AD-15 supersession-closing, with `subprocess.run` mocked
throughout -- no real `git`/`gh` process in the committed suite (mirrors how
test_analysis_graph.py mocks the `claude` CLI call).
"""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import open_implementation_pr
import state_io


def _ok(stdout=""):
    return SimpleNamespace(returncode=0, stdout=stdout, stderr="")


def _fail(stderr="boom"):
    return SimpleNamespace(returncode=1, stdout="", stderr=stderr)


def _pr_list_output(prs):
    return json.dumps(prs)


def _labeled_pr_list_output(head_ref_names):
    return json.dumps([{"headRefName": h} for h in head_ref_names])


def _is_head_query(cmd):
    # find_open_pr's exact-branch query, as opposed to supersede_prior_prs's repo-wide one.
    return cmd[:3] == ["gh", "pr", "list"] and "--head" in cmd


def _is_supersession_query(cmd):
    return cmd[:3] == ["gh", "pr", "list"] and "--head" not in cmd and "--label" not in cmd


def _open_pr_list_output(prs):
    return json.dumps([{"number": n, "headRefName": h} for n, h in prs])


SUPERSESSION_QUERY = ["gh", "pr", "list", "--state", "open", "--limit", "100", "--json", "number,headRefName"]


# --- fresh-create success path -----------------------------------------------------------


def test_fresh_create_creates_branch_commits_pushes_and_opens_pr(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(_open_pr_list_output([]))
        if _is_head_query(cmd):
            # First call (pre-create check): nothing open yet. Second call (post-create
            # read-back): the PR gh pr create just made.
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 42, "url": "https://github.com/org/repo/pull/42"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        result = open_implementation_pr.open_pr_for_story(
            "foo", "run-1", state_base=tmp_path
        )

    assert result == {
        "branch": "software-factory/foo/run-1",
        "pr_number": 42,
        "pr_url": "https://github.com/org/repo/pull/42",
    }

    checkout_calls = [c for c in calls if c[:2] == ["git", "checkout"]]
    assert checkout_calls == [["git", "checkout", "-b", "software-factory/foo/run-1"]]

    commit_calls = [c for c in calls if "commit" in c]
    assert len(commit_calls) == 1
    assert "-c" in commit_calls[0] and "user.name=software-factory-bot" in commit_calls[0]
    assert "user.email=software-factory-bot@users.noreply.github.com" in commit_calls[0]

    push_calls = [c for c in calls if c[:2] == ["git", "push"]]
    assert push_calls == [["git", "push", "-u", "origin", "software-factory/foo/run-1"]]

    create_calls = [c for c in calls if c[:3] == ["gh", "pr", "create"]]
    assert len(create_calls) == 1
    assert "--title" in create_calls[0]
    assert create_calls[0][create_calls[0].index("--title") + 1] == "software-factory: foo (run-1)"

    # first run for this slug: the supersession query ran, but nothing is closed or commented.
    assert calls.count(SUPERSESSION_QUERY) == 1
    assert [c for c in calls if c[:3] in (["gh", "pr", "close"], ["gh", "pr", "comment"])] == []


def test_fresh_create_commits_the_correct_state_files(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(_open_pr_list_output([]))
        if _is_head_query(cmd):
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 1, "url": "https://github.com/org/repo/pull/1"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)

    add_calls = [c for c in calls if c[:2] == ["git", "add"]]
    assert len(add_calls) == 1
    added_paths = set(add_calls[0][2:])
    expected_dir = state_io.state_dir("foo", "run-1", base=tmp_path)
    assert added_paths == {str(expected_dir / "plan.md"), str(expected_dir / "decisions.md")}


# --- idempotent-reuse (Acceptance Criterion 3) ---------------------------------------------


def test_idempotent_reuse_returns_existing_pr_without_recreating(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(_open_pr_list_output([(7, "software-factory/foo/run-1")]))
        if _is_head_query(cmd):
            return _ok(_pr_list_output([{"number": 7, "url": "https://github.com/org/repo/pull/7"}]))
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        result = open_implementation_pr.open_pr_for_story(
            "foo", "run-1", state_base=tmp_path
        )

    assert result == {
        "branch": "software-factory/foo/run-1",
        "pr_number": 7,
        "pr_url": "https://github.com/org/repo/pull/7",
    }
    # only the pre-create existence check and the supersession query ran -- no git/gh
    # mutation calls (the only open PR on the slug prefix is this run's own).
    assert calls == [
        ["gh", "pr", "list", "--head", "software-factory/foo/run-1", "--state", "open", "--json", "number,url"],
        SUPERSESSION_QUERY,
    ]


# --- git/gh subprocess failure raises PROpenError -------------------------------------------


def test_git_checkout_failure_raises_pr_open_error(tmp_path):
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if _is_head_query(cmd):
            return _ok(_pr_list_output([]))
        if cmd[:2] == ["git", "checkout"]:
            return _fail(stderr="fatal: a branch named 'software-factory/foo/run-1' already exists")
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="already exists"):
            open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)


def test_gh_pr_create_failure_raises_pr_open_error(tmp_path):
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if _is_head_query(cmd):
            return _ok(_pr_list_output([]))
        if cmd[:3] == ["gh", "pr", "create"]:
            return _fail(stderr="gh: authentication required")
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="authentication required"):
            open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)


def test_subprocess_oserror_raises_pr_open_error(tmp_path):
    with patch("open_implementation_pr.subprocess.run", side_effect=OSError("gh not found")):
        with pytest.raises(open_implementation_pr.PROpenError, match="gh not found"):
            open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=tmp_path)


# --- state_base is forwarded to state_io.state_dir, not hardcoded -------------------------


# --- supersede_prior_prs (AD-15) ----------------------------------------------------------


def _supersession_fake_run(open_prs, calls):
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(_open_pr_list_output(open_prs))
        if cmd[:3] in (["gh", "pr", "close"], ["gh", "pr", "comment"]):
            return _ok()
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    return fake_run


def test_supersede_prior_prs_queries_open_prs_only():
    calls = []

    with patch("open_implementation_pr.subprocess.run", side_effect=_supersession_fake_run([], calls)):
        open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)

    assert calls == [SUPERSESSION_QUERY]


def test_supersede_prior_prs_first_run_closes_and_comments_nothing():
    calls = []
    open_prs = [(9, "software-factory/foo/run-2")]

    with patch("open_implementation_pr.subprocess.run", side_effect=_supersession_fake_run(open_prs, calls)):
        closed = open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)

    assert closed == []
    assert calls == [SUPERSESSION_QUERY]


def test_supersede_prior_prs_closes_one_predecessor_and_links_both_ways():
    calls = []
    open_prs = [(7, "software-factory/foo/run-1"), (9, "software-factory/foo/run-2")]

    with patch("open_implementation_pr.subprocess.run", side_effect=_supersession_fake_run(open_prs, calls)):
        closed = open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)

    assert closed == [7]
    assert calls[1:] == [
        ["gh", "pr", "comment", "9", "--body", "Retry of #7"],
        ["gh", "pr", "close", "7", "--comment", "Superseded by #9"],
    ]
    assert all("--delete-branch" not in c for c in calls)


def test_supersede_prior_prs_closes_cascading_predecessors_with_one_retry_comment():
    calls = []
    # unsorted on purpose: the result and the comment are in ascending order regardless.
    open_prs = [
        (7, "software-factory/foo/run-1b"),
        (9, "software-factory/foo/run-2"),
        (5, "software-factory/foo/run-1a"),
    ]

    with patch("open_implementation_pr.subprocess.run", side_effect=_supersession_fake_run(open_prs, calls)):
        closed = open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)

    assert closed == [5, 7]
    assert calls[1:] == [
        ["gh", "pr", "comment", "9", "--body", "Retry of #5, #7"],
        ["gh", "pr", "close", "5", "--comment", "Superseded by #9"],
        ["gh", "pr", "close", "7", "--comment", "Superseded by #9"],
    ]
    assert all("--delete-branch" not in c for c in calls)


def test_supersede_prior_prs_leaves_other_stories_and_non_factory_prs_untouched():
    calls = []
    open_prs = [
        (3, "software-factory/foo-bar/run-3"),  # shares the slug as a string prefix only
        (4, "software-factory/other/run-4"),
        (6, "feature/foo"),
        (8, "software-factory/foo"),  # no trailing slash, not a run branch
        (9, "software-factory/foo/run-2"),
    ]

    with patch("open_implementation_pr.subprocess.run", side_effect=_supersession_fake_run(open_prs, calls)):
        closed = open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)

    assert closed == []
    assert calls == [SUPERSESSION_QUERY]


def test_supersede_prior_prs_closes_only_the_matching_slug_among_decoys():
    calls = []
    open_prs = [
        (3, "software-factory/foo-bar/run-3"),
        (7, "software-factory/foo/run-1"),
        (9, "software-factory/foo/run-2"),
    ]

    with patch("open_implementation_pr.subprocess.run", side_effect=_supersession_fake_run(open_prs, calls)):
        closed = open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)

    assert closed == [7]
    assert [c[3] for c in calls if c[:3] == ["gh", "pr", "close"]] == ["7"]


@pytest.mark.parametrize("failing", ["list", "close", "comment"])
def test_supersede_prior_prs_gh_failure_raises_pr_open_error(failing):
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[2] == failing:
            return _fail(stderr=f"gh: {failing} failed")
        if _is_supersession_query(cmd):
            return _ok(_open_pr_list_output([(7, "software-factory/foo/run-1")]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match=f"{failing} failed"):
            open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)


def test_supersede_prior_prs_posts_retry_comment_before_a_failing_close():
    # #5 closes, #7 fails: the back-link naming both is already on the new PR, so a
    # same-run-id re-run only has #7 left to close and no link is ever lost.
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(
                _open_pr_list_output(
                    [(5, "software-factory/foo/run-1a"), (7, "software-factory/foo/run-1b")]
                )
            )
        if cmd[:4] == ["gh", "pr", "close", "7"]:
            return _fail(stderr="gh: close failed")
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="close failed"):
            open_implementation_pr.supersede_prior_prs("foo", "run-2", 9)

    assert calls[1:] == [
        ["gh", "pr", "comment", "9", "--body", "Retry of #5, #7"],
        ["gh", "pr", "close", "5", "--comment", "Superseded by #9"],
        ["gh", "pr", "close", "7", "--comment", "Superseded by #9"],
    ]


# --- open_pr_for_story runs supersession on both return paths --------------------------------


def test_fresh_create_supersedes_predecessor_after_the_new_pr_exists(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(
                _open_pr_list_output(
                    [(7, "software-factory/foo/run-1"), (9, "software-factory/foo/run-2")]
                )
            )
        if _is_head_query(cmd):
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 9, "url": "https://github.com/org/repo/pull/9"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        result = open_implementation_pr.open_pr_for_story("foo", "run-2", state_base=tmp_path)

    # returned dict shape is unchanged by supersession.
    assert result == {
        "branch": "software-factory/foo/run-2",
        "pr_number": 9,
        "pr_url": "https://github.com/org/repo/pull/9",
    }
    create_index = next(i for i, c in enumerate(calls) if c[:3] == ["gh", "pr", "create"])
    assert calls[create_index + 1 :] == [
        ["gh", "pr", "list", "--head", "software-factory/foo/run-2", "--state", "open", "--json", "number,url"],
        SUPERSESSION_QUERY,
        ["gh", "pr", "comment", "9", "--body", "Retry of #7"],
        ["gh", "pr", "close", "7", "--comment", "Superseded by #9"],
    ]


def test_same_run_id_rerun_completes_an_interrupted_supersession(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(
                _open_pr_list_output(
                    [(7, "software-factory/foo/run-1"), (9, "software-factory/foo/run-2")]
                )
            )
        if _is_head_query(cmd):
            return _ok(_pr_list_output([{"number": 9, "url": "https://github.com/org/repo/pull/9"}]))
        if cmd[:3] in (["gh", "pr", "close"], ["gh", "pr", "comment"]):
            return _ok()
        raise AssertionError(f"unexpected subprocess call: {cmd}")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        result = open_implementation_pr.open_pr_for_story("foo", "run-2", state_base=tmp_path)

    assert result == {
        "branch": "software-factory/foo/run-2",
        "pr_number": 9,
        "pr_url": "https://github.com/org/repo/pull/9",
    }
    # existing PR reused (no git, no gh pr create), predecessor still superseded.
    assert calls == [
        ["gh", "pr", "list", "--head", "software-factory/foo/run-2", "--state", "open", "--json", "number,url"],
        SUPERSESSION_QUERY,
        ["gh", "pr", "comment", "9", "--body", "Retry of #7"],
        ["gh", "pr", "close", "7", "--comment", "Superseded by #9"],
    ]


def test_supersession_failure_fails_open_pr_for_story_and_leaves_new_pr_open(tmp_path):
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _fail(stderr="gh: rate limited")
        if _is_head_query(cmd):
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 9, "url": "https://github.com/org/repo/pull/9"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="rate limited"):
            open_implementation_pr.open_pr_for_story("foo", "run-2", state_base=tmp_path)

    # the new PR was created and nothing closed it.
    assert len([c for c in calls if c[:3] == ["gh", "pr", "create"]]) == 1
    assert [c for c in calls if c[:3] == ["gh", "pr", "close"]] == []


# --- close_for_clarification --------------------------------------------------------------


def test_close_for_clarification_posts_comment_and_closes_pr():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.close_for_clarification(42, ["what about X?", "and Y?"])

    assert len(calls) == 1
    cmd = calls[0]
    assert cmd[:3] == ["gh", "pr", "close"]
    assert cmd[3] == "42"
    assert "--comment" in cmd
    comment = cmd[cmd.index("--comment") + 1]
    assert "what about X?" in comment
    assert "and Y?" in comment
    assert "--delete-branch" not in cmd


def test_close_for_clarification_subprocess_failure_raises_pr_open_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _fail(stderr="gh: pull request not found")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="not found"):
            open_implementation_pr.close_for_clarification(42, ["what about X?"])


# --- count_clarification_rounds -----------------------------------------------------------


def test_count_clarification_rounds_zero_prior_returns_zero():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        assert cmd[:3] == ["gh", "pr", "list"]
        assert "--label" in cmd and cmd[cmd.index("--label") + 1] == "clarification-round"
        assert "--state" in cmd and cmd[cmd.index("--state") + 1] == "all"
        return _ok(_labeled_pr_list_output([]))

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        assert open_implementation_pr.count_clarification_rounds("foo", "run-2") == 0


def test_count_clarification_rounds_counts_one_prior_open_pr():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _ok(_labeled_pr_list_output(["software-factory/foo/run-1"]))

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        assert open_implementation_pr.count_clarification_rounds("foo", "run-2") == 1


def test_count_clarification_rounds_counts_one_prior_closed_pr():
    # --state all means a closed PR counts exactly the same as an open one.
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _ok(_labeled_pr_list_output(["software-factory/foo/run-1"]))

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        assert open_implementation_pr.count_clarification_rounds("foo", "run-2") == 1


def test_count_clarification_rounds_excludes_decoy_pr_from_different_slug():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _ok(
            _labeled_pr_list_output(
                ["software-factory/foo/run-1", "software-factory/other-story/run-9"]
            )
        )

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        assert open_implementation_pr.count_clarification_rounds("foo", "run-2") == 1


def test_count_clarification_rounds_excludes_own_run_id_branch_on_same_run_retry():
    # A same-run-id retry after a partial failure (e.g. label_clarification_round already
    # succeeded, then a later step failed) must not count this run's own already-labeled
    # PR as a *prior* round -- only genuinely earlier runs count.
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _ok(
            _labeled_pr_list_output(
                ["software-factory/foo/run-1", "software-factory/foo/run-2"]
            )
        )

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        assert open_implementation_pr.count_clarification_rounds("foo", "run-2") == 1


def test_count_clarification_rounds_gh_failure_raises_pr_open_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _fail(stderr="gh: rate limited")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="rate limited"):
            open_implementation_pr.count_clarification_rounds("foo", "run-2")


# --- clarification_status -------------------------------------------------------------------


def test_clarification_status_below_cap_with_zero_prior():
    with patch("open_implementation_pr.count_clarification_rounds", return_value=0):
        assert open_implementation_pr.clarification_status("foo", "run-2") == "awaiting-clarification"


def test_clarification_status_below_cap_with_one_prior():
    with patch("open_implementation_pr.count_clarification_rounds", return_value=1):
        assert open_implementation_pr.clarification_status("foo", "run-2") == "awaiting-clarification"


def test_clarification_status_at_cap_with_two_prior():
    with patch("open_implementation_pr.count_clarification_rounds", return_value=2):
        assert open_implementation_pr.clarification_status("foo", "run-2") == "clarification-cap-reached"


def test_clarification_status_at_cap_with_more_than_two_prior():
    with patch("open_implementation_pr.count_clarification_rounds", return_value=5):
        assert open_implementation_pr.clarification_status("foo", "run-2") == "clarification-cap-reached"


# --- label_clarification_round ----------------------------------------------------------------


def test_label_clarification_round_creates_label_then_adds_it():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.label_clarification_round(42)

    assert calls[0][:3] == ["gh", "label", "create"]
    assert "clarification-round" in calls[0]
    assert "--force" in calls[0]
    assert calls[1] == ["gh", "pr", "edit", "42", "--add-label", "clarification-round"]


def test_label_clarification_round_failure_raises_pr_open_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        return _fail(stderr="gh: label create failed")

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="label create failed"):
            open_implementation_pr.label_clarification_round(42)


# --- post_clarification_cap_notice ------------------------------------------------------------


def test_post_clarification_cap_notice_labels_and_comments_but_never_closes():
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.post_clarification_cap_notice(42, ["what about X?", "and Y?"])

    label_create_calls = [c for c in calls if c[:3] == ["gh", "label", "create"]]
    assert len(label_create_calls) == 1

    add_label_calls = [c for c in calls if c[:3] == ["gh", "pr", "edit"]]
    assert add_label_calls == [["gh", "pr", "edit", "42", "--add-label", "clarification-round"]]

    comment_calls = [c for c in calls if c[:3] == ["gh", "pr", "comment"]]
    assert len(comment_calls) == 1
    comment = comment_calls[0][comment_calls[0].index("--body") + 1]
    assert "budget" in comment.lower()
    assert "what about X?" in comment
    assert "and Y?" in comment

    close_calls = [c for c in calls if c[:3] == ["gh", "pr", "close"]]
    assert close_calls == []


def test_post_clarification_cap_notice_failure_raises_pr_open_error():
    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        if cmd[:3] == ["gh", "pr", "comment"]:
            return _fail(stderr="gh: comment failed")
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        with pytest.raises(open_implementation_pr.PROpenError, match="comment failed"):
            open_implementation_pr.post_clarification_cap_notice(42, ["what about X?"])


def test_state_base_override_is_used_for_git_add_paths(tmp_path):
    custom_base = tmp_path / "custom-factory-base"
    calls = []

    def fake_run(cmd, cwd=None, capture_output=True, text=True, check=False):
        calls.append(cmd)
        if _is_supersession_query(cmd):
            return _ok(_open_pr_list_output([]))
        if _is_head_query(cmd):
            if calls.count(cmd) == 1:
                return _ok(_pr_list_output([]))
            return _ok(_pr_list_output([{"number": 1, "url": "https://github.com/org/repo/pull/1"}]))
        return _ok()

    with patch("open_implementation_pr.subprocess.run", side_effect=fake_run):
        open_implementation_pr.open_pr_for_story("foo", "run-1", state_base=custom_base)

    add_calls = [c for c in calls if c[:2] == ["git", "add"]]
    assert str(custom_base) in add_calls[0][2]
