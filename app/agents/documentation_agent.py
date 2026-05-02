from __future__ import annotations

from app.agents.base_agent import AuditContext, BaseAgent
from app.audit.models import AgentResult, FindingModel
from app.schemas.scan_schemas import FileCategory


class DocumentationAgent(BaseAgent):
    name = "DocumentationAgent"

    def analyze(self, context: AuditContext) -> AgentResult:
        findings: list[FindingModel] = []
        files = context.scan_result.files
        categories = {f.category for f in files}

        if FileCategory.README not in categories:
            findings.append(self._make_finding(
                category="documentation",
                severity="high",
                title="Missing README",
                description="No README file was found in the repository.",
                recommendation="Add a README.md describing the project purpose, setup instructions, and usage examples.",
                evidence="No README detected in scan results",
            ))

        doc_files = [f for f in files if f.category == FileCategory.DOCS]
        source_files = [f for f in files if f.category == FileCategory.SOURCE_CODE]
        if not doc_files and source_files:
            findings.append(self._make_finding(
                category="documentation",
                severity="low",
                title="No dedicated documentation directory",
                description="No docs/ or documentation directory was found.",
                recommendation="Consider adding a docs/ directory for architecture diagrams, API documentation, and contribution guides.",
            ))

        context_chunks = context.retrieve("README documentation setup usage API guide", 3)
        return AgentResult(
            agent_name=self.name,
            findings=findings,
            context_chunks_used=len(context_chunks),
        )
