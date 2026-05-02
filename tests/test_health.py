def test_health_returns_200(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_body(client):
    response = client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ai-project-control-tower"


def test_ready_response_structure(client):
    # Status is 200 (DB up) or 503 (DB not reachable) — both are valid
    response = client.get("/api/v1/ready")
    assert response.status_code in (200, 503)
    data = response.json()
    assert "status" in data
    assert data["status"] in ("ready", "not_ready")
    assert "checks" in data
    assert "database" in data["checks"]
    assert "pgvector" in data["checks"]
