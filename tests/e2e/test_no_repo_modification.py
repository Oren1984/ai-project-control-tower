"""
Mandatory E2E non-modification safety test.

Verifies that scanning a repository leaves every file byte-for-byte identical.
This test must remain in the project until final release.
"""

import hashlib
import os
from pathlib import Path

import pytest

from app.scanner.repo_scanner import RepoScanner


def _hash_all_files(directory: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for root, _dirs, files in os.walk(str(directory)):
        root_path = Path(root)
        for filename in files:
            fp = root_path / filename
            try:
                content = fp.read_bytes()
            except OSError:
                continue
            rel = str(fp.relative_to(directory))
            hashes[rel] = hashlib.sha256(content).hexdigest()
    return hashes


@pytest.fixture
def sample_repo(tmp_path):
    repo = tmp_path / "sample_repo"
    repo.mkdir()

    src = repo / "src"
    src.mkdir()
    (src / "main.py").write_text("def main():\n    print('hello')\n")
    (src / "utils.py").write_text("def add(a, b):\n    return a + b\n")

    tests = repo / "tests"
    tests.mkdir()
    (tests / "test_main.py").write_text("def test_main(): pass\n")

    (repo / "README.md").write_text("# Sample Repo\n")
    (repo / "requirements.txt").write_text("requests>=2.0\n")
    (repo / ".gitignore").write_text("*.pyc\n__pycache__/\n")
    (repo / ".env.example").write_text("API_KEY=your_key_here\n")
    (repo / ".hidden_config").write_text("setting=value\n")

    return repo


def test_scanner_does_not_modify_any_files(sample_repo):
    hashes_before = _hash_all_files(sample_repo)
    file_count_before = len(hashes_before)

    RepoScanner(include_hidden=True, skip_git_internals=True).scan(sample_repo)

    hashes_after = _hash_all_files(sample_repo)
    file_count_after = len(hashes_after)

    assert file_count_after == file_count_before, (
        f"File count changed: {file_count_before} → {file_count_after}"
    )

    for rel_path, before_hash in hashes_before.items():
        assert rel_path in hashes_after, f"File was deleted by scanner: {rel_path}"
        assert hashes_after[rel_path] == before_hash, (
            f"File was modified by scanner: {rel_path}"
        )


def test_scanner_adds_no_new_files(sample_repo):
    before = set(_hash_all_files(sample_repo).keys())
    RepoScanner().scan(sample_repo)
    after = set(_hash_all_files(sample_repo).keys())
    new_files = after - before
    assert not new_files, f"Scanner created unexpected files: {new_files}"


def test_scanner_deletes_no_files(sample_repo):
    before = set(_hash_all_files(sample_repo).keys())
    RepoScanner().scan(sample_repo)
    after = set(_hash_all_files(sample_repo).keys())
    deleted_files = before - after
    assert not deleted_files, f"Scanner deleted files: {deleted_files}"


def test_scan_result_counts_are_consistent(sample_repo):
    result = RepoScanner(include_hidden=True, skip_git_internals=True).scan(sample_repo)
    assert result.total_files_found == result.total_files_scanned + result.total_files_skipped
    assert len(result.files) == result.total_files_scanned
    assert len(result.skipped) == result.total_files_skipped


def test_scanner_is_idempotent(sample_repo):
    scanner = RepoScanner(include_hidden=True)
    result1 = scanner.scan(sample_repo)
    result2 = scanner.scan(sample_repo)

    paths1 = {f.path for f in result1.files}
    paths2 = {f.path for f in result2.files}
    assert paths1 == paths2

    hashes1 = {f.path: f.sha256 for f in result1.files}
    hashes2 = {f.path: f.sha256 for f in result2.files}
    assert hashes1 == hashes2
