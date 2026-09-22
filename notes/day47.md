# Day 47 - Introduction to Automated API Testing with Pytest

## Overview

Today I started learning automated testing for FastAPI applications.

Until now, most API testing was done manually by running the FastAPI application and interacting with endpoints through tools such as Swagger UI.

Manual testing is useful during development, but it becomes inefficient as an application grows.

For example, if an API contains many endpoints, manually checking every endpoint after every code change would take too much time and would make it easy to forget important cases.

Automated testing solves this problem by allowing me to write Python code that automatically:

1. Sends requests to the application.
2. Receives responses.
3. Checks the HTTP status code.
4. Checks the returned data.
5. Reports whether the expected behaviour occurred.

The main tools introduced today were:

- pytest
- FastAPI TestClient
- assert
- response.status_code
- response.json()

The main testing pattern was:

Test

↓

Send Request

↓

Receive Response

↓

Check Status Code

↓

Check Response Data

↓

Pass or Fail


# What Is Automated Testing?

Automated testing means writing code that checks whether another part of the application behaves as expected.

Instead of manually performing the same checks repeatedly, a test can perform them automatically.

For example, if the application contains:

GET /health

and the expected response is:

{"status": "ok"}

a test can automatically send the request and verify both the HTTP status code and the returned JSON.

Automated testing becomes increasingly important as applications grow because existing behaviour can be checked again whenever code changes.


# pytest

pytest is a Python testing framework.

It discovers and executes Python test functions.

Test functions normally begin with:

test_

Examples include:

test_health

test_tasks

test_get_task

test_task_not_found

This naming convention allows pytest to identify functions that should be executed as tests.

Tests can be run using:

pytest

The verbose version is:

pytest -v

The `-v` option provides more information about which individual tests passed or failed.


# FastAPI TestClient

FastAPI provides `TestClient` for testing API endpoints.

It allows test code to make HTTP-style requests to the FastAPI application without manually opening Swagger UI or a browser.

The basic setup is:

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

The `app` is the FastAPI application being tested.

The `client` can then make requests such as:

client.get("/health")

client.get("/tasks")

client.get("/tasks/1")

Conceptually:

Test Function

↓

TestClient

↓

FastAPI Application

↓

Endpoint

↓

Response

This makes it possible to test API behaviour directly from Python.


# The Response Object

When TestClient sends a request, it returns a response object.

For example:

response = client.get("/health")

The response contains information about what the API returned.

Two important things I used today were:

response.status_code

and:

response.json()


# response.status_code

`response.status_code` contains the HTTP status code returned by the endpoint.

For example:

200

means the request succeeded.

404

means the requested resource was not found.

A test can verify the expected status code using:

assert response.status_code == 200

or:

assert response.status_code == 404

This allows the test to verify the HTTP behaviour of the endpoint.


# response.json()

`response.json()` converts the JSON response body into normal Python data.

For example, if the API returns:

{"status": "ok"}

then:

data = response.json()

produces a Python dictionary.

The test can then inspect values using normal Python operations.

For example:

data["status"]

or:

data["title"]

If the endpoint returns a JSON array, `response.json()` produces a Python list.

Therefore, understanding the structure returned by an endpoint is important when writing tests.


# assert

`assert` is used to verify that an expected condition is true.

For example:

assert response.status_code == 200

means:

"I expect this endpoint to return HTTP 200."

If the condition is true, the test continues.

If the condition is false, the test fails.

Another example is:

assert data["title"] == "Learn FastAPI"

This checks whether the returned Task has the expected title.

The basic mental model is:

Expected Behaviour

↓

assert

↓

True

↓

PASS

or:

Expected Behaviour

↓

assert

↓

False

↓

FAIL


# Testing the Health Endpoint

The first test checked:

GET /health

The endpoint returns:

{"status": "ok"}

The test verifies two things.

First:

The endpoint returns HTTP 200.

Second:

The response body contains the expected data.

This introduced an important testing principle:

A test should not always check only whether the request succeeded.

It should also check whether the application returned the correct information.


# Testing Collection Endpoints

The next test checked:

GET /tasks

This endpoint returns multiple Tasks.

Therefore, the JSON response becomes a Python list.

The test checked that:

- the response status was 200
- the response was a list
- the list contained at least two Tasks
- the first Task had the expected title

This introduced the use of:

isinstance(data, list)

to verify the type of returned data.

It also reinforced normal Python list access:

data[0]

The first Task can therefore be accessed using:

data[0]["title"]


# Collection vs Single Resource

One of the most important corrections from today's practical was understanding the difference between:

/tasks

and:

/tasks/1

These endpoints represent different resources.


## /tasks

GET /tasks

requests the Task collection.

It returns multiple Tasks.

Conceptually:

/tasks

↓

Many Tasks

↓

List

Example:

[
    {
        "id": 1,
        "title": "Learn FastAPI"
    },
    {
        "id": 2,
        "title": "Learn Pytest"
    }
]


## /tasks/1

GET /tasks/1

requests one specific Task.

It returns a single Task.

Conceptually:

/tasks/1

↓

One Task

↓

Dictionary

Example:

{
    "id": 1,
    "title": "Learn FastAPI",
    "priority": 5
}

Therefore, if I request:

/tasks

I might access:

data[0]["title"]

because `data` is a list.

If I request:

/tasks/1

I can access:

data["title"]

because `data` is one dictionary.

This distinction caused one of the mistakes in my initial implementation.


# Testing a Single Resource

To test Task 1, the correct request is:

GET /tasks/1

The test can then verify:

- status code is 200
- ID is 1
- title is "Learn FastAPI"
- priority is 5

This verifies that the endpoint retrieves the correct individual resource.


# Testing Failure Behaviour

Testing should not only verify successful operations.

It should also verify that the application fails correctly when invalid requests occur.

For example:

GET /tasks/999

requests a Task that does not exist.

The API should return:

404 Not Found

with:

{"detail": "Task not found"}

The test therefore checks both:

response.status_code

and:

response.json()

This is an example of testing a failure path.


# Success Paths and Failure Paths

A success path represents behaviour where the requested operation succeeds.

Examples include:

GET /health

GET /tasks

GET /tasks/1

A failure path represents expected behaviour when an operation cannot be completed.

For example:

GET /tasks/999

If Task 999 does not exist, returning 404 is the correct behaviour.

Therefore, a 404 response does not automatically mean that the application is broken.

If the requested resource genuinely does not exist, 404 is the expected and correct response.

Testing failure paths verifies that the application handles problems deliberately instead of producing unpredictable behaviour.


# Status Code vs Response Body

A strong API test often checks both:

HTTP status code

and:

response body

These verify different things.


## Status Code

The status code answers:

"Did the HTTP operation produce the expected type of result?"

For example:

200

means success.

404

means resource not found.


## Response Body

The response body answers:

"Did the endpoint return the correct information?"

An endpoint could theoretically return:

200 OK

while still returning incorrect data.

Therefore:

Status Code

↓

HTTP behaviour

Response Body

↓

Application data

Testing both gives stronger confidence in the endpoint's behaviour.


# Important Corrections From Today's Practical

Several useful mistakes were identified during today's exercise.


## Mistake 1 - Using /tasks When Testing One Task

I initially used:

GET /tasks

while trying to access:

data["id"]

This was incorrect because `/tasks` returns a list.

The correct endpoint was:

GET /tasks/1

which returns one Task dictionary.


## Mistake 2 - Testing 404 Against /tasks

I initially attempted to expect a 404 response from:

GET /tasks

However, `/tasks` is a valid endpoint.

Therefore, it should return 200.

To test a missing Task, I should request an ID that does not exist.

For example:

GET /tasks/999

This correctly tests the application's 404 behaviour.


## Mistake 3 - Accessing detail Directly From Response

I initially treated the response object as though the error detail were directly available as:

response.detail

Instead, the response body must first be converted from JSON:

data = response.json()

Then the error detail can be accessed using:

data["detail"]

This reinforced the distinction between:

response

and:

response.json()


## Mistake 4 - Exact Expected Values

Tests should compare against the actual expected values.

For example, if the API returns:

"Task not found"

then the test should expect exactly:

"Task not found"

rather than:

"task not found"

unless the application was intentionally designed otherwise.


# What I Successfully Implemented

Today I successfully worked with four tests:

1. Health endpoint test
2. Task collection test
3. Single Task test
4. Missing Task test

These covered:

- TestClient
- GET requests
- status-code assertions
- JSON response assertions
- lists
- dictionaries
- collection endpoints
- individual-resource endpoints
- successful responses
- 404 responses


# Main Testing Workflow

The most important workflow from today is:

Create TestClient

↓

Send Request

↓

Receive Response

↓

Check response.status_code

↓

Convert Response With response.json()

↓

Check Returned Data

↓

Test Passes or Fails

For example:

Request

↓

GET /tasks/1

↓

Response

↓

200

↓

JSON

↓

Task ID 1

↓

Assertions Pass


# Key Mental Models

## TestClient

Test Code

↓

TestClient

↓

FastAPI Application

↓

Endpoint


## assert

Expected == Actual

↓

True

↓

PASS

Expected == Actual

↓

False

↓

FAIL


## Collection Endpoint

/tasks

↓

Many Tasks

↓

List


## Individual Resource Endpoint

/tasks/1

↓

One Task

↓

Dictionary


## Missing Resource

/tasks/999

↓

Task Does Not Exist

↓

404 Not Found


## API Test

Request

↓

Response

↓

Status Code

+

Response Body

↓

Assertions


# Day 47 Q&A Review

## 1. What is automated testing?

Automated testing means writing code that automatically checks whether another part of the application behaves as expected.

It reduces the need to manually repeat the same checks whenever the application changes.


## 2. What does assert do?

`assert` verifies that a condition is true.

If the condition is true, the test continues.

If the condition is false, the test fails.


## 3. What is FastAPI TestClient used for?

TestClient allows tests to send HTTP-style requests to a FastAPI application.

This allows endpoints to be tested directly from Python without manually using a browser or Swagger UI.


## 4. What is the difference between /tasks and /tasks/1?

`/tasks` represents the collection of Tasks and normally returns a list.

`/tasks/1` represents one specific Task and normally returns a single dictionary/object.


## 5. Why test both status code and response body?

The status code verifies the HTTP result.

The response body verifies that the application returned the expected data.

Checking both gives a stronger test of endpoint behaviour.


## 6. Why does /tasks/999 return 404?

It requests a Task that does not exist.

The application correctly reports that the requested resource was not found using HTTP status code 404.

Testing this verifies the application's failure behaviour.


# Completion Checklist

- [x] Understood the purpose of automated testing
- [x] Introduced pytest
- [x] Used FastAPI TestClient
- [x] Sent GET requests from tests
- [x] Used assert
- [x] Checked HTTP status codes
- [x] Used response.json()
- [x] Tested JSON response data
- [x] Tested a collection endpoint
- [x] Tested a single-resource endpoint
- [x] Tested a successful request
- [x] Tested a 404 failure path
- [x] Understood list vs dictionary responses
- [x] Corrected /tasks vs /tasks/{id} confusion
- [x] Corrected response.detail usage
- [x] Completed four introductory API tests
- [x] Completed Day 47 Q&A


# Final Review

Day 47 introduced automated API testing.

The main goal was not to learn every feature of pytest.

The goal was to understand the fundamental testing loop:

Send Request

↓

Receive Response

↓

Assert Expected Behaviour

The four tests demonstrated how TestClient can interact with a FastAPI application and how pytest assertions can verify the results.

The most important practical distinction from today was:

/tasks

↓

Collection

↓

List

while:

/tasks/1

↓

Single Resource

↓

Dictionary

and:

/tasks/999

↓

Missing Resource

↓

404

I also learned that a useful API test should often check both the HTTP status code and the returned response data.

This creates the foundation for more advanced testing concepts later, including testing POST requests, validation, database-backed endpoints, test isolation, fixtures and dependency overrides.

**Day 47: Completed - Introduction to Automated API Testing**