import pytest

from app.scanner.secret_masker import REDACTED, mask_secrets


def test_mask_aws_access_key():
    content = "key = AKIAIOSFODNN7EXAMPLE"
    result = mask_secrets(content)
    assert "AKIAIOSFODNN7EXAMPLE" not in result
    assert REDACTED in result


def test_mask_openai_key():
    key = "sk-" + "A" * 48
    result = mask_secrets(f"OPENAI_KEY={key}")
    assert key not in result
    assert REDACTED in result


def test_mask_anthropic_key():
    key = "sk-ant-" + "A" * 40
    result = mask_secrets(f"value={key}")
    assert key not in result
    assert REDACTED in result


def test_mask_google_api_key():
    key = "AIza" + "A" * 35
    result = mask_secrets(f"google_key={key}")
    assert key not in result
    assert REDACTED in result


def test_mask_github_token_ghp():
    token = "ghp_" + "A" * 36
    result = mask_secrets(f"GITHUB_TOKEN={token}")
    assert token not in result
    assert REDACTED in result


def test_mask_github_token_gho():
    token = "gho_" + "B" * 36
    result = mask_secrets(token)
    assert token not in result
    assert REDACTED in result


def test_mask_jwt_token():
    jwt = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        ".eyJzdWIiOiIxMjM0NTY3ODkwIn0"
        ".TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ"
    )
    result = mask_secrets(f"Authorization: {jwt}")
    assert jwt not in result
    assert REDACTED in result


def test_mask_env_password():
    result = mask_secrets("PASSWORD=super_secret_password123")
    assert "super_secret_password123" not in result
    assert REDACTED in result


def test_mask_env_api_key():
    result = mask_secrets("API_KEY=sk_live_abcdefghijk1234567890")
    assert "sk_live_abcdefghijk1234567890" not in result
    assert REDACTED in result


def test_mask_env_token():
    result = mask_secrets("TOKEN=verylongsecrettoken1234567890")
    assert "verylongsecrettoken1234567890" not in result
    assert REDACTED in result


def test_mask_bearer_token():
    secret = "abcdefghijklmnopqrstuvwxyz12345678"
    result = mask_secrets(f"Authorization: bearer {secret}")
    assert secret not in result
    assert REDACTED in result


def test_mask_preserves_non_secret_content():
    content = "This is a regular comment with no secrets."
    assert mask_secrets(content) == content


def test_mask_preserves_short_values():
    # Values shorter than 4 chars should not be masked by the .env pattern
    content = "VERSION=1.0"
    result = mask_secrets(content)
    assert result == content


def test_mask_multiple_secrets_in_one_string():
    aws_key = "AKIAIOSFODNN7EXAMPLE"
    openai_key = "sk-" + "C" * 48
    content = f"aws={aws_key}\nopenai={openai_key}"
    result = mask_secrets(content)
    assert aws_key not in result
    assert openai_key not in result
    assert result.count(REDACTED) >= 2


def test_mask_does_not_alter_structure():
    content = "normal_key=value\nPASSWORD=supersecret123\nother=data"
    result = mask_secrets(content)
    assert "normal_key=value" in result
    assert "other=data" in result
    assert "supersecret123" not in result
