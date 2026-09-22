from fastapi.testclient import TestClient

from main import app


# ============================================================
# TEST CLIENT
# ============================================================

client = TestClient(app)


# ============================================================
# TEST HEALTH ENDPOINT
# ============================================================

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


# ============================================================
# TEST GET ALL TASKS
# ============================================================

def test_tasks():

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) >= 2

    assert data[0]["title"] == "Learn FastAPI"


# ============================================================
# TEST GET ONE TASK
# ============================================================

def test_get_task():

    response = client.get("/tasks/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1

    assert data["title"] == "Learn FastAPI"

    assert data["priority"] == 5


# ============================================================
# TEST TASK NOT FOUND
# ============================================================

def test_task_not_found():

    response = client.get("/tasks/999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Task not found"

# Day 47 Q&A - Introduction to Automated API Testing

## 1. What is automated testing?

# Automated testing means writing code that automatically checks whether another part of an application behaves as expected.

# Instead of manually opening the API and testing every endpoint, tests can send requests and verify the responses automatically.

# For example, a test can send a request to `/health` and verify that the API returns status code `200`.

# ---

# ## 2. What does `assert` do?

# `assert` checks whether a condition is true.

# For example:

# `assert response.status_code == 200`

# This means I expect the response status code to be `200`.

# If the condition is true, the test continues and can pass.

# If the condition is false, the assertion fails and pytest reports the test as failed.

# ---

# ## 3. What is FastAPI's TestClient used for?

# `TestClient` allows tests to send HTTP-style requests to a FastAPI application.

# For example:

# `client.get("/tasks")`

# can be used to test the `/tasks` endpoint without manually opening Swagger or a browser.

# The basic flow is:

# Test Function

# ↓

# TestClient

# ↓

# FastAPI Application

# ↓

# Endpoint

# ↓

# Response

# ---

# ## 4. What is the difference between `/tasks` and `/tasks/1`?

# `/tasks` represents the collection of Tasks.

# Therefore:

# `GET /tasks`

# returns multiple Tasks, normally as a list.

# For example:

# `[{"id": 1, ...}, {"id": 2, ...}]`

# `/tasks/1` represents one specific Task.

# Therefore:

# `GET /tasks/1`

# returns the Task whose ID is `1`.

# For example:

# `{"id": 1, "title": "Learn FastAPI", "priority": 5}`

# The important distinction is:

# `/tasks`

# → Multiple resources

# → List

# While:

# `/tasks/1`

# → One resource

# → Dictionary/object

# ---

# ## 5. Why do we test both the HTTP status code and the response body?

# They test different parts of the API's behaviour.

# The status code tells us whether the HTTP operation produced the expected result.

# For example:

# `assert response.status_code == 200`

# However, an endpoint could return status code `200` while still returning incorrect data.

# Therefore, we should also check the response body.

# For example:

# `assert data["title"] == "Learn FastAPI"`

# The status code checks the HTTP behaviour, while the response body checks the returned data.

# ---

# ## 6. Why does `/tasks/999` return 404?

# `/tasks/999` asks the API for the Task whose ID is `999`.

# If that Task does not exist, the endpoint raises an `HTTPException` with status code `404`.

# The API therefore returns:

# `404 Not Found`

# with a response containing:

# `{"detail": "Task not found"}`

# This is an example of testing a failure path.

# A good test suite should not only check what happens when valid requests succeed. It should also verify that the application responds correctly when something goes wrong.