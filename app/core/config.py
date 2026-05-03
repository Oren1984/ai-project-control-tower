import json
from typing import Any

from pydantic import field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

_UNHANDLED = object()  # sentinel: caller must invoke the original prepare_field_value


def _parse_str_list(v: object) -> list[str]:
    """Parse a string into list[str] — supports JSON array or comma-separated."""
    if v is None or (isinstance(v, str) and not v.strip()):
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    if isinstance(v, str):
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
        except (json.JSONDecodeError, ValueError):
            pass
        return [p.strip() for p in v.split(",") if p.strip()]
    return []


def _intercept_complex_str(source: Any, field: Any, value: Any, value_is_complex: bool) -> Any:
    """Intercept complex-field env values to prevent pydantic_settings SettingsError.

    pydantic_settings 2.x raises SettingsError when json.loads() fails on list-typed
    fields (e.g. ALLOWED_SCAN_PATHS=, or ALLOWED_SCAN_PATHS=/app,/workspace).
    This function intercepts before that attempt.

    Returns _UNHANDLED sentinel if the caller should fall through to the original logic.
    """
    is_complex = value_is_complex
    if not is_complex:
        try:
            is_complex, _ = source._field_is_complex(field)
        except Exception:
            pass

    if is_complex and isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None  # empty string → use field default
        try:
            return json.loads(stripped)  # valid JSON → pass parsed value
        except (json.JSONDecodeError, ValueError):
            return stripped  # non-JSON (e.g. comma-separated) → field_validator handles it

    return _UNHANDLED


def _patch_source(source: Any) -> None:
    """Monkey-patch a settings source instance to use _intercept_complex_str.

    We patch the *existing* source instance (rather than recreating it with a subclass)
    so we don't have to replicate all of the source's constructor parameters.
    """
    original_pfv = source.prepare_field_value

    def _safe_pfv(field_name: str, field: Any, value: Any, value_is_complex: bool) -> Any:
        result = _intercept_complex_str(source, field, value, value_is_complex)
        if result is not _UNHANDLED:
            return result
        return original_pfv(field_name, field, value, value_is_complex)

    source.prepare_field_value = _safe_pfv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # pydantic_settings 2.10+ defaults to 'forbid'; ignore .env extras
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

    @field_validator("allowed_scan_paths", "cors_allowed_origins", mode="before")
    @classmethod
    def _parse_list_field(cls, v: object) -> list[str]:
        return _parse_str_list(v)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        **kwargs: Any,  # accepts secrets_settings or file_secret_settings across versions
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Patch existing source instances in-place — preserves all their constructor config.
        _patch_source(env_settings)
        _patch_source(dotenv_settings)
        return (init_settings, env_settings, dotenv_settings, *kwargs.values())


settings = Settings()
