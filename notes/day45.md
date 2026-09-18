# Day 45 - Database Constraints and Data Integrity with SQLAlchemy

## Overview

Today I learned how to protect the integrity of data stored in a database using database constraints.

In previous lessons, I focused heavily on how data is structured, queried and loaded efficiently.

For example, I have already learned about:

- primary keys
- foreign keys
- SQLAlchemy relationships
- database transactions
- Alembic migrations
- database indexes
- one-to-many relationships
- multi-level relationships
- lazy loading
- eager loading
- the N+1 query problem

Today introduced another important responsibility of a backend system:

Making sure invalid data cannot enter or remain in the database.

A backend application should not only retrieve data correctly and efficiently.

It should also protect the correctness and consistency of the data it stores.

Database constraints provide rules that are enforced directly by the database.

The major concepts covered today were:

- database constraints
- data integrity
- PRIMARY KEY
- FOREIGN KEY
- NOT NULL
- UNIQUE
- CHECK
- SQLAlchemy `CheckConstraint`
- column-level uniqueness
- application validation vs database validation
- defence in depth
- concurrency and uniqueness
- constraint violations
- `IntegrityError`
- transaction rollback after constraint failures
- constraints and Alembic migrations
- existing-data migration safety

The main mental model from today is:

Application Validation

↓

Application Logic

↓

SQLAlchemy

↓

Database Constraints

↓

Valid Stored Data

The database therefore acts as the final layer protecting the integrity of stored information.

---

## What Is a Database Constraint?

A database constraint is a rule enforced by the database that restricts what data is allowed to be stored.

For example, imagine that the application defines Task priority as a number between:

1

and:

5

Without any validation or database constraint, it could theoretically be possible to store:

priority = 100

or:

priority = -10

These values would violate the business rules of the application.

A database constraint allows the database itself to reject such values.

This means the database does not simply accept everything SQLAlchemy sends to it.

The database can enforce its own rules.

---

## Why Data Integrity Matters

Data integrity means maintaining accurate, valid and consistent data.

For example, the system should not contain:

- Tasks with impossible priority values
- Users with duplicate account emails when emails should be unique
- Tasks referencing Projects that do not exist
- required fields containing NULL
- duplicate primary keys

If invalid data enters the database, application behaviour can become unpredictable.

The problem may not appear immediately.

Instead, invalid data may later cause:

- incorrect API responses
- broken relationships
- failed queries
- inconsistent application behaviour
- difficult debugging
- incorrect reports
- security or authorization problems
- migration problems

Therefore, preventing invalid data is generally better than trying to repair it later.

---

## Defence in Depth

One of the important concepts today was defence in depth.

The application can protect data at multiple layers.

Conceptually:

Client

↓

Pydantic Validation

↓

Application / Business Logic

↓

SQLAlchemy

↓

Database Constraints

↓

Database

For example, suppose someone sends:

priority = 100

Pydantic validation could reject the value before it reaches SQLAlchemy.

This is useful because the application can immediately return a clear validation error.

However, the database can also contain:

CHECK priority between 1 and 5

If application validation is accidentally bypassed, the database still protects itself.

This creates multiple layers of protection.

---

## Constraints I Was Already Using

Although UNIQUE and CHECK were the main new constraints today, I realised that I had already been using database constraints throughout the previous lessons.

These include:

PRIMARY KEY

NOT NULL

FOREIGN KEY

For example, defining:

`primary_key=True`

creates primary-key behaviour.

Defining:

`nullable=False`

requires the column to contain a non-NULL value.

Defining:

`ForeignKey("users.id")`

creates a relationship at the database level between a foreign-key column and the referenced table.

Therefore, database constraints were not completely new.

Today I learned to reason about them more deliberately.

---

## PRIMARY KEY

A primary key uniquely identifies a row within a table.

For example:

users.id

projects.id

tasks.id

Each row should have a unique primary-key value.

Conceptually:

Task 1

Task 2

Task 3

can be individually identified using their IDs.

Primary keys are therefore fundamental to relational database design.

They also provide the values referenced by foreign keys.

---

## NOT NULL

The NOT NULL constraint prevents a database column from storing NULL.

In SQLAlchemy, I commonly express this using:

`nullable=False`

For example, a Task title is required.

Therefore:

Task.title

should not contain NULL.

An important distinction I learned today is that:

NULL

and:

an empty string

are not necessarily the same thing.

For example:

NULL

means that no value exists.

While:

""

is still a string value, even though it contains zero characters.

Therefore, NOT NULL protects specifically against NULL.

Application validation may still be required if the business rule says that a string must contain meaningful content.

---

## UNIQUE

The UNIQUE constraint prevents duplicate values from being stored where uniqueness is required.

Today I applied this concept to:

User.email

If email represents the unique identity of a user account, the database should not allow:

Michael
michael@example.com

and:

Sarah
michael@example.com

to coexist if the email must uniquely identify one account.

I updated the SQLAlchemy model so that email is unique.

The important concept is:

UNIQUE(email)

means:

No two permitted rows should contain the same constrained email value according to the database's uniqueness semantics.

This constraint applies specifically to email.

It does not mean that the entire User row must be unique.

For example, two users may still have the same name while having different email addresses.

---

## UNIQUE vs NOT NULL

UNIQUE and NOT NULL solve different problems.

NOT NULL answers:

"Must this column contain a value?"

UNIQUE answers:

"Can this value appear more than once?"

For the User email column, both rules are useful.

The email should exist:

NOT NULL

and should not be duplicated:

UNIQUE

Therefore, multiple constraints can work together to define valid database state.

---

## Why Application-Level Uniqueness Checks Are Not Enough

The application may check whether an email already exists before creating a User.

Conceptually:

Check Email

↓

Email Does Not Exist

↓

Create User

This is useful for application behaviour and user-friendly error messages.

However, application checks alone cannot always guarantee uniqueness.

One important reason is concurrency.

Imagine two requests arrive almost simultaneously.

Request A asks:

Does this email exist?

The answer is:

No.

At almost the same time, Request B asks the same question.

The answer may also be:

No.

Both requests could then attempt to insert the same email.

The database UNIQUE constraint provides the final authority.

Even if both requests attempt the INSERT, the database can prevent the duplicate state.

This taught me an important production database principle:

If something must truly be unique, enforce that requirement in the database.

---

## CHECK Constraints

A CHECK constraint allows the database to verify that a value satisfies a condition.

Today I applied a CHECK constraint to:

Task.priority

The application's priority system allows:

1

2

3

4

5

Therefore, values outside this range should not be stored.

The rule is conceptually:

priority >= 1

AND

priority <= 5

This allows:

priority = 1

priority = 3

priority = 5

but rejects values such as:

priority = 0

priority = -10

priority = 6

priority = 100

This protects the database from invalid Task priority values.

---

## SQLAlchemy CheckConstraint

SQLAlchemy provides:

`CheckConstraint`

for defining table-level CHECK constraints.

The important distinction I corrected today was between:

the SQLAlchemy constraint class

and:

the name of the constraint.

`CheckConstraint`

creates the constraint.

A name such as:

`ck_tasks_priority_range`

identifies the constraint.

Therefore, the mental model is:

CheckConstraint

↓

Type of database rule

`ck_tasks_priority_range`

↓

Name assigned to that rule

This naming becomes useful for:

- debugging
- migrations
- database inspection
- changing constraints
- removing constraints
- understanding database errors

---

## Constraint Naming

Today I also learned a useful database naming pattern.

Common prefixes include:

`pk_`

for primary keys

`fk_`

for foreign keys

`uq_`

for unique constraints

`ck_`

for check constraints

`ix_`

for indexes

For example:

`ck_tasks_priority_range`

clearly communicates:

ck

↓

CHECK constraint

tasks

↓

Task table

priority_range

↓

Rule being enforced

Good database naming becomes increasingly valuable as schemas grow.

---

## Multiple Table Arguments

My Task model already contained a composite index from Day 42.

The index covered:

user_id

and:

completed

Today I needed to add a CHECK constraint without deleting that existing index.

I learned that `__table_args__` can contain multiple table-level database definitions.

Conceptually:

Task.__table_args__

↓

Composite Index

+

CHECK Constraint

This allowed me to preserve the performance work from Day 42 while adding the integrity rule from Day 45.

This reinforces an important principle:

New schema changes should build on previous database design rather than accidentally removing earlier work.

---

## FOREIGN KEY Constraints

Foreign keys protect relationships between database tables.

For example:

Task.project_id

references:

Project.id

Conceptually:

Task

↓

project_id

↓

Existing Project

The foreign-key constraint helps prevent Tasks from referencing nonexistent Projects when the relationship value is present and foreign-key enforcement is active.

This property is called:

referential integrity.

The database protects the relationship between the child and parent records.

---

## Nullable Foreign Keys

My Task.project_id column remains nullable.

This means a Task can exist without belonging to a Project.

Therefore:

project_id = NULL

can be valid.

However, when project_id contains an actual Project ID, that value should reference a valid Project.

This combines:

NULL behaviour

with:

FOREIGN KEY behaviour.

It also connects back to Day 41, where I learned why introducing nullable columns can be safer when existing records do not yet have values for a new relationship.

---

## SQLite Foreign-Key Consideration

Because my current learning database uses SQLite, I learned that SQLite has an important foreign-key enforcement detail.

Foreign-key definitions can exist in the schema, but foreign-key enforcement must be enabled on the SQLite connection for those constraints to actually be enforced.

This means defining a ForeignKey in SQLAlchemy and verifying runtime enforcement are related but distinct concerns.

This is another example of why backend engineers should understand the behaviour of the actual database engine rather than relying only on ORM syntax.

---

## Application Validation vs Database Constraints

One of the most important distinctions today was between application validation and database constraints.

Application validation asks:

"Should the application accept this input?"

Database constraints ask:

"Should this data ever be allowed to exist in the database?"

For example:

priority = 100

Pydantic could reject this before the database is contacted.

This gives the client a clear error response and avoids unnecessary database work.

However, database constraints provide another layer.

If:

- a script accesses the database
- another application uses the database
- validation contains a bug
- application validation is accidentally bypassed
- a developer writes incorrect persistence code

the database still protects its integrity.

Therefore, the two layers complement each other.

---

## Why Database Constraints Do Not Replace Pydantic

Database constraints are powerful, but they do not make application validation unnecessary.

Suppose a client submits:

priority = 100

It is better for the API to recognise the problem immediately and return something understandable such as:

Priority must be between 1 and 5.

Rather than allowing the request to travel through the application until the database rejects it.

Application validation improves:

- API usability
- error messages
- performance
- developer experience
- input handling

Database constraints provide the final guarantee.

Therefore:

Pydantic Validation

↓

Early Protection

Database Constraint

↓

Final Protection

---

## Constraints and Alembic

Today also reinforced a rule that has appeared repeatedly throughout the database section:

Changing the SQLAlchemy model does not automatically change an existing database schema.

Adding:

`unique=True`

to User.email

does not magically add a UNIQUE constraint to an existing `day40.db`.

Likewise, adding:

`CheckConstraint`

to the Task ORM model does not automatically modify the existing Tasks table.

The correct workflow remains:

Change ORM Model

↓

Generate Alembic Migration

↓

Inspect Migration

↓

Check Existing Data

↓

Apply Migration

↓

Verify Database Schema

↓

Test Behaviour

This distinction between:

ORM definition

and:

actual database schema

is now one of the most important concepts in my SQLAlchemy work.

---

## Existing Data and New Constraints

Adding a constraint to a database that already contains data can be dangerous.

For example, suppose Tasks already contain:

priority = 100

Then I introduce:

CHECK priority between 1 and 5

The existing row violates the new rule.

Likewise, suppose Users already contain duplicate email addresses.

Then I attempt to introduce:

UNIQUE(email)

The existing database state conflicts with the new constraint.

Therefore, introducing stricter constraints may require:

Inspect Existing Data

↓

Find Violations

↓

Clean / Resolve Existing Data

↓

Apply Constraint

This directly connects to the migration-safety principles from Day 41.

---

## Alembic Autogenerate Is Not Magic

Today reinforced another Alembic lesson:

Autogenerate should be inspected.

The workflow should not be:

Change Model

↓

Autogenerate

↓

Blindly Upgrade Production Database

Instead:

Change Model

↓

Autogenerate

↓

Read upgrade()

↓

Read downgrade()

↓

Consider Existing Data

↓

Consider Database Engine

↓

Apply When Safe

This becomes especially important for constraints because changing constraints on existing tables may require more complicated migration operations.

---

## SQLite Migration Limitations

SQLite does not support every schema alteration operation in the same way as databases such as PostgreSQL.

Some changes to constraints may require a table-recreation or Alembic batch migration strategy.

Therefore, if Alembic cannot directly apply a constraint change, the correct response is not to randomly delete:

- the database
- migration files
- Alembic history

Instead, I should inspect the generated migration and understand what operation SQLite supports.

This reinforces the principle:

Migration tools automate schema operations.

They do not remove the need for database knowledge.

---

## Testing Valid Data

A constraint should not only reject invalid data.

It should also allow valid data.

Today I tested a Task with:

priority = 4

Since the allowed range is:

1 to 5

the database should accept the Task.

This verifies one side of the constraint:

Valid Input

↓

Constraint Satisfied

↓

INSERT Allowed

This is important because an incorrectly defined constraint could accidentally reject valid data.

---

## Testing Invalid Data

I also tested:

priority = 100

This violates the Task priority CHECK constraint.

The expected flow is:

Create Invalid Task

↓

Add to Session

↓

Attempt Commit

↓

Database Evaluates CHECK

↓

Constraint Fails

↓

Database Rejects Operation

↓

SQLAlchemy Raises IntegrityError

This demonstrates that the database itself is protecting its state.

---

## IntegrityError

SQLAlchemy can raise:

`IntegrityError`

when a database operation violates an integrity constraint.

Examples can include violations involving:

- UNIQUE
- CHECK
- NOT NULL
- FOREIGN KEY

depending on the database and operation.

Instead of allowing the entire application to crash unexpectedly, I can catch the exception and handle the failed transaction appropriately.

This is particularly important when writing production API endpoints.

---

## Why rollback() Matters

If:

`session.commit()`

fails because the database rejects an operation, the transaction has failed.

The Session should then perform:

`session.rollback()`

The rollback does two important things conceptually.

First, it rolls back the failed transaction.

Second, it resets the Session's transactional state so that the Session can continue to be used appropriately.

The mental model is:

Attempt Database Change

↓

Constraint Violation

↓

Commit Fails

↓

IntegrityError

↓

Rollback

↓

Failed Transaction Cleared

This connects directly back to the transaction work from Day 34.

---

## Testing Duplicate Emails

Today I also tested the UNIQUE constraint by attempting to create two Users with the same email.

Conceptually:

Create Sarah

↓

duplicate@example.com

↓

Commit

↓

Success

Then:

Create John

↓

duplicate@example.com

↓

Commit

↓

UNIQUE Constraint Checks Email

↓

Duplicate Found

↓

INSERT Rejected

↓

IntegrityError

↓

Rollback

This verifies that email uniqueness is enforced by the database rather than merely being a rule written in application code.

---

## Session.add() vs Session.add_all()

Today I corrected another SQLAlchemy Session mistake.

`session.add()`

is used when adding one ORM object.

Conceptually:

One Object

↓

`session.add(object)`

When explicitly adding multiple objects:

Multiple Objects

↓

`session.add_all([...])`

For example:

User

Project

Task

can be supplied as a collection to `add_all()`.

SQLAlchemy relationships and default save-update cascade behaviour can also cause connected transient objects to become part of the Session when one related object is added, but `add_all()` can make the intended objects explicit while learning.

---

## commit() Commits the Transaction

Another important correction was understanding what:

`session.commit()`

actually commits.

It does not receive individual ORM objects as arguments.

Instead, the objects are already being tracked by the Session.

The mental model is:

Create Objects

↓

Add Objects to Session

↓

Session Tracks Changes

↓

commit()

↓

Commit Current Transaction

Therefore:

`commit()`

operates on the Session's current transaction.

It does not mean:

"Commit this specific Python object passed as an argument."

---

## Correct Session Construction

I also reinforced the distinction between:

`Session`

and:

`Session(engine)`

`Session`

is the Session class.

`Session(engine)`

creates an actual Session bound to the database engine.

Therefore:

Session

↓

Class / Blueprint

while:

Session(engine)

↓

Actual Session Used for Database Work

This is a Python and SQLAlchemy distinction I need to keep consistent going forward.

---

## Constraint Failure Does Not Mean the Constraint Is Bad

A failed INSERT caused by a constraint is sometimes exactly the desired behaviour.

For example:

priority = 100

↓

Database rejects it

That failure means:

The protection worked.

Therefore, not every database error represents a broken database.

Sometimes an error is the database correctly refusing to enter an invalid state.

The application then has the responsibility to handle that rejection properly.

---

## Database Constraints as Invariants

A useful way to think about constraints is as database invariants.

An invariant is something that should remain true regardless of which application code performs the operation.

For this system:

User email uniqueness should remain true.

Task priority between 1 and 5 should remain true.

Task title being non-NULL should remain true.

Valid foreign-key relationships should remain true when enforced.

This means the database has rules describing valid state.

Application code operates inside those rules.

---

## Final Challenge Review

Today's final challenge connected business rules to database mechanisms.

### User email must be unique

Mechanism:

UNIQUE

Purpose:

Prevent duplicate email values.

---

### Task priority must be between 1 and 5

Mechanism:

CHECK

Purpose:

Reject priority values outside the permitted range.

---

### Task title must exist

Mechanism:

NOT NULL

Purpose:

Prevent NULL titles from being stored.

Additional application validation may still be required if empty strings or whitespace-only titles should also be rejected.

---

### Task.project_id must reference an existing Project when present

Mechanism:

FOREIGN KEY

Purpose:

Protect referential integrity between Tasks and Projects when foreign-key enforcement is active.

---

## Mistakes I Corrected Today

### Mistake 1 - Duplicate Model Definitions

My original file accidentally contained repeated definitions for:

- engine
- Base
- User
- Project
- Task fields

I removed the duplicates and restored a clean file structure.

A model should have one clear definition.

---

### Mistake 2 - Missing CheckConstraint Import

I attempted to create a CHECK constraint without importing SQLAlchemy's:

`CheckConstraint`

I corrected the import and used the proper SQLAlchemy construct.

---

### Mistake 3 - Confusing Constraint Name With Constraint Type

I initially attempted to call:

`ck_tasks_priority_range`

as though it were a function.

I corrected my understanding.

`CheckConstraint`

is the SQLAlchemy construct.

`ck_tasks_priority_range`

is simply the name assigned to the resulting database constraint.

---

### Mistake 4 - Incorrect Session Usage

I initially used:

`Session`

directly in the context manager.

I corrected this to create a Session connected to the engine.

The correct mental model is:

Session

↓

Class

Session(engine)

↓

Instance

---

### Mistake 5 - Incorrect add() Usage

I attempted to pass multiple objects directly into `session.add()`.

I corrected this by understanding:

One Object

↓

add()

Multiple Explicit Objects

↓

add_all()

---

### Mistake 6 - Passing Objects to commit()

I attempted to provide ORM objects as arguments to:

`commit()`

I corrected this because commit operates on the current Session transaction.

The Session already knows which objects are pending.

---

### Mistake 7 - Missing IntegrityError Handling

My original invalid Task test attempted to commit the bad data without catching the expected database exception.

I corrected this using:

IntegrityError

and:

rollback()

This allows the application to handle the database rejection deliberately.

---

### Mistake 8 - Missing Valid Constraint Test

I initially only attempted invalid data.

I added a valid priority test to confirm that the constraint accepts legitimate values.

A useful constraint test should verify both:

Valid Data Accepted

and:

Invalid Data Rejected

---

### Mistake 9 - Missing Duplicate Email Test

Although I correctly added email uniqueness to the ORM model, I initially did not verify the behaviour.

I added a test that attempts to insert two Users with the same email.

This proves whether the actual database schema is enforcing uniqueness.

---

### Mistake 10 - UNIQUE Does Not Prevent All Duplicate Data

I initially described UNIQUE as preventing duplicated data from entering the database.

I corrected this to be more precise.

A UNIQUE constraint on:

User.email

specifically prevents duplicate values for that constrained email column.

It does not automatically prevent duplicate values in unrelated columns such as User.name.

---

### Mistake 11 - NOT NULL vs Empty Values

I initially described NOT NULL as preventing empty values.

I corrected this distinction.

NOT NULL prevents:

NULL

It does not necessarily prevent:

""

Application validation may be required to enforce meaningful non-empty strings.

---

## Important Mental Models

### Database Constraint

Rule

↓

Enforced by Database

↓

Invalid State Rejected

---

### Defence in Depth

Client

↓

Pydantic Validation

↓

Business Logic

↓

SQLAlchemy

↓

Database Constraints

↓

Stored Data

---

### UNIQUE

Value Already Exists

↓

Attempt Duplicate

↓

Database Rejects Duplicate

---

### CHECK

Incoming Value

↓

Evaluate Condition

↓

True → Allow

False → Reject

---

### NOT NULL

Value Is NULL

↓

Reject

---

### FOREIGN KEY

Child Reference

↓

Referenced Parent Must Exist

↓

Protect Relationship

---

### Constraint Violation

INSERT / UPDATE

↓

Constraint Evaluated

↓

Violation

↓

Database Rejects Operation

↓

IntegrityError

↓

Rollback

---

### ORM Schema Change

Change Python Model

↓

Does NOT Automatically Change Existing Database

↓

Generate Migration

↓

Inspect

↓

Apply

↓

Verify

---

### Safe Constraint Migration

New Constraint

↓

Inspect Existing Data

↓

Resolve Violations

↓

Generate / Inspect Migration

↓

Apply Constraint

↓

Verify

---

### Session

Session

↓

Class

Session(engine)

↓

Database Session Instance

---

### Adding Objects

One Object

↓

session.add()

Multiple Objects

↓

session.add_all([...])

---

### Commit

Objects Tracked by Session

↓

session.commit()

↓

Commit Transaction

---

## Progress From Day 44 to Day 45

Day 44 focused on database performance through relationship loading.

I learned:

Lazy Loading

↓

Potential N+1

↓

Eager Loading

↓

More Deliberate Query Strategy

Today focused on database correctness.

The progression is:

Day 44:

"How efficiently am I retrieving related data?"

Day 45:

"How do I guarantee that the stored data remains valid?"

These are two different responsibilities of a production backend.

A system can have perfectly valid data while performing terribly.

A system can also perform extremely quickly while storing corrupted or inconsistent data.

A strong backend needs both:

Performance

and:

Integrity

---

## Broader Database Progression

The recent database lessons now connect together:

Day 32

↓

SQLAlchemy ORM Fundamentals

Day 33

↓

Sessions, INSERT and SELECT

Day 34

↓

Transactions, Updates, Deletes and Rollbacks

Day 35

↓

Database-Backed FastAPI

Day 36

↓

Database-Backed PATCH and DELETE

Day 37

↓

Relationship Fundamentals

Day 38

↓

Creating Related Objects

Day 39

↓

Relationship Queries and JOINs

Day 40

↓

Alembic Migrations

Day 41

↓

Migration Safety

Day 42

↓

Indexes and Query Performance

Day 43

↓

Projects and Multi-Level Relationships

Day 44

↓

Relationship Loading and N+1 Queries

Day 45

↓

Constraints and Data Integrity

The database section is therefore progressing from simply:

"How do I store data?"

toward:

"How do I design, evolve, protect and efficiently access production data?"

---

## Completion Checklist

### Constraint Fundamentals

- [x] Understood database constraints
- [x] Understood data integrity
- [x] Reviewed PRIMARY KEY
- [x] Reviewed NOT NULL
- [x] Reviewed FOREIGN KEY
- [x] Learned UNIQUE
- [x] Learned CHECK

### User Email Constraint

- [x] Added uniqueness to User.email
- [x] Understood what email uniqueness protects
- [x] Understood concurrency concerns
- [x] Understood why application checks alone are insufficient
- [x] Tested duplicate email behaviour

### Task Priority Constraint

- [x] Imported CheckConstraint
- [x] Added priority range CHECK
- [x] Named the constraint
- [x] Preserved the existing composite index
- [x] Tested a valid priority
- [x] Tested an invalid priority

### Error Handling

- [x] Imported IntegrityError
- [x] Caught constraint violations
- [x] Used session.rollback()
- [x] Understood failed transaction state
- [x] Understood why rollback is required

### SQLAlchemy Session Usage

- [x] Corrected Session construction
- [x] Reinforced session.add()
- [x] Learned session.add_all()
- [x] Reinforced session.commit()
- [x] Understood that commit operates on the transaction

### Validation

- [x] Understood application validation
- [x] Understood database validation
- [x] Compared Pydantic and constraints
- [x] Understood defence in depth
- [x] Understood why both layers are useful

### Alembic

- [x] Understood that ORM changes do not automatically modify the existing database
- [x] Connected constraints to migrations
- [x] Understood existing-data migration risks
- [x] Understood the need to inspect generated migrations
- [x] Considered SQLite migration limitations

### Corrections

- [x] Removed duplicate model definitions
- [x] Corrected CheckConstraint usage
- [x] Corrected constraint naming
- [x] Corrected Session usage
- [x] Corrected add() usage
- [x] Corrected commit() usage
- [x] Added IntegrityError handling
- [x] Added valid-data testing
- [x] Added invalid-data testing
- [x] Added duplicate-email testing
- [x] Corrected UNIQUE explanation
- [x] Corrected NOT NULL explanation
- [x] Completed Day 45 Q&A

---

## Overall Review

Day 45 introduced database constraints as another major layer of production backend engineering.

Previously, much of my database work focused on how data is created, queried, related, migrated and loaded.

Today I focused on determining what database states should be considered valid in the first place.

The database should not simply be treated as passive storage.

It should actively enforce important rules about its own data.

I learned that application validation and database constraints have different responsibilities.

Application validation provides early feedback and protects the application boundary.

Database constraints protect the final stored state.

Together they create defence in depth.

I also connected today's lesson to several previous days.

The `IntegrityError` and rollback behaviour connected back to transaction management.

Adding constraints connected back to Alembic migrations and migration safety.

Foreign keys connected back to relationships.

The existing composite index connected back to performance optimisation.

This shows that database concepts are not isolated topics.

They interact with one another.

A production backend must think about:

Schema Design

↓

Relationships

↓

Transactions

↓

Migrations

↓

Indexes

↓

Query Loading

↓

Constraints

↓

Data Integrity

Today's practical mistakes were mostly SQLAlchemy API and code-structure mistakes rather than a complete misunderstanding of database constraints.

The important corrections were:

Use `CheckConstraint` to define the CHECK rule.

Use a name such as `ck_tasks_priority_range` to identify that constraint.

Use `Session(engine)` to create a Session.

Use `add()` for one object or `add_all()` for multiple explicit objects.

Use `commit()` to commit the transaction.

Catch `IntegrityError` when the database rejects invalid data.

Call `rollback()` after the failed transaction.

Most importantly, I learned that:

Changing an ORM model is not proof that the actual database is protected.

The real proof is:

Define Constraint

↓

Generate Migration

↓

Inspect Migration

↓

Apply Migration

↓

Attempt Valid Data

↓

Accepted

↓

Attempt Invalid Data

↓

Rejected

That completes the full lifecycle from application model definition to actual database integrity enforcement.

**Day 45: Completed after corrections**