from prometheus_client import Counter, Histogram

audit_runs_total = Counter(
    "audit_runs_total",
    "Total number of audit runs started",
    ["mode"],
)
audit_runs_failed_total = Counter(
    "audit_runs_failed_total",
    "Total number of audit runs that failed",
)
audit_duration_seconds = Histogram(
    "audit_duration_seconds",
    "Wall-clock duration of a completed audit run",
    buckets=[1, 5, 10, 30, 60, 120, 300, 600],
)

files_scanned_total = Counter(
    "files_scanned_total",
    "Total number of files scanned across all audit runs",
)

findings_total = Counter(
    "findings_total",
    "Total number of findings emitted",
    ["severity"],
)

rag_queries_total = Counter(
    "rag_queries_total",
    "Total number of RAG retrieval queries",
)
rag_retrieval_latency_seconds = Histogram(
    "rag_retrieval_latency_seconds",
    "RAG retrieval latency",
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

agent_reviews_total = Counter(
    "agent_reviews_total",
    "Total number of agent reviews executed",
    ["agent_name"],
)
agent_review_duration_seconds = Histogram(
    "agent_review_duration_seconds",
    "Duration of individual agent reviews",
    ["agent_name"],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)

report_generation_total = Counter(
    "report_generation_total",
    "Total number of reports generated",
    ["format"],
)

api_request_duration_seconds = Histogram(
    "api_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint", "status"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

db_query_errors_total = Counter(
    "db_query_errors_total",
    "Total number of database query errors",
)
