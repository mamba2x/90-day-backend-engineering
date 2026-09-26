import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from main import (
    app,
    Base,
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

# Requests made through TestClient use the test database.

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_database():

    Base.metadata.drop_all(test_engine)

    Base.metadata.create_all(test_engine)

    yield


# --------------------------------------------------
# Day 50 Tests
# --------------------------------------------------

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

    assert isinstance(data, list)
    assert len(data) == 0


# --------------------------------------------------
# Day 51 Tests
# --------------------------------------------------

def test_update_task():

    # ARRANGE
    create_response = client.post(
        "/tasks",
        json={
            "title": "Old Task",
            "priority": 2
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.json()
    task_id = created_task["id"]

    # ACT
    update_response = client.patch(
        f"/tasks/{task_id}",
        json={
            "priority": 5
        }
    )

    # ASSERT
    assert update_response.status_code == 200

    updated_task = update_response.json()

    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Old Task"
    assert updated_task["priority"] == 5

    # Verify that the update was persisted
    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 200

    saved_task = get_response.json()

    assert saved_task["title"] == "Old Task"
    assert saved_task["priority"] == 5


def test_delete_task():

    # ARRANGE
    create_response = client.post(
        "/tasks",
        json={
            "title": "Delete Me",
            "priority": 3
        }
    )

    assert create_response.status_code == 201

    created_task = create_response.json()
    task_id = created_task["id"]

    # ACT
    delete_response = client.delete(
        f"/tasks/{task_id}"
    )

    # ASSERT
    assert delete_response.status_code == 204

    # Verify that the Task was actually deleted
    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 404

    data = get_response.json()

    assert data["detail"] == "Task not found"


def test_update_missing_task():

    # ACT
    response = client.patch(
        "/tasks/999",
        json={
            "priority": 5
        }
    )

    # ASSERT
    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Task not found"