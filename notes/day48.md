# Day 48 - Testing POST Requests and Pydantic Validation

## Overview

Today I continued learning automated API testing with pytest and FastAPI's `TestClient`.

In Day 47, I focused mainly on testing GET requests. I learned how to send requests to endpoints, inspect HTTP status codes, convert JSON responses into Python data, and use assertions to verify expected behaviour.

Day 48 extended this by introducing tests for POST requests.

The main difference is that a POST request normally sends data into the application.

The testing flow therefore becomes:

Test Function

↓

TestClient

↓

POST Request + JSON Data

↓

FastAPI

↓

Pydantic Validation

↓

Endpoint

↓

Response

↓

Assertions

The main concepts covered today were:

- Testing POST endpoints
- Sending JSON request bodies
- Testing `201 Created`
- Testing returned resource data
- Avoiding unnecessary assumptions about generated IDs
- Testing invalid request data
- Understanding Pydantic validation
- Testing `422` validation responses
- Understanding shared test state
- Recognising the importance of test isolation


# Testing POST Requests

A POST request is commonly used when creating a new resource.

For example:

`POST /tasks`

creates a new Task.

Unlike the GET requests tested previously, POST requests usually contain data that must be sent to the API.

For example, creating a Task might require:

- title
- priority

The request body could contain:

`{"title": "Write Tests", "priority": 5}`

The API receives this information, validates it and then creates the new Task.


# Sending JSON With TestClient

FastAPI's `TestClient` provides a `json=` argument when sending requests.

For example:

`client.post("/tasks", json={"title": "Write Tests", "priority": 5})`

The `json=` argument sends the supplied Python dictionary as a JSON request body.

The basic flow is:

Python Dictionary

↓

`json=`

↓

JSON Request Body

↓

FastAPI

↓

Pydantic Model

↓

Endpoint

This allows automated tests to simulate the same type of request that a frontend application or another API client could send.


# Testing a Successful POST Request

The first practical task was testing successful Task creation.

The request sent:

`POST /tasks`

with:

`{"title": "Write Tests", "priority": 5}`

The expected behaviour was:

- The request succeeds
- A new Task is created
- The API returns HTTP 201
- The returned title is correct
- The returned priority is correct
- The created Task contains an ID

The test therefore checked:

`response.status_code == 201`

and then converted the response into Python data using:

`response.json()`

The returned data was then checked using assertions.


# Understanding 201 Created

A successful POST request that creates a new resource commonly returns:

`201 Created`

This is more specific than simply returning:

`200 OK`

Both indicate successful HTTP operations, but `201` communicates additional meaning.

It tells the client:

"The request succeeded and a new resource was created."

Therefore:

GET existing resource

↓

200 OK

while:

POST new resource

↓

201 Created

Using appropriate HTTP status codes makes an API easier for clients and developers to understand.


# Testing Returned Resource Data

Testing only the status code would confirm that the request succeeded, but it would not confirm that the correct Task was created.

Therefore, the test also checked the response body.

The important assertions were:

- title equals `"Write Tests"`
- priority equals `5`
- an ID exists

This verifies both HTTP behaviour and application behaviour.

The mental model is:

HTTP Status

↓

Did the operation succeed correctly?

Response Body

↓

Did the API return the correct resource?


# Testing Generated IDs

When a Task is created, the application generates an ID.

It might be tempting to write a test that expects an exact value such as:

`id == 3`

However, this can make the test unnecessarily dependent on the application's current state.

For example:

Initial Tasks:

1
2

New Task:

3

But if another Task has already been created, the next ID could instead be:

4

The important behaviour is usually not:

"The generated ID must be exactly 3."

The important behaviour is:

"The newly created Task must have an ID."

Therefore, checking that `"id"` exists in the response is more flexible.

This introduced an important testing principle:

Tests should verify the behaviour that actually matters instead of unnecessarily depending on implementation details.


# Pydantic Validation

FastAPI uses Pydantic models to validate incoming request data.

The Task creation schema contains fields such as:

`title: str`

and:

`priority: int`

This means the application expects:

- title to contain string-compatible data
- priority to contain integer-compatible data

When a request enters the API, Pydantic checks whether the supplied data matches the expected schema.

The flow is:

Request

↓

Pydantic Model

↓

Validate Fields

↓

Valid?

If yes:

↓

Endpoint continues processing

If no:

↓

Validation error response


# Testing Invalid Data

The second practical task tested what happens when invalid data is sent to the API.

The request contained:

`"priority": "not-a-number"`

However, the Pydantic schema expects:

`priority: int`

The string `"not-a-number"` cannot be interpreted as a valid integer.

Therefore, request validation fails.

The expected result is:

`422`

The test verifies this using:

`assert response.status_code == 422`

This demonstrates that automated tests should not only test successful requests.

They should also verify that invalid requests are rejected correctly.


# Understanding 422 Validation Errors

A `422` response can occur when FastAPI receives request data that does not satisfy the expected request schema.

For today's example:

Request

↓

`priority = "not-a-number"`

↓

Pydantic expects integer

↓

Value cannot be converted into integer

↓

Validation fails

↓

422 response

This means the API correctly prevented invalid input from reaching normal endpoint processing.


# Validation Before Endpoint Processing

One important idea from today is that Pydantic validation happens before the endpoint successfully processes the request data.

Conceptually:

Client Request

↓

FastAPI

↓

Pydantic Validation

↓

Endpoint Logic

Therefore, if the request fails validation, FastAPI can reject it before normal endpoint logic proceeds.

This prevents every endpoint from manually implementing basic type validation.

Instead of repeatedly writing logic such as:

"If priority is not an integer, reject it"

the schema declares:

`priority: int`

and Pydantic performs the validation.


# Successful and Invalid POST Requests

Today demonstrated two important paths for the same endpoint.


## Success Path

Request:

POST /tasks

Valid Data

↓

Pydantic Validation Passes

↓

Endpoint Creates Task

↓

201 Created


## Validation Failure Path

Request:

POST /tasks

Invalid Data

↓

Pydantic Validation Fails

↓

Endpoint does not normally process the invalid model

↓

422 Response

Testing both paths gives better confidence than testing only successful behaviour.


# Shared Test State

Another important concept introduced today was shared state between tests.

The current learning application stores Tasks in a global Python list.

For example:

`tasks = [...]`

When the POST test creates a Task, the endpoint adds the Task to this list.

Conceptually:

Before Test:

Task 1
Task 2

↓

POST Test Runs

↓

Task 3 Created

↓

After Test:

Task 1
Task 2
Task 3

The application state has now changed.


# Why Shared State Can Become a Problem

Suppose another test expects there to be exactly two Tasks.

If the POST test has already created another Task, the second test may now see three Tasks.

This means:

Test A

↓

Changes Shared Data

↓

Test B

↓

Sees Test A's Changes

This can create tests that depend on execution order.

For example:

Test B may pass when executed alone but fail when executed after Test A.

That is undesirable because automated tests should ideally behave consistently regardless of the order in which they are executed.


# Test Isolation

The solution to shared-state problems is test isolation.

Test isolation means each test should ideally run with predictable data and should not depend on changes made by another test.

The ideal mental model is:

Test A

↓

Clean State

↓

Run Test

↓

Finish

Then:

Test B

↓

Clean State

↓

Run Test

↓

Finish

Rather than:

Test A

↓

Changes State

↓

Test B Inherits Changed State

Test isolation becomes especially important when testing database-backed applications.

This concept was introduced today, but the more advanced implementation details such as fixtures, test databases and dependency overrides will be handled separately rather than adding unnecessary complexity to today's lesson.


# Pytest File Name Collision Encountered Today

While running the Day 48 tests, pytest produced an import file mismatch error.

The project contained:

`day47-folder/test_main.py`

and:

`day48-folder/test_main.py`

When pytest was executed from the root of the entire repository, it discovered both files.

Both files had the same Python module name:

`test_main`

This caused a module import collision during pytest's test collection process.

The important lesson is that test discovery is affected by project structure and module naming.

For the current daily-learning structure, the simple solution was to enter the current day's folder before running pytest.

For example:

`cd python-practice/day48-folder`

Then:

`pytest -v`

This limits the current test run to the Day 48 folder and ensures that `from main import app` refers to the Day 48 application.


# Day 48 Practical Work

Two new tests were implemented today.


## Test 1 - Successful Task Creation

The test:

- sends a POST request
- sends JSON data
- expects HTTP 201
- reads the returned JSON
- verifies the Task title
- verifies the Task priority
- verifies that an ID exists

This tests the successful Task creation path.


## Test 2 - Invalid Priority

The test:

- sends a POST request
- supplies an invalid priority
- expects HTTP 422

This verifies that FastAPI and Pydantic reject invalid request data correctly.


# Important Corrections and Improvements

The implementation was functionally correct.

One improvement was making the invalid test name more descriptive.

Instead of:

`test_create_task_invalid`

a clearer name is:

`test_create_task_invalid_priority`

Descriptive test names are useful because pytest displays test names when reporting results.

As the number of tests grows, a descriptive name makes it much easier to understand what behaviour failed.


# Day 48 Q&A Review

## 1. What does `json=` do when using `client.post()`?

`json=` sends data to the API as a JSON request body.

FastAPI receives the data and can validate it against the appropriate Pydantic schema before processing the request.


## 2. Why does a successful POST /tasks return 201 instead of 200?

`201 Created` specifically indicates that the request succeeded and created a new resource.

Since `POST /tasks` creates a new Task, `201` is an appropriate response status.


## 3. Why can we check that an ID exists instead of checking an exact ID?

The exact generated ID can depend on the current application state.

The important behaviour is that the application generates an ID for the newly created resource.

Checking that the ID exists avoids unnecessarily coupling the test to a specific generated value.


## 4. What role does Pydantic play when a request enters a FastAPI endpoint?

Pydantic validates incoming request data against the application's schema.

It checks whether the supplied values satisfy the expected field types and requirements.

Invalid data can therefore be rejected before normal endpoint processing continues.


## 5. Why does `"priority": "not-a-number"` produce a 422 response?

The schema expects priority to be an integer.

`"not-a-number"` cannot be converted into a valid integer.

Pydantic validation therefore fails and FastAPI returns a validation error with HTTP status code 422.


## 6. What problem can happen when one test changes shared data that another test also uses?

The second test may see changes created by the first test.

This can cause tests to depend on execution order and produce inconsistent results.

Tests should ideally be isolated so each test begins with predictable state.


# Key Mental Models

## POST Testing

Test

↓

POST Request

↓

JSON Body

↓

FastAPI

↓

Pydantic

↓

Endpoint

↓

Response

↓

Assertions


## Successful Creation

POST /tasks

↓

Valid Data

↓

Validation Passes

↓

Task Created

↓

201 Created


## Invalid Request

POST /tasks

↓

Invalid Data

↓

Validation Fails

↓

422


## Generated IDs

Do I care that ID == exactly 3?

Usually no.

Do I care that the created resource has an ID?

Yes.

Therefore:

Test the behaviour that matters.


## Shared State

Test A

↓

Changes Data

↓

Test B

↓

May See Changed Data

This can create test-order dependency.


## Test Isolation

Each Test

↓

Predictable Starting State

↓

Independent Behaviour

↓

Reliable Result


# Completion Checklist

- [x] Reviewed GET testing concepts from Day 47
- [x] Learned how to test POST requests
- [x] Used `client.post()`
- [x] Sent JSON request bodies with `json=`
- [x] Tested HTTP 201 Created
- [x] Tested returned Task data
- [x] Verified generated ID existence
- [x] Understood why exact generated IDs should not always be asserted
- [x] Reviewed Pydantic request validation
- [x] Tested invalid request data
- [x] Tested HTTP 422 validation errors
- [x] Understood successful and failure paths
- [x] Introduced shared test state
- [x] Understood why shared state can affect other tests
- [x] Introduced the concept of test isolation
- [x] Identified pytest duplicate test-module naming issue
- [x] Learned to run the current day's tests from its folder
- [x] Completed Day 48 practical work
- [x] Completed Day 48 Q&A


# Final Review

Day 48 extended automated API testing from GET requests into POST requests and request validation.

The main new testing flow is:

POST Request

↓

JSON Data

↓

Pydantic Validation

↓

Endpoint

↓

Response

↓

Assertions

A successful creation request should return the expected HTTP status and resource data.

An invalid request should also behave predictably and return the appropriate validation response.

The most important broader lesson from today is that automated tests should verify both successful and unsuccessful behaviour.

I also learned that tests can modify application state. This means test isolation will become important as testing becomes more advanced, especially when databases are introduced.

Day 48 therefore builds directly on Day 47 and provides the foundation for more reliable and isolated API testing.

**Day 48: Completed - Testing POST Requests and Validation**