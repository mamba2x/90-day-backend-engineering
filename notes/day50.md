# Day 50 - Testing Database-Backed FastAPI Endpoints

## Overview

Today I learned how to test FastAPI endpoints that interact with a real database through SQLAlchemy.

In the previous testing lessons, the application stored Tasks inside a normal Python list.

That allowed test isolation to be handled by resetting the list before each test.

However, real backend applications usually store persistent data inside a database.

Once an endpoint performs operations such as:

- INSERT
- UPDATE
- DELETE
- COMMIT

the application state exists inside the database rather than only inside Python memory.

Therefore, automated tests need a safe and isolated database environment.

The main concepts covered today were:

- Testing database-backed FastAPI endpoints
- Separate test databases
- SQLAlchemy test engines
- Test database sessions
- FastAPI dependency overrides
- Database test isolation
- Pytest `autouse` fixtures
- Fixture setup and teardown with `yield`
- `Base.metadata.drop_all()`
- `Base.metadata.create_all()`
- Protecting the normal application database


# Moving From In-Memory Testing to Database Testing

Previously, Tasks were stored in a Python list.

For example:

tasks

↓

Task 1

Task 2

When a test created another Task, the list changed.

The solution was to reset the list before each test.

The flow was:

Shared Python List

↓

Pytest Fixture

↓

Clear List

↓

Restore Original Data

↓

Run Test

This worked because the application state existed in Python memory.

With SQLAlchemy, the situation changes.

The application now follows:

FastAPI Endpoint

↓

SQLAlchemy Session

↓

Database Engine

↓

Database

Therefore, resetting a Python list is no longer enough.


# The Risk of Testing Against the Normal Database

A database-backed API can perform destructive operations.

For example:

POST /tasks

can create records.

PATCH /tasks/1

can modify records.

DELETE /tasks/1

can remove records.

If automated tests use the normal application database, the tests could modify or destroy actual application data.

For example:

Automated Test

↓

DELETE /tasks/1

↓

Normal Database

↓

Real Task Deleted

This is unsafe.

Automated tests should therefore have their own database.


# Separate Test Database

The normal application database might use:

`sqlite:///./tasks.db`

The automated tests use:

`sqlite:///./test.db`

This creates a clear separation:

Normal Application

↓

tasks.db


Automated Tests

↓

test.db

The test suite can now create, update and delete records without affecting the normal application database.


# Database Engines

SQLAlchemy uses an engine to communicate with a database.

The normal application has an engine connected to:

tasks.db

The test environment creates another engine connected to:

test.db

Conceptually:

Application Engine

↓

tasks.db


Test Engine

↓

test.db

These are separate database connections pointing to separate database files.


# Creating the Test Engine

The test database URL is:

`sqlite:///./test.db`

A separate SQLAlchemy engine is created using this URL.

The important idea is that all database operations performed during testing should eventually reach this test engine.

This provides safety because the normal application database is not being modified.


# SQLite and check_same_thread

The test engine uses:

`connect_args={"check_same_thread": False}`

This is commonly needed when using SQLite with FastAPI's TestClient because requests and database operations may occur across different threads.

Disabling SQLite's same-thread restriction allows the test setup to work correctly with FastAPI's testing environment.


# The Normal Database Dependency

The application already contains a dependency responsible for creating SQLAlchemy sessions.

Conceptually:

`get_session()`

↓

Session

↓

Normal Engine

↓

tasks.db

FastAPI endpoints declare this dependency using:

`Depends(get_session)`

This means the endpoints themselves do not manually create their database connections.

They ask FastAPI for a session.


# Creating a Test Session Dependency

For testing, another dependency is created:

`get_test_session()`

Instead of creating a session using the normal engine, it creates a session using:

`test_engine`

The flow becomes:

`get_test_session()`

↓

Session

↓

test_engine

↓

test.db

The remaining problem is that the endpoints still request:

`get_session`

This is solved using dependency overrides.


# FastAPI Dependency Overrides

FastAPI allows dependencies to be replaced during testing.

The important statement is:

`app.dependency_overrides[get_session] = get_test_session`

This means:

Whenever the application asks for:

`get_session`

during these tests, FastAPI should provide:

`get_test_session`

instead.

Conceptually:

Normal Application:

Endpoint

↓

Depends(get_session)

↓

Normal Session

↓

Normal Engine

↓

tasks.db


Testing:

Endpoint

↓

Depends(get_session)

↓

Dependency Override

↓

get_test_session

↓

Test Session

↓

Test Engine

↓

test.db

This allows the same endpoint implementation to be tested without modifying the endpoint itself.


# Why Dependency Injection Makes Testing Easier

Without dependency injection, an endpoint might directly create its own database connection.

That would make replacing the database during testing more difficult.

Because the endpoint declares:

`Depends(get_session)`

the source of the session can be replaced.

This demonstrates one major advantage of dependency injection.

The endpoint declares what it needs.

FastAPI decides what implementation to provide.

During normal execution:

FastAPI provides the normal database session.

During testing:

FastAPI provides the test database session.


# TestClient and the Test Database

The TestClient sends HTTP requests to the FastAPI application.

The complete testing flow is now:

Test

↓

TestClient

↓

FastAPI Endpoint

↓

Depends(get_session)

↓

Dependency Override

↓

get_test_session()

↓

Session(test_engine)

↓

test.db

Therefore, requests made during the tests operate against the test database rather than the normal application database.


# Why a Separate Test Database Is Not Enough

Creating `test.db` protects the normal application database.

However, it does not automatically provide test isolation.

Suppose Test A creates a Task.

Test A

↓

POST /tasks

↓

Task inserted into test.db

↓

COMMIT

The Task now exists permanently inside the test database until something removes it.

If Test B uses the same test database, it could see the record created by Test A.

Therefore:

Separate Test Database

does not automatically mean:

Isolated Tests

The test database must also be reset between tests.


# Database Test Isolation

Database test isolation means that each test begins with a predictable database state.

For today's tests, that predictable state is an empty database.

The desired behaviour is:

Test A

↓

Fresh Database

↓

Creates Task

↓

Test Ends


Test B

↓

Fresh Database Again

↓

No Tasks

Changes from Test A should not leak into Test B.


# The reset_database Fixture

A pytest fixture was created to reset the database.

The fixture uses:

`Base.metadata.drop_all(test_engine)`

followed by:

`Base.metadata.create_all(test_engine)`

This removes the existing test tables and recreates them.

The process is:

Old Test Database State

↓

drop_all()

↓

Tables Removed

↓

create_all()

↓

Fresh Empty Tables

↓

Test Runs

This provides a predictable starting state for each test.


# Understanding drop_all()

`Base.metadata.drop_all(test_engine)` removes SQLAlchemy tables associated with the application's metadata from the test database.

This is a destructive operation.

That is why it is extremely important that it receives:

`test_engine`

rather than the normal application engine.

Correct:

`Base.metadata.drop_all(test_engine)`

This affects:

test.db

Using the normal application engine could remove tables from the normal application database.


# Understanding create_all()

After the tables are removed, the test suite needs fresh tables.

This is done with:

`Base.metadata.create_all(test_engine)`

SQLAlchemy uses the model metadata to recreate the tables inside the test database.

The process becomes:

drop_all()

↓

No Tables

↓

create_all()

↓

Fresh Empty Tables

This gives the next test a clean database.


# autouse=True

The database fixture uses:

`@pytest.fixture(autouse=True)`

Normally, a fixture must be requested through a test parameter.

For example:

`def test_create_task(reset_database):`

However, `autouse=True` tells pytest to automatically execute the fixture for every applicable test.

Therefore, the test can simply be:

`def test_create_task():`

Pytest still runs the database fixture automatically.

The flow becomes:

pytest discovers test

↓

autouse fixture detected

↓

reset_database runs

↓

database prepared

↓

test runs

This reduces repetition when every test requires the same setup.


# Understanding yield in Fixtures

Fixtures can contain:

`yield`

Code before `yield` is setup.

Code after `yield` is teardown.

The general structure is:

Fixture Starts

↓

Setup

↓

yield

↓

Test Runs

↓

Teardown

For today's fixture:

drop_all()

↓

create_all()

↓

yield

↓

Test Runs

There is currently no additional teardown code after `yield`.

However, the structure allows cleanup behaviour to be added later if necessary.


# Setup and Teardown

Setup prepares everything required before a test.

Examples include:

- Creating database tables
- Creating test users
- Preparing temporary files
- Opening database connections

Teardown cleans resources after the test.

Examples include:

- Removing temporary files
- Closing connections
- Deleting test data
- Removing test resources

Fixtures allow both behaviours to be managed in one reusable location.


# Testing POST /tasks

The first test sends a POST request to:

`/tasks`

with:

- title: Learn Database Testing
- priority: 5

The expected response is:

201 Created

The test then checks that:

- the returned title is correct
- the returned priority is correct
- an ID was generated

Unlike the earlier in-memory POST test, this endpoint now creates a SQLAlchemy object and commits it to the test database.


# Database POST Request Flow

The complete request flow is:

Test

↓

POST /tasks

↓

FastAPI

↓

Pydantic validates TaskCreate

↓

Endpoint creates SQLAlchemy Task

↓

session.add()

↓

session.commit()

↓

Database generates ID

↓

session.refresh()

↓

Task returned

↓

TaskResponse

↓

201 Created

The important difference is that the Task is actually persisted to:

test.db


# Testing That the Database Starts Empty

The second test sends:

GET /tasks

It verifies:

- status code is 200
- response data is a list
- the list contains zero Tasks

The important assertion is:

`len(data) == 0`

This proves that data created by another test does not remain available when this test begins.


# How the Isolation Test Works

Suppose pytest runs the creation test first.

The flow is:

Fixture

↓

Fresh Database

↓

Creation Test

↓

Task Created

↓

1 Task in test.db

↓

Test Ends

Then pytest begins the second test.

Because the fixture has:

`autouse=True`

it runs again.

The flow becomes:

drop_all()

↓

Previous Task Table Removed

↓

create_all()

↓

Fresh Empty Task Table

↓

GET /tasks

↓

[]

Therefore:

`len(data) == 0`

passes.

This demonstrates database test isolation.


# Removing Unnecessary Fixture Parameters

Because the database fixture uses:

`autouse=True`

it does not need to be explicitly added to test parameters.

Instead of:

`def test_create_task(reset_database):`

the cleaner version is:

`def test_create_task():`

Both can result in the fixture being available, but explicitly requesting an autouse fixture is unnecessary when the test does not directly use its returned value.

Understanding this distinction helps keep test code clean.


# Removing Unused Imports

The initial test file imported:

`Task`

However, the tests interact with the API through TestClient and do not directly create or query `Task` ORM objects.

Therefore, the `Task` import is unnecessary.

Removing unused imports makes the test file easier to read and reduces unnecessary dependencies.


# API-Level Testing

Today's tests interact with the application through HTTP requests rather than directly calling database functions.

For example:

`client.post("/tasks", ...)`

and:

`client.get("/tasks")`

This means the test exercises several layers together:

HTTP Request

↓

FastAPI Routing

↓

Pydantic Validation

↓

Dependency Injection

↓

SQLAlchemy Session

↓

Database

↓

Response Serialization

This is more integrated than testing only an individual Python function.


# Day 50 Q&A Review

## 1. Why should automated tests use a separate database?

Tests may create, modify and delete records.

Using a separate database prevents those operations from affecting normal application data.


## 2. What does dependency_overrides do?

It replaces the normal FastAPI database dependency with the test database dependency during testing.

This redirects endpoint database operations to the test database.


## 3. What is the difference between engine and test_engine?

The normal engine connects to the normal application database.

The test engine connects to the test database.

They serve the same general SQLAlchemy purpose but target different database environments.


## 4. Why is a separate test database not enough for isolation?

Records created by one test can remain inside the test database and affect later tests.

The test database therefore needs to be reset between tests.


## 5. What does autouse=True do?

It tells pytest to automatically execute the fixture without requiring every test to explicitly request it as a parameter.


## 6. What happens around yield?

Code before `yield` performs setup.

The test runs when the fixture reaches `yield`.

Code after `yield` performs teardown.


## 7. Why must drop_all() and create_all() use test_engine?

These operations should only modify the test database.

Using the normal application engine could destroy or alter normal application database tables.


## 8. What does it mean if Test A creates a Task but Test B sees zero Tasks?

It demonstrates test isolation.

The fixture successfully resets the database so that data created by one test does not affect another.


# Important Mental Models

## Separate Databases

Application

↓

Normal Engine

↓

tasks.db


Tests

↓

Test Engine

↓

test.db


## Dependency Override

Endpoint

↓

Depends(get_session)

↓

Override

↓

get_test_session

↓

test.db


## Database Isolation

Test A

↓

Fresh DB

↓

Create Data

↓

Finish


Test B

↓

Fresh DB

↓

Previous Data Gone

↓

Run Independently


## Autouse Fixture

Test Discovered

↓

Fixture Automatically Runs

↓

Database Reset

↓

Test Runs


## Fixture Yield

Setup

↓

yield

↓

Test

↓

Teardown


# Progression Through Testing

Day 47

↓

Introduction to Automated API Testing

↓

GET Requests + Failure Paths


Day 48

↓

POST Requests + Pydantic Validation

↓

Understanding Shared State


Day 49

↓

Pytest Fixtures

↓

Test Isolation for In-Memory State


Day 50

↓

Separate Test Database

↓

FastAPI Dependency Overrides

↓

Database Test Isolation

The testing work has now progressed from simple HTTP assertions to safely testing endpoints that perform real database operations.


# Key Lessons

1. Automated tests should not use the normal application database.

2. A separate test database protects normal application data.

3. SQLAlchemy requires a separate test engine to connect to the test database.

4. FastAPI dependency overrides allow endpoints to use the test session without modifying endpoint code.

5. A separate database alone does not guarantee test isolation.

6. Database state must be reset between tests.

7. Pytest fixtures provide reusable database setup.

8. `autouse=True` automatically applies a fixture.

9. Code before `yield` is setup and code after `yield` is teardown.

10. Destructive database test operations must always target the test engine.

11. Tests should produce the same results regardless of execution order.

12. Test isolation becomes increasingly important as backend applications become more complex.


# Completion Checklist

- [x] Understood why database-backed APIs require different testing techniques
- [x] Created a separate test database
- [x] Created a separate SQLAlchemy test engine
- [x] Created a test database session dependency
- [x] Used FastAPI dependency overrides
- [x] Redirected API requests to the test database
- [x] Understood why separate databases do not automatically provide isolation
- [x] Created an automatic database-reset fixture
- [x] Used `Base.metadata.drop_all()`
- [x] Used `Base.metadata.create_all()`
- [x] Understood `autouse=True`
- [x] Understood fixture setup and teardown
- [x] Understood `yield` inside pytest fixtures
- [x] Tested database-backed POST requests
- [x] Verified generated database IDs
- [x] Tested GET requests against the database
- [x] Verified that each test starts with an empty database
- [x] Demonstrated database test isolation
- [x] Understood why test operations must use `test_engine`
- [x] Completed Day 50 Q&A


# Final Review

Day 50 connected FastAPI testing with SQLAlchemy database operations.

The most important architecture is:

TestClient

↓

FastAPI Endpoint

↓

Depends(get_session)

↓

Dependency Override

↓

get_test_session()

↓

Session(test_engine)

↓

test.db

The second major concept is database isolation:

Previous Test Data

↓

drop_all(test_engine)

↓

create_all(test_engine)

↓

Fresh Database

↓

Next Test

This allows automated tests to perform real database operations while protecting the normal application database and preventing tests from contaminating one another.

The central lesson is:

**A reliable backend test should control both where its data is stored and what state that data is in before the test begins.**

**Day 50: Completed - Testing Database-Backed FastAPI Endpoints**