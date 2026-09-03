from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Query,
    status
)

from pydantic import BaseModel, Field


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


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100
    )

    completed: bool = False

    priority: int = Field(
        default=3,
        ge=1,
        le=5
    )


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    completed: bool | None = None

    priority: int | None = Field(
        default=None,
        ge=1,
        le=5
    )


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    priority: int


# --------------------------------
# DEPENDENCIES
# --------------------------------

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


def get_high_priority_tasks_dependency():

    return [
        item
        for item in tasks
        if item["priority"] >= 4
    ]


def get_task_or_404(task_id: int):

    for item in tasks:

        if item["id"] == task_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )


# --------------------------------
# FIXED ROUTES FIRST
# --------------------------------

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def create_task(task_create: TaskCreate):

    if not tasks:
        new_id = 1

    else:
        new_id = max(
            task["id"] for task in tasks
        ) + 1

    new_task = task_create.model_dump()

    new_task["id"] = new_id

    tasks.append(new_task)

    return new_task


@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks():
    return tasks


@app.get("/tasks/filtered-count")
def get_filtered_count(
    filtered_tasks: list[dict] = Depends(
        get_filtered_tasks
    )
):

    return {
        "count": len(filtered_tasks)
    }


@app.get(
    "/tasks/high-priority",
    response_model=list[TaskResponse]
)
def get_high_priority_tasks(
    high_priority_tasks: list[dict] = Depends(
        get_high_priority_tasks_dependency
    )
):

    return high_priority_tasks


# --------------------------------
# DYNAMIC ROUTES AFTER
# --------------------------------

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task: dict = Depends(get_task_or_404)
):
    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_update: TaskUpdate,
    task: dict = Depends(get_task_or_404)
):

    update_data = task_update.model_dump(
        exclude_unset=True
    )

    task.update(update_data)

    return task


@app.delete("/tasks/{task_id}")
def delete_task(
    task: dict = Depends(get_task_or_404)
):

    tasks.remove(task)

    return {
        "message": "Task deleted successfully"
    }


# Question 1:
# What problem does get_task_or_404 solve?
#
# Answer: it gets the task by id and if the task is not found it raises an HTTPException with a 404 status code and a detail message "Task not found". This helps to avoid repeating the same logic in multiple routes and makes the code more reusable and maintainable.


# Question 2:
# What does HTTPException do?
#
# Answer:it helps to stop the execution of the code and return an error response to the client with a specific status code and detail message. It is used to handle errors and exceptions in FastAPI applications.


# Question 3:
# Why do we use raise instead of return
# with HTTPException?
#
# Answer:raise is used to stop the execution of the code and return an error response to the client. If we use return, the code will continue to execute and may return a successful response even if there was an error. Using raise ensures that the error is properly handled and communicated to the client.


# Question 4:
# What is the difference between:
#
# GET /tasks/abc
#
# and:
#
# GET /tasks/999
#
# Answer:one is path error and the other is not found error. GET /tasks/abc will return a 422 Unprocessable Entity error because "abc" is not a valid integer for the task_id path parameter. GET /tasks/999 will return a 404 Not Found error because there is no task with the id of 999 in the tasks list.


# Question 5:
# Why is get_task_or_404 useful in GET,
# PATCH and DELETE?
#
# Answer: It ensures that the task exists before performing the operation, providing a consistent way to handle cases where the task is not found.


# Question 6:
# What does Depends(get_task_or_404) give
# the route?
#
# Answer:it returns a task dictionary if the task is found, or raises an HTTPException with a 404 status code if the task is not found. This allows the route to access the task data without having to implement the lookup logic in each route.


# Question 7:
# Why is reusable lookup logic better than
# repeating a for loop in every route?
#
# Answer:it ensures consistency, reduces code duplication, and makes the code easier to maintain. If the lookup logic needs to be changed, it can be updated in one place rather than in multiple routes.


# Question 8:
# What does status.HTTP_201_CREATED mean?
#
# Answer: It indicates that the request was successful and a new resource was created.


# Question 9:
# What does tasks.remove(task) do?
#
# Answer: It removes the specified task from the tasks list.


# Question 10:
# Name the four CRUD operations and their
# HTTP methods in this API.
#
# Answer: Create (POST), Read (GET), Update (PUT), Delete (DELETE)