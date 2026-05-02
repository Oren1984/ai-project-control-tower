from __future__ import annotations

from app.agents.base_agent import AuditContext, BaseAgent
from app.audit.models import AgentResult, FindingModel
from app.schemas.scan_schemas import FileCategory


class DevOpsMLOpsAgent(BaseAgent):
    name = "DevOpsMLOpsAgent"

    def analyze(self, context: AuditContext) -> AgentResult:
        findings: list[FindingModel] = []
        files = context.scan_result.files
        categories = {f.category for f in files}

        has_docker = FileCategory.DOCKER in categories or FileCategory.COMPOSE in categories
        if not has_docker:
            findings.append(self._make_finding(
                category="devops",
                severity="medium",
                title="No Docker configuration found",
                description="Neither Dockerfile nor docker-compose.yml was found in the repository.",
                recommendation="Add Docker configuration to enable reproducible builds and containerised deployments.",
                evidence="Missing: Dockerfile, docker-compose.yml",
            ))

        if FileCategory.CI_CD not in categories:
            findings.append(self._make_finding(
                category="devops",
                severity="medium",
                title="No CI/CD configuration detected",
                description="No CI/CD pipeline configuration was found.",
                recommendation="Add a CI/CD pipeline to automate builds, tests, and deployments.",
                evidence="Missing: .github/workflows/, .gitlab-ci.yml, Jenkinsfile",
            ))

        k8s_files = [f for f in files if f.category == FileCategory.KUBERNETES]
        terraform_files = [f for f in files if f.category == FileCategory.TERRAFORM]
        if not k8s_files and not terraform_files and has_docker:
            findings.append(self._make_finding(
                category="mlops",
                severity="low",
                title="No infrastructure-as-code found",
                description="No Kubernetes manifests or Terraform files were found.",
                recommendation="Consider adding infrastructure-as-code for reproducible production deployments.",
                evidence="Missing: k8s/*.yaml, terraform/*.tf",
            ))

        context_chunks = context.retrieve("docker kubernetes deployment pipeline infrastructure", 3)
        return AgentResult(
            agent_name=self.name,
            findings=findings,
            context_chunks_used=len(context_chunks),
        )
