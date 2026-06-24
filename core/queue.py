import asyncio
from uuid import UUID

from models.task import Priority, Task


class TaskQueue:
    """
    A singleton-style wrapper around asyncio.PriorityQueue
    """

    def __init__(self, maxsize: int = 0):
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=maxsize)
        self._all_tasks: dict[UUID, Task] = {}

    async def enqueue(self, task: Task) -> None:
        """Put a task into the Queue.
        store (priority.value, task) as a tuple.
        PriorityQueue compares tuples element by element
        """
        self._all_tasks[task.id] = task
        await self._queue.put((task.priority.value, task))
