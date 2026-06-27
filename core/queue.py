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

    async def dequeue(self) -> Task:
        """Block (cooperatively) until a task is available."""
        priority_value, task = await self._queue.get()
        return task

    def task_done(self) -> None:
        """Must be called after processing each dequeue task.
        Decrement the internal counter - required for queue.join() to work.
        """
        self._queue.task_done()

    def get_task(self, task_id: UUID):
        return self._all_tasks.get(task_id)

    def update_task(self, task: Task) -> None:
        self._all_tasks[task.id] = task

    @property
    def depth(self) -> int:
        """How many tasks are waiting rn"""
        return self._queue.qsize()

    @property
    def all_tasks(self) -> list[Task]:
        return list(self._all_tasks.values())


async def queue_consumer(task_queue: TaskQueue):
    """A long running co-routine that drains the queue.
    This is started once at app startup and runs for the app's lifetime.
    `while True` + `await` is the standard asyncio consumer pattern —
    the await on dequeue() yields control back to the loop between tasks.
    """
    print("Queue consumer started...")
    while True:
        # this awaits suspend us until a task arrives - no-busy waiting.
        task = await task_queue.dequeue()

        try:
            task.status = "running"
            task_queue.update_task(task)
            print(f"Running task: {task.name} (priority={task.priority.name})")

            await asyncio.sleep(2)  # simulate work

            task.status = "done"
            task.result = f"completed: {task.name}"
            task_queue.update_task(task)
            print(f"Fone: {task.name}")

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task_queue.update_task(task)
            print(f"Failed: {task.name} - {e}")

        finally:
            task_queue.task_done()
