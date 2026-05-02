from __future__ import annotations

import os

import streamlit as st

from ui.services import api_client


def render() -> None:
    st.title("Settings / Providers")

    st.subheader("API Connection")
    current_base = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
    st.markdown(f"**API Base URL:** `{current_base}`")

    try:
        health = api_client.health()
        st.success(f"API connected — {health.get('status', 'ok')}")
    except Exception as exc:
        st.error(f"API not reachable: {exc}")

    st.markdown("---")
    st.subheader("LLM Provider")
    st.info(
        "LLM provider configuration is managed via environment variables in `.env`. "
        "The audit agents use pattern-based analysis by default (no API key required)."
    )

    provider = st.selectbox(
        "LLM Provider (informational — configure in .env)",
        ["Local / No LLM", "OpenAI", "Anthropic Claude", "Google Gemini"],
        index=0,
    )

    if provider != "Local / No LLM":
        st.warning(
            f"To use **{provider}**, set the corresponding API key in your `.env` file. "
            "Provider integration is available but must be configured server-side."
        )

    st.markdown("---")
    st.subheader("Retrieval Mode")
    st.info(
        "Retrieval mode is selected per audit run on the **Audit Mode** page. "
        "Options: TF-IDF (local, no API), pgvector (requires DB), Hybrid."
    )

    st.markdown("---")
    st.subheader("Security")
    st.markdown(
        "- Reports are sanitized before display and storage.\n"
        "- Secrets and API keys are masked using pattern-based redaction.\n"
        "- Auto-fix instructions are stripped from all reports.\n"
        "- The system never modifies the target repository.\n"
        "- Path validation prevents scanning outside allowed directories."
    )

    st.markdown("---")
    st.subheader("Export Format")
    st.info("Report format is selected per report on the **Final Report** page. Options: Markdown, HTML, JSON.")
