import hashlib
import os
from pathlib import Path

import pytest

from app.scanner.repo_scanner import RepoScanner, _sha256
from app.schemas.scan_schemas import FileCategory, SkipReason


@pytest.fixture
def temp_repo(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')")
    (tmp_path / "tests" / "test_main.py").write_text("def test_foo(): pass")
    (tmp_path / "README.md").write_text("# Test Repo")
    (tmp_path / ".gitignore").write_text("*.pyc\n__pycache__/")
    (tmp_path / ".hidden_config.yaml").write_text("key: value")
    return tmp_path


def test_scanner_finds_text_files(temp_repo):
    result = RepoScanner().scan(temp_repo)
    assert result.total_files_scanned >= 3


def test_scanner_recursive(temp_repo):
    result = RepoScanner().scan(temp_repo)
    rel_paths = {f.relative_path for f in result.files}
    assert any("main.py" in p for p in rel_paths)
    assert any("test_main.py" in p for p in rel_paths)


def test_scanner_includes_hidden_files_by_default(temp_repo):
    result = RepoScanner(include_hidden=True).scan(temp_repo)
    hidden = [f for f in result.files if f.is_hidden]
    assert len(hidden) >= 1


def test_scanner_excludes_hidden_files_when_disabled(temp_repo):
    result = RepoScanner(include_hidden=False).scan(temp_repo)
    hidden = [f for f in result.files if f.is_hidden]
    assert len(hidden) == 0


def test_scanner_skips_binary_files(tmp_path):
    (tmp_path / "image.bin").write_bytes(b"\x00\x01\x02\x03" * 100)
    (tmp_path / "normal.py").write_text("x = 1")
    result = RepoScanner().scan(tmp_path)
    skipped_reasons = {s.reason for s in result.skipped}
    assert SkipReason.BINARY in skipped_reasons


def test_scanner_skips_oversized_files(tmp_path):
    (tmp_path / "big.txt").write_text("x" * 10_000)
    (tmp_path / "small.py").write_text("y = 1")
    result = RepoScanner(max_file_size_bytes=100).scan(tmp_path)
    skipped_reasons = {s.reason for s in result.skipped}
    assert SkipReason.OVERSIZED in skipped_reasons


def test_oversized_file_detail_message(tmp_path):
    (tmp_path / "big.txt").write_text("x" * 10_000)
    result = RepoScanner(max_file_size_bytes=100).scan(tmp_path)
    oversized = [s for s in result.skipped if s.reason == SkipReason.OVERSIZED]
    assert len(oversized) == 1
    assert oversized[0].details is not None


def test_sha256_hash_matches_expected(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("hello world")
    expected = hashlib.sha256(b"hello world").hexdigest()
    assert _sha256(f) == expected


def test_sha256_differs_for_different_content(tmp_path):
    f1 = tmp_path / "a.txt"
    f2 = tmp_path / "b.txt"
    f1.write_text("content A")
    f2.write_text("content B")
    assert _sha256(f1) != _sha256(f2)


def test_scanner_skips_git_internals(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("[core]\nbare = false")
    (tmp_path / "app.py").write_text("pass")
    result = RepoScanner(skip_git_internals=True).scan(tmp_path)
    all_paths = {f.path for f in result.files} | {f.path for f in result.skipped}
    git_paths = {p for p in all_paths if ".git" in Path(p).parts}
    assert not git_paths


def test_scanner_includes_git_internals_when_enabled(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("[core]\nbare = false")
    (tmp_path / "app.py").write_text("pass")
    result = RepoScanner(skip_git_internals=False).scan(tmp_path)
    all_paths = {f.path for f in result.files} | {f.path for f in result.skipped}
    git_paths = {p for p in all_paths if ".git" in Path(p).parts}
    assert git_paths


def test_total_files_found_equals_scanned_plus_skipped(tmp_path):
    (tmp_path / "code.py").write_text("x = 1")
    (tmp_path / "binary.bin").write_bytes(b"\x00" * 50)
    result = RepoScanner().scan(tmp_path)
    assert result.total_files_found == result.total_files_scanned + result.total_files_skipped


def test_scanner_classifies_readme(temp_repo):
    result = RepoScanner().scan(temp_repo)
    readme_files = [f for f in result.files if f.category == FileCategory.README]
    assert len(readme_files) >= 1


def test_scanner_classifies_gitignore(temp_repo):
    result = RepoScanner(include_hidden=True).scan(temp_repo)
    gitignore_files = [f for f in result.files if f.category == FileCategory.GITIGNORE]
    assert len(gitignore_files) >= 1


def test_scanner_classifies_tests(temp_repo):
    result = RepoScanner().scan(temp_repo)
    test_files = [f for f in result.files if f.category == FileCategory.TEST]
    assert len(test_files) >= 1


def test_scanner_handles_empty_directory(tmp_path):
    result = RepoScanner().scan(tmp_path)
    assert result.total_files_scanned == 0
    assert result.total_files_skipped == 0
    assert result.total_files_found == 0
