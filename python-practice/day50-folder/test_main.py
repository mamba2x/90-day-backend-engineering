import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from main import (
    app,
    Base,
    Task,
    get_session,
)

TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

def get_test_session():

    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = get_test_session
# request made through test client uses test database

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():

    Base.metadata.drop_all(test_engine)

    Base.metadata.create_all(test_engine)

    yield

def test_create_task():

    response = client.post(
        "/tasks",
        json={
            "title": "Learn Database Testing",
            "priority": 5
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Learn Database Testing"
    assert data["priority"] == 5
    assert "id" in data

def test_database_starts_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data,list)
    assert len(data) == 0

# # Day 50 Q&A - Testing Database-Backed FastAPI Endpoints

# ## 1. Why should automated tests use a separate database instead of the normal application database?

# Automated tests should use a separate database so that testing operations do not affect real application data.

# Tests may create, update, or delete records while checking API behaviour.

# If tests used the normal application database, operations such as:

# POST

# UPDATE

# DELETE

# could modify or destroy actual application data.

# Using a separate test database allows tests to freely manipulate data without affecting the normal application database.

# The separation is:

# Normal Application

# ↓

# tasks.db


# Automated Tests

# ↓

# test.db

# ---

# ## 2. What is the purpose of `app.dependency_overrides[get_session] = get_test_session`?

# It tells FastAPI to replace the normal `get_session` dependency with `get_test_session` while the tests are running.

# Normally:

# Endpoint

# ↓

# `get_session`

# ↓

# Normal SQLAlchemy Engine

# ↓

# tasks.db


# During testing:

# Endpoint

# ↓

# `get_session`

# ↓

# Dependency Override

# ↓

# `get_test_session`

# ↓

# Test Engine

# ↓

# test.db

# This allows the same API endpoints to be tested without changing their actual implementation.

# ---

# ## 3. What is the difference between `engine` and `test_engine`?

# `engine` connects the normal application to its normal database.

# For example:

# `engine`

# ↓

# tasks.db


# `test_engine` connects the automated tests to a separate test database.

# For example:

# `test_engine`

# ↓

# test.db

# The normal engine is used when the application runs normally, while the test engine is used during automated testing.

# ---

# ## 4. Why is having a separate test database not enough by itself to guarantee test isolation?

# A separate test database protects the normal application database, but data created by one test can still remain inside the test database.

# For example:

# Test A

# ↓

# Creates Task

# ↓

# Task saved to test.db


# Then:

# Test B

# ↓

# Uses same test.db

# ↓

# Can see Task created by Test A

# Therefore, the test database must also be reset between tests so that each test receives a predictable starting state.

# ---

# ## 5. What does `autouse=True` do on a pytest fixture?

# `autouse=True` tells pytest to automatically execute the fixture for every applicable test without requiring the fixture name to be added to each test's parameters.

# For example:

# `@pytest.fixture(autouse=True)`

# means I can write:

# `def test_create_task():`

# instead of:

# `def test_create_task(reset_database):`

# Pytest automatically runs `reset_database` before the test.

# ---

# ## 6. What happens before and after `yield` inside a pytest fixture?

# Code before `yield` is setup code and runs before the test.

# Code after `yield` is teardown code and runs after the test.

# The flow is:

# Fixture Starts

# ↓

# Setup Code

# ↓

# `yield`

# ↓

# Test Runs

# ↓

# Teardown Code

# For example, database tables could be created before `yield` and cleaned up after the test.

# In today's fixture, `drop_all()` and `create_all()` run before `yield`, giving the test a fresh database.

# ---

# ## 7. Why are we calling `drop_all()` and `create_all()` using `test_engine` rather than the normal application engine?

# We use `test_engine` because we only want to delete and recreate tables inside the test database.

# Using:

# `Base.metadata.drop_all(test_engine)`

# affects:

# test.db

# Using the normal application engine could delete tables from the normal application database.

# Therefore, destructive test setup operations must target the test database rather than the application's real database.

# ---

# ## 8. If Test A creates a Task but Test B immediately sees zero Tasks, what does that demonstrate?

# It demonstrates that the tests are properly isolated.

# Test A can create and commit a Task to the test database.

# Before Test B begins, the fixture resets the database.

# Therefore:

# Test A

# ↓

# Creates Task

# ↓

# 1 Task


# Next Test Starts

# ↓

# Fixture Runs

# ↓

# Database Reset

# ↓

# Test B

# ↓

# 0 Tasks

# This shows that changes made by one test do not leak into another test.

# That is database test isolation.