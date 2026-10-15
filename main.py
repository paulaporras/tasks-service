from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, EmailStr, StringConstraints, ConfigDict

from models import Task, TaskPriority, TaskStatus


TaskTitle = Annotated[
	str,
	StringConstraints(strip_whitespace=True, min_length=1, max_length=200),
]


class TaskCreate(BaseModel):
	title: TaskTitle
	description: str | None = None
	status: TaskStatus = TaskStatus.TODO
	priority: TaskPriority = TaskPriority.MEDIUM
	assignee: EmailStr | None = None


class TaskPatch(BaseModel):
	model_config = ConfigDict(extra="forbid")
	
	title: TaskTitle | None = None
	description: str | None = None
	status: TaskStatus | None = None
	priority: TaskPriority | None = None
	assignee: EmailStr | None = None


app = FastAPI(title="tasks-service")
tasks: dict[UUID, Task] = {}


def get_or_404(task_id: UUID) -> Task:
	task = tasks.get(task_id)
	if task is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Task not found",
		)
	return task


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
	task = Task.model_validate(payload.model_dump())
	tasks[task.id] = task
	return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(
	status_filter: TaskStatus | None = Query(default=None, alias="status"),
	priority_filter: TaskPriority | None = Query(default=None, alias="priority"),
) -> list[Task]:
	return [
		task
		for task in tasks.values()
		if (status_filter is None or task.status == status_filter)
		and (priority_filter is None or task.priority == priority_filter)
	]


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: UUID) -> Task:
	return get_or_404(task_id)


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, payload: TaskPatch) -> Task:
	task = get_or_404(task_id)
	changes = payload.model_dump(exclude_unset=True)
	if any(changes.get(field) is None for field in ("title", "status") if field in changes):
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
			detail="title and status cannot be null",
		)

	updated_task = Task.model_validate({**task.model_dump(), **changes})
	tasks[task_id] = updated_task
	return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID) -> Response:
	get_or_404(task_id)
	del tasks[task_id]
	return Response(status_code=status.HTTP_204_NO_CONTENT)