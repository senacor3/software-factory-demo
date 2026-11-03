"""Local unit test of the stub handler's response shape.

Run via `cd orchestrator && uv run --with pytest --with "PyJWT[crypto]"
pytest tests/ -v` (per the story's Verification section) -- no deploy, no
AWS credentials needed. PyJWT[crypto] is required even for this module:
`handler.py` imports `github_app.py`, which imports `jwt` at module level.
"""

import json
import sys
from pathlib import Path

# orchestrator/ has no requirements.txt-driven package layout (see Design
# Notes), so make the sibling handler.py importable without adding a
# conftest.py or __init__.py beyond what the plan's Code Map lists.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from handler import handler  # noqa: E402


def test_handler_returns_200_with_json_content_type():
    response = handler({}, None)

    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"


def test_handler_body_is_valid_json_object():
    response = handler({}, None)

    body = json.loads(response["body"])

    assert isinstance(body, dict)
    assert body == {"status": "ok"}


def test_handler_ignores_event_and_context_contents():
    # Any HTTP request shape must round-trip the same minimal response --
    # the stub has no auth/FSM logic yet to branch on event contents.
    response = handler({"some": "payload"}, context=object())

    assert response["statusCode"] == 200
