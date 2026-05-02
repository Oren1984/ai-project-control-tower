"""
API-level tests for the report endpoint.
These tests use mocking — they do not require a live DB or API server.
"""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.audit.models import AuditResult, AuditScores, FindingModel, Severity
from app.reports.report_schema import ReportFormat, ReportRecord


def _make_scores(**overrides) -> AuditScores:
    defaults = dict(
        overall=85.0, architecture=90.0, qa=80.0, security=85.0,
        devops=90.0, mlops=80.0, documentation=85.0, rag_agent=90.0, observability=75.0,
    )
    defaults.update(overrides)
    return AuditScores(**defaults)


def _make_result(findings: list[FindingModel] | None = None) -> AuditResult:
    findings = findings or []
    return AuditResult(
        audit_run_id=1,
        status="completed",
        mode="hybrid",
        scores=_make_scores(),
        findings=findings,
        agent_results=[],
        total_findings=len(findings),
        started_at=datetime(2026, 5, 2, 10, 0, 0, tzinfo=timezone.utc),
        completed_at=datetime(2026, 5, 2, 10, 5, 0, tzinfo=timezone.utc),
    )


class TestReportRecord:
    def test_report_record_schema(self):
        record = ReportRecord(
            audit_run_id=1,
            report_format=ReportFormat.MARKDOWN,
            content="# Test Report",
        )
        assert record.audit_run_id == 1
        assert record.report_format == ReportFormat.MARKDOWN
        assert "# Test Report" in record.content

    def test_report_format_enum(self):
        assert ReportFormat("markdown") == ReportFormat.MARKDOWN
        assert ReportFormat("json") == ReportFormat.JSON
        assert ReportFormat("html") == ReportFormat.HTML

    def test_report_format_invalid(self):
        with pytest.raises(ValueError):
            ReportFormat("xml")


class TestReportStoreInterface:
    def test_store_report_calls_db(self):
        from app.reports.report_store import store_report

        mock_db = MagicMock()
        mock_record = MagicMock()
        mock_record.id = 99
        mock_record.audit_run_id = 1
        mock_record.report_format = "markdown"
        mock_record.content = "# Report"
        mock_record.created_at = datetime(2026, 5, 2, tzinfo=timezone.utc)

        with patch("app.reports.report_store.Report", return_value=mock_record):
            result = store_report(mock_db, 1, ReportFormat.MARKDOWN, "# Report")

        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

    def test_get_latest_report_not_found(self):
        from app.reports.report_store import get_latest_report

        mock_db = MagicMock()
        mock_query = MagicMock()
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.first.return_value = None

        result = get_latest_report(mock_db, 999, ReportFormat.MARKDOWN)

        assert result is None


class TestReportEndpointLogic:
    def test_generate_markdown_is_not_empty(self):
        from app.reports.report_generator import generate_markdown

        result = _make_result()
        md = generate_markdown(result, project_name="TestProject")
        assert len(md) > 100
        assert "TestProject" in md

    def test_generate_json_is_valid(self):
        import json

        from app.reports.report_generator import generate_json

        result = _make_result()
        content = generate_json(result)
        data = json.loads(content)
        assert data["status"] == "completed"
        assert data["scores"]["overall"] == 85.0

    def test_generate_html_is_valid(self):
        from app.reports.report_generator import generate_html

        result = _make_result()
        html = generate_html(result)
        assert "<html" in html
        assert "85" in html

    def test_no_auto_fix_in_any_format(self):
        from app.reports.report_generator import (
            generate_html,
            generate_json,
            generate_markdown,
        )

        result = _make_result()
        for fn in [generate_markdown, generate_html, generate_json]:
            output = fn(result)
            assert "auto fix" not in output.lower()
            assert "patch plan" not in output.lower()

    def test_no_secrets_across_formats(self):
        from app.reports.report_generator import (
            generate_html,
            generate_json,
            generate_markdown,
        )

        finding = FindingModel(
            agent_name="SecurityAgent",
            category="security",
            severity=Severity.HIGH,
            title="Token found",
            description="Raw token in code",
            evidence="TOKEN=secrettoken999",
            recommendation="Remove token from source.",
        )
        result = _make_result([finding])
        for fn in [generate_markdown, generate_html, generate_json]:
            output = fn(result)
            assert "secrettoken999" not in output
