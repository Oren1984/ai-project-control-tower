from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AuditMode(str, Enum):
    RAG_ONLY = "rag_only"
    AGENT_ONLY = "agent_only"
    HYBRID = "hybrid"


class AuditRunRequest(BaseModel):
    project_id: int
    repo_path: str
    mode: AuditMode = AuditMode.HYBRID
    blueprint_id: Optional[int] = None
