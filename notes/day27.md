# Day 27: FastAPI Routes and Request Handling

## What I Learned

Today I started building real API endpoints using FastAPI.

I learned how FastAPI connects:

```text
HTTP Method + URL Path
        ↓
FastAPI Route
        ↓
Python Function
        ↓
JSON Response / HTTP Error
```

I practised:

* Creating a FastAPI application
* Creating GET, POST and DELETE routes
* Returning JSON responses
* Using path parameters
* Using query parameters
* Filtering in-memory data
* Finding resources by ID
* Using `HTTPException`
* Returning `404 Not Found`
* Returning `201 Created`
* Running FastAPI with the CLI
* Using `/docs`
* Understanding FastAPI's automatic type validation

---

## Creating a FastAPI Application

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()
```

`app` represents the FastAPI application.

Routes are registered on this application.

---

## API Routes

An API route is identified by:

```text
HTTP Method + Path
```

Examples:

```text
GET /tasks
GET /tasks/1
POST /tasks/demo
DELETE /tasks/1
```

Although two routes can use the same path, different HTTP methods represent different operations.

Example:

```text
GET /tasks
→ retrieve tasks

POST /tasks
→ create a task
```

---

## Route Decorators

FastAPI uses decorators to connect paths to Python functions.

Example:

```python
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
```

This means:

```text
GET /health
     ↓
health()
     ↓
JSON response
```

Common decorators include:

```python
@app.get(...)
@app.post(...)
@app.put(...)
@app.patch(...)
@app.delete(...)
```

---

## Returning JSON

FastAPI automatically converts Python dictionaries and lists into JSON.

Python:

```python
return {
    "status": "ok"
}
```

API response:

```json
{
  "status": "ok"
}
```

---

## In-Memory Storage

For today's lesson, tasks were stored in a Python list:

```python
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
```

This is called in-memory storage.

Any changes made to this list disappear when the FastAPI server restarts because the information is not stored in a database.

---

## Health Route

```python
@app.get("/health")
def health():
    return {
        "status": "ok"
    }
```

Endpoint:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## Root Route

```python
@app.get("/")
def root():
    return {
        "message": "Task API"
    }
```

Endpoint:

```text
GET /
```

Expected response:

```json
{
  "message": "Task API"
}
```

---

## GET All Tasks

The tasks endpoint can return every task when no filter is supplied.

```python
@app.get("/tasks")
def get_tasks(completed: bool | None = None):

    if completed is None:
        return tasks

    filtered_tasks = []

    for item in tasks:
        if item["completed"] == completed:
            filtered_tasks.append(item)

    return filtered_tasks
```

Behaviour:

```text
GET /tasks
→ all tasks

GET /tasks?completed=true
→ completed tasks

GET /tasks?completed=false
→ incomplete tasks
```

---

## Query Parameters

A query parameter is normally used to filter or modify a request.

Example:

```text
/tasks?completed=true
```

In FastAPI:

```python
completed: bool | None = None
```

If the query parameter is omitted:

```python
completed = None
```

If:

```text
?completed=true
```

FastAPI converts it to:

```python
True
```

---

## Path Parameters

A path parameter identifies part of the URL.

Example:

```text
GET /tasks/2
```

Route:

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
```

FastAPI extracts:

```python
task_id = 2
```

---

## Path Parameters vs Query Parameters

Path parameter:

```text
/tasks/4
```

usually identifies one resource.

Query parameter:

```text
/tasks?completed=true
```

usually filters or modifies a collection request.

---

## FastAPI Type Validation

This:

```python
task_id: int
```

tells FastAPI that the path value must be interpreted as an integer.

Valid:

```text
/tasks/2
```

Invalid:

```text
/tasks/abc
```

FastAPI handles invalid input automatically before the route logic runs.

---

## Finding One Task

Each item inside `tasks` is a dictionary.

Correct:

```python
for item in tasks:
    if item["id"] == task_id:
        return item
```

Incorrect:

```python
if task_id == item:
```

because that compares:

```text
integer == dictionary
```

instead of:

```text
integer == task ID
```

---

## HTTPException

`HTTPException` allows FastAPI routes to return proper HTTP errors.

Example:

```python
raise HTTPException(
    status_code=404,
    detail="Task not found"
)
```

---

## GET One Task

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    for item in tasks:
        if item["id"] == task_id:
            return item

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

The `404` must be raised after the whole list has been searched.

---

## Important Loop Lesson

Incorrect:

```python
for item in tasks:
    if item["id"] == task_id:
        return item

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
```

This may stop after checking only the first task.

Correct:

```python
for item in tasks:
    if item["id"] == task_id:
        return item

raise HTTPException(
    status_code=404,
    detail="Task not found"
)
```

---

## 404 Not Found

A missing task should return:

```text
404 Not Found
```

because the requested resource does not exist.

It should not return `200 OK`.

---

## POST Route

```python
@app.post("/tasks/demo", status_code=201)
def create_demo_task():
    return {
        "message": "Task creation endpoint"
    }
```

Endpoint:

```text
POST /tasks/demo
```

---

## 201 Created

The correct HTTP status code should be configured on the route:

```python
@app.post(
    "/tasks/demo",
    status_code=201
)
```

This is different from simply returning:

```python
{
    "status_code": 201
}
```

A JSON field called `status_code` does not change the real HTTP response code.

---

## DELETE Route

```python
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
```

Endpoint:

```text
DELETE /tasks/{task_id}
```

---

## Removing Tasks

The list contains dictionaries, not integer IDs directly.

Incorrect:

```python
tasks.remove(task_id)
```

Correct:

```python
tasks.remove(item)
```

---

## Avoid Duplicate Routes

I initially created more than one:

```python
@app.get("/tasks")
```

route.

Instead, the optional filtering logic should be added to one route:

```python
@app.get("/tasks")
def get_tasks(completed: bool | None = None):
```

---

## Variable and Function Naming

I initially used similar names for my task list and route functions.

Bad:

```python
task = [...]
```

and:

```python
def task():
```

A function definition can replace the previous value stored under the same name.

Better:

```python
tasks = [...]
```

and:

```python
def create_demo_task():
```

---

## FastAPI CLI

My file is located at:

```text
python-practice/day27-folder/day27_fastapi_routes.py
```

From the project root, the development server can be started with:

```bash
fastapi dev python-practice/day27-folder/day27_fastapi_routes.py
```

The Python file must contain:

```python
app = FastAPI()
```

for FastAPI to detect the application.

---

## CLI Problems I Fixed

### Wrong File Path

I initially received:

```text
Path does not exist
```

because the path passed to the FastAPI CLI did not match the location of the file.

### FastAPI Application Not Found

I also received:

```text
Could not find FastAPI app in module
```

FastAPI needs a valid application object such as:

```python
app = FastAPI()
```

inside the file.

---

## Interactive Documentation

FastAPI automatically provides interactive API documentation.

When the server is running:

```text
http://127.0.0.1:8000/docs
```

can be used to:

* View routes
* See HTTP methods
* View parameters
* Send requests
* Test endpoints
* Inspect responses
* Check status codes

FastAPI also provides:

```text
/redoc
```

for alternative API documentation.

---

# Mistakes I Corrected

## 1. Wrong Root Response

Incorrect:

```python
return {
    "status": "ok"
}
```

Correct:

```python
return {
    "message": "Task API"
}
```

---

## 2. Integer vs Dictionary Comparison

Incorrect:

```python
if task_id == item:
```

Correct:

```python
if task_id == item["id"]:
```

---

## 3. Returning All Tasks Instead of One Task

Incorrect:

```python
return tasks
```

Correct:

```python
return item
```

when retrieving one specific task.

---

## 4. Raising 404 Inside a Loop

The error should only be raised after every task has been checked.

---

## 5. Wrong HTTPException Parameter

Incorrect:

```python
details="Task not found"
```

Correct:

```python
detail="Task not found"
```

---

## 6. Duplicate GET `/tasks` Routes

I combined retrieval and query filtering into a single route.

---

## 7. Wrong POST Status Code Handling

Incorrect:

```python
def create_task(status_code=201):
```

Correct:

```python
@app.post("/tasks/demo", status_code=201)
```

---

## 8. Wrong DELETE Decorator

Incorrect:

```python
@app.get("/tasks/{task_id}")
```

Correct:

```python
@app.delete("/tasks/{task_id}")
```

---

## 9. Removing an ID Instead of a Dictionary

Incorrect:

```python
tasks.remove(task_id)
```

Correct:

```python
tasks.remove(item)
```

---

## 10. Naming Collision

Instead of:

```python
task = [...]
```

and:

```python
def task():
```

I should use:

```python
tasks = [...]
```

and descriptive function names.

---

# Day 27 Questions and Answers

## 1. What is FastAPI?

FastAPI is a Python web framework used to build APIs.

## 2. What is an API route?

An API route connects an HTTP method and URL path to Python application code that handles the request.

## 3. What does `@app.get("/tasks")` mean?

It tells FastAPI that the function below should handle GET requests sent to `/tasks`.

## 4. What is the difference between `/tasks/4` and `/tasks?completed=true`?

`/tasks/4` uses a path parameter to identify a specific task.

`/tasks?completed=true` uses a query parameter to filter the tasks collection.

## 5. What does `task_id: int` tell FastAPI?

It tells FastAPI that `task_id` should be validated and converted to an integer.

## 6. Why should a missing task return 404 instead of 200?

Because the requested resource does not exist.

`200` means the request successfully returned the requested resource.

## 7. What does HTTPException help us do?

It allows a FastAPI application to return appropriate HTTP errors with status codes and error details.

## 8. What happens to the tasks when the server restarts?

Any changes disappear because the data is stored only in memory rather than in a persistent database.

## 9. What is JSON used for in an API?

JSON is a structured format used to exchange data between clients and servers.

## 10. What is the relationship between an HTTP method and an API path?

Together, the HTTP method and path identify the operation being requested.

Example:

```text
GET /tasks
```

means retrieve tasks.

```text
DELETE /tasks/2
```

means delete task 2.

---

# Remaining Day 27 Practical Work

## Task 8

Test:

```text
GET /tasks/abc
```

and observe FastAPI's automatic validation because:

```python
task_id: int
```

requires an integer.

## Task 9

Test:

```text
GET /tasks/100
```

Expected:

```text
404 Not Found
```

if the task does not exist.

## Task 10

Use:

```text
/docs
```

to test the API endpoints interactively.

## Final Challenge

Create:

```text
GET /tasks/{task_id}/status
```

Expected response:

```json
{
  "task_id": 1,
  "completed": true
}
```

A missing task should return `404`.

---

# Day 27 Completion Checklist

* [x] Understand what FastAPI is
* [x] Understand `FastAPI()`
* [x] Understand API routes
* [x] Understand HTTP method + path
* [x] Understand route decorators
* [x] Understand `@app.get()`
* [x] Understand `@app.post()`
* [x] Understand `@app.delete()`
* [x] Understand returning dictionaries as JSON
* [x] Understand in-memory storage
* [x] Understand path parameters
* [x] Understand query parameters
* [x] Understand path vs query parameters
* [x] Understand optional query parameters
* [x] Understand FastAPI type validation
* [x] Understand `task_id: int`
* [x] Understand `HTTPException`
* [x] Understand `404 Not Found`
* [x] Understand `201 Created`
* [x] Understand searching tasks by ID
* [x] Understand Python list filtering
* [x] Understand deleting objects from an in-memory list
* [x] Understand route naming
* [x] Understand FastAPI CLI basics
* [x] Fixed incorrect CLI file path
* [x] Fixed FastAPI application detection
* [x] Created `/health`
* [x] Created `/`
* [x] Created `GET /tasks`
* [x] Created `GET /tasks/{task_id}`
* [x] Added completed query filtering
* [x] Created `POST /tasks/demo`
* [x] Created `DELETE /tasks/{task_id}`
* [x] Reviewed and corrected Tasks 1-7
* [x] Test `/tasks/abc`
* [x] Test `/tasks/100`
* [x] Test all routes through `/docs`
* [x] Complete `/tasks/{task_id}/status`
* [x] Complete final runtime review
