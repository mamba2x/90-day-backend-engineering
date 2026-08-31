# Day 28: FastAPI Request Bodies, Pydantic Models and PATCH Updates

## What I Learned

Today I learned how FastAPI receives structured data from clients using request bodies and how Pydantic models help define and validate that data.

I also learned how to create new resources using `POST` and partially update existing resources using `PATCH`.

The main concepts I covered were:

- Request bodies
- JSON request data
- Pydantic `BaseModel`
- Request schemas
- Required fields
- Default values
- Server-generated IDs
- `model_dump()`
- `model_dump(exclude_unset=True)`
- Creating resources with `POST`
- Updating resources with `PATCH`
- `201 Created`
- `404 Not Found`
- `HTTPException`
- In-memory storage
- Partial updates
- Handling boolean values correctly

---

## Request Bodies

A request body is the data sent by a client to a server as part of an HTTP request.

Example:

```json
{
  "title": "Learn FastAPI",
  "completed": false
}
# Day 28 Completion Checklist

- [x] Understand request bodies
- [x] Understand JSON request data
- [x] Understand Pydantic `BaseModel`
- [x] Understand request schemas
- [x] Understand required fields
- [x] Understand default values
- [x] Create `TaskCreate`
- [x] Receive request bodies in FastAPI
- [x] Understand `model_dump()`
- [x] Convert a Pydantic model into a dictionary
- [x] Generate server-side IDs
- [x] Handle an empty task list
- [x] Understand why `len(tasks) + 1` can fail
- [x] Use `max(existing IDs) + 1`
- [x] Add generated IDs to tasks
- [x] Append new tasks to in-memory storage
- [x] Create `POST /tasks`
- [x] Return `201 Created`
- [x] Understand default `completed=False`
- [x] Understand missing required-field validation
- [x] Create `TaskUpdate`
- [x] Understand optional update fields
- [x] Understand POST vs PATCH
- [x] Create `PATCH /tasks/{task_id}`
- [x] Understand partial updates
- [x] Understand `exclude_unset=True`
- [x] Update only supplied fields
- [x] Understand why `False` is valid update data
- [x] Understand list vs dictionary access
- [x] Search tasks by ID
- [x] Update task dictionaries
- [x] Understand `HTTPException`
- [x] Return `404 Not Found`
- [x] Correct PATCH implementation
- [x] Review Day 28 mistakes
- [x] Answer all Day 28 questions
- [x] Complete Day 28 review

## Day 28 Status

**Completed ✅**