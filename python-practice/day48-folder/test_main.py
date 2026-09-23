from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_create_task():

    response = client.post(
        "/tasks",
        json={
            "title": "Write Tests",
            "priority": 5
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Write Tests"
    assert data["priority"] == 5
    assert "id" in data


def test_create_task_invalid_priority():

    response = client.post(
        "/tasks",
        json={
            "title": "Broken Task",
            "priority": "not-a-number"
        }
    )

    assert response.status_code == 422

# Day 48 Q&A - Testing POST Requests and Validation

## 1. What does `json=` do when using `client.post()`?

# `json=` sends data to the API as a JSON request body.

# For example:

# `client.post("/tasks", json={"title": "Write Tests", "priority": 5})`

# sends the title and priority to the `/tasks` endpoint.

# FastAPI receives this data and passes it through the appropriate Pydantic model before the endpoint processes it.

# ---

# ## 2. Why does a successful `POST /tasks` return `201` instead of `200`?

# `201 Created` is used because the POST request successfully created a new resource.

# `200 OK` generally indicates that a request succeeded, while `201 Created` specifically communicates that a new resource was created successfully.

# In this case:

# `POST /tasks`

# creates a new Task, so `201` is the more appropriate status code.

# ---

# ## 3. Why can we use `assert "id" in data` instead of checking an exact ID?

# The important behaviour being tested is that the API generates an ID for the newly created Task.

# The exact ID may change depending on how many Tasks already exist.

# For example, the new Task could receive ID 3 during one test and ID 4 after another Task has already been created.

# Therefore:

# `assert "id" in data`

# checks the behaviour we actually care about without unnecessarily depending on a specific generated ID.

# ---

# ## 4. What role does Pydantic play when a request enters a FastAPI endpoint?

# Pydantic validates the incoming request data against the schema defined by the application.

# For example, if the schema contains:

# `priority: int`

# Pydantic checks that the supplied priority can be treated as an integer.

# If the request contains valid data, FastAPI can continue processing the request.

# If the data fails validation, FastAPI rejects the request before normal endpoint processing continues.

# ---

# ## 5. Why does `"priority": "not-a-number"` produce a `422` response?

# The `TaskCreate` schema expects `priority` to be an integer.

# The value `"not-a-number"` is a string that cannot be converted into a valid integer.

# Therefore, Pydantic validation fails and FastAPI returns a `422` validation error.

# The flow is:

# Request

# ↓

# Pydantic Validation

# ↓

# `priority` should be an integer

# ↓

# `"not-a-number"` is invalid

# ↓

# Validation Fails

# ↓

# 422 Response

# ---

# ## 6. What problem can happen when one test changes shared data that another test also uses?

# One test can affect the result of another test.

# For example, if one test creates a new Task and adds it to the global `tasks` list, that Task remains in the list when another test runs in the same process.

# This means later tests may see data created by earlier tests.

# This can make tests dependent on their execution order and can cause inconsistent or unexpected failures.

# Ideally, tests should be isolated so that each test starts with a predictable state and does not depend on changes made by another test.