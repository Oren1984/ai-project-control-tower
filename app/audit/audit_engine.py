from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.agents.base_agent import AuditContext
from app.agents.orchestrator_agent import OrchestratorAgent
from app.audit.models import AuditResult, FindingModel
from app.audit.scoring import compute_scores
from app.core.logging import get_logger
from app.rag.rag_service import RAGService
from app.scanner.path_validator import PathValidationError, validate_scan_path
from app.scanner.repo_scanner import RepoScanner

logger = get_logger(__name__)


class AuditEngine:
    def __init__(
        self,
        rag_service: RAGService | None = None,
        orchestrator: OrchestratorAgent | None = None,
    ) -> None:
        self._rag = rag_service or RAGService(mode="hybrid")
        self._orchestrator = orchestrator or OrchestratorAgent()

    def run(
        self,
        repo_path: str,
        audit_run_id: int,
        mode: str = "hybrid",
        db_session: Any | None = None,
    ) -> AuditResult:
        started_at = datetime.now(timezone.utc)
        logger.info("audit_engine_start", audit_run_id=audit_run_id, repo_path=repo_path, mode=mode)

        try:
            validated_path = validate_scan_path(repo_path)
        except PathValidationError as exc:
            logger.error("audit_path_invalid", audit_run_id=audit_run_id, error=str(exc))
            return AuditResult(
                audit_run_id=audit_run_id,
                status="failed",
                mode=mode,
                scores=compute_scores([]),
                findings=[],
                agent_results=[],
                total_findings=0,
                started_at=started_at,
                completed_at=datetime.now(timezone.utc),
            )

        scan_result = RepoScanner().scan(validated_path)
        logger.info("audit_engine_scanned", files=scan_result.total_files_scanned)

        chunks_indexed = self._rag.index_scan_result(scan_result)
        logger.info("audit_engine_indexed", chunks=chunks_indexed)

        context = AuditContext(
            scan_result=scan_result,
            repo_path=validated_path,
            mode=mode,
            retrieve=self._rag.retrieve,
            audit_run_id=audit_run_id,
        )

        agent_results = self._orchestrator.run_all(context)

        all_findings: list[FindingModel] = []
        for result in agent_results:
            all_findings.extend(result.findings)

        if db_session is not None:
            self._persist(db_session, audit_run_id, all_findings)

        scores = compute_scores(all_findings)
        completed_at = datetime.now(timezone.utc)

        logger.info(
            "audit_engine_complete",
            audit_run_id=audit_run_id,
            total_findings=len(all_findings),
            overall_score=scores.overall,
        )

        return AuditResult(
            audit_run_id=audit_run_id,
            status="completed",
            mode=mode,
            scores=scores,
            findings=all_findings,
            agent_results=agent_results,
            total_findings=len(all_findings),
            started_at=started_at,
            completed_at=completed_at,
        )

    def _persist(self, db_session: Any, audit_run_id: int, findings: list[FindingModel]) -> None:
        from app.db.models.audit_run import AuditRun
        from app.db.models.finding import Finding

        try:
            for f in findings:
                db_session.add(Finding(
                    audit_run_id=audit_run_id,
                    agent_name=f.agent_name,
                    category=f.category,
                    severity=f.severity.value,
                    title=f.title,
                    description=f.description,
                    evidence=f.evidence,
                    recommendation=f.recommendation,
                    file_path=f.file_path,
                    line_number=f.line_number,
                ))

            audit_run = db_session.get(AuditRun, audit_run_id)
            if audit_run:
                audit_run.status = "completed"
                audit_run.completed_at = datetime.now(timezone.utc)

            db_session.commit()
            logger.info("audit_engine_persisted", audit_run_id=audit_run_id, count=len(findings))
        except Exception as exc:
            logger.error("audit_engine_persist_failed", error=str(exc))
            db_session.rollback()
