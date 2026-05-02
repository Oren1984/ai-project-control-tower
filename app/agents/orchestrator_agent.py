from __future__ import annotations

from app.agents.architecture_agent import ArchitectureAgent
from app.agents.base_agent import AuditContext, BaseAgent
from app.agents.devops_mlops_agent import DevOpsMLOpsAgent
from app.agents.documentation_agent import DocumentationAgent
from app.agents.qa_agent import QAAgent
from app.agents.rag_ai_agent import RAGAIAgent
from app.agents.security_agent import SecurityAgent
from app.audit.models import AgentResult
from app.core.logging import get_logger

logger = get_logger(__name__)


class OrchestratorAgent:
    """Runs all specialist agents and collects their results."""

    def __init__(self) -> None:
        self._agents: list[BaseAgent] = [
            ArchitectureAgent(),
            SecurityAgent(),
            QAAgent(),
            DevOpsMLOpsAgent(),
            DocumentationAgent(),
            RAGAIAgent(),
        ]

    def run_all(self, context: AuditContext) -> list[AgentResult]:
        results: list[AgentResult] = []
        for agent in self._agents:
            try:
                result = agent.analyze(context)
                results.append(result)
                logger.info("agent_complete", agent=agent.name, findings=len(result.findings))
            except Exception as exc:
                logger.error("agent_failed", agent=agent.name, error=str(exc))
                results.append(AgentResult(agent_name=agent.name, findings=[]))
        return results
