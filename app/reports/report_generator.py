from __future__ import annotations

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.audit.models import AuditResult, FindingModel, Severity
from app.reports.report_sanitizer import sanitize_report

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=False,
    keep_trailing_newline=True,
)


def _build_context(
    result: AuditResult,
    project_name: str,
    blueprint_name: str,
) -> dict:
    audit_date = (
        result.completed_at.strftime("%Y-%m-%d %H:%M UTC")
        if result.completed_at
        else "N/A"
    )

    by_agent: dict[str, list[FindingModel]] = {}
    for f in result.findings:
        by_agent.setdefault(f.agent_name, []).append(f)

    return {
        "result": result,
        "project_name": project_name or "N/A",
        "blueprint_name": blueprint_name or "N/A",
        "audit_date": audit_date,
        "critical_findings": [f for f in result.findings if f.severity == Severity.CRITICAL],
        "high_findings": [f for f in result.findings if f.severity == Severity.HIGH],
        "medium_findings": [f for f in result.findings if f.severity == Severity.MEDIUM],
        "low_findings": [f for f in result.findings if f.severity == Severity.LOW],
        "info_findings": [f for f in result.findings if f.severity == Severity.INFO],
        "findings_by_agent": by_agent,
    }


def generate_markdown(
    result: AuditResult,
    project_name: str = "",
    blueprint_name: str = "",
) -> str:
    ctx = _build_context(result, project_name, blueprint_name)
    raw = _env.get_template("report.md.j2").render(**ctx)
    return sanitize_report(raw)


def generate_html(
    result: AuditResult,
    project_name: str = "",
    blueprint_name: str = "",
) -> str:
    ctx = _build_context(result, project_name, blueprint_name)
    raw = _env.get_template("report.html.j2").render(**ctx)
    return sanitize_report(raw)


def generate_json(
    result: AuditResult,
    project_name: str = "",
    blueprint_name: str = "",
) -> str:
    data = {
        "audit_run_id": result.audit_run_id,
        "project_name": project_name or "N/A",
        "blueprint_name": blueprint_name or "N/A",
        "status": result.status,
        "mode": result.mode,
        "audit_date": (
            result.completed_at.isoformat() if result.completed_at else None
        ),
        "started_at": result.started_at.isoformat() if result.started_at else None,
        "completed_at": result.completed_at.isoformat() if result.completed_at else None,
        "scores": {
            "overall": result.scores.overall,
            "architecture": result.scores.architecture,
            "qa": result.scores.qa,
            "security": result.scores.security,
            "devops": result.scores.devops,
            "mlops": result.scores.mlops,
            "documentation": result.scores.documentation,
            "rag_agent": result.scores.rag_agent,
            "observability": result.scores.observability,
        },
        "total_findings": result.total_findings,
        "findings": [
            {
                "agent_name": f.agent_name,
                "category": f.category,
                "severity": f.severity.value,
                "title": f.title,
                "description": f.description,
                "evidence": f.evidence,
                "recommendation": f.recommendation,
                "file_path": f.file_path,
                "line_number": f.line_number,
            }
            for f in result.findings
        ],
    }
    raw = json.dumps(data, indent=2, ensure_ascii=False)
    return sanitize_report(raw)
