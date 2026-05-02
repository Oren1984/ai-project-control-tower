"""
Tests for the Prometheus /metrics endpoint and request-ID middleware.
"""


def test_metrics_endpoint_returns_200(client):
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_content_type_is_prometheus(client):
    response = client.get("/metrics")
    assert "text/plain" in response.headers["content-type"]


def test_metrics_contains_api_duration_metric(client):
    # Hit the health endpoint first so the histogram has at least one observation.
    client.get("/api/v1/health")
    response = client.get("/metrics")
    assert "api_request_duration_seconds" in response.text


def test_request_id_header_present(client):
    response = client.get("/api/v1/health")
    assert "x-request-id" in response.headers


def test_request_id_is_uuid_format(client):
    import uuid
    response = client.get("/api/v1/health")
    raw = response.headers.get("x-request-id", "")
    try:
        uuid.UUID(raw)
    except ValueError:
        raise AssertionError(f"X-Request-ID is not a valid UUID: {raw!r}")


def test_different_requests_get_different_ids(client):
    r1 = client.get("/api/v1/health")
    r2 = client.get("/api/v1/health")
    assert r1.headers["x-request-id"] != r2.headers["x-request-id"]
