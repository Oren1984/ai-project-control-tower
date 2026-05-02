from __future__ import annotations

import streamlit as st

from ui.services import api_client


def render() -> None:
    st.title("Audit History")

    try:
        audits = api_client.get_audit_history(limit=50)
    except Exception as exc:
        st.error(f"Could not load audit history: {exc}")
        return

    if not audits:
        st.info("No audit runs found. Run an audit via **Repository Scan**.")
        return

    st.markdown(f"Showing **{len(audits)}** most recent audits.")
    st.markdown("---")

    for audit in audits:
        score = audit.get("overall_score")
        score_str = f"{score}/100" if score is not None else "N/A"
        status = audit.get("status", "")
        status_icon = {"completed": "✅", "failed": "❌", "running": "⏳"}.get(status, "❓")

        with st.expander(
            f"{status_icon} Audit #{audit['id']} | Score: {score_str} | "
            f"Mode: {audit.get('mode', '')} | {audit.get('created_at', '')[:10]}"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**ID:** {audit['id']}")
                st.markdown(f"**Project ID:** {audit.get('project_id', '')}")
                st.markdown(f"**Blueprint ID:** {audit.get('blueprint_id', 'None')}")
                st.markdown(f"**Mode:** {audit.get('mode', '')}")
            with col2:
                st.markdown(f"**Status:** {status}")
                st.markdown(f"**Overall Score:** {score_str}")
                st.markdown(f"**Started:** {(audit.get('started_at') or '')[:19]}")
                st.markdown(f"**Completed:** {(audit.get('completed_at') or '')[:19]}")

            if st.button("Load this audit", key=f"load_{audit['id']}"):
                st.session_state["audit_id"] = audit["id"]
                st.session_state.pop("audit_result", None)
                for fmt in ["markdown", "html", "json"]:
                    st.session_state.pop(f"report_{fmt}", None)
                st.success(f"Loaded audit #{audit['id']} — navigate to Findings Dashboard or Final Report.")
