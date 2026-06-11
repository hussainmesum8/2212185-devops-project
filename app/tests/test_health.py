def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_contains_status_ok(client):
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"


def test_health_contains_student_reg(client):
    response = client.get("/health")
    data = response.json()
    assert data["student"] == "BSCS-2022-001"
