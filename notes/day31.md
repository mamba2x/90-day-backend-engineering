# Day 31: FastAPI Error Handling, Reusable Resource Dependencies and Week 19 Checkpoint

## What I Learned

Today I learned how to remove repeated task lookup logic from FastAPI routes by creating a reusable dependency.

I also completed the Week 19 FastAPI checkpoint by combining:

- Pydantic schemas
- Schema validation
- Response models
- Query validation
- Dependency injection
- Reusable filtering
- Reusable resource lookup
- `HTTPException`
- HTTP status constants
- CRUD operations
- Route ordering
- Error handling

---

# Reusable Task Lookup Dependency

Previously, GET, PATCH and DELETE could each contain their own task lookup logic:

```python
for item in tasks:
    if item["id"] == task_id:
        return item

# Day 31 Completion Checklist

* [x] Understand reusable resource dependencies
* [x] Understand `get_task_or_404`
* [x] Understand reusable task lookup
* [x] Understand `HTTPException`
* [x] Understand `raise` vs `return`
* [x] Import and use `status`
* [x] Understand HTTP status constants
* [x] Use `status.HTTP_201_CREATED`
* [x] Use `status.HTTP_404_NOT_FOUND`
* [x] Keep `TaskCreate`
* [x] Keep `TaskUpdate`
* [x] Keep `TaskResponse`
* [x] Understand request vs response models
* [x] Keep reusable filtering dependency
* [x] Create reusable task lookup dependency
* [x] Return existing task from dependency
* [x] Raise 404 when task does not exist
* [x] Use `Depends(get_task_or_404)`
* [x] Refactor GET-one route
* [x] Remove duplicated lookup loop from GET
* [x] Refactor PATCH route
* [x] Remove duplicated lookup loop from PATCH
* [x] Use `exclude_unset=True`
* [x] Use `TaskResponse` for PATCH response
* [x] Create DELETE route
* [x] Use `tasks.remove(task)`
* [x] Remove duplicated lookup loop from DELETE
* [x] Understand successful DELETE behaviour
* [x] Understand missing DELETE behaviour
* [x] Correct POST response model
* [x] Correct empty-task ID generation
* [x] Generate new task IDs safely
* [x] Add ID before appending task
* [x] Understand fixed routes
* [x] Understand dynamic routes
* [x] Correct route ordering
* [x] Keep `/tasks/filtered-count`
* [x] Correct filtered-count response
* [x] Keep `/tasks/high-priority`
* [x] Understand validation error vs 404 error
* [x] Understand `/tasks/abc` behaviour
* [x] Understand `/tasks/999` behaviour
* [x] Understand all four CRUD operations
* [x] Use POST for Create
* [x] Use GET for Read
* [x] Use PATCH for Update
* [x] Use DELETE for Delete
* [x] Review Day 31 code
* [x] Correct Day 31 implementation mistakes
* [x] Answer all Day 31 questions
* [x] Complete Week 19 FastAPI checkpoint
* [x] Complete Day 31 review

## Day 31 Status

**Completed ✅**