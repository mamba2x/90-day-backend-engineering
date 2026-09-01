# Day 29: FastAPI Schema Validation and Response Models

## What I Learned

Today I learned how to make FastAPI reject invalid input before it reaches the normal business logic.

I also learned how request schemas and response schemas can be separated so that the API has a clear and predictable contract.

The main concepts covered were:

- Schema validation
- Pydantic `Field`
- `min_length`
- `max_length`
- `ge`
- `le`
- Boundary validation
- Default values
- Request schemas
- Response schemas
- `response_model`
- Validation errors
- `404 Not Found`
- POST validation
- PATCH validation
- Route ordering
- Fixed routes vs dynamic routes
- High-priority filtering

---

## Schema Validation

Schema validation checks incoming data against rules before the application's business logic runs.

For example:

```python
title: str = Field(
    min_length=3,
    max_length=100
)
# Day 29 Completion Checklist

* [x] Understand schema validation
* [x] Understand why APIs validate external input
* [x] Understand Pydantic `Field`
* [x] Understand `min_length`
* [x] Understand `max_length`
* [x] Understand `ge`
* [x] Understand `le`
* [x] Understand boundary validation
* [x] Add title validation
* [x] Add priority field
* [x] Add priority validation
* [x] Understand default priority
* [x] Test valid POST input
* [x] Test too-short title
* [x] Test minimum title boundary
* [x] Test priority 1
* [x] Test priority 5
* [x] Test priority 0
* [x] Test priority 6
* [x] Test default priority
* [x] Test default completed value
* [x] Understand validation before business logic
* [x] Upgrade `TaskUpdate`
* [x] Add title validation to PATCH
* [x] Add priority validation to PATCH
* [x] Test valid PATCH input
* [x] Test invalid PATCH priority
* [x] Understand request schemas
* [x] Understand response schemas
* [x] Create `TaskCreate`
* [x] Create `TaskUpdate`
* [x] Create `TaskResponse`
* [x] Understand `response_model`
* [x] Add response model to POST
* [x] Add response model to GET-one
* [x] Add response model to high-priority route
* [x] Understand validation errors
* [x] Understand `404 Not Found`
* [x] Understand validation error vs 404
* [x] Understand fixed routes
* [x] Understand dynamic routes
* [x] Understand route ordering
* [x] Fix high-priority route conflict
* [x] Create `/tasks/high-priority`
* [x] Filter tasks with `priority >= 4`
* [x] Return all high-priority tasks
* [x] Correct request and response schema separation
* [x] Review and correct Day 29 mistakes
* [x] Answer all Day 29 questions
* [x] Complete Day 29 review

## Day 29 Status

**Completed ✅**