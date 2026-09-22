# def test_addition():
#     result= 4+4

#     assert result == 8

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class TaskCreate(BaseModel):
    title: str
    priority: int = 3


tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "priority": 5
    },
    {
        "id": 2,
        "title": "Learn Pytest",
        "priority": 4
    }
]


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for task in tasks:

        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.post(
    "/tasks",
    status_code=201
)
def create_task(task: TaskCreate):

    new_id = max(
        item["id"] for item in tasks
    ) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "priority": task.priority
    }

    tasks.append(new_task)

    return new_task

