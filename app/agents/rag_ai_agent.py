from __future__ import annotations

from app.agents.base_agent import AuditContext, BaseAgent
from app.audit.models import AgentResult, FindingModel


class RAGAIAgent(BaseAgent):
    """Uses RAG retrieval to surface structural patterns and blueprint alignment signals."""

    name = "RAGAIAgent"

    _QUERIES = [
        "blueprint architecture required components",
        "expected project structure layout",
        "missing required services or modules",
    ]

    def analyze(self, context: AuditContext) -> AgentResult:
        findings: list[FindingModel] = []
        all_chunks = []

        for query in self._QUERIES:
            chunks = context.retrieve(query, 3)
            all_chunks.extend(chunks)

        if not all_chunks:
            findings.append(self._make_finding(
                category="rag",
                severity="info",
                title="No RAG context retrieved",
                description="No relevant content was retrieved from the indexed repository documents.",
                recommendation="Ensure files are indexed and the repository contains readable text content.",
            ))
        else:
            unique_sources = {c.source_path for c in all_chunks}
            findings.append(self._make_finding(
                category="rag",
                severity="info",
                title="RAG context retrieved successfully",
                description=(
                    f"Retrieved {len(all_chunks)} chunk(s) from {len(unique_sources)} source(s). "
                    "Use these results to compare against blueprint expectations."
                ),
                recommendation="Review retrieved context against documented blueprint requirements.",
                evidence=", ".join(list(unique_sources)[:5]),
            ))

        return AgentResult(
            agent_name=self.name,
            findings=findings,
            context_chunks_used=len(all_chunks),
        )
