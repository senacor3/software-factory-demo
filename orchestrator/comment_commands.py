"""comment_commands -- gate-agnostic PR-comment command grammar (AD-2).

Parses an `issue_comment` body into one of the three gate-action commands
AD-2 defines for `plan-approval` -- `/approve`, `/rework <feedback>`,
`/reject` -- or `none` for anything else. A standalone helper with no
Lambda/event-shape coupling: `handler.py` owns the `issue_comment` guard
(action == "created", `issue.pull_request` present, non-bot author) and
calls this only with the comment's raw body text. Deliberately
gate-agnostic -- `evidence-approval` (a later entry) reuses this verbatim;
it simply never constructs a `rework` command, since that gate has no
`/rework`-equivalent action.

Grammar:
  - `/approve` / `/reject`: matched against the comment's FIRST LINE only
    (stripped of surrounding whitespace), exact match. Free text on a
    later line (e.g. "/approve\nLGTM!") doesn't change the match; free text
    sharing the first line (e.g. "/approve please proceed") does -- that
    first line isn't an exact match, so the whole comment is `none`.
  - `/rework <feedback>`: `^/rework\\s+(.+)` matched with `re.DOTALL` against
    the whole (stripped) body, so feedback may itself span multiple lines.
    Empty or whitespace-only feedback (including bare `/rework` with
    nothing after it) is `none`, same as a non-command comment -- per this
    story's own I/O matrix, a human must never get a bot reply for either.

A comment matching none of the three is `none`: callers must take no
action and send no reply -- a human chatting normally on the PR must never
get a bot reply.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

GateCommandKind = Literal["approve", "rework", "reject", "none"]

# DOTALL: feedback may span multiple lines. Matched against the whole
# stripped body (not just the first line) since feedback legitimately
# continues past the first line. Requires at least one whitespace char
# immediately after the literal "/rework" -- this is what keeps a word
# like "/reworking" from matching, and what makes bare "/rework" (no
# trailing whitespace at all) fail to match outright.
_REWORK_PATTERN = re.compile(r"^/rework\s+(.+)", re.DOTALL)


@dataclass(frozen=True)
class GateCommand:
    kind: GateCommandKind
    feedback: str | None = None


_NONE = GateCommand(kind="none", feedback=None)


def parse_gate_command(body: str) -> GateCommand:
    """Parse a PR comment body into a GateCommand. Never raises -- any
    input that isn't a recognized command (including an empty body) comes
    back as `GateCommand(kind="none")`.
    """
    if not body or not body.strip():
        return _NONE

    stripped = body.strip()
    first_line = stripped.splitlines()[0].strip()

    if first_line == "/approve":
        return GateCommand(kind="approve")
    if first_line == "/reject":
        return GateCommand(kind="reject")

    match = _REWORK_PATTERN.match(stripped)
    if match:
        feedback = match.group(1).strip()
        if feedback:
            return GateCommand(kind="rework", feedback=feedback)

    return _NONE
