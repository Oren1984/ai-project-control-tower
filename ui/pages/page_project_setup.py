from __future__ import annotations

import streamlit as st

from ui.services import api_client


def render() -> None:
    st.title("Project Setup")
    st.markdown("Register a target project for auditing.")

    with st.form("create_project"):
        name = st.text_input("Project Name", placeholder="my-ai-project")
        repo_path = st.text_input("Local Repository Path", placeholder="/home/user/repos/my-project")
        repo_url = st.text_input("Repository URL (optional)", placeholder="https://github.com/...")
        description = st.text_area("Description (optional)", height=80)
        submitted = st.form_submit_button("Create Project")

    if submitted:
        if not name.strip():
            st.error("Project name is required.")
        else:
            try:
                project = api_client.create_project(
                    name=name.strip(),
                    repo_path=repo_path.strip() or "",
                    description=description.strip(),
                )
                st.success(f"Project created: **{project['name']}** (ID: {project['id']})")
                st.session_state["project_id"] = project["id"]
                st.session_state["project_name"] = project["name"]
                st.session_state["repo_path"] = project.get("repo_path", "")
            except Exception as exc:
                st.error(f"Failed to create project: {exc}")

    st.markdown("---")
    st.subheader("Existing Projects")

    try:
        projects = api_client.list_projects()
    except Exception as exc:
        st.warning(f"Could not load projects: {exc}")
        return

    if not projects:
        st.info("No projects yet. Create one above.")
        return

    for p in projects:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{p['name']}** (ID: {p['id']}) — `{p.get('repo_path') or 'no path'}`")
        with col2:
            if st.button("Select", key=f"sel_{p['id']}"):
                st.session_state["project_id"] = p["id"]
                st.session_state["project_name"] = p["name"]
                st.session_state["repo_path"] = p.get("repo_path", "")
                st.success(f"Selected project: **{p['name']}**")
