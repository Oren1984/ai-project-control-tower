from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ReportFormat(str, Enum):
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"


class ReportRecord(BaseModel):
    id: Optional[int] = None
    audit_run_id: int
    report_format: ReportFormat
    content: str
    file_path: Optional[str] = None
    created_at: Optional[datetime] = None
