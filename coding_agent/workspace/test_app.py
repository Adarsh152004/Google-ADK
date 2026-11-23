import pytest
from fastapi.testclient import TestClient
from app import app, todos, next_id

@pytest.fixture(autouse=True)
def run_around_tests():
    # Before each test, clear the todos and reset next_id
    todos.clear()
    global next_id
    next_id = 1
    yield

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos/", json={"title": "Test Todo", "description": "This is a test todo"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo"
    assert data["id"] == 1
    assert data["completed"] == False

def test_list_todos():
    client.post("/todos/", json={"title": "Todo 1"})
    client.post("/todos/", json={"title": "Todo 2"})
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"

def test_get_todo():
    response = client.post("/todos/", json={"title": "Get Me"})
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Get Me"

def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_update_todo():
    response = client.post("/todos/", json={"title": "Update Me", "description": "Old description"})
    todo_id = response.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "Updated Todo", "description": "New description", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo"
    assert data["description"] == "New description"
    assert data["completed"] == True

def test_update_todo_not_found():
    response = client.put("/todos/999", json={"title": "Non existent"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo():
    response = client.post("/todos/", json={"title": "Delete Me"})
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404

def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
