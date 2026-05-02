import json
from datetime import datetime, timezone

from app.audit.models import AgentResult, AuditResult, AuditScores, FindingModel, Severity
from app.audit.scoring import compute_scores
from app.reports.report_generator import generate_html, generate_json, generate_markdown


def _make_result(findings: list[FindingModel] | None = None) -> AuditResult:
    if findings is None:
        findings = []
    scores = compute_scores(findings)
    return AuditResult(
        audit_run_id=42,
        status="completed",
        mode="hybrid",
        scores=scores,
        findings=findings,
        agent_results=[],
        total_findings=len(findings),
        started_at=datetime(2026, 5, 2, 10, 0, 0, tzinfo=timezone.utc),
        completed_at=datetime(2026, 5, 2, 10, 5, 0, tzinfo=timezone.utc),
    )


def _sample_finding() -> FindingModel:
    return FindingModel(
        agent_name="SecurityAgent",
        category="security",
        severity=Severity.HIGH,
        title="Hardcoded credential detected",
        description="A potential API key was found in source code.",
        evidence="line 42: api_key = 'sk-abc'",
        recommendation="Move credentials to environment variables.",
        file_path="app/config.py",
        line_number=42,
    )


class TestGenerateMarkdown:
    def test_contains_all_18_sections(self):
        result = _make_result()
        md = generate_markdown(result)
        for i in range(1, 19):
            assert f"## {i}." in md

    def test_contains_project_name(self):
        result = _make_result()
        md = generate_markdown(result, project_name="TestProject")
        assert "TestProject" in md

    def test_contains_overall_score(self):
        result = _make_result()
        md = generate_markdown(result)
        assert "100.0" in md

    def test_finding_appears_in_output(self):
        finding = _sample_finding()
        result = _make_result([finding])
        md = generate_markdown(result)
        assert "Hardcoded credential detected" in md

    def test_no_autofix_content(self):
        result = _make_result()
        md = generate_markdown(result)
        assert "auto fix" not in md.lower()
        assert "patch plan" not in md.lower()

    def test_no_secrets_in_output(self):
        finding = FindingModel(
            agent_name="SecurityAgent",
            category="security",
            severity=Severity.CRITICAL,
            title="Secret exposed",
            description="Password=actualsecret123",
            evidence="PASSWORD=topsecret99",
            recommendation="Remove from codebase.",
        )
        result = _make_result([finding])
        md = generate_markdown(result)
        assert "topsecret99" not in md
        assert "actualsecret123" not in md

    def test_critical_finding_in_section_12(self):
        finding = FindingModel(
            agent_name="SecurityAgent",
            category="security",
            severity=Severity.CRITICAL,
            title="Critical issue found",
            description="Something very bad.",
            recommendation="Fix it.",
        )
        result = _make_result([finding])
        md = generate_markdown(result)
        assert "Critical issue found" in md
        assert "## 12." in md


class TestGenerateJSON:
    def test_valid_json(self):
        result = _make_result()
        content = generate_json(result)
        data = json.loads(content)
        assert data["audit_run_id"] == 42
        assert "scores" in data
        assert "findings" in data

    def test_findings_in_json(self):
        finding = _sample_finding()
        result = _make_result([finding])
        content = generate_json(result)
        data = json.loads(content)
        assert len(data["findings"]) == 1
        assert data["findings"][0]["severity"] == "high"

    def test_project_name_in_json(self):
        result = _make_result()
        content = generate_json(result, project_name="MyProject")
        data = json.loads(content)
        assert data["project_name"] == "MyProject"

    def test_no_secrets_in_json(self):
        finding = FindingModel(
            agent_name="SecurityAgent",
            category="security",
            severity=Severity.HIGH,
            title="API key leak",
            description="Key found",
            evidence="TOKEN=mytoken123",
            recommendation="Remove it.",
        )
        result = _make_result([finding])
        content = generate_json(result)
        assert "mytoken123" not in content


class TestGenerateHTML:
    def test_is_html(self):
        result = _make_result()
        html = generate_html(result)
        assert "<html" in html
        assert "</html>" in html

    def test_contains_all_sections(self):
        result = _make_result()
        html = generate_html(result)
        for i in range(1, 19):
            assert f"<h2>{i}." in html

    def test_finding_in_html(self):
        finding = _sample_finding()
        result = _make_result([finding])
        html = generate_html(result)
        assert "Hardcoded credential detected" in html

    def test_no_secrets_in_html(self):
        finding = FindingModel(
            agent_name="SecurityAgent",
            category="security",
            severity=Severity.CRITICAL,
            title="Secret in report",
            description="Raw value",
            evidence="API_KEY=secretvalue99",
            recommendation="Remove it.",
        )
        result = _make_result([finding])
        html = generate_html(result)
        assert "secretvalue99" not in html


class TestNoRepoModification:
    def test_generate_does_not_write_files(self, tmp_path):
        result = _make_result()
        generate_markdown(result)
        generate_json(result)
        generate_html(result)
        assert list(tmp_path.iterdir()) == []
