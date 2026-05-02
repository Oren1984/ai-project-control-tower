from __future__ import annotations

import streamlit as st

from ui.services import api_client

_SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
_SEVERITY_COLORS = {
    "critical": "🔴",
    "high": "🟠",
    "medium": "🟡",
    "low": "🟢",
    "info": "⚪",
}


def render() -> None:
    st.title("Findings Dashboard")

    audit_id = st.session_state.get("audit_id")
    if not audit_id:
        st.warning("No audit run selected. Run an audit first via **Repository Scan**.")
        return

    st.markdown(f"Audit: **#{audit_id}**")

    try:
        data = api_client.get_findings(audit_id)
    except Exception as exc:
        st.error(f"Could not load findings: {exc}")
        return

    findings = data.get("findings", [])
    total = data.get("total_findings", 0)

    if not findings:
        st.info("No findings for this audit.")
        return

    severity_counts: dict[str, int] = {}
    for f in findings:
        sev = f.get("severity", "info")
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    cols = st.columns(5)
    for i, sev in enumerate(["critical", "high", "medium", "low", "info"]):
        cols[i].metric(
            f"{_SEVERITY_COLORS[sev]} {sev.title()}",
            severity_counts.get(sev, 0),
        )

    st.markdown("---")
    st.subheader(f"All Findings ({total})")

    filter_options = ["all", "critical", "high", "medium", "low", "info"]
    selected_filter = st.selectbox("Filter by severity", filter_options, index=0)

    agent_options = ["all"] + sorted({f.get("agent_name", "") for f in findings})
    selected_agent = st.selectbox("Filter by agent", agent_options, index=0)

    filtered = findings
    if selected_filter != "all":
        filtered = [f for f in filtered if f.get("severity") == selected_filter]
    if selected_agent != "all":
        filtered = [f for f in filtered if f.get("agent_name") == selected_agent]

    filtered.sort(key=lambda f: _SEVERITY_ORDER.get(f.get("severity", "info"), 9))

    for f in filtered:
        sev = f.get("severity", "info")
        icon = _SEVERITY_COLORS.get(sev, "⚪")
        with st.expander(f"{icon} [{sev.upper()}] {f.get('title', '')} — {f.get('agent_name', '')}"):
            st.markdown(f"**Category:** {f.get('category', '')}")
            st.markdown(f"**Description:** {f.get('description', '')}")
            if f.get("evidence"):
                st.markdown(f"**Evidence:** `{f['evidence']}`")
            st.markdown(f"**Recommendation:** {f.get('recommendation', '')}")
            if f.get("file_path"):
                loc = f"**File:** `{f['file_path']}`"
                if f.get("line_number"):
                    loc += f" line {f['line_number']}"
                st.markdown(loc)
