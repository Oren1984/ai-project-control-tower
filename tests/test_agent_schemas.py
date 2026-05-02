import pytest

from app.audit.models import AgentResult, FindingModel, Severity

_FORBIDDEN_FIELDS = {"auto_fix", "fix_plan", "patch", "diff", "generated_code"}


def _finding(**kwargs) -> FindingModel:
    defaults = dict(
        category="security",
        severity=Severity.HIGH,
        title="Test finding",
        description="A test description",
        recommendation="Do something about it",
        agent_name="TestAgent",
    )
    defaults.update(kwargs)
    return FindingModel(**defaults)


def test_finding_required_fields_present():
    f = _finding()
    assert f.category == "security"
    assert f.severity == Severity.HIGH
    assert f.title == "Test finding"
    assert f.description == "A test description"
    assert f.recommendation == "Do something about it"
    assert f.agent_name == "TestAgent"


def test_finding_optional_fields_default_to_none():
    f = _finding()
    assert f.evidence is None
    assert f.file_path is None
    assert f.line_number is None


def test_finding_optional_fields_accepted():
    f = _finding(file_path="src/main.py", line_number=42, evidence="line 42 content")
    assert f.file_path == "src/main.py"
    assert f.line_number == 42
    assert f.evidence == "line 42 content"


def test_no_forbidden_fields_in_model():
    model_fields = set(FindingModel.model_fields.keys())
    assert not model_fields & _FORBIDDEN_FIELDS, (
        f"Forbidden fields in FindingModel: {model_fields & _FORBIDDEN_FIELDS}"
    )


def test_no_forbidden_fields_in_json_schema():
    schema_str = str(FindingModel.model_json_schema()).lower()
    for field in _FORBIDDEN_FIELDS:
        assert field not in schema_str, f"Forbidden field '{field}' found in JSON schema"


def test_all_severity_values_valid():
    for sev in Severity:
        f = _finding(severity=sev)
        assert f.severity == sev


def test_agent_result_structure():
    result = AgentResult(
        agent_name="SecurityAgent",
        findings=[_finding(severity=Severity.CRITICAL)],
        context_chunks_used=5,
    )
    assert result.agent_name == "SecurityAgent"
    assert len(result.findings) == 1
    assert result.context_chunks_used == 5


def test_agent_result_defaults():
    result = AgentResult(agent_name="QAAgent", findings=[])
    assert result.context_chunks_used == 0
    assert result.findings == []


def test_finding_serializes_without_forbidden_keys():
    f = _finding(file_path="app/main.py", evidence="some evidence")
    data = f.model_dump()
    assert not set(data.keys()) & _FORBIDDEN_FIELDS
    assert "category" in data
    assert "severity" in data
    assert "recommendation" in data
    assert "agent_name" in data
