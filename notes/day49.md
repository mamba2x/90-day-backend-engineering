# Day 49 - Pytest Fixtures and Test Isolation

## Overview

Today I learned how to make automated tests more reliable by introducing test isolation and pytest fixtures.

In Day 48, I learned how to test POST requests and Pydantic validation. One important problem was also introduced: tests can modify shared application state.

For example, the current FastAPI application stores Tasks inside a global Python list.

When a POST test creates a new Task, that Task is added to the shared list.

Without resetting the list, another test running afterwards could see the Task created by the previous test.

This can cause tests to behave differently depending on the order in which they run.

Day 49 introduced pytest fixtures as a way to prepare a predictable starting state before each test.

The main concepts covered today were:

- Shared state between tests
- Test isolation
- Pytest fixtures
- The `@pytest.fixture` decorator
- Fixture dependency injection
- Function-scoped fixtures
- Resetting mutable application state
- `clear()` and `extend()`
- Independent tests
- Test-order dependency
- Reusable test setup


# The Shared State Problem

The current FastAPI application contains a global list of Tasks.

Conceptually:

tasks

↓

Task 1

Task 2

This list is shared by the application while the Python process is running.

When a test sends:

POST /tasks

the endpoint creates another Task and appends it to the same list.

The state then becomes:

Task 1

Task 2

Task 3

The important problem is that Task 3 does not automatically disappear when the test finishes.

Another test running afterwards can therefore see the modified list.


# Why Shared State Is Dangerous

Suppose one test creates a Task.

The application state changes from:

2 Tasks

to:

3 Tasks

Another test might expect:

`len(tasks) == 2`

If the second test runs before the creation test, it could pass.

If it runs after the creation test, it could fail.

The result would therefore depend on test execution order.

Conceptually:

Test B runs first

↓

2 Tasks

↓

PASS

But:

Test A runs first

↓

Creates Task 3

↓

Test B runs

↓

3 Tasks

↓

FAIL

This is undesirable because automated tests should produce predictable results.


# Test Isolation

Test isolation means that each test should run independently with a predictable starting state.

One test should not depend on changes made by another test.

The ideal model is:

Test A

↓

Known Starting State

↓

Run Test

↓

Finish

Then:

Test B

↓

Known Starting State

↓

Run Test

↓

Finish

Rather than:

Test A

↓

Changes Shared State

↓

Test B Inherits Changes

A useful question when evaluating a test is:

"Will this test behave the same way if I run it by itself?"

Ideally, the answer should be yes.


# Why Independent Tests Matter

Independent tests are easier to:

- understand
- debug
- maintain
- run individually
- run together
- execute in different orders

If a test fails because another unrelated test ran before it, debugging becomes much more difficult.

A failing test should ideally indicate a problem with the behaviour being tested, rather than a side effect from another test.


# Introduction to Pytest Fixtures

A pytest fixture is reusable setup that pytest can provide to tests.

Fixtures can prepare the environment that a test needs before the test runs.

A fixture is created using:

`@pytest.fixture`

For example:

`@pytest.fixture`

`def reset_tasks():`

The decorator tells pytest that the function is a fixture.

The fixture can then be requested by test functions.


# The reset_tasks Fixture

For today's practical, I created a fixture that resets the global Tasks list.

The fixture performs two operations:

1. Removes all existing Tasks.
2. Restores the original two Tasks.

Conceptually:

Current State

↓

Task 1
Task 2
Task 3
Task 4

↓

`tasks.clear()`

↓

Empty List

↓

`tasks.extend(...)`

↓

Task 1
Task 2

The application is therefore returned to a predictable starting state.


# Understanding tasks.clear()

`tasks.clear()` removes every item from the existing list.

For example:

Before:

Task 1
Task 2
Task 3

After:

`tasks.clear()`

the list becomes empty.

Importantly, `clear()` modifies the existing list object.

It does not create a completely different list.


# Understanding tasks.extend()

`tasks.extend(...)` adds multiple items to an existing list.

After clearing the Tasks list, `extend()` was used to restore the original Tasks.

Conceptually:

[]

↓

extend original Tasks

↓

Task 1
Task 2

Combining `clear()` and `extend()` therefore resets the existing shared list.


# Why We Modify the Existing List

The application and test code are referring to the same Tasks list.

Conceptually:

main.py

↓

tasks
     ↘
      Same List Object
     ↗
test_main.py

Therefore, modifying the existing list changes what both the application and tests see.

Using:

`tasks.clear()`

followed by:

`tasks.extend(...)`

preserves the existing list object while changing its contents.

This is important because simply creating another unrelated list would not necessarily modify the list being used by the FastAPI application.


# Requesting a Fixture

A test requests a fixture by including the fixture name as a function parameter.

For example:

`def test_create_task(reset_tasks):`

There is no need to manually call:

`reset_tasks()`

Pytest sees the parameter and automatically finds the fixture with the matching name.

The process is:

pytest discovers test

↓

pytest sees `reset_tasks`

↓

pytest finds fixture

↓

pytest executes fixture

↓

fixture prepares state

↓

test executes


# Fixture Dependency Injection

The way pytest provides fixtures to test functions is similar to dependency injection.

The test declares what it needs:

`reset_tasks`

Pytest provides it automatically.

This is conceptually similar to FastAPI dependencies, where a route declares a dependency and FastAPI provides it.

The important idea is:

Test declares dependency

↓

pytest resolves dependency

↓

pytest prepares dependency

↓

Test runs


# Function Scope

Pytest fixtures have different possible scopes.

The default scope is:

function

A function-scoped fixture runs separately for every test function that requests it.

For example:

Test A

↓

Fixture Runs

↓

Test A Runs

Then:

Test B

↓

Fixture Runs Again

↓

Test B Runs

Therefore, the setup is repeated for each test.

This is useful for test isolation because every test receives a predictable starting state.


# Testing Task Creation With a Fixture

The Task creation test now requests:

`reset_tasks`

Before the POST request occurs, pytest resets the Tasks list.

The sequence becomes:

Fixture Runs

↓

Task 1
Task 2

↓

POST /tasks

↓

Task 3 Created

↓

Assertions Run

The test can therefore safely create data without depending on what another test previously did.


# Proving That Isolation Works

A second test checks that the application starts with exactly two Tasks.

It also requests:

`reset_tasks`

Therefore, even if the creation test previously added Task 3, pytest resets the state before this test begins.

The sequence becomes:

Previous Test

↓

Task 3 Created

↓

Previous Test Ends

↓

Next Test Requests Fixture

↓

Fixture Clears Tasks

↓

Original Tasks Restored

↓

GET /tasks

↓

Exactly 2 Tasks

↓

PASS

This demonstrates test isolation.


# Checking the Response Type

The Task collection test should verify both:

- the response contains a list
- the list contains exactly two Tasks

Checking the type ensures that `/tasks` still behaves as a collection endpoint.

Conceptually:

GET /tasks

↓

200 OK

↓

JSON

↓

Python List

↓

Exactly 2 Items

This provides stronger verification than checking only the number of items.


# Testing Invalid Priority With the Fixture

The invalid-priority test sends:

`"priority": "not-a-number"`

Pydantic rejects the request and FastAPI returns:

422

Because validation fails before the Task is successfully created, the invalid request does not currently modify the Tasks list.

However, using the fixture for Task-related tests can still provide a consistent and predictable starting state.

This makes the test suite easier to understand and maintain.


# Test Order Dependency

A test has an order dependency when its result depends on another test running before or after it.

For example:

Test A creates Task 3.

Test B expects two Tasks.

If Test B does not reset the state, its result depends on whether Test A ran first.

This produces:

Same Tests

↓

Different Order

↓

Different Result

That is a warning sign in a test suite.

Tests should ideally be designed so that:

Different Order

↓

Same Behaviour

↓

Same Results


# Running Tests Individually

An isolated test should work when executed alone.

For example, a developer should be able to run only the Task creation test and receive the expected result.

They should also be able to run only the Task-count test.

Finally, running both tests together should produce the same results.

Conceptually:

Run Test A Alone

↓

PASS

Run Test B Alone

↓

PASS

Run A + B Together

↓

PASS

This is one useful indication that tests are properly isolated.


# Fixtures Beyond Python Lists

The fixture used today is deliberately simple.

In real backend applications, fixtures can provide much more complex setup.

Examples include:

- Test database sessions
- Test databases
- Test users
- Test Tasks
- Test Projects
- Authentication tokens
- API clients
- Temporary files
- Mocked external services
- Configuration values

Fixtures become especially important when testing database-backed APIs.


# Why Fixtures Improve Test Code

Without fixtures, every test might repeat the same setup code.

For example:

Reset Tasks

↓

Create User

↓

Prepare Data

↓

Run Test

Then another test repeats the same preparation.

Fixtures allow common setup to be defined once and reused.

This improves:

- readability
- consistency
- maintainability
- isolation

Instead of each test manually preparing everything, tests can declare the setup they require.


# Important Distinction: Setup vs Test Behaviour

Fixtures should generally prepare the environment required by a test.

The actual test should focus on the behaviour being verified.

Conceptually:

Fixture

↓

Prepare Environment

Test

↓

Perform Operation

↓

Assert Behaviour

For today's example:

Fixture

↓

Restore original Tasks

Test

↓

POST new Task

↓

Verify 201 and returned data

This separation makes tests easier to understand.


# Day 49 Practical Work

Today's practical focused on three pieces.


## 1. reset_tasks Fixture

A pytest fixture was created to restore the Tasks list to its original state.

It uses:

`tasks.clear()`

and:

`tasks.extend(...)`


## 2. Isolated Task Creation Test

The POST test requests the fixture.

Therefore, it always begins with the original two Tasks before creating another Task.


## 3. Starting-State Test

A GET test also requests the fixture.

It verifies that:

- the endpoint returns 200
- the returned data is a list
- exactly two Tasks exist at the beginning of the test

This demonstrates that the previous test's changes do not leak into the next test.


# Day 49 Q&A Review

## 1. What is test isolation?

Test isolation means that each test runs independently with a predictable starting state.

One test should not rely on changes made by another test.


## 2. What is a pytest fixture?

A pytest fixture is reusable setup that pytest can provide to tests.

It can prepare data, objects or environments that tests require.


## 3. What does @pytest.fixture tell pytest?

It tells pytest that the decorated function is a fixture that can be requested by tests.


## 4. Why do we put reset_tasks inside the test function parameters instead of manually calling it?

Including the fixture name as a parameter declares that the test depends on the fixture.

Pytest automatically finds and executes the fixture before running the test.


## 5. Why use tasks.clear() and tasks.extend(...) instead of assigning a new list?

These operations modify the existing shared list object.

The FastAPI application and test code therefore continue referring to the same list.

Creating an unrelated replacement list could result in the test changing a different reference from the one used by the application.


## 6. What does function scope mean for a pytest fixture?

Function scope means the fixture runs separately for every test function that requests it.

This provides fresh setup for each test.


## 7. Why is it dangerous if tests depend on execution order?

The same tests could pass or fail depending on which test runs first.

This makes the test suite unreliable and difficult to debug.


## 8. What else can fixtures provide?

Fixtures can provide many types of reusable setup.

Examples include:

- test database sessions
- test users
- authentication tokens
- API clients
- temporary files
- mocked services


# Key Mental Models

## Shared State Problem

Test A

↓

Changes Shared Data

↓

Test B

↓

Unexpectedly Sees Changes


## Test Isolation

Test A

↓

Fresh State

↓

Run

↓

Finish

Test B

↓

Fresh State

↓

Run

↓

Finish


## Fixture

Test Requests Fixture

↓

pytest Finds Fixture

↓

Fixture Runs

↓

Environment Prepared

↓

Test Runs


## Function Scope

Test A

↓

Fixture

↓

Test A

Test B

↓

Fixture Again

↓

Test B


## clear() + extend()

Existing Shared List

↓

Clear Contents

↓

Restore Original Contents

↓

Same List Object

↓

Predictable State


# Progression So Far

Day 47

↓

Basic GET Testing

↓

Day 48

↓

POST Requests + Validation Testing

↓

Day 49

↓

Fixtures + Test Isolation

The testing knowledge is now progressing from simply checking endpoints toward building tests that remain reliable as the application grows.


# Completion Checklist

- [x] Understood the shared-state problem
- [x] Understood test isolation
- [x] Learned what pytest fixtures are
- [x] Used `@pytest.fixture`
- [x] Requested fixtures through test parameters
- [x] Understood fixture dependency injection
- [x] Used `tasks.clear()`
- [x] Used `tasks.extend(...)`
- [x] Reset shared state before tests
- [x] Understood why modifying the existing list matters
- [x] Learned about function-scoped fixtures
- [x] Tested Task creation with predictable state
- [x] Tested that each test starts with two Tasks
- [x] Checked collection response type
- [x] Understood test-order dependency
- [x] Understood why tests should work individually
- [x] Learned other practical uses for fixtures
- [x] Completed Day 49 Q&A


# Final Review

Day 49 introduced one of the most important principles of automated testing: tests should be independent.

A test should not succeed or fail because another test happened to execute before it.

Pytest fixtures provide reusable setup that helps create predictable test environments.

For the current FastAPI application, the `reset_tasks` fixture restores the global Tasks list before each test that requests it.

The central progression is:

Shared State

↓

Potential Test Contamination

↓

Fixture

↓

Reset State

↓

Independent Tests

↓

Reliable Test Suite

This provides the foundation required before moving into more realistic database-backed API testing, where isolation becomes even more important.

**Day 49: Completed - Pytest Fixtures and Test Isolation**