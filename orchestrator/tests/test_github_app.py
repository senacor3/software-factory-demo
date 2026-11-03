"""Unit tests for GitHub App JWT minting, installation-token exchange, and
PR-comment posting (orchestrator/github_app.py).

No real network calls: get_installation_token/post_comment mock
urllib.request.urlopen; mint_jwt is local signing only (no network), tested
against a throwaway RSA key generated for the test, per the story's I/O
matrix and Verification section.

Run via `cd orchestrator && uv run --with pytest --with PyJWT[crypto]
pytest tests/ -v`.
"""

import json
import sys
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from github_app import get_installation_token, mint_jwt, post_comment  # noqa: E402


@pytest.fixture(scope="module")
def rsa_keypair() -> tuple[str, str]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    public_pem = (
        private_key.public_key()
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode("utf-8")
    )
    return private_pem, public_pem


def _fake_http_response(payload: dict) -> MagicMock:
    response = MagicMock()
    response.read.return_value = json.dumps(payload).encode("utf-8")
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class TestMintJwt:
    def test_mints_rs256_jwt_with_required_claims(self, rsa_keypair):
        private_pem, public_pem = rsa_keypair

        token = mint_jwt("123456", private_pem)

        header = jwt.get_unverified_header(token)
        assert header["alg"] == "RS256"

        claims = jwt.decode(token, public_pem, algorithms=["RS256"])
        assert claims["iss"] == "123456"
        assert "iat" in claims
        assert "exp" in claims
        assert claims["exp"] > claims["iat"]

    def test_jwt_validity_window_is_at_most_ten_minutes(self, rsa_keypair):
        private_pem, _ = rsa_keypair

        token = mint_jwt("123456", private_pem)
        claims = jwt.decode(token, options={"verify_signature": False})

        assert claims["exp"] - claims["iat"] <= 600 + 60


class TestGetInstallationToken:
    @patch("github_app.urllib.request.urlopen")
    def test_returns_token_from_github_response(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response({"token": "ghs_abc123"})

        token = get_installation_token("fake.jwt.token", "987654")

        assert token == "ghs_abc123"
        request = mock_urlopen.call_args[0][0]
        assert (
            request.full_url
            == "https://api.github.com/app/installations/987654/access_tokens"
        )
        assert request.get_header("Authorization") == "Bearer fake.jwt.token"

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_github_error_body_on_failure(self, mock_urlopen):
        error_body = json.dumps({"message": "Bad credentials"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url="https://api.github.com/app/installations/987654/access_tokens",
            code=401,
            msg="Unauthorized",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match="Bad credentials"):
            get_installation_token("fake.jwt.token", "987654")


class TestPostComment:
    @patch("github_app.urllib.request.urlopen")
    def test_posts_comment_to_fixed_repo_and_pr(self, mock_urlopen):
        mock_urlopen.return_value = _fake_http_response({"id": 1, "body": "hello"})

        result = post_comment("ghs_abc123", 42, "hello")

        assert result == {"id": 1, "body": "hello"}
        request = mock_urlopen.call_args[0][0]
        assert request.full_url == (
            "https://api.github.com/repos/senacor3/software-factory-demo/issues/42/comments"
        )
        assert request.get_header("Authorization") == "Bearer ghs_abc123"
        assert json.loads(request.data.decode("utf-8")) == {"body": "hello"}

    @patch("github_app.urllib.request.urlopen")
    def test_surfaces_github_error_body_on_failure(self, mock_urlopen):
        error_body = json.dumps({"message": "Not Found"}).encode("utf-8")
        mock_urlopen.side_effect = urllib.error.HTTPError(
            url=(
                "https://api.github.com/repos/senacor3/software-factory-demo"
                "/issues/42/comments"
            ),
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=BytesIO(error_body),
        )

        with pytest.raises(RuntimeError, match="Not Found"):
            post_comment("ghs_abc123", 42, "hello")
