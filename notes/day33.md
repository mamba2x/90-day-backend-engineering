# Day 33: SQLAlchemy Sessions, INSERT, Commit, Refresh and SELECT

## What I Learned

Today I learned how to use SQLAlchemy sessions to create, save and retrieve ORM objects from an SQLite database.

I moved beyond only defining database tables and started performing actual database operations.

Main concepts covered:

- SQLAlchemy `Session`
- Engine vs Session
- ORM object creation
- `session.add()`
- `session.add_all()`
- `session.commit()`
- `session.refresh()`
- Persistent database data
- Automatic primary-key generation
- `select()`
- `.where()`
- `session.scalars()`
- `session.scalar()`
- `.all()`
- Querying multiple records
- Querying one record
- Handling `None`
- ORM attribute access

---

# SQLAlchemy Session

A SQLAlchemy `Session` is a workspace used to interact with the database.

It manages operations such as:

- creating records
- querying records
- updating records
- deleting records
- committing transactions
- rolling back transactions

Example:

```python
with Session(engine) as session:
    ...
```

# Day 33 Completion Checklist

* [x] Understand what a SQLAlchemy Session is
* [x] Understand engine vs Session
* [x] Import `Session`
* [x] Import `select`
* [x] Open a session with `Session(engine)`
* [x] Understand the `with` context manager
* [x] Understand automatic Session closing
* [x] Create a `Task` ORM object
* [x] Understand object creation vs database insertion
* [x] Use `session.add()`
* [x] Understand pending database changes
* [x] Use `session.add_all()`
* [x] Add multiple ORM objects
* [x] Use `session.commit()`
* [x] Understand commit and persistence
* [x] Use `session.refresh()`
* [x] Understand why refresh is useful
* [x] Understand database-generated IDs
* [x] Stop manually generating IDs
* [x] Confirm data persists after the script stops
* [x] Understand why IDs continue increasing
* [x] Use `Base.metadata.create_all(engine)`
* [x] Understand why tables must exist before queries
* [x] Understand `select(Task)`
* [x] Understand SQLAlchemy query statements
* [x] Use `session.scalars()`
* [x] Use `.all()`
* [x] Retrieve multiple ORM objects
* [x] Access ORM attributes with dot notation
* [x] Understand `task.title` vs `task["title"]`
* [x] Use `.where()`
* [x] Filter tasks by priority
* [x] Understand ORM `where()` vs SQL `WHERE`
* [x] Use `session.scalar()`
* [x] Retrieve one ORM object
* [x] Handle a query returning `None`
* [x] Understand `scalar()` vs `scalars()`
* [x] Use a variable such as `chosen_id` in a query
* [x] Avoid unnecessary hard-coded IDs
* [x] Create three tasks in the final challenge
* [x] Query all tasks
* [x] Query high-priority tasks
* [x] Query one task by ID
* [x] Understand the relationship between Session and transactions
* [x] Answer all Day 33 questions
* [x] Review Day 33 implementation
* [x] Correct Day 33 query mistakes
* [x] Complete Day 33 SQLAlchemy sessions practice

## Day 33 Status

**Completed ✅**