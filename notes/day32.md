# Day 32: SQLAlchemy ORM Fundamentals and SQLite Setup

## What I Learned

Today I learned how to define database tables using SQLAlchemy ORM instead of manually writing SQL table creation statements.

I also learned how SQLAlchemy connects Python classes to relational database tables and how SQLite stores persistent data in a database file.

Main concepts covered:

- Persistent data
- SQLite
- SQLAlchemy
- ORM
- Database engine
- `DeclarativeBase`
- ORM models
- `Mapped`
- `mapped_column`
- Primary keys
- Column types
- `nullable=False`
- Python-side defaults
- `Base.metadata`
- `create_all()`
- Pydantic schemas vs SQLAlchemy models

---

# Persistent Data

Previously, the Task API stored data inside a Python list:

```python
tasks = [
    {
        "id": 1,
        "title": "Learn Python"
    }
]
```

# Day 32 Completion Checklist

* [x] Understand persistent vs in-memory data
* [x] Understand what an ORM is
* [x] Understand what ORM stands for
* [x] Understand what problem an ORM solves
* [x] Understand why SQL still matters with an ORM
* [x] Install SQLAlchemy
* [x] Understand SQLite
* [x] Understand the SQLite database URL
* [x] Create `DATABASE_URL`
* [x] Understand `tasks.db`
* [x] Understand the SQLAlchemy engine
* [x] Create the engine
* [x] Use `echo=True`
* [x] Understand `DeclarativeBase`
* [x] Create `Base`
* [x] Understand why ORM models inherit from `Base`
* [x] Understand ORM models
* [x] Create the `Task` ORM model
* [x] Understand `__tablename__`
* [x] Understand `Mapped`
* [x] Understand `mapped_column`
* [x] Understand database column types
* [x] Use `String`
* [x] Use `Boolean`
* [x] Use `Integer`
* [x] Understand primary keys
* [x] Use `primary_key=True`
* [x] Understand `nullable=False`
* [x] Add database defaults
* [x] Understand Pydantic schema vs ORM model
* [x] Understand `Base.metadata`
* [x] Understand `create_all()`
* [x] Use `Base.metadata.create_all(engine)`
* [x] Create the SQLite database file
* [x] Understand that ORM models can create SQL tables
* [x] Understand that manual `CREATE TABLE` is not required here
* [x] Run database setup multiple times
* [x] Understand why existing tables are not recreated
* [x] Translate ORM structure into rough SQL
* [x] Create the `Category` ORM model
* [x] Create the `categories` table definition
* [x] Understand how new ORM models are detected
* [x] Correct raw SQL placement in Python
* [x] Correct `create_all()` placement
* [x] Understand ORM vs database persistence
* [x] Answer all Day 32 questions
* [x] Complete Day 32 code review
* [x] Correct Day 32 implementation issues
* [x] Complete Day 32 ORM fundamentals

## Day 32 Status

**Completed ✅**