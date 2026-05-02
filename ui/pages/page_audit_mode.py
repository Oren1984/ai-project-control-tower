from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Audit Mode")

    project_id = st.session_state.get("project_id")
    if not project_id:
        st.warning("No project selected. Go to **Project Setup** first.")
        return

    project_name = st.session_state.get("project_name", f"ID {project_id}")
    st.markdown(f"Project: **{project_name}**")

    st.subheader("Select Audit Mode")
    mode_options = {
        "Hybrid (RAG + Agents)": "hybrid",
        "Agent Only": "agent_only",
        "RAG Only": "rag_only",
    }
    selected_label = st.radio(
        "Audit Mode",
        list(mode_options.keys()),
        index=0,
        help="Hybrid combines retrieval with agent reasoning for the most complete audit.",
    )
    selected_mode = mode_options[selected_label]

    st.markdown("---")
    st.subheader("Retrieval Mode")
    retrieval_options = ["hybrid", "tfidf", "pgvector"]
    retrieval_mode = st.selectbox(
        "Retrieval Mode",
        retrieval_options,
        index=0,
        help="Hybrid uses both TF-IDF and pgvector. TF-IDF works without embeddings.",
    )

    st.markdown("---")
    st.subheader("Severity Threshold")
    severity_threshold = st.selectbox(
        "Minimum severity to report",
        ["info", "low", "medium", "high", "critical"],
        index=0,
    )

    if st.button("Save Settings", type="primary"):
        st.session_state["audit_mode"] = selected_mode
        st.session_state["retrieval_mode"] = retrieval_mode
        st.session_state["severity_threshold"] = severity_threshold
        st.success(
            f"Saved — Mode: **{selected_mode}** | Retrieval: **{retrieval_mode}** | "
            f"Min Severity: **{severity_threshold}**"
        )

    st.markdown("---")
    st.info(
        "**Mode descriptions:**\n\n"
        "- **Hybrid**: RAG retrieval + agent reasoning. Most comprehensive.\n"
        "- **Agent Only**: Agents reason from scanned files without RAG context.\n"
        "- **RAG Only**: Retrieval-based similarity search, no agent reasoning."
    )
