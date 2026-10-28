import os
os.environ["DATABASE_URL"] = "sqlite:///./test_tasks.db"
from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}

def test_tasks():
    with TestClient(app) as client:
        assert client.post("/tasks", json={"title": "Review CI"}).status_code == 201
        tasks = client.get("/tasks")
        assert tasks.status_code == 200
        task_id = tasks.json()[0]["id"]
        assert client.patch(f"/tasks/{task_id}").json()["done"] is True
        assert client.patch("/tasks/99999999").status_code == 404
        assert client.post("/tasks", json={"title": ""}).status_code == 422
