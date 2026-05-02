import pytest

from app.audit.models import FindingModel, Severity
from app.audit.scoring import SEVERITY_WEIGHTS, compute_scores


def _finding(category: str, severity: Severity) -> FindingModel:
    return FindingModel(
        category=category,
        severity=severity,
        title="Test",
        description="desc",
        recommendation="rec",
        agent_name="TestAgent",
    )


def test_no_findings_gives_perfect_score():
    scores = compute_scores([])
    assert scores.overall == 100.0
    assert scores.security == 100.0
    assert scores.architecture == 100.0
    assert scores.qa == 100.0
    assert scores.devops == 100.0
    assert scores.mlops == 100.0
    assert scores.documentation == 100.0
    assert scores.rag_agent == 100.0
    assert scores.observability == 100.0


def test_critical_security_finding_reduces_security_score():
    findings = [_finding("security", Severity.CRITICAL)]
    scores = compute_scores(findings)
    expected = 100.0 - SEVERITY_WEIGHTS[Severity.CRITICAL]
    assert scores.security == expected
    assert scores.architecture == 100.0  # unaffected


def test_score_floored_at_zero():
    findings = [_finding("security", Severity.CRITICAL)] * 20
    scores = compute_scores(findings)
    assert scores.security == 0.0


def test_overall_is_mean_of_dimensions():
    findings = [_finding("security", Severity.HIGH)]
    scores = compute_scores(findings)
    dims = [
        scores.architecture, scores.qa, scores.security,
        scores.devops, scores.mlops, scores.documentation,
        scores.rag_agent, scores.observability,
    ]
    assert scores.overall == round(sum(dims) / len(dims), 1)


def test_multiple_categories_affect_distinct_dimensions():
    findings = [
        _finding("security", Severity.HIGH),
        _finding("testing", Severity.MEDIUM),
        _finding("devops", Severity.LOW),
    ]
    scores = compute_scores(findings)
    assert scores.security < 100.0
    assert scores.qa < 100.0
    assert scores.devops < 100.0
    assert scores.architecture == 100.0


def test_info_severity_has_zero_weight():
    findings = [_finding("security", Severity.INFO)]
    scores = compute_scores(findings)
    assert scores.security == 100.0


def test_documentation_finding_affects_documentation_dimension():
    findings = [_finding("documentation", Severity.HIGH)]
    scores = compute_scores(findings)
    assert scores.documentation < 100.0
    assert scores.security == 100.0


def test_rag_finding_affects_rag_agent_dimension():
    findings = [_finding("rag", Severity.MEDIUM)]
    scores = compute_scores(findings)
    assert scores.rag_agent < 100.0
