from pathlib import Path

from app.schemas.scan_schemas import FileCategory

_FILENAME_MAP: dict[str, FileCategory] = {
    "dockerfile": FileCategory.DOCKER,
    "docker-compose.yml": FileCategory.COMPOSE,
    "docker-compose.yaml": FileCategory.COMPOSE,
    "docker-compose.override.yml": FileCategory.COMPOSE,
    "docker-compose.override.yaml": FileCategory.COMPOSE,
    ".gitignore": FileCategory.GITIGNORE,
    ".gitattributes": FileCategory.GITIGNORE,
    ".env.example": FileCategory.ENV_EXAMPLE,
    ".env.sample": FileCategory.ENV_EXAMPLE,
    ".env.template": FileCategory.ENV_EXAMPLE,
    "requirements.txt": FileCategory.REQUIREMENTS,
    "requirements-dev.txt": FileCategory.REQUIREMENTS,
    "requirements-test.txt": FileCategory.REQUIREMENTS,
    "pyproject.toml": FileCategory.PACKAGE,
    "setup.py": FileCategory.PACKAGE,
    "setup.cfg": FileCategory.PACKAGE,
    "package.json": FileCategory.PACKAGE,
    "package-lock.json": FileCategory.LOCK,
    "poetry.lock": FileCategory.LOCK,
    "pipfile.lock": FileCategory.LOCK,
    "yarn.lock": FileCategory.LOCK,
    "alembic.ini": FileCategory.CONFIG,
    ".pre-commit-config.yaml": FileCategory.CONFIG,
}

_EXTENSION_MAP: dict[str, FileCategory] = {
    ".py": FileCategory.SOURCE_CODE,
    ".js": FileCategory.SOURCE_CODE,
    ".ts": FileCategory.SOURCE_CODE,
    ".jsx": FileCategory.SOURCE_CODE,
    ".tsx": FileCategory.SOURCE_CODE,
    ".go": FileCategory.SOURCE_CODE,
    ".java": FileCategory.SOURCE_CODE,
    ".rs": FileCategory.SOURCE_CODE,
    ".rb": FileCategory.SOURCE_CODE,
    ".sh": FileCategory.SOURCE_CODE,
    ".bash": FileCategory.SOURCE_CODE,
    ".zsh": FileCategory.SOURCE_CODE,
    ".md": FileCategory.DOCS,
    ".rst": FileCategory.DOCS,
    ".txt": FileCategory.DOCS,
    ".yaml": FileCategory.CONFIG,
    ".yml": FileCategory.CONFIG,
    ".json": FileCategory.CONFIG,
    ".toml": FileCategory.CONFIG,
    ".ini": FileCategory.CONFIG,
    ".cfg": FileCategory.CONFIG,
    ".conf": FileCategory.CONFIG,
    ".tf": FileCategory.TERRAFORM,
    ".tfvars": FileCategory.TERRAFORM,
}


def classify_file(path: Path, repo_root: Path) -> FileCategory:
    name_lower = path.name.lower()

    if name_lower.startswith("readme"):
        return FileCategory.README

    if name_lower in _FILENAME_MAP:
        return _FILENAME_MAP[name_lower]

    try:
        rel_parts = path.relative_to(repo_root).parts
    except ValueError:
        rel_parts = path.parts

    # CI/CD by directory structure
    if ".github" in rel_parts or ".circleci" in rel_parts or ".gitlab-ci" in name_lower:
        return FileCategory.CI_CD

    # Kubernetes manifests
    if any(p in rel_parts for p in ("k8s", "kubernetes", "manifests")):
        return FileCategory.KUBERNETES

    # Test files by directory or naming convention
    if "tests" in rel_parts or "test" in rel_parts:
        return FileCategory.TEST
    if name_lower.startswith("test_") or name_lower.endswith("_test.py"):
        return FileCategory.TEST

    # Terraform
    if "terraform" in rel_parts:
        return FileCategory.TERRAFORM

    # Hidden config files
    if path.name.startswith(".") and path.suffix.lower() in (
        ".json", ".yaml", ".yml", ".ini", ".toml", ".cfg", ".conf"
    ):
        return FileCategory.HIDDEN_CONFIG

    return _EXTENSION_MAP.get(path.suffix.lower(), FileCategory.OTHER)
