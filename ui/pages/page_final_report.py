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
            # st.html() is the forward-compatible API (Streamlit >= 1.36).
            # st.components.v1.html() is deprecated and removed after 2026-06-01.
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
