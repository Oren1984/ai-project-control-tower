"""
Security guardrail tests.

Verify path traversal blocking, secret masking, report sanitization,
and that the scanner never modifies the target repository.
"""
import hashlib
import os
from pathlib import Path
from unittest.mock import patch

import pytest

from app.reports.report_sanitizer import sanitize_report
from app.scanner.path_validator import PathValidationError, validate_scan_path
from app.scanner.repo_scanner import RepoScanner
from app.scanner.secret_masker import mask_secrets


# ---------------------------------------------------------------------------
# Path traversal
# ---------------------------------------------------------------------------

def _mock_settings(allowed: list[str]):
    return patch("app.scanner.path_validator.settings", allowed_scan_paths=allowed)


def test_path_traversal_dot_dot_blocked(tmp_path):
    allowed = tmp_path / "allowed"
    sibling = tmp_path / "secret"
    allowed.mkdir()
    sibling.mkdir()
    traversal = str(allowed) + "/../secret"
    with _mock_settings([str(allowed)]):
        with pytest.raises(PathValidationError):
            validate_scan_path(traversal)


def test_symlink_outside_allowlist_blocked(tmp_path):
    allowed = tmp_path / "allowed"
    outside = tmp_path / "outside"
    allowed.mkdir()
    outside.mkdir()
    link = allowed / "link_to_outside"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("symlinks not supported on this platform")
    # The resolved path of the link itself is inside allowed, but the target
    # directory outside is not — validate_scan_path checks the given path.
    # The link itself resolves to outside, so it must be blocked.
    with _mock_settings([str(allowed)]):
        with pytest.raises(PathValidationError):
            validate_scan_path(str(link))


def test_empty_allowlist_always_rejects(tmp_path):
    with _mock_settings([]):
        with pytest.raises(PathValidationError, match="No allowed scan paths"):
            validate_scan_path(str(tmp_path))


# ---------------------------------------------------------------------------
# Secret masking
# ---------------------------------------------------------------------------

def test_aws_key_masked():
    text = "export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"
    result = mask_secrets(text)
    assert "AKIAIOSFODNN7EXAMPLE" not in result


def test_openai_key_masked():
    text = "key = sk-" + "A" * 48
    result = mask_secrets(text)
    assert "A" * 48 not in result


def test_password_env_masked():
    # Pattern matches env vars that START with PASSWORD/SECRET/TOKEN/etc.
    text = "PASSWORD=supersecret123"
    result = mask_secrets(text)
    assert "supersecret123" not in result


def test_clean_text_not_mangled():
    text = "The quick brown fox jumps over the lazy dog."
    assert mask_secrets(text) == text


# ---------------------------------------------------------------------------
# Report sanitization — no auto-fix or patch content
# ---------------------------------------------------------------------------

def test_report_has_no_diff_blocks():
    raw = "Here is a diff:\n```diff\n- old\n+ new\n```\nEnd."
    result = sanitize_report(raw)
    assert "- old" not in result
    assert "+ new" not in result


def test_report_has_no_autofix_section():
    raw = "## Auto Fix\nstep 1: do this\n\n## Findings\nstuff"
    result = sanitize_report(raw)
    assert "Auto Fix" not in result
    assert "Findings" in result


def test_report_masks_embedded_secrets():
    raw = "Found key: sk-" + "X" * 48 + " in config."
    result = sanitize_report(raw)
    assert "X" * 48 not in result


# ---------------------------------------------------------------------------
# Scanner read-only guarantee (complementary to E2E test)
# ---------------------------------------------------------------------------

def _sha256_dir(directory: Path) -> dict[str, str]:
    result = {}
    for root, _, files in os.walk(str(directory)):
        for fname in files:
            fp = Path(root) / fname
            try:
                result[str(fp.relative_to(directory))] = hashlib.sha256(
                    fp.read_bytes()
                ).hexdigest()
            except OSError:
                pass
    return result


def test_scanner_does_not_write_files(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "main.py").write_text("print('hello')\n")
    (repo / "README.md").write_text("# Repo\n")

    before = _sha256_dir(repo)
    RepoScanner().scan(repo)
    after = _sha256_dir(repo)

    assert before == after, "Scanner modified repository files"


def test_scanner_does_not_create_files(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "app.py").write_text("x = 1\n")
    count_before = len(list(repo.rglob("*")))
    RepoScanner().scan(repo)
    count_after = len(list(repo.rglob("*")))
    assert count_after == count_before, "Scanner created extra files"


# ---------------------------------------------------------------------------
# Binary / oversized file skipping
# ---------------------------------------------------------------------------

def test_binary_file_is_skipped(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "data.bin").write_bytes(bytes(range(256)))
    result = RepoScanner().scan(repo)
    scanned_paths = {f.path for f in result.files}
    assert not any("data.bin" in p for p in scanned_paths)


def test_oversized_file_is_skipped(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    big = repo / "big.txt"
    big.write_bytes(b"x" * (2 * 1024 * 1024))  # 2 MB > default 1 MB limit
    result = RepoScanner().scan(repo)
    scanned_paths = {f.path for f in result.files}
    assert not any("big.txt" in p for p in scanned_paths)
