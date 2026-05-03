from __future__ import annotations

import streamlit as st

from ui.services import api_client


def render() -> None:
    st.title("Final Report")

    audit_id = st.session_state.get("audit_id")
    if not audit_id:
        st.warning("No audit run selected. Run an audit first via **Repository Scan**.")
        return

    st.markdown(f"Audit: **#{audit_id}**")

    # Check audit status before attempting report generation.
    try:
        audit_info = api_client.get_audit(audit_id)
        audit_status = audit_info.get("status", "")
    except Exception as exc:
        st.error(f"Could not load audit details: {exc}")
        return

    if audit_status != "completed":
        icon = "⏳" if audit_status == "running" else "❌"
        st.error(
            f"{icon} **Cannot generate report** — audit #{audit_id} has status "
            f"**{audit_status}**, not *completed*.\n\n"
            + (
                "The audit is still in progress. Please wait and refresh."
                if audit_status == "running"
                else
                "This audit did not complete successfully (likely an invalid repository path or "
                "path outside `ALLOWED_SCAN_PATHS`).  \n"
                "Fix the path, run a new audit, and generate the report from that one."
            )
        )
        return

    fmt_options = {"Markdown": "markdown", "HTML": "html", "JSON": "json"}
    selected_fmt_label = st.selectbox("Report Format", list(fmt_options.keys()), index=0)
    selected_fmt = fmt_options[selected_fmt_label]

    if st.button("Generate / Load Report", type="primary"):
        with st.spinner("Generating report..."):
            try:
                report_data = api_client.get_report(audit_id, fmt=selected_fmt)
                st.session_state[f"report_{selected_fmt}"] = report_data.get("content", "")
                st.success("Report ready.")
            except Exception as exc:
                st.error(f"Failed to generate report: {exc}")

    content_key = f"report_{selected_fmt}"
    content = st.session_state.get(content_key, "")

    if content:
        st.markdown("---")

        if selected_fmt == "markdown":
            st.download_button(
                "Download Markdown",
                data=content,
                file_name=f"audit_{audit_id}_report.md",
                mime="text/markdown",
            )
            st.markdown(content, unsafe_allow_html=False)

        elif selected_fmt == "html":
            st.download_button(
                "Download HTML",
                data=content,
                file_name=f"audit_{audit_id}_report.html",
                mime="text/html",
            )
            if hasattr(st, "html"):
                st.html(content)
            else:
                st.components.v1.html(content, height=800, scrolling=True)

        elif selected_fmt == "json":
            st.download_button(
                "Download JSON",
                data=content,
                file_name=f"audit_{audit_id}_report.json",
                mime="application/json",
            )
            st.code(content, language="json")
    else:
        st.info("Click **Generate / Load Report** to create the report.")
