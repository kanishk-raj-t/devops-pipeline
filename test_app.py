import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Todo API is running"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_create_and_fetch_todo(client):
    post_res = client.post("/todos", json={"task": "Verify CI unit test"})
    assert post_res.status_code == 201
    assert post_res.get_json()["task"] == "Verify CI unit test"

    get_res = client.get("/todos")
    assert get_res.status_code == 200
    tasks = [item["task"] for item in get_res.get_json()["todos"]]
    assert "Verify CI unit test" in tasks