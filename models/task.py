from datetime import UTC, datetime
from enum import IntEnum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 5
    LOW = 10


class TaskStatus(str):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"


class TaskRequest(BaseModel):
    """What client sends us"""

    name: str
    priority: Priority = Priority.MEDIUM
    payload: dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    """Internal representation with full state."""

    id: UUID = Field(default_factory=uuid4)
    name: str
    priority: Priority
    payload: dict[str, Any]
    status: str = "pending"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    result: Any = None
    error: str | None = None
