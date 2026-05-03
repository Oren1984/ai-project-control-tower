from __future__ import annotations

import streamlit as st

from ui.services import api_client


def render() -> None:
    st.title("Repository Scan")

    project_id = st.session_state.get("project_id")
    if not project_id:
        st.warning("No project selected. Go to **Project Setup** first.")
        return

    project_name = st.session_state.get("project_name", f"ID {project_id}")
    repo_path = st.session_state.get("repo_path", "")
    audit_mode = st.session_state.get("audit_mode", "hybrid")
    blueprint_id = st.session_state.get("blueprint_id")
    blueprint_name = st.session_state.get("blueprint_name", "None")

    st.markdown(f"Project: **{project_name}**")
    st.markdown(f"Audit Mode: **{audit_mode}**")
    st.markdown(f"Blueprint: **{blueprint_name}**")

    st.subheader("Repository Path")

    with st.info("", icon="ℹ️"):
        st.markdown(
            "**Docker path guide** — the API runs inside a container, so you must enter "
            "the **container path**, not the Windows host path.\n\n"
            "Your host directory `C:/Users/ORENS` is mounted as `/workspace` inside the container.\n\n"
            "| Windows host path | Enter this in the field below |\n"
            "|---|---|\n"
            "| `C:\\Users\\ORENS\\investment-mcp-multi-agent-system` | `/workspace/investment-mcp-multi-agent-system` |\n"
            "| `C:\\Users\\ORENS\\rag-retrieval-evaluation-lab` | `/workspace/rag-retrieval-evaluation-lab` |\n"
            "| *(this project itself)* | `/app` |"
        )

    repo_path_input = st.text_input(
        "Container path to target repository",
        value=repo_path,
        placeholder="/workspace/my-repo",
    )
    if repo_path_input:
        st.session_state["repo_path"] = repo_path_input

    st.markdown("---")

    if st.button("Run Audit", type="primary", disabled=not repo_path_input):
        with st.spinner("Running audit — this may take a few minutes..."):
            try:
                result = api_client.run_audit(
                    project_id=project_id,
                    repo_path=repo_path_input,
                    mode=audit_mode,
                    blueprint_id=blueprint_id,
                )
                st.session_state["audit_id"] = result["audit_run_id"]
                st.session_state["audit_result"] = result

                scores = result.get("scores", {})
                status = result.get("status", "")

                col1, col2, col3 = st.columns(3)
                col3.metric("Status", status)

                if status == "completed":
                    st.success(
                        f"Audit complete — Overall score: **{scores.get('overall', 'N/A')}/100**"
                    )
                    col1.metric("Total Findings", result.get("total_findings", 0))
                    col2.metric("Overall Score", f"{scores.get('overall', 0)}/100")
                    st.markdown("---")
                    st.success(
                        f"Audit **#{result['audit_run_id']}** saved — "
                        "navigate to **Findings Dashboard**, **Scores**, or **Final Report**."
                    )
                else:
                    st.error(
                        f"Audit did not complete (status: **{status}**).  \n"
                        "Make sure the path you entered exists inside the container and is "
                        "listed in `ALLOWED_SCAN_PATHS`. See the guide above."
                    )
                    col1.metric("Total Findings", "N/A")
                    col2.metric("Overall Score", "N/A")

            except Exception as exc:
                st.error(f"Audit request failed: {exc}")
    else:
        if not repo_path_input:
            st.info("Enter a container repository path above and click **Run Audit**.")

    if st.session_state.get("audit_id") and st.session_state.get("audit_result", {}).get("status") == "completed":
        if not st.session_state.get("_scan_just_ran"):
            st.markdown("---")
            st.success(
                f"Last audit: **#{st.session_state['audit_id']}** — "
                "navigate to Findings Dashboard or Final Report."
            )
