# Day 51 - Testing UPDATE and DELETE Database Endpoints

## Overview

Today I extended automated testing of the database-backed FastAPI application to cover UPDATE and DELETE operations.

In Day 50, I learned how to:

- Create a separate test database
- Create a test SQLAlchemy engine
- Override FastAPI's database dependency
- Reset the test database before each test
- Test database-backed POST and GET endpoints

Day 51 builds on that foundation by testing operations that modify existing database state.

The main concepts covered today were:

- Testing PATCH endpoints
- Testing DELETE endpoints
- Arrange, Act, Assert
- Creating test data inside each test
- Partial updates
- `model_dump(exclude_unset=True)`
- Testing persisted database changes
- Verifying deletion
- Testing 404 failure paths
- Keeping tests independent


# Why UPDATE and DELETE Tests Are Different

POST testing mainly verifies that a new resource can be created.

PATCH and DELETE operate on resources that must already exist.

Therefore, a PATCH or DELETE test usually needs to create the required resource before performing the operation being tested.

For example:

Create Task

↓

Get Task ID

↓

PATCH Task

or:

Create Task

↓

Get Task ID

↓

DELETE Task

Each test therefore prepares its own required data.


# Arrange, Act, Assert

A common structure for automated tests is:

Arrange

↓

Act

↓

Assert

This is often called the AAA pattern.


## Arrange

Arrange means preparing everything required for the test.

For example, before testing PATCH, the test creates:

- title: Old Task
- priority: 2

The created Task's ID is then stored.

This gives the test a known resource to update.


## Act

Act means performing the behaviour being tested.

For the update test:

PATCH /tasks/{task_id}

is the Act step.

For the deletion test:

DELETE /tasks/{task_id}

is the Act step.


## Assert

Assert means verifying that the application behaved as expected.

For example:

- PATCH returns 200
- priority becomes 5
- title remains unchanged
- DELETE returns 204
- deleted Task can no longer be retrieved

The overall mental model is:

ARRANGE

↓

Prepare Scenario

↓

ACT

↓

Perform Behaviour

↓

ASSERT

↓

Verify Behaviour


# Testing PATCH

The PATCH test first creates a Task.

The initial Task contains:

title = Old Task

priority = 2

The test then retrieves the generated Task ID.

This is important because database-generated IDs should generally not be assumed.

Instead of assuming:

Task ID = 1

the test uses the actual ID returned by the API.

The flow is:

POST /tasks

↓

Database Creates Task

↓

API Returns Task

↓

Read `id`

↓

Use ID for PATCH


# Partial Updates

PATCH represents a partial update.

This means the client does not need to send every field.

For example:

`{"priority": 5}`

means:

Update priority

but:

Do not modify title

Therefore, after the PATCH request, the expected Task is:

title = Old Task

priority = 5

The title remaining unchanged is an important part of the test.


# TaskUpdate Schema

The update schema allows fields to be optional.

Conceptually:

title = optional

priority = optional

This allows requests such as:

`{"priority": 5}`

without requiring the client to resend the title.


# model_dump(exclude_unset=True)

The PATCH endpoint uses:

`model_dump(exclude_unset=True)`

This returns only fields that were actually supplied by the client.

For example, if the request contains:

`{"priority": 5}`

the update data becomes:

`{"priority": 5}`

The missing title is not treated as an update.

This is important for implementing correct partial-update behaviour.


# Applying Updates Dynamically

The endpoint loops through the supplied update fields and uses:

`setattr()`

to modify the SQLAlchemy object.

Conceptually:

Update Data

↓

priority = 5

↓

setattr(task, "priority", 5)

↓

Task Object Updated

After the changes are applied:

`session.commit()`

persists them to the database.

Then:

`session.refresh(task)`

reloads the current database state into the SQLAlchemy object.


# Why Testing the PATCH Response Is Not Enough

The PATCH response may appear correct, but a strong database test should verify that the change was actually persisted.

Therefore, the test performs another request:

GET /tasks/{task_id}

after the PATCH request.

The complete flow becomes:

PATCH

↓

Response Says priority = 5

↓

GET Same Task

↓

Database Returns priority = 5

This gives stronger evidence that:

`session.commit()`

successfully persisted the change.


# Testing Persistence

Persistence means that a change remains stored after the operation that created the change has finished.

For today's PATCH test:

PATCH /tasks/{id}

↓

priority becomes 5

↓

COMMIT

↓

GET /tasks/{id}

↓

priority is still 5

This proves that the update exists in the database rather than only appearing in the PATCH response.


# Testing Unchanged Fields

The PATCH request only sends:

priority = 5

The test also checks:

title = Old Task

This is important.

If the title unexpectedly changed or became null, the PATCH implementation would not be correctly preserving fields that were omitted from the request.

Therefore, a partial-update test should verify both:

Changed fields changed correctly

and:

Unspecified fields remained unchanged.


# Testing DELETE

The DELETE test also begins by creating its own Task.

The Task contains:

title = Delete Me

priority = 3

The API returns the generated ID.

The test then sends:

DELETE /tasks/{task_id}

The expected response is:

204 No Content


# Understanding 204 No Content

HTTP status code 204 means that the request succeeded but there is no response body that needs to be returned.

For the DELETE endpoint:

Task Found

↓

Task Deleted

↓

Transaction Committed

↓

204 No Content

The client therefore knows that the deletion request completed successfully.


# Why 204 Alone Is Not Enough

Receiving a 204 response tells us that the endpoint claims the operation succeeded.

However, when testing database behaviour, we can verify the result more strongly.

After DELETE, the test performs:

GET /tasks/{task_id}

The expected response is:

404 Not Found

This demonstrates that the Task is no longer available in the database.


# Verifying Deletion

The deletion test therefore follows:

ARRANGE

↓

Create Task

↓

ACT

↓

DELETE Task

↓

ASSERT

↓

204

↓

VERIFY STATE

↓

GET Same Task

↓

404

This provides stronger verification than checking the DELETE response alone.


# Reusable 404 Lookup

The application uses a helper function for retrieving a Task.

Conceptually:

get_task_or_404(task_id, session)

↓

session.get(Task, task_id)

↓

Does Task Exist?

If yes:

Return Task

If no:

Raise HTTPException 404

This helper prevents GET, PATCH and DELETE endpoints from duplicating the same lookup logic.


# Testing the Failure Path

Testing successful behaviour is not enough.

Backend tests should also verify what happens when operations cannot be completed.

Today's failure-path test attempts:

PATCH /tasks/999

Because the database starts empty, Task 999 does not exist.

The expected response is:

404 Not Found

with:

`"detail": "Task not found"`

This verifies that the API handles missing resources correctly.


# Why Each Test Creates Its Own Data

The update test does not depend on the creation test.

The deletion test does not depend on the update test.

Instead, each test creates the resource it needs.

This is intentional.

A bad test design would look like:

Test A

↓

Creates Task

↓

Test B

↓

Assumes Task from Test A exists

This creates test-order dependency.

Instead:

Update Test

↓

Creates Its Own Task

↓

Updates It


Delete Test

↓

Creates Its Own Task

↓

Deletes It

Each test owns its own scenario.


# Database Isolation Still Applies

The database fixture from Day 50 still runs automatically before every test.

The fixture:

1. Drops the test database tables.
2. Recreates fresh tables.
3. Allows the test to run.

Because it uses:

`autouse=True`

the tests do not need to explicitly request the fixture.

The flow is:

Test 1

↓

Fresh Database

↓

Create + Update Task

↓

Test Ends


Next Test

↓

Database Reset

↓

Fresh Database

↓

Create + Delete Task

↓

Test Ends


Next Test

↓

Database Reset

↓

Fresh Database

↓

PATCH Missing Task

↓

404

No test relies on data left behind by another test.


# Testing State Instead of Only Responses

One of the major lessons today is the difference between testing an HTTP response and testing application state.

A weaker update test might only check:

PATCH response = 200

A stronger test checks:

PATCH response = 200

↓

Returned values correct

↓

GET resource again

↓

Stored values correct

Similarly, a weaker DELETE test might only check:

DELETE response = 204

A stronger test checks:

DELETE response = 204

↓

GET deleted resource

↓

404

This verifies the actual state transition.


# State Transitions

PATCH represents:

Existing Resource

↓

Modified Resource

DELETE represents:

Existing Resource

↓

No Resource

Testing these operations means verifying those transitions.

For PATCH:

priority 2

↓

PATCH

↓

priority 5

For DELETE:

Task Exists

↓

DELETE

↓

Task Does Not Exist


# Generated IDs in Tests

The tests create resources and read the generated ID from the API response.

For example:

Create Task

↓

Response

↓

Read `id`

↓

Use ID in PATCH or DELETE URL

This is safer than assuming a particular ID such as:

`/tasks/1`

Database IDs can vary depending on the state of the database and how records are created.

Tests should therefore use the actual generated identifier whenever possible.


# Day 51 Test Suite

The test suite now contains database-backed tests covering:

- POST creation
- GET collection
- PATCH update
- DELETE
- Missing-resource handling
- Database isolation

The progression is becoming closer to testing a real CRUD API.


# Day 51 Q&A Review

## 1. What does Arrange, Act, Assert mean?

Arrange means preparing the test scenario.

Act means performing the behaviour being tested.

Assert means verifying that the actual result matches the expected result.

The pattern is:

Arrange

↓

Act

↓

Assert


## 2. Why should a PATCH test verify fields that were not supplied?

PATCH is a partial update.

Fields that were not supplied should remain unchanged.

Testing those fields ensures that the endpoint does not accidentally overwrite existing data.


## 3. What does model_dump(exclude_unset=True) do?

It returns only fields that were explicitly supplied by the client.

This allows the endpoint to update only the requested fields.


## 4. Why isn't checking only the PATCH response enough?

The response might contain the expected value without proving that the change was correctly persisted.

Performing a later GET confirms that the database contains the updated state.


## 5. Why perform GET after PATCH?

The GET verifies persistence.

It confirms that the updated values can be retrieved from the database after the PATCH operation has completed.


## 6. Why perform GET after DELETE?

The GET verifies that the deleted resource is actually gone.

The expected result is:

404 Not Found


## 7. Why does each test create its own Task?

Each test should be independent.

Depending on a Task created by another test would introduce execution-order dependency and weaken test isolation.


## 8. What should happen when PATCH targets a missing Task?

The API should return:

404 Not Found

with an appropriate error message such as:

`Task not found`


# Important Mental Models

## Arrange, Act, Assert

Prepare

↓

Perform

↓

Verify


## PATCH Testing

Create Resource

↓

PATCH Resource

↓

Check Response

↓

GET Resource

↓

Verify Persisted Update


## DELETE Testing

Create Resource

↓

DELETE Resource

↓

204

↓

GET Resource

↓

404


## Partial Update

Existing Task:

title = Old Task
priority = 2

↓

PATCH:

priority = 5

↓

Result:

title = Old Task
priority = 5


## Test Independence

Test A

↓

Creates Own Data

↓

Runs Scenario

↓

Ends


Test B

↓

Fresh Database

↓

Creates Own Data

↓

Runs Scenario

↓

Ends


# Progression Through Testing

Day 47

↓

Basic API Testing


Day 48

↓

POST + Validation Testing


Day 49

↓

Fixtures + In-Memory Test Isolation


Day 50

↓

Database Testing + Dependency Overrides


Day 51

↓

UPDATE + DELETE Testing

↓

Persistence Verification

↓

Failure-Path Testing

The tests are now moving beyond simply checking HTTP responses and are verifying actual database state changes.


# Key Lessons

1. PATCH and DELETE tests usually need existing resources.

2. Each test should arrange its own required data.

3. Arrange, Act, Assert provides a clean structure for tests.

4. PATCH should modify only fields supplied by the client.

5. `exclude_unset=True` supports partial updates.

6. Unspecified fields should remain unchanged after PATCH.

7. A successful response does not always prove that database state changed correctly.

8. GET requests can verify persisted updates.

9. DELETE tests should verify that the resource can no longer be retrieved.

10. Failure paths such as 404 responses should be tested.

11. Generated database IDs should be read from API responses rather than assumed.

12. Tests should remain independent regardless of execution order.


# Completion Checklist

- [x] Added GET single Task endpoint
- [x] Added reusable Task lookup helper
- [x] Added TaskUpdate schema
- [x] Added PATCH endpoint
- [x] Used `exclude_unset=True`
- [x] Preserved fields omitted from PATCH requests
- [x] Added DELETE endpoint
- [x] Used `session.delete()`
- [x] Committed database deletions
- [x] Learned Arrange, Act, Assert
- [x] Created test resources inside individual tests
- [x] Tested PATCH response
- [x] Verified PATCH persistence with GET
- [x] Verified unchanged fields after PATCH
- [x] Tested DELETE response
- [x] Verified deletion with GET
- [x] Tested missing-resource PATCH
- [x] Verified 404 error response
- [x] Maintained database test isolation
- [x] Understood state-transition testing


# Final Review

Day 51 extended database-backed API testing from resource creation into resource modification and deletion.

The most important improvement was learning not to stop at the immediate HTTP response.

For updates:

PATCH

↓

Check Response

↓

GET Resource

↓

Verify Database State

For deletion:

DELETE

↓

Check 204

↓

GET Resource

↓

Verify 404

This means the tests are verifying both the API response and the resulting database state.

The central principle from Day 51 is:

**Do not only test what the API says happened. Test the resulting state to prove that it actually happened.**

**Day 51: Completed - Testing UPDATE and DELETE Database Endpoints**