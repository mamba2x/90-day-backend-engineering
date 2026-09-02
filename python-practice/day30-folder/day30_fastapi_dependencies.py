from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel


app = FastAPI()


tasks = [
    {
        "id": 1,
        "title": "Learn Python",
        "completed": True,
        "priority": 3
    },
    {
        "id": 2,
        "title": "Learn FastAPI",
        "completed": False,
        "priority": 4
    },
    {
        "id": 3,
        "title": "Build Task API",
        "completed": False,
        "priority": 5
    }
]


# RESPONSE MODEL

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    priority: int


# REUSABLE FILTERING DEPENDENCY

def get_filtered_tasks(
    completed: bool | None = Query(default=None),
    min_priority: int | None = Query(
        default=None,
        ge=1,
        le=5
    )
):

    filtered_tasks = tasks.copy()

    if completed is not None:

        filtered_tasks = [
            item
            for item in filtered_tasks
            if item["completed"] == completed
        ]

    if min_priority is not None:

        filtered_tasks = [
            item
            for item in filtered_tasks
            if item["priority"] >= min_priority
        ]

    return filtered_tasks


# GET FILTERED TASKS

@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    filtered_tasks: list[dict] = Depends(
        get_filtered_tasks
    )
):
    return filtered_tasks


# GET NUMBER OF FILTERED TASKS

@app.get("/tasks/filtered-count")
def get_filtered_count(
    filtered_tasks: list[dict] = Depends(
        get_filtered_tasks
    )
):

    return {
        "count": len(filtered_tasks)
    }