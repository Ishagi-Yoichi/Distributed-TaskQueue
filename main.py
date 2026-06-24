from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up- initializing queue and worker pool")
    yield
    print("Shutting down- draining workers")


app = FastAPI(
    title="Distributed Task Queue",
    description="A lightweight Clerly-like system built with FastAPI",
    lifespan=lifespan,
)


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
