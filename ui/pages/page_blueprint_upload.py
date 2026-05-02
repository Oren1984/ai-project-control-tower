from __future__ import annotations

import streamlit as st

from ui.services import api_client


def render() -> None:
    st.title("Blueprint Upload / Select")

    project_id = st.session_state.get("project_id")
    if not project_id:
        st.warning("No project selected. Go to **Project Setup** first.")
        return

    project_name = st.session_state.get("project_name", f"ID {project_id}")
    st.markdown(f"Project: **{project_name}**")

    with st.form("register_blueprint"):
        bp_name = st.text_input("Blueprint Name", placeholder="v1.0 Architecture Blueprint")
        file_path = st.text_input(
            "Blueprint File Path (on server)",
            placeholder="/home/user/repos/my-project/BLUEPRINT.md",
        )
        submitted = st.form_submit_button("Register Blueprint")

    if submitted:
        if not bp_name.strip():
            st.error("Blueprint name is required.")
        else:
            try:
                bp = api_client.create_blueprint(
                    project_id=project_id,
                    name=bp_name.strip(),
                    file_path=file_path.strip(),
                )
                st.success(f"Blueprint registered: **{bp['name']}** (ID: {bp['id']})")
                st.session_state["blueprint_id"] = bp["id"]
                st.session_state["blueprint_name"] = bp["name"]
            except Exception as exc:
                st.error(f"Failed to register blueprint: {exc}")

    st.markdown("---")
    st.subheader("Available Blueprints")

    try:
        blueprints = api_client.list_blueprints(project_id=project_id)
    except Exception as exc:
        st.warning(f"Could not load blueprints: {exc}")
        return

    if not blueprints:
        st.info("No blueprints registered for this project.")
        return

    for bp in blueprints:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{bp['name']}** (ID: {bp['id']}) — `{bp.get('file_path') or 'no path'}`")
        with col2:
            if st.button("Use", key=f"bp_{bp['id']}"):
                st.session_state["blueprint_id"] = bp["id"]
                st.session_state["blueprint_name"] = bp["name"]
                st.success(f"Blueprint selected: **{bp['name']}**")
