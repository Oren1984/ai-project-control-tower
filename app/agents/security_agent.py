from __future__ import annotations

from app.agents.base_agent import AuditContext, BaseAgent
from app.audit.models import AgentResult, FindingModel
from app.schemas.scan_schemas import FileCategory


class SecurityAgent(BaseAgent):
    name = "SecurityAgent"

    def analyze(self, context: AuditContext) -> AgentResult:
        findings: list[FindingModel] = []
        files = context.scan_result.files
        categories = {f.category for f in files}

        if FileCategory.GITIGNORE not in categories:
            findings.append(self._make_finding(
                category="security",
                severity="high",
                title="Missing .gitignore",
                description="No .gitignore file was found in the repository.",
                recommendation="Add a .gitignore to prevent committing secrets, .env files, and build artifacts.",
                evidence="No .gitignore detected in scan results",
            ))

        if FileCategory.ENV_EXAMPLE not in categories:
            findings.append(self._make_finding(
                category="security",
                severity="medium",
                title="Missing .env.example",
                description="No .env.example or environment variable template was found.",
                recommendation="Add a .env.example documenting required environment variables without real values.",
                evidence="No .env.example detected in scan results",
            ))

        hidden_files = [
            f for f in files
            if f.is_hidden and f.category not in {
                FileCategory.GITIGNORE, FileCategory.ENV_EXAMPLE, FileCategory.HIDDEN_CONFIG
            }
        ]
        if hidden_files:
            findings.append(self._make_finding(
                category="security",
                severity="low",
                title="Hidden files present in repository",
                description=f"{len(hidden_files)} hidden file(s) found that may contain sensitive data.",
                recommendation="Review hidden files to confirm no sensitive data is tracked in version control.",
                evidence=", ".join(f.relative_path for f in hidden_files[:5]),
            ))

        context_chunks = context.retrieve("password secret api_key credentials token", 3)
        for chunk in context_chunks:
            text_lower = chunk.text.lower()
            if any(kw in text_lower for kw in ["password =", "secret =", "api_key =", "token ="]):
                findings.append(self._make_finding(
                    category="security",
                    severity="critical",
                    title="Potential hardcoded credentials",
                    description="A file contains patterns that suggest hardcoded secrets or credentials.",
                    recommendation="Move secrets to environment variables and ensure they are not committed to version control.",
                    evidence=f"Detected in: {chunk.source_path}",
                    file_path=chunk.source_path,
                ))
                break

        return AgentResult(
            agent_name=self.name,
            findings=findings,
            context_chunks_used=len(context_chunks),
        )
