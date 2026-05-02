from __future__ import annotations

from app.agents.base_agent import AuditContext, BaseAgent
from app.audit.models import AgentResult, FindingModel
from app.schemas.scan_schemas import FileCategory


class ArchitectureAgent(BaseAgent):
    name = "ArchitectureAgent"

    def analyze(self, context: AuditContext) -> AgentResult:
        findings: list[FindingModel] = []
        files = context.scan_result.files

        source_files = [f for f in files if f.category == FileCategory.SOURCE_CODE]
        if not source_files:
            findings.append(self._make_finding(
                category="architecture",
                severity="high",
                title="No source code files detected",
                description="The repository contains no recognizable source code files.",
                recommendation="Ensure source files are present and properly organized in the repository.",
                evidence=f"Total files scanned: {len(files)}",
            ))

        has_config = any(f.category in {FileCategory.CONFIG, FileCategory.ENV_EXAMPLE} for f in files)
        if not has_config and source_files:
            findings.append(self._make_finding(
                category="architecture",
                severity="medium",
                title="No configuration management detected",
                description="No dedicated configuration files were found. Configuration may be hardcoded.",
                recommendation="Externalize configuration to config files or environment variables following the 12-factor app methodology.",
            ))

        has_package = any(f.category in {FileCategory.PACKAGE, FileCategory.REQUIREMENTS} for f in files)
        if not has_package and source_files:
            findings.append(self._make_finding(
                category="architecture",
                severity="medium",
                title="No dependency manifest found",
                description="No requirements.txt, pyproject.toml, package.json, or similar file was found.",
                recommendation="Add a dependency manifest so the project can be installed reproducibly.",
                evidence="Missing: requirements.txt, pyproject.toml, package.json",
            ))

        context_chunks = context.retrieve("architecture layers separation of concerns module structure", 3)
        return AgentResult(
            agent_name=self.name,
            findings=findings,
            context_chunks_used=len(context_chunks),
        )
