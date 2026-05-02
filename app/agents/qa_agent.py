from __future__ import annotations

from app.agents.base_agent import AuditContext, BaseAgent
from app.audit.models import AgentResult, FindingModel
from app.schemas.scan_schemas import FileCategory


class QAAgent(BaseAgent):
    name = "QAAgent"

    def analyze(self, context: AuditContext) -> AgentResult:
        findings: list[FindingModel] = []
        files = context.scan_result.files

        test_files = [f for f in files if f.category == FileCategory.TEST]
        source_files = [f for f in files if f.category == FileCategory.SOURCE_CODE]

        if not test_files and source_files:
            findings.append(self._make_finding(
                category="testing",
                severity="high",
                title="No test files detected",
                description="No test files were found in the repository.",
                recommendation="Add unit and integration tests to validate functionality and prevent regressions.",
                evidence=f"Source files: {len(source_files)}, Test files: 0",
            ))
        elif test_files and source_files:
            test_ratio = len(test_files) / len(source_files)
            if test_ratio < 0.2:
                findings.append(self._make_finding(
                    category="testing",
                    severity="medium",
                    title="Low test-to-source ratio",
                    description=f"{len(test_files)} test file(s) for {len(source_files)} source file(s).",
                    recommendation="Increase test coverage by adding tests for uncovered modules.",
                    evidence=f"Ratio: {test_ratio:.1%} (recommended: >= 20%)",
                ))

        has_ci = any(f.category == FileCategory.CI_CD for f in files)
        if not has_ci and source_files:
            findings.append(self._make_finding(
                category="quality",
                severity="medium",
                title="No CI/CD pipeline detected",
                description="No CI/CD configuration files were found.",
                recommendation="Add a CI/CD pipeline to automate testing on every commit.",
                evidence="Missing: .github/workflows, .gitlab-ci.yml, Jenkinsfile",
            ))

        context_chunks = context.retrieve("test coverage pytest unit integration assertions", 3)
        return AgentResult(
            agent_name=self.name,
            findings=findings,
            context_chunks_used=len(context_chunks),
        )
