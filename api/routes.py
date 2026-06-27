from uuid import UUID

from fastapi import APIRouter, HTTPException

from core.state import task_queue
from models.task import Task, TaskRequest

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=202)  # 202 = Accepted (not yet done)
async def submit_task(request: TaskRequest):
    """
    Submit a task. Returns immediately — processing is async.

    202 Accepted is semantically correct here:
    we've accepted the work, but haven't done it yet.
    """
    task = Task(
        name=request.name,
        priority=request.priority,
        payload=request.payload,
    )
    await task_queue.enqueue(task)
    return {"task_id": task.id, "status": task.status, "queue_depth": task_queue.depth}


@router.get("/")
async def list_tasks():
    return task_queue.all_tasks


@router.get("/{task_id}")
async def get_task(task_id: UUID):
    task = task_queue.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
