from fastapi import FastAPI, HTTPException
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


# REQUEST MODEL FOR CREATING TASKS

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


# REQUEST MODEL FOR UPDATING TASKS

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


# RESPONSE MODEL

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool
    priority: int


# CREATE TASK

@app.post(
    "/tasks",
    status_code=201,
    response_model=TaskResponse
)
def create_task(new_task: TaskCreate):

    if not tasks:
        new_id = 1

    else:
        new_id = max(
            item["id"] for item in tasks
        ) + 1

    task_dict = new_task.model_dump()

    task_dict["id"] = new_id

    tasks.append(task_dict)

    return task_dict


# GET ALL TASKS

@app.get("/tasks")
def get_tasks():
    return tasks


# GET HIGH PRIORITY TASKS
# Must come before /tasks/{task_id}

@app.get(
    "/tasks/high-priority",
    response_model=list[TaskResponse]
)
def get_high_priority_tasks():

    high_priority_tasks = []

    for item in tasks:

        if item["priority"] >= 4:
            high_priority_tasks.append(item)

    return high_priority_tasks


# GET ONE TASK

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(task_id: int):

    for item in tasks:

        if item["id"] == task_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# UPDATE TASK

@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    data: TaskUpdate
):

    for item in tasks:

        if item["id"] == task_id:

            update_data = data.model_dump(
                exclude_unset=True
            )

            item.update(update_data)

            return item

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# ----------------------------------------
# PRACTICAL TEST ANSWERS
# ----------------------------------------

# Should "Hi" succeed?
#
# Answer:
# No.

# Why?
#
# Answer:
# The minimum allowed title length is 3 characters.
# "Hi" contains only 2 characters, so Pydantic
# rejects the request before the route logic runs.


# Should "Hey" succeed?
#
# Answer:
# Yes.

# Why?
#
# Answer:
# "Hey" has exactly 3 characters, which satisfies
# min_length=3.


# priority 1:
# Result:
# Accepted because 1 is the minimum allowed value.


# priority 5:
# Result:
# Accepted because 5 is the maximum allowed value.


# priority 0:
# Result:
# Rejected because priority must be greater than
# or equal to 1.


# priority 6:
# Result:
# Rejected because priority must be less than
# or equal to 5.


# What priority did the task receive when
# priority was omitted?
#
# Answer:
# 3


# What completed value did it receive?
#
# Answer:
# False


# Why?
#
# Answer:
# Because TaskCreate defines priority=3 and
# completed=False as default values.


# Why didn't priority 100 reach the normal
# PATCH logic?
#
# Answer:
# Pydantic validated the TaskUpdate request before
# the route business logic ran.
#
# Since priority must be between 1 and 5,
# priority=100 failed validation immediately.


# ----------------------------------------
# DAY 29 QUESTIONS AND ANSWERS
# ----------------------------------------

# Question 1:
# What is schema validation?
#
# Answer:
# Schema validation checks incoming data against
# defined rules such as field types, required fields,
# length limits, and numeric ranges.
#
# Invalid data is rejected before the normal
# business logic runs.


# Question 2:
# What problem does Field solve?
#
# Answer:
# Field allows us to define additional validation
# rules and defaults for fields in Pydantic models.
#
# Examples include:
# min_length
# max_length
# ge
# le
# default


# Question 3:
# What does min_length=3 mean?
#
# Answer:
# It means the value must contain at least
# 3 characters.


# Question 4:
# What do ge=1 and le=5 mean?
#
# Answer:
# ge=1 means greater than or equal to 1.
#
# le=5 means less than or equal to 5.
#
# Therefore the valid range is:
#
# 1 <= value <= 5


# Question 5:
# Why are priority 1 and priority 5 valid?
#
# Answer:
# Because both boundary values are included.
#
# ge=1 includes 1 and le=5 includes 5.


# Question 6:
# What is the difference between TaskCreate
# and TaskResponse?
#
# Answer:
# TaskCreate defines the data the client is allowed
# to send when creating a task.
#
# TaskResponse defines the structure of the task
# returned by the API.
#
# TaskCreate does not require an ID because the
# server generates it.
#
# TaskResponse contains the ID because the created
# task now has one.


# Question 7:
# What does response_model tell FastAPI?
#
# Answer:
# response_model tells FastAPI what structure and
# field types the endpoint response should follow.
#
# It helps create a stable and predictable API
# response contract.


# Question 8:
# What is the difference between a validation
# error and a 404 error?
#
# Answer:
# A validation error means the input sent by the
# client does not satisfy the API's schema rules.
#
# A 404 error means the request itself may be valid,
# but the requested resource does not exist.


# Question 9:
# Why should PATCH use the same validation
# rules for fields as POST?
#
# Answer:
# Because the same data should remain valid whether
# it is created or updated.
#
# Otherwise a client could create valid data and
# later use PATCH to change it into invalid data.


# Question 10:
# Why is rejecting bad input before business
# logic useful?
#
# Answer:
# It prevents invalid data from reaching application
# logic, reduces unnecessary processing, makes errors
# easier to understand, and helps keep application
# data consistent.