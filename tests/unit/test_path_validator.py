import pytest
from pathlib import Path
from unittest.mock import patch

from app.scanner.path_validator import PathValidationError, validate_scan_path


def _mock_settings(allowed: list[str]):
    """Return a patch context that sets allowed_scan_paths."""
    return patch(
        "app.scanner.path_validator.settings",
        allowed_scan_paths=allowed,
    )


def test_path_within_allowed_passes(tmp_path):
    sub = tmp_path / "my_repo"
    sub.mkdir()
    with _mock_settings([str(tmp_path)]):
        result = validate_scan_path(str(sub))
    assert result == sub.resolve()


def test_exact_allowed_path_passes(tmp_path):
    with _mock_settings([str(tmp_path)]):
        result = validate_scan_path(str(tmp_path))
    assert result == tmp_path.resolve()


def test_path_outside_allowed_fails(tmp_path):
    allowed = tmp_path / "allowed"
    outside = tmp_path / "outside"
    allowed.mkdir()
    outside.mkdir()
    with _mock_settings([str(allowed)]):
        with pytest.raises(PathValidationError, match="outside all allowed"):
            validate_scan_path(str(outside))


def test_empty_allowlist_fails(tmp_path):
    with _mock_settings([]):
        with pytest.raises(PathValidationError, match="No allowed scan paths"):
            validate_scan_path(str(tmp_path))


def test_nonexistent_path_fails(tmp_path):
    with _mock_settings([str(tmp_path)]):
        with pytest.raises(PathValidationError, match="does not exist"):
            validate_scan_path(str(tmp_path / "nonexistent"))


def test_file_path_fails(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("content")
    with _mock_settings([str(tmp_path)]):
        with pytest.raises(PathValidationError, match="not a directory"):
            validate_scan_path(str(f))


def test_path_traversal_blocked(tmp_path):
    allowed = tmp_path / "allowed"
    sibling = tmp_path / "sibling"
    allowed.mkdir()
    sibling.mkdir()
    traversal = str(allowed) + "/../sibling"
    with _mock_settings([str(allowed)]):
        with pytest.raises(PathValidationError, match="outside all allowed"):
            validate_scan_path(traversal)


def test_multiple_allowed_paths_first_match(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    target = tmp_path / "b" / "repo"
    a.mkdir()
    b.mkdir()
    target.mkdir()
    with _mock_settings([str(a), str(b)]):
        result = validate_scan_path(str(target))
    assert result == target.resolve()


def test_multiple_allowed_paths_no_match(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    outside = tmp_path / "outside"
    a.mkdir()
    b.mkdir()
    outside.mkdir()
    with _mock_settings([str(a), str(b)]):
        with pytest.raises(PathValidationError, match="outside all allowed"):
            validate_scan_path(str(outside))
