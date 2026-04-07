from celery.result import AsyncResult
from fastapi import FastAPI
from pydantic import BaseModel

from tasks import add, send_email
import uvicorn

app = FastAPI(title="Celery + RabbitMQ demo")


# ── Request bodies ──────────────────────────────────────────────────────────


class AddRequest(BaseModel):
    x: int
    y: int


class EmailRequest(BaseModel):
    to: str
    subject: str


# ── Endpoints ───────────────────────────────────────────────────────────────


@app.post("/tasks/add")
def dispatch_add(req: AddRequest):
    """Dispatch a fast task and return the task ID immediately."""
    task = add.delay(req.x, req.y)
    return {"task_id": task.id}


@app.post("/tasks/email")
def dispatch_email(req: EmailRequest):
    """Dispatch a slow task (5 s). Poll /tasks/{id}/status to track it."""
    task = send_email.delay(req.to, req.subject)
    return {"task_id": task.id}


@app.get("/tasks/{task_id}/status")
def get_task_status(task_id: str):
    """
    Poll this endpoint after dispatching a task.

    Possible states: PENDING → STARTED → SUCCESS | FAILURE | RETRY
    """
    result = AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "status": result.status,
    }
    if result.ready():
        if result.successful():
            response["result"] = result.get()
        else:
            response["error"] = str(result.result)
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
