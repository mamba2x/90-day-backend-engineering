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
