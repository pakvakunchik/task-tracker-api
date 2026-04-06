import pytest
from app.models import TaskModel

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test","description": "description", "priority": "high"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test"
    assert data["status"] == "todo"
    assert "id" in data

def test_get_empty_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_task_by_id(client):
    create_resp = client.post("/tasks/", json={"title": "Get me"})
    task_id = create_resp.json()["id"]
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Get me"

def test_update_task(client):
    create_resp = client.post("/tasks/", json={"title": "Old title"})
    task_id = create_resp.json()["id"]
    update_resp = client.put(f"/tasks/{task_id}",  json={"title": "New title", "status": "todo", "priority": "high"})
    assert update_resp.status_code == 200
    assert update_resp.json()["title"] == "New title"

def test_delete_task(client):
    create_resp = client.post("/tasks/", json={"title": "To delete"})
    task_id = create_resp.json()["id"]
    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404

def test_filter_and_sort(client, db_session):
    task = TaskModel(title="Test", status="complete", priority="high")
    db_session.add(task)
    db_session.flush()

    response = client.get("/tasks/?status=complete&sort_by_date=asc&sort_by_priority=desc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test"

