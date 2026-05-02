from __future__ import annotations

import os
from typing import Optional

import requests

_API_BASE = os.getenv("API_BASE_URL", "http://localhost:8013/api/v1")

# Module-level demo data import (lazy — only loaded when demo mode is active).
try:
    from ui import demo_data as _DEMO
except (ImportError, ModuleNotFoundError):
    _DEMO = None  # type: ignore[assignment]


def _is_demo() -> bool:
    """Return True when demo mode is active (UI toggle or DEMO_MODE env var)."""
    try:
        import streamlit as st
        return bool(st.session_state.get("demo_mode", False))
    except Exception:
        pass
    return os.getenv("DEMO_MODE", "false").lower() == "true"


def _get(path: str, params: Optional[dict] = None) -> dict:
    r = requests.get(f"{_API_BASE}{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _post(path: str, body: dict) -> dict:
    r = requests.post(f"{_API_BASE}{path}", json=body, timeout=120)
    r.raise_for_status()
    return r.json()


# ─── Public API ────────────────────────────────────────────────────────────────

def health() -> dict:
    if _is_demo():
        return {"status": "ok", "service": "ai-project-control-tower", "mode": "demo"}
    return _get("/health")


def create_project(name: str, repo_path: str = "", description: str = "") -> dict:
    if _is_demo():
        return {"id": 1, "name": name, "repo_path": repo_path, "description": description}
    return _post("/projects", {"name": name, "repo_path": repo_path, "description": description})


def list_projects() -> list[dict]:
    if _is_demo() and _DEMO:
        return _DEMO.DEMO_PROJECTS
    return _get("/projects").get("projects", [])


def get_project(project_id: int) -> dict:
    if _is_demo() and _DEMO:
        return _DEMO.DEMO_PROJECTS[0]
    return _get(f"/projects/{project_id}")


def create_blueprint(project_id: int, name: str, file_path: str = "") -> dict:
    if _is_demo():
        return {"id": 1, "project_id": project_id, "name": name, "file_path": file_path}
    return _post("/blueprints", {"project_id": project_id, "name": name, "file_path": file_path})


def list_blueprints(project_id: Optional[int] = None) -> list[dict]:
    if _is_demo() and _DEMO:
        return _DEMO.DEMO_BLUEPRINTS
    params = {"project_id": project_id} if project_id else {}
    return _get("/blueprints", params=params).get("blueprints", [])


def run_audit(
    project_id: int,
    repo_path: str,
    mode: str = "hybrid",
    blueprint_id: Optional[int] = None,
) -> dict:
    if _is_demo() and _DEMO:
        return _DEMO.DEMO_AUDIT_RESULT
    body: dict = {"project_id": project_id, "repo_path": repo_path, "mode": mode}
    if blueprint_id is not None:
        body["blueprint_id"] = blueprint_id
    return _post("/audits/run", body)


def get_audit(audit_id: int) -> dict:
    if _is_demo() and _DEMO:
        return _DEMO.DEMO_AUDIT_RESULT
    return _get(f"/audits/{audit_id}")


def get_findings(audit_id: int) -> dict:
    if _is_demo() and _DEMO:
        return {
            "audit_run_id": audit_id,
            "total_findings": len(_DEMO.DEMO_FINDINGS),
            "findings": _DEMO.DEMO_FINDINGS,
        }
    return _get(f"/audits/{audit_id}/findings")


def get_report(audit_id: int, fmt: str = "markdown") -> dict:
    if _is_demo() and _DEMO:
        if fmt == "json":
            return {"content": _DEMO.DEMO_REPORT_JSON}
        if fmt == "html":
            md = _DEMO.DEMO_REPORT_MARKDOWN
            body = md.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html = (
                "<!DOCTYPE html><html><head><meta charset='utf-8'>"
                "<style>body{font-family:sans-serif;max-width:860px;margin:40px auto;"
                "padding:0 24px;line-height:1.6}pre{background:#f6f8fa;padding:12px;"
                "border-radius:4px;overflow-x:auto}</style></head>"
                f"<body><pre>{body}</pre></body></html>"
            )
            return {"content": html}
        return {"content": _DEMO.DEMO_REPORT_MARKDOWN}
    return _get(f"/audits/{audit_id}/report", params={"format": fmt})


def get_audit_history(limit: int = 20) -> list[dict]:
    if _is_demo() and _DEMO:
        return _DEMO.DEMO_AUDIT_HISTORY[:limit]
    return _get("/audits/history", params={"limit": limit}).get("audits", [])
