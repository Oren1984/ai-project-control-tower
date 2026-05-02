import json

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "AI Project Control Tower"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    database_url: str = (
        "postgresql://control_tower:control_tower_pass@localhost:5432/control_tower_db"
    )

    # Scanner security: only paths in this list may be scanned
    allowed_scan_paths: list[str] = []
    max_scan_file_size_bytes: int = 1_048_576  # 1 MB

    # CORS: origins allowed to call the API
    cors_allowed_origins: list[str] = [
        "http://localhost:8513",
        "http://localhost:3012",
        "http://ui:8501",
    ]

    @field_validator("allowed_scan_paths", mode="before")
    @classmethod
    def _parse_allowed_scan_paths(cls, v: object) -> list[str]:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            # Fall back to comma-separated string
            return [p.strip() for p in v.split(",") if p.strip()]
        return []

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v: object) -> list[str]:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            return [o.strip() for o in v.split(",") if o.strip()]
        return []


settings = Settings()
