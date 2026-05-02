from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from app.audit.models import AgentResult, FindingModel
from app.schemas.scan_schemas import ScanResult


@dataclass
class AuditContext:
    scan_result: ScanResult
    repo_path: Path
    mode: str
    retrieve: Callable[[str, int], list] = field(default_factory=lambda: lambda q, k=5: [])
    audit_run_id: int = 0


class BaseAgent(ABC):
    name: str = "BaseAgent"

    @abstractmethod
    def analyze(self, context: AuditContext) -> AgentResult:
        ...

    def _make_finding(
        self,
        category: str,
        severity: str,
        title: str,
        description: str,
        recommendation: str,
        evidence: str | None = None,
        file_path: str | None = None,
        line_number: int | None = None,
    ) -> FindingModel:
        return FindingModel(
            category=category,
            severity=severity,
            title=title,
            description=description,
            evidence=evidence,
            recommendation=recommendation,
            file_path=file_path,
            line_number=line_number,
            agent_name=self.name,
        )
