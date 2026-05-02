from __future__ import annotations

from app.audit.models import AuditScores, FindingModel, Severity

SEVERITY_WEIGHTS: dict[Severity, float] = {
    Severity.CRITICAL: 10.0,
    Severity.HIGH: 5.0,
    Severity.MEDIUM: 2.0,
    Severity.LOW: 1.0,
    Severity.INFO: 0.0,
}

_CATEGORY_TO_DIMENSION: dict[str, str] = {
    "architecture": "architecture",
    "quality": "qa",
    "testing": "qa",
    "security": "security",
    "devops": "devops",
    "mlops": "mlops",
    "documentation": "documentation",
    "rag": "rag_agent",
    "observability": "observability",
}

_BASE_SCORE = 100.0
_ALL_DIMENSIONS = ("architecture", "qa", "security", "devops", "mlops", "documentation", "rag_agent", "observability")


def compute_scores(findings: list[FindingModel]) -> AuditScores:
    penalties: dict[str, float] = {dim: 0.0 for dim in _ALL_DIMENSIONS}

    for finding in findings:
        weight = SEVERITY_WEIGHTS.get(finding.severity, 0.0)
        dim = _map_category(finding.category)
        penalties[dim] += weight

    scores = {dim: max(0.0, round(_BASE_SCORE - penalties[dim], 1)) for dim in _ALL_DIMENSIONS}
    overall = round(sum(scores.values()) / len(scores), 1)

    return AuditScores(
        overall=overall,
        architecture=scores["architecture"],
        qa=scores["qa"],
        security=scores["security"],
        devops=scores["devops"],
        mlops=scores["mlops"],
        documentation=scores["documentation"],
        rag_agent=scores["rag_agent"],
        observability=scores["observability"],
    )


def _map_category(category: str) -> str:
    cat_lower = category.lower()
    for key, dim in _CATEGORY_TO_DIMENSION.items():
        if key in cat_lower:
            return dim
    return "architecture"
