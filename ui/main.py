from __future__ import annotations

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

from ui.pages import (
    page_audit_history,
    page_audit_mode,
    page_blueprint_upload,
    page_final_report,
    page_findings_dashboard,
    page_project_setup,
    page_repository_scan,
    page_scores,
    page_settings,
)

st.set_page_config(
    page_title="AI Project Control Tower",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide Streamlit's automatic multipage sidebar nav — we use our own radio nav.
st.markdown(
    "<style>[data-testid='stSidebarNav']{display:none!important}</style>",
    unsafe_allow_html=True,
)

PAGES: dict = {
    "Project Setup": page_project_setup,
    "Blueprint Upload": page_blueprint_upload,
    "Audit Mode": page_audit_mode,
    "Repository Scan": page_repository_scan,
    "Findings Dashboard": page_findings_dashboard,
    "Scores": page_scores,
    "Final Report": page_final_report,
    "Audit History": page_audit_history,
    "Settings / Providers": page_settings,
}

# ─── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("AI Project Control Tower")
st.sidebar.caption("Audit · Analyze · Recommend")
st.sidebar.markdown("---")

selected = st.sidebar.radio("Navigation", list(PAGES.keys()), label_visibility="collapsed")

# ─── Demo Mode ────────────────────────────────────────────────────────────────
st.sidebar.markdown("---")

# Honour DEMO_MODE env var on first load
if "demo_mode" not in st.session_state:
    st.session_state["demo_mode"] = os.getenv("DEMO_MODE", "false").lower() == "true"

_was_demo = st.session_state["demo_mode"]

demo_mode = st.sidebar.checkbox(
    "🎭 Demo Mode",
    value=_was_demo,
    help=(
        "Load realistic sample data without a live backend or real repository. "
        "All data is fabricated for portfolio demonstration."
    ),
)

if demo_mode and not _was_demo:
    # Turning ON — pre-populate session with demo context
    st.session_state.update(
        {
            "demo_mode": True,
            "project_id": 1,
            "project_name": "sample-mlops-pipeline",
            "repo_path": "/home/demo/repos/sample-mlops-pipeline",
            "blueprint_id": 1,
            "blueprint_name": "MLOps Platform Architecture v1",
            "audit_id": 1,
            "audit_mode": "hybrid",
        }
    )
    st.session_state.pop("audit_result", None)
    for fmt in ("markdown", "html", "json"):
        st.session_state.pop(f"report_{fmt}", None)
    st.rerun()
elif not demo_mode and _was_demo:
    # Turning OFF — clear all demo state
    for key in (
        "demo_mode", "project_id", "project_name", "repo_path",
        "blueprint_id", "blueprint_name", "audit_id", "audit_mode",
        "audit_result", "report_markdown", "report_html", "report_json",
    ):
        st.session_state.pop(key, None)
    st.rerun()
else:
    st.session_state["demo_mode"] = demo_mode

if st.session_state.get("demo_mode"):
    st.sidebar.info("🎭 Demo Mode — sample data only")

# ─── Context indicators ───────────────────────────────────────────────────────
st.sidebar.markdown("---")
if "project_id" in st.session_state:
    st.sidebar.caption(f"Project: **{st.session_state.get('project_name', '')}**")
if "audit_id" in st.session_state:
    st.sidebar.caption(f"Audit: **#{st.session_state['audit_id']}**")

# ─── Render ───────────────────────────────────────────────────────────────────
PAGES[selected].render()
