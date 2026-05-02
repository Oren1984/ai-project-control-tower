from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingModel(BaseModel):
    category: str
    severity: Severity
    title: str
    description: str
    evidence: Optional[str] = None
    recommendation: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    agent_name: str


class AgentResult(BaseModel):
    agent_name: str
    findings: list[FindingModel]
    context_chunks_used: int = 0


class AuditScores(BaseModel):
    overall: float
    architecture: float
    qa: float
    security: float
    devops: float
    mlops: float
    documentation: float
    rag_agent: float
    observability: float


class AuditResult(BaseModel):
    audit_run_id: int
    status: str
    mode: str
    scores: AuditScores
    findings: list[FindingModel]
    agent_results: list[AgentResult]
    total_findings: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
