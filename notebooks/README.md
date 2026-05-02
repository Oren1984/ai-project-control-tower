# Notebooks — AI Project Control Tower

## Why Notebooks Are Not the Primary Demo Format

AI Project Control Tower is a service-oriented application:

- **Backend**: FastAPI REST API on port 8000
- **Frontend**: Streamlit UI on port 8512
- **Database**: PostgreSQL + pgvector on port 5432

The natural demo format is the Streamlit UI, not a Jupyter notebook. The audit pipeline runs as a multi-service stack; there is no Python library to import and drive from a notebook without calling the REST API.

---

## What Is Here

### `01_project_control_tower_demo.ipynb`

A conceptual walkthrough notebook using static sample data. It does **not** call any live API endpoints and does **not** require a running Docker stack.

It illustrates:
- The structure of a Project, Blueprint, and AuditRun
- What a `FindingModel` looks like (with evidence, severity, dimension, recommendation)
- How the 9-dimension scoring model works
- What a generated report section looks like
- The overall audit workflow from a data-model perspective

This is useful for understanding the system design before working with the live application.

---

## Requirements

The conceptual notebook requires only Python's standard library and `pandas` (optional, for display formatting):

```bash
pip install jupyter pandas
```

No API keys. No running Docker stack. No paid services.

---

## Running the Notebook

```bash
# Install Jupyter if needed
pip install jupyter

# Launch
jupyter notebook notebooks/

# Or with JupyterLab
jupyter lab notebooks/
```

---

## Limitations

- Notebook output is **static sample data**, not real audit results
- Real audit results require a running backend (`docker compose up`)
- pgvector semantic search requires a configured embedding provider
- LLM agent output requires provider API keys in `.env`

For the full live experience, use the Streamlit UI at http://localhost:8512 after `docker compose up --build`.
