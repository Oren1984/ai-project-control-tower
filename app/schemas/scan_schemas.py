from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class FileType(str, Enum):
    TEXT = "text"
    BINARY = "binary"


class FileCategory(str, Enum):
    README = "readme"
    DOCS = "docs"
    SOURCE_CODE = "source_code"
    TEST = "test"
    DOCKER = "docker"
    COMPOSE = "compose"
    CI_CD = "ci_cd"
    ENV_EXAMPLE = "env_example"
    GITIGNORE = "gitignore"
    HIDDEN_CONFIG = "hidden_config"
    PACKAGE = "package"
    REQUIREMENTS = "requirements"
    LOCK = "lock"
    KUBERNETES = "kubernetes"
    TERRAFORM = "terraform"
    CONFIG = "config"
    OTHER = "other"


class SkipReason(str, Enum):
    BINARY = "binary"
    OVERSIZED = "oversized"
    ENCODING_ERROR = "encoding_error"
    GIT_INTERNAL = "git_internal"
    SYMLINK = "symlink"


class ScannedFile(BaseModel):
    path: str
    relative_path: str
    extension: str
    size_bytes: int
    modified_at: datetime
    file_type: FileType
    category: FileCategory
    sha256: str
    is_hidden: bool


class SkippedFile(BaseModel):
    path: str
    relative_path: str
    reason: SkipReason
    details: Optional[str] = None


class ScanResult(BaseModel):
    repo_path: str
    scanned_at: datetime
    total_files_found: int
    total_files_scanned: int
    total_files_skipped: int
    files: list[ScannedFile]
    skipped: list[SkippedFile]


class ScanRequest(BaseModel):
    repo_path: str
    max_file_size_bytes: int = 1_048_576
    include_hidden: bool = True
    skip_git_internals: bool = True
    follow_symlinks: bool = False
