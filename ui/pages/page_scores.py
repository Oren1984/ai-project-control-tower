from __future__ import annotations

import streamlit as st

from ui.services import api_client


def _score_color(score: float) -> str:
    if score >= 80:
        return "normal"
    if score >= 60:
        return "off"
    return "inverse"


def render() -> None:
    st.title("Scores")

    audit_id = st.session_state.get("audit_id")
    audit_result = st.session_state.get("audit_result")

    if not audit_id:
        st.warning("No audit run selected. Run an audit first via **Repository Scan**.")
        return

    if not audit_result:
        try:
            audit_result = api_client.get_audit(audit_id)
            st.session_state["audit_result"] = audit_result
        except Exception as exc:
            st.error(f"Could not load audit: {exc}")
            return

    scores = audit_result.get("scores", {})
    if not scores:
        st.info("Score data not available for this audit.")
        return

    st.markdown(f"Audit: **#{audit_id}** | Status: **{audit_result.get('status', '')}**")
    st.markdown("---")

    overall = scores.get("overall", 0)
    st.metric("Overall Score", f"{overall}/100")

    st.progress(int(overall))

    st.markdown("---")
    st.subheader("Dimension Scores")

    dimensions = [
        ("Architecture", "architecture"),
        ("QA / Testing", "qa"),
        ("Security", "security"),
        ("DevOps", "devops"),
        ("MLOps", "mlops"),
        ("Documentation", "documentation"),
        ("RAG / Agents", "rag_agent"),
        ("Observability", "observability"),
    ]

    col1, col2 = st.columns(2)
    for i, (label, key) in enumerate(dimensions):
        val = scores.get(key, 0)
        col = col1 if i % 2 == 0 else col2
        with col:
            st.metric(label, f"{val}/100")
            st.progress(int(val))
            st.markdown("")

    st.markdown("---")
    st.caption(
        "Scores are heuristic and penalty-based. "
        "They reflect patterns found during static analysis, not runtime behavior."
    )
