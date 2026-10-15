from datetime import datetime, timezone
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from main import app, tasks


@pytest.fixture(autouse=True)
def isolate_tasks():
	tasks.clear()
	yield
	tasks.clear()


@pytest.fixture
def client():
	with TestClient(app) as test_client:
		yield test_client


def test_create_task_returns_201_and_generates_id_and_timestamp(client):
	started_at = datetime.now(timezone.utc)
	response = client.post("/tasks", json={"title": "Revisar API"})
	finished_at = datetime.now(timezone.utc)

	assert response.status_code == 201
	task = response.json()
	created_id = UUID(task["id"])
	created_at = datetime.fromisoformat(task["created_at"].replace("Z", "+00:00"))
	assert task["status"] == "todo"
	assert started_at <= created_at <= finished_at

	second_response = client.post("/tasks", json={"title": "Documentar API"})
	assert second_response.status_code == 201
	assert UUID(second_response.json()["id"]) != created_id


def test_list_tasks_and_filter_by_status(client):
	todo_response = client.post("/tasks", json={"title": "Pendiente"})
	done_response = client.post(
		"/tasks",
		json={"title": "Terminada", "status": "done"},
	)

	assert todo_response.status_code == 201
	assert done_response.status_code == 201
	assert len(client.get("/tasks").json()) == 2

	filtered_response = client.get("/tasks", params={"status": "done"})
	assert filtered_response.status_code == 200
	assert [task["id"] for task in filtered_response.json()] == [done_response.json()["id"]]


def test_list_tasks_and_filter_by_priority(client):
	medium_todo = client.post("/tasks", json={"title": "Media y todo"})
	high_todo = client.post(
		"/tasks",
		json={"title": "Alta y todo", "priority": "high"},
	)
	high_done = client.post(
		"/tasks",
		json={"title": "Alta y done", "status": "done", "priority": "high"},
	)

	assert medium_todo.status_code == 201
	assert high_todo.status_code == 201
	assert high_done.status_code == 201
	assert medium_todo.json()["priority"] == "medium"
	assert len(client.get("/tasks").json()) == 3

	by_priority = client.get("/tasks", params={"priority": "high"})
	assert by_priority.status_code == 200
	assert [task["id"] for task in by_priority.json()] == [
		high_todo.json()["id"],
		high_done.json()["id"],
	]

	combined = client.get("/tasks", params={"status": "todo", "priority": "high"})
	assert combined.status_code == 200
	assert [task["id"] for task in combined.json()] == [high_todo.json()["id"]]


def test_get_existing_and_missing_task(client):
	created = client.post("/tasks", json={"title": "Consultar"})
	task_id = created.json()["id"]

	existing_response = client.get(f"/tasks/{task_id}")
	missing_response = client.get(f"/tasks/{uuid4()}")

	assert existing_response.status_code == 200
	assert existing_response.json()["id"] == task_id
	assert missing_response.status_code == 404


def test_patch_updates_only_provided_fields(client):
	created = client.post(
		"/tasks",
		json={"title": "Título original", "status": "in_progress"},
	)
	task_id = created.json()["id"]

	response = client.patch(
		f"/tasks/{task_id}",
		json={"description": "Descripción actualizada"},
	)

	assert response.status_code == 200
	assert response.json()["title"] == "Título original"
	assert response.json()["status"] == "in_progress"
	assert response.json()["description"] == "Descripción actualizada"


def test_delete_task_then_get_returns_404(client):
	created = client.post("/tasks", json={"title": "Eliminar"})
	task_id = created.json()["id"]

	delete_response = client.delete(f"/tasks/{task_id}")
	get_response = client.get(f"/tasks/{task_id}")

	assert delete_response.status_code == 204
	assert get_response.status_code == 404


@pytest.mark.parametrize(
	"payload",
	[
		{"title": "   "},
		{"title": "x" * 201},
		{"title": "Tarea", "assignee": "no-es-un-email"},
	],
)


def test_create_task_rejects_invalid_data(client, payload):
	response = client.post("/tasks", json=payload)

	assert response.status_code == 422


def test_patch_rejects_unknown_fields(client):
    created = client.post("/tasks", json={"title": "Original"})
    task_id = created.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"titel": "Nuevo título"},
    )

    assert response.status_code == 422

    unchanged = client.get(f"/tasks/{task_id}")
    assert unchanged.json()["title"] == "Original"


def test_create_task_rejects_missing_title(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_rejects_invalid_status(client):
    response = client.post(
        "/tasks",
        json={"title": "Tarea", "status": "invalid"},
    )

    assert response.status_code == 422