from fastapi.testclient import TestClient
import pytest

from main import app, tasks


client = TestClient(app)

# This function provides setup that tests can request.
@pytest.fixture
def reset_tasks():

    tasks.clear()

    tasks.extend([
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
    ])


def test_create_task(reset_tasks):

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

def test_tasks_start_with_two_items(reset_tasks):

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    
def test_create_task_invalid_priority():

    response = client.post(
        "/tasks",
        json={
            "title": "Broken Task",
            "priority": "not-a-number"
        }
    )

    assert response.status_code == 422

# # Day 49 Q&A - Pytest Fixtures and Test Isolation

# ## 1. What is test isolation?

# Test isolation means that each test should run independently with its own predictable starting state.

# One test should not depend on changes made by another test.

# For example, if one test creates a new Task, another test should not unexpectedly see that Task simply because it ran afterwards.

# Ideally, a test should behave the same whether it is run by itself or as part of the entire test suite.

# ---

# ## 2. What is a pytest fixture?

# A pytest fixture is reusable setup that pytest can provide to test functions.

# Fixtures can prepare the data, objects, or environment that a test needs before the test runs.

# For example, our `reset_tasks` fixture restores the Tasks list to its original state before a test uses it.

# This gives the test a predictable starting point.

# ---

# ## 3. What does `@pytest.fixture` tell pytest?

# `@pytest.fixture` tells pytest that the function below it is a fixture that can be provided to test functions.

# For example:

# `@pytest.fixture`

# `def reset_tasks():`

# tells pytest that `reset_tasks` is setup functionality that tests can request.

# Pytest can then automatically execute the fixture when a test declares that it needs it.

# ---

# ## 4. Why do we put `reset_tasks` inside the test function parameters instead of manually calling `reset_tasks()`?

# Putting `reset_tasks` in the function parameters tells pytest that the test depends on that fixture.

# For example:

# `def test_create_task(reset_tasks):`

# Pytest sees the fixture name, finds the corresponding fixture and automatically runs it before the test.

# The flow becomes:

# pytest discovers test

# ↓

# pytest sees `reset_tasks`

# ↓

# pytest runs the fixture

# ↓

# fixture prepares the starting state

# ↓

# pytest runs the test

# This allows pytest to manage test setup instead of us manually calling setup functions ourselves.

# ---

# ## 5. Why do we use `tasks.clear()` and `tasks.extend(...)` instead of simply assigning a completely new list?

# `tasks.clear()` and `tasks.extend(...)` modify the existing list object.

# Both `main.py` and the test file are referring to that same list object.

# Therefore, modifying the existing list changes the data that the FastAPI application sees.

# If we simply created a completely new local list, we could end up changing what the test file refers to without changing the original list that the FastAPI application is using.

# The important idea is:

# `clear()` + `extend()`

# ↓

# Modify the existing shared list object

# rather than:

# Create a separate replacement list.

# ---

# ## 6. What does function scope mean for a pytest fixture?

# Function scope means that the fixture runs separately for each test function that requests it.

# For example:

# Test A requests fixture

# ↓

# Fixture runs

# ↓

# Test A runs

# Then:

# Test B requests fixture

# ↓

# Fixture runs again

# ↓

# Test B runs

# This means each test receives fresh setup instead of automatically inheriting the state left behind by the previous test.

# Function scope is the default scope for pytest fixtures.

# ---

# ## 7. Why is it dangerous if tests depend on the order in which they run?

# Tests that depend on execution order can produce inconsistent results.

# For example, Test A might create a new Task.

# If Test B expects exactly two Tasks but runs after Test A, it might now find three Tasks and fail.

# However, if Test B runs before Test A, it could pass.

# This creates a situation where:

# Same tests

# ↓

# Different execution order

# ↓

# Different results

# Tests should ideally be independent so they produce the same result regardless of the order in which pytest executes them.

# ---

# ## 8. Apart from resetting lists, name two things fixtures could provide in a real backend application.

# Fixtures could provide many types of reusable test setup.

# Two examples are:

# 1. A test database or database session.
# 2. A test user.

# Other examples could include authentication tokens, API clients, temporary files, test Tasks, Projects, or mocked external services.

# Fixtures are therefore useful for much more than resetting Python lists. They provide reusable and predictable setup for automated tests.

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