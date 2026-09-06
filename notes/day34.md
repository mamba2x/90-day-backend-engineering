# Day 34: SQLAlchemy Transactions, Rollback, Update and Delete

## What I Learned

Today I learned how SQLAlchemy handles database transactions, how to update and delete ORM objects, and how to recover safely from failed database operations using `rollback()`.

Main concepts covered:

- Database transactions
- Atomicity
- `session.commit()`
- `session.rollback()`
- `IntegrityError`
- Updating ORM objects
- SQLAlchemy change tracking
- `session.delete()`
- Confirming deletion
- Same-session recovery after rollback
- Transaction failure handling
- Keeping database operations consistent

---

# Database Transactions

A database transaction is a unit of work that contains one or more database operations.

The operations are treated together.

Mental model:

```text
Database operations
       ↓
Transaction
       ↓
All succeed?
   ↙        ↘
 Yes        No
 ↓           ↓
commit()   rollback()
 ↓           ↓
Save       Cancel
```

# Day 34 Completion Checklist

- [x] Understand database transactions
- [x] Understand transaction units of work
- [x] Understand atomicity
- [x] Understand the all-or-nothing rule
- [x] Understand commit vs rollback
- [x] Import `IntegrityError`
- [x] Understand what `IntegrityError` represents
- [x] Understand NOT NULL integrity violations
- [x] Create a transaction practice task
- [x] Use `session.add()`
- [x] Use `session.commit()`
- [x] Use `session.refresh()`
- [x] Correctly use `session.refresh(task)`
- [x] Update an existing ORM object
- [x] Understand SQLAlchemy change tracking
- [x] Update multiple fields
- [x] Commit an update
- [x] Refresh an updated object
- [x] Query updated data in a new Session
- [x] Confirm update persistence
- [x] Understand why `session.add()` is not required again for loaded objects
- [x] Correct ORM query column references
- [x] Use `Task.id` instead of Python's `id`
- [x] Create a dedicated delete-test task
- [x] Store the delete-test task ID
- [x] Query the intended task before deletion
- [x] Use `session.delete()`
- [x] Understand that delete is initially pending
- [x] Commit a deletion
- [x] Query the deleted record again
- [x] Confirm deleted record returns `None`
- [x] Understand why `delete_id` itself does not become `None`
- [x] Deliberately create an invalid ORM object
- [x] Cause an `IntegrityError`
- [x] Catch database failure with `try/except`
- [x] Use `session.rollback()`
- [x] Understand that rollback cancels uncommitted work
- [x] Understand why rollback resets a failed transaction
- [x] Query successfully using the same Session after rollback
- [x] Understand transaction recovery
- [x] Create valid and invalid objects in one transaction
- [x] Use `session.add_all()`
- [x] Complete the atomicity challenge
- [x] Explain why the valid operation is not committed when the transaction fails
- [x] Understand why partial transaction success can be dangerous
- [x] Answer all Day 34 questions
- [x] Review Day 34 implementation
- [x] Correct update errors
- [x] Correct deletion logic
- [x] Correct deletion confirmation
- [x] Correct rollback recovery test
- [x] Complete Day 34 transaction practice

## Day 34 Status

**Completed ✅**
