from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.audit.audit_engine import AuditEngine
from app.audit.models import AuditResult, AuditScores, FindingModel, Severity
from app.audit.scoring import compute_scores
from app.core.logging import get_logger
from app.db.models.audit_run import AuditRun
from app.db.models.project import Project
from app.db.session import get_db
from app.reports.report_generator import generate_html, generate_json, generate_markdown
from app.reports.report_schema import ReportFormat
from app.reports.report_store import get_latest_report, store_report
from app.schemas.agent_schemas import AuditRunRequest

router = APIRouter()
logger = get_logger(__name__)


def _run_audit_impl(request: AuditRunRequest, db: Session) -> AuditResult:
    project = db.get(Project, request.project_id)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project {request.project_id} not found")

    audit_run = AuditRun(
        project_id=request.project_id,
        blueprint_id=request.blueprint_id,
        mode=request.mode.value,
        status="running",
        started_at=datetime.now(timezone.utc),
    )
    db.add(audit_run)
    db.commit()
    db.refresh(audit_run)

    engine = AuditEngine()
    try:
        result = engine.run(
            repo_path=request.repo_path,
            audit_run_id=audit_run.id,
            mode=request.mode.value,
            db_session=db,
        )
    except Exception as exc:
        logger.error("audit_run_failed", audit_run_id=audit_run.id, error=str(exc))
        audit_run.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail="Audit failed unexpectedly")

    if audit_run.overall_score is None:
        audit_run.overall_score = result.scores.overall
        db.commit()

    return result


@router.post("/audits/run", response_model=AuditResult, status_code=201)
def run_audit_v2(request: AuditRunRequest, db: Session = Depends(get_db)) -> AuditResult:
    return _run_audit_impl(request, db)


@router.post("/audits", response_model=AuditResult, status_code=201)
def run_audit(request: AuditRunRequest, db: Session = Depends(get_db)) -> AuditResult:
    return _run_audit_impl(request, db)


@router.get("/audits/history")
def get_audit_history(
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> dict:
    runs = (
        db.query(AuditRun)
        .order_by(AuditRun.created_at.desc())
        .limit(limit)
        .all()
    )
    return {
        "audits": [
            {
                "id": r.id,
                "project_id": r.project_id,
                "blueprint_id": r.blueprint_id,
                "mode": r.mode,
                "status": r.status,
                "overall_score": r.overall_score,
                "started_at": r.started_at.isoformat() if r.started_at else None,
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "created_at": r.created_at.isoformat(),
            }
            for r in runs
        ]
    }


@router.get("/audits/{audit_run_id}")
def get_audit(audit_run_id: int, db: Session = Depends(get_db)) -> dict:
    from app.db.models.finding import Finding

    audit_run = db.get(AuditRun, audit_run_id)
    if audit_run is None:
        raise HTTPException(status_code=404, detail=f"Audit run {audit_run_id} not found")

    findings = db.query(Finding).filter(Finding.audit_run_id == audit_run_id).all()
    return {
        "id": audit_run.id,
        "project_id": audit_run.project_id,
        "blueprint_id": audit_run.blueprint_id,
        "mode": audit_run.mode,
        "status": audit_run.status,
        "overall_score": audit_run.overall_score,
        "started_at": audit_run.started_at.isoformat() if audit_run.started_at else None,
        "completed_at": audit_run.completed_at.isoformat() if audit_run.completed_at else None,
        "created_at": audit_run.created_at.isoformat(),
        "total_findings": len(findings),
    }


@router.get("/audits/{audit_run_id}/findings")
def get_audit_findings(audit_run_id: int, db: Session = Depends(get_db)) -> dict:
    from app.db.models.finding import Finding

    audit_run = db.get(AuditRun, audit_run_id)
    if audit_run is None:
        raise HTTPException(status_code=404, detail=f"Audit run {audit_run_id} not found")

    findings = db.query(Finding).filter(Finding.audit_run_id == audit_run_id).all()
    return {
        "audit_run_id": audit_run_id,
        "status": audit_run.status,
        "total_findings": len(findings),
        "findings": [
            {
                "id": f.id,
                "agent_name": f.agent_name,
                "category": f.category,
                "severity": f.severity,
                "title": f.title,
                "description": f.description,
                "evidence": f.evidence,
                "recommendation": f.recommendation,
                "file_path": f.file_path,
                "line_number": f.line_number,
            }
            for f in findings
        ],
    }


@router.get("/audits/{audit_run_id}/report")
def get_audit_report(
    audit_run_id: int,
    format: str = Query(default="markdown", pattern="^(markdown|json|html)$"),
    db: Session = Depends(get_db),
) -> dict:
    from app.db.models.finding import Finding

    audit_run = db.get(AuditRun, audit_run_id)
    if audit_run is None:
        raise HTTPException(status_code=404, detail=f"Audit run {audit_run_id} not found")
    if audit_run.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Audit run {audit_run_id} is not completed (status={audit_run.status})",
        )

    report_format = ReportFormat(format)
    existing = get_latest_report(db, audit_run_id, report_format)
    if existing:
        return {
            "audit_run_id": audit_run_id,
            "format": format,
            "content": existing.content,
            "report_id": existing.id,
            "created_at": existing.created_at.isoformat() if existing.created_at else None,
        }

    db_findings = db.query(Finding).filter(Finding.audit_run_id == audit_run_id).all()
    findings = [
        FindingModel(
            agent_name=f.agent_name,
            category=f.category,
            severity=Severity(f.severity),
            title=f.title,
            description=f.description,
            evidence=f.evidence,
            recommendation=f.recommendation,
            file_path=f.file_path,
            line_number=f.line_number,
        )
        for f in db_findings
    ]

    scores = compute_scores(findings)
    result = AuditResult(
        audit_run_id=audit_run_id,
        status=audit_run.status,
        mode=audit_run.mode,
        scores=scores,
        findings=findings,
        agent_results=[],
        total_findings=len(findings),
        started_at=audit_run.started_at,
        completed_at=audit_run.completed_at,
    )

    project = db.get(Project, audit_run.project_id)
    project_name = project.name if project else ""
    blueprint_name = ""
    if audit_run.blueprint_id:
        from app.db.models.blueprint import Blueprint
        bp = db.get(Blueprint, audit_run.blueprint_id)
        blueprint_name = bp.name if bp else ""

    if report_format == ReportFormat.MARKDOWN:
        content = generate_markdown(result, project_name, blueprint_name)
    elif report_format == ReportFormat.HTML:
        content = generate_html(result, project_name, blueprint_name)
    else:
        content = generate_json(result, project_name, blueprint_name)

    record = store_report(db, audit_run_id, report_format, content)
    return {
        "audit_run_id": audit_run_id,
        "format": format,
        "content": content,
        "report_id": record.id,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }
