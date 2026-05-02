import os
from pathlib import Path
from unittest.mock import patch

import pytest

from app.audit.audit_engine import AuditEngine
from app.audit.models import AuditResult


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    (tmp_path / "README.md").write_text("# Test Repo\nA minimal test repository.")
    (tmp_path / "main.py").write_text("print('hello')\n")
    (tmp_path / "requirements.txt").write_text("fastapi\n")
    (tmp_path / ".gitignore").write_text("*.pyc\n__pycache__\n.env\n")
    return tmp_path


def test_audit_engine_happy_path(tmp_repo: Path):
    with patch("app.audit.audit_engine.validate_scan_path", return_value=tmp_repo):
        result = AuditEngine().run(
            repo_path=str(tmp_repo),
            audit_run_id=1,
            mode="hybrid",
        )

    assert isinstance(result, AuditResult)
    assert result.status == "completed"
    assert result.audit_run_id == 1
    assert result.mode == "hybrid"
    assert 0.0 <= result.scores.overall <= 100.0
    assert isinstance(result.findings, list)
    assert len(result.agent_results) > 0
    assert result.total_findings == len(result.findings)


def test_audit_engine_invalid_path_returns_failed():
    result = AuditEngine().run(
        repo_path="/no/such/path/xyzzy",
        audit_run_id=999,
        mode="hybrid",
    )
    assert result.status == "failed"
    assert result.audit_run_id == 999


def test_audit_engine_does_not_modify_target_repo(tmp_repo: Path):
    snapshot: dict[str, bytes] = {}
    for root, _dirs, files in os.walk(str(tmp_repo)):
        for fname in files:
            full = Path(root) / fname
            snapshot[str(full)] = full.read_bytes()

    with patch("app.audit.audit_engine.validate_scan_path", return_value=tmp_repo):
        AuditEngine().run(repo_path=str(tmp_repo), audit_run_id=99, mode="agent_only")

    after: dict[str, bytes] = {}
    for root, _dirs, files in os.walk(str(tmp_repo)):
        for fname in files:
            full = Path(root) / fname
            after[str(full)] = full.read_bytes()

    assert snapshot == after, "Audit engine must not modify target repository files"


def test_audit_result_contains_no_forbidden_fields(tmp_repo: Path):
    with patch("app.audit.audit_engine.validate_scan_path", return_value=tmp_repo):
        result = AuditEngine().run(repo_path=str(tmp_repo), audit_run_id=2, mode="hybrid")

    forbidden = {"auto_fix", "fix_plan", "patch", "diff", "generated_code"}
    for finding in result.findings:
        keys = set(finding.model_dump().keys())
        assert not keys & forbidden, f"Forbidden keys in finding: {keys & forbidden}"


def test_audit_engine_rag_only_mode(tmp_repo: Path):
    with patch("app.audit.audit_engine.validate_scan_path", return_value=tmp_repo):
        result = AuditEngine().run(repo_path=str(tmp_repo), audit_run_id=3, mode="rag_only")

    assert result.status == "completed"
    assert result.mode == "rag_only"


def test_audit_engine_agent_only_mode(tmp_repo: Path):
    with patch("app.audit.audit_engine.validate_scan_path", return_value=tmp_repo):
        result = AuditEngine().run(repo_path=str(tmp_repo), audit_run_id=4, mode="agent_only")

    assert result.status == "completed"
    assert result.mode == "agent_only"


def test_all_agent_results_have_name(tmp_repo: Path):
    with patch("app.audit.audit_engine.validate_scan_path", return_value=tmp_repo):
        result = AuditEngine().run(repo_path=str(tmp_repo), audit_run_id=5, mode="hybrid")

    for ar in result.agent_results:
        assert ar.agent_name
        assert isinstance(ar.findings, list)
