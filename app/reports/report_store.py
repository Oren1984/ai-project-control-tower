from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from app.core.logging import get_logger
from app.db.models.report import Report
from app.reports.report_schema import ReportFormat, ReportRecord

logger = get_logger(__name__)


def store_report(
    db_session: Any,
    audit_run_id: int,
    report_format: ReportFormat,
    content: str,
) -> ReportRecord:
    record = Report(
        audit_run_id=audit_run_id,
        report_format=report_format.value,
        content=content,
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)
    logger.info(
        "report_stored",
        audit_run_id=audit_run_id,
        format=report_format.value,
        report_id=record.id,
    )
    return ReportRecord(
        id=record.id,
        audit_run_id=record.audit_run_id,
        report_format=ReportFormat(record.report_format),
        content=record.content,
        created_at=record.created_at,
    )


def get_latest_report(
    db_session: Any,
    audit_run_id: int,
    report_format: ReportFormat = ReportFormat.MARKDOWN,
) -> Optional[ReportRecord]:
    record = (
        db_session.query(Report)
        .filter(
            Report.audit_run_id == audit_run_id,
            Report.report_format == report_format.value,
        )
        .order_by(Report.created_at.desc())
        .first()
    )
    if record is None:
        return None
    return ReportRecord(
        id=record.id,
        audit_run_id=record.audit_run_id,
        report_format=ReportFormat(record.report_format),
        content=record.content,
        created_at=record.created_at,
    )
