import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.routes import router
from core.queue import queue_consumer
from core.state import task_queue


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = asyncio.create_task(queue_consumer(task_queue))
    print("App started, Consumer is Live")
    yield
    # cancel consumer cleanly on shutdown
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        print("Consumer shutdown cleanly")


app = FastAPI(
    title="Distributed Task Queue",
    description="A lightweight Clerly-like system built with FastAPI",
    lifespan=lifespan,
)
app.include_router(router)


@app.get("/health")
async def health():
    return {"status: OK"}


@app.get("/nik")
async def nik():
    import asyncio
    import os

    loop = asyncio.get_running_loop()
    return {
        "pid": os.getpid(),
        "loop_running": loop.is_running(),
        "python_thread": "main thrtead",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
