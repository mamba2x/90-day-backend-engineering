# Day 36: Database-Backed PATCH, DELETE and Safe Transactions

## Summary

Today I completed the remaining CRUD operations in my FastAPI Task API by connecting PATCH and DELETE directly to the SQLite database through SQLAlchemy. Before today, my API could already create and retrieve persistent task records. Today I extended that functionality so existing database records can also be updated and deleted through HTTP requests, giving the API full database-backed CRUD capability.

I started by creating a separate `TaskUpdate` Pydantic model for PATCH requests. Unlike `TaskCreate`, the fields in `TaskUpdate` are optional because a PATCH request is meant for partial updates. This means the client can change only one field, such as `completed`, without being forced to resend the title or priority. I learned that having a dedicated update model is important because creation and partial updates have different validation requirements.

I then created a reusable `get_task_or_404()` helper function. This function queries the database for a task using its ID and raises an HTTP 404 error if no matching record exists. This removed duplicated lookup and error-handling logic from the GET, PATCH and DELETE routes. Instead of writing the same `select()`, `session.scalar()` and `HTTPException` logic in several places, the routes can now reuse one helper function.

For partial updates, I used `model_dump(exclude_unset=True, exclude_none=True)` on the incoming `TaskUpdate` model. I learned that `exclude_unset=True` is especially important for PATCH because it ensures that only fields actually supplied by the client are included in the update. Fields that were not sent should remain unchanged. Using `exclude_none=True` also prevents explicit `None` values from being applied to fields that should not become null in this version of the API.

I also learned how to update ORM fields dynamically using `setattr()`. Instead of writing a separate `if` statement for every possible field, I looped through the supplied update data and used `setattr(task, field, value)` to change the corresponding attribute on the SQLAlchemy ORM object. This means the update logic can handle different combinations of fields without needing repetitive code.

One important concept I reinforced today was SQLAlchemy Session tracking. When a task is retrieved through a Session, that ORM object is already being tracked by the Session. Because of this, I do not need to call `session.add()` again before updating it. I can change the object's attributes directly and then call `session.commit()` to persist those changes to the database.

I added transaction safety to the PATCH route using `try`, `except`, `session.rollback()` and `IntegrityError`. If the database rejects an update during `commit()`, the transaction is rolled back so uncommitted changes are cancelled and the Session is returned to a usable state. This connected the transaction concepts from the previous lesson directly to a real FastAPI database route.

After a successful PATCH commit, the ORM object should be refreshed before returning it. Using `session.refresh(task)` reloads the latest database state into the object before FastAPI serializes it through the response model.

I also implemented database-backed DELETE functionality. The DELETE route first retrieves the requested task using `get_task_or_404()`, then uses `session.delete(task)` to mark the ORM object for deletion and `session.commit()` to make the deletion permanent. I learned that `session.delete()` alone does not permanently remove the database row. The transaction must still be committed.

I used HTTP `204 No Content` for successful DELETE requests. I corrected my understanding of this status code today. HTTP 204 does not mean that a task could not be found. It means the request completed successfully but the server intentionally returns no response body. A missing task should instead result in HTTP `404 Not Found`.

I also learned how to properly confirm that a DELETE operation succeeded. After deleting a task, I can perform `GET /tasks/{deleted_id}`. If the task has actually been removed from SQLite, SQLAlchemy returns no matching ORM object and the API responds with HTTP 404 through `get_task_or_404()`.

Another part of today's review was correcting the duplicate `GET /tasks` route that remained from the previous lesson. I had both the original GET route and the newer optional `min_priority` version registered at the same path. The correct design is to keep only one `/tasks` endpoint and let it optionally filter using the `min_priority` query parameter.

The empty PATCH challenge also helped confirm my understanding of partial updates. When the client sends an empty JSON object, `model_dump(exclude_unset=True)` produces an empty update dictionary. The update loop therefore changes nothing, and the route simply returns the existing task unchanged. This is valid behaviour for the current API.

Overall, today's work completed the transition from a basic in-memory CRUD API to a full persistent CRUD backend. The application can now create, retrieve, filter, update and delete task records in SQLite using FastAPI, Pydantic and SQLAlchemy. I also improved the structure of the code by reusing resource lookup logic and applying transaction safety to database writes.

## Key Things I Can Now Explain

- Why PATCH needs a separate `TaskUpdate` model
- Why fields in a PATCH model are optional
- What `model_dump(exclude_unset=True)` does
- Why `exclude_unset=True` is important for partial updates
- What `exclude_none=True` does in the current update design
- How `setattr()` dynamically updates ORM attributes
- Why a queried ORM object does not need `session.add()` again
- How SQLAlchemy Session tracking works
- How to update a database record through FastAPI
- Why `session.commit()` is required after updates
- Why `session.refresh()` is useful after an update
- How to handle failed database writes using rollback
- Why `session.rollback()` is needed after a failed commit
- How to reuse database lookup logic with `get_task_or_404()`
- How database-backed DELETE works
- What `session.delete()` does
- Why deletion must still be committed
- What HTTP 204 No Content means
- The difference between HTTP 204 and HTTP 404
- How to prove that a database row was actually deleted
- Why duplicate routes should be removed
- How an empty PATCH request behaves

## Day 36 Review Score

**7/10**

The main implementation was correct. The strongest parts were the `TaskUpdate` model, partial PATCH logic, `exclude_unset=True`, dynamic updates with `setattr()`, reusable task lookup, PATCH rollback handling, DELETE implementation and the empty PATCH challenge.

The main corrections were removing the duplicate `GET /tasks` route, refreshing the ORM object after PATCH, improving the explanation of Session tracking, correcting the meaning of HTTP 204, and properly explaining how to verify that a deleted task no longer exists.

## Day 36 Completion Checklist

- [x] Understand database-backed PATCH
- [x] Understand partial updates
- [x] Create `TaskUpdate`
- [x] Make PATCH fields optional
- [x] Use `model_dump()`
- [x] Use `exclude_unset=True`
- [x] Understand why unset fields must remain unchanged
- [x] Use `exclude_none=True`
- [x] Use `setattr()` for dynamic updates
- [x] Retrieve existing task before updating
- [x] Return 404 for missing update targets
- [x] Understand Session tracking
- [x] Update ORM objects without calling `session.add()` again
- [x] Commit database updates
- [x] Use rollback for failed PATCH transactions
- [x] Understand why rollback resets failed transactions
- [x] Complete the empty PATCH challenge
- [x] Create reusable `get_task_or_404()`
- [x] Reuse task lookup logic across routes
- [x] Understand database-backed DELETE
- [x] Retrieve task before deletion
- [x] Use `session.delete()`
- [x] Commit deletion
- [x] Use HTTP 204 for successful DELETE
- [x] Understand HTTP 204 No Content
- [x] Understand the difference between 204 and 404
- [x] Know how to confirm deletion using GET
- [x] Correct duplicate route design
- [x] Review Day 36 implementation
- [x] Correct conceptual mistakes from review
- [x] Complete database-backed CRUD flow

## Day 36 Status

**Completed ✅**