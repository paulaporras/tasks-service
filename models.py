from datetime import datetime, timezone
from enum import Enum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, StringConstraints


class TaskStatus(str, Enum):
	TODO = "todo"
	IN_PROGRESS = "in_progress"
	DONE = "done"


class TaskPriority(str, Enum):
	LOW = "low"
	MEDIUM = "medium"
	HIGH = "high"


class Task(BaseModel):
	id: UUID = Field(default_factory=uuid4)
	title: Annotated[
		str,
		StringConstraints(strip_whitespace=True, min_length=1, max_length=200),
	]
	description: str | None = None
	status: TaskStatus = TaskStatus.TODO
	priority: TaskPriority = TaskPriority.MEDIUM
	assignee: EmailStr | None = None
	created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
