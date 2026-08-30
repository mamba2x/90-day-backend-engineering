from fastapi import FastAPI, HTTPException

app = FastAPI()


tasks = [
    {
        "id": 1,
        "title": "Learn Python",
        "completed": True
    },
    {
        "id": 2,
        "title": "Learn FastAPI",
        "completed": False
    },
    {
        "id": 3,
        "title": "Build Task API",
        "completed": False
    }
]


# Task 1

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# Task 2

@app.get("/")
def root():
    return {
        "message": "Task API"
    }


# Tasks 3 + 5

@app.get("/tasks")
def get_tasks(completed: bool | None = None):

    if completed is None:
        return tasks

    filtered_tasks = []

    for item in tasks:
        if item["completed"] == completed:
            filtered_tasks.append(item)

    return filtered_tasks


# Task 4

@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for item in tasks:
        if item["id"] == task_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# Task 6

@app.post("/tasks/demo", status_code=201)
def create_demo_task():
    return {
        "message": "Task creation endpoint"
    }


# Task 7

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for item in tasks:
        if item["id"] == task_id:
            tasks.remove(item)

            return {
                "message": "Task deleted"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )