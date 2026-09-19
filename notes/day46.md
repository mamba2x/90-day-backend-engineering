# Day 46 - Database Integration Checkpoint

## Overview

Today was a database integration checkpoint.

Instead of introducing another isolated SQLAlchemy feature, I combined the major concepts from the previous database lessons into one complete exercise.

The purpose was to determine whether I could work with:

- SQLAlchemy ORM models
- primary keys
- foreign keys
- one-to-many relationships
- multi-level relationships
- Session management
- transactions
- SELECT queries
- filtering
- JOINs
- relationship traversal
- lazy loading
- eager loading
- the N+1 query problem
- indexes
- database constraints
- IntegrityError
- rollback
- transaction atomicity
- Alembic migrations
- schema evolution

The database now represents a small but realistic backend domain containing:

User

↓

Projects

↓

Tasks

A User can own multiple Projects.

A Project can contain multiple Tasks.

Tasks are also directly associated with Users in the current schema.

The checkpoint helped expose not only what I understand but also the SQLAlchemy patterns that I still need to practise.

---

# Final Database Structure

The system currently contains three main entities:

- User
- Project
- Task

The relationship structure is:

User

↓

One-to-Many

↓

Projects

and:

Project

↓

One-to-Many

↓

Tasks

The database also currently contains a direct relationship between:

User

and:

Task

through `tasks.user_id`.

Conceptually:

User
│
├── Projects
│      │
│      └── Tasks
│
└── Tasks

The important foreign-key paths are:

projects.user_id

↓

users.id

and:

tasks.project_id

↓

projects.id

There is also:

tasks.user_id

↓

users.id

---

# User Model

The User model represents an application user.

Important fields include:

`id`

The primary key that uniquely identifies the User.

`name`

The User's name.

`email`

The User's email address.

The email column is:

- NOT NULL
- UNIQUE

This means every User must have an email and duplicate email values are rejected by the database.

The User model also contains ORM relationships for:

`tasks`

and:

`projects`

These allow navigation from a User ORM object to the related Task and Project objects.

For example:

user.projects

returns the Projects associated with that User.

---

# Project Model

The Project model represents a collection of Tasks owned by a User.

Important fields include:

`id`

Primary key.

`name`

The Project's name.

`user_id`

Foreign key referencing:

users.id

This identifies the User that owns the Project.

The Project model contains:

`user`

which allows navigation from a Project to its User.

It also contains:

`tasks`

which allows navigation from a Project to its Tasks.

Conceptually:

project.user_id

is the database-level relationship.

While:

project.user

is the ORM-level navigation property.

---

# Task Model

The Task model contains the most database features because it has evolved throughout several lessons.

Important fields include:

- id
- title
- completed
- priority
- description
- due_date
- user_id
- project_id

The model contains relationships to:

- User
- Project

It also contains indexes and constraints.

This means the Task model demonstrates several important relational database concepts at once.

---

# Primary Keys

Each major table contains a primary key:

users.id

projects.id

tasks.id

A primary key uniquely identifies each row.

Primary keys also provide the values that foreign keys can reference.

For example:

projects.user_id

references:

users.id

Therefore, primary keys form the identity foundation of the relational model.

---

# Foreign Keys

Foreign keys create relationships between database tables.

The current schema contains:

projects.user_id

↓

users.id

This means each Project belongs to a User.

The schema also contains:

tasks.project_id

↓

projects.id

This means a Task can belong to a Project.

Finally:

tasks.user_id

↓

users.id

creates the direct relationship between a Task and User.

Foreign keys provide database-level relationships and help maintain referential integrity when enforcement is active.

---

# Foreign Keys vs ORM Relationships

One of the most important distinctions reinforced during the checkpoint was the difference between:

foreign-key columns

and:

SQLAlchemy relationships.

For example:

project.user_id

contains an integer representing the related User's primary key.

Conceptually:

project.user_id = 4

However:

project.user

represents the related User ORM object.

Conceptually:

project.user

↓

<User Michael>

Therefore:

Foreign Key

↓

Database relationship

while:

relationship()

↓

Python ORM navigation

They work together but serve different purposes.

---

# Creating an Object Graph

The checkpoint required creating multiple related objects.

The dataset included:

Michael

with:

- Backend Engineering
- API Project

and Sarah with:

- DevOps Project

The Projects contained Tasks.

Michael's Backend Engineering Project contained:

- Study SQLAlchemy
- Practice Alembic

Michael's API Project contained:

- Build Authentication
- Add Rate Limiting

Sarah's DevOps Project contained:

- Learn Docker
- Study CI/CD

Instead of manually assigning foreign-key IDs, I created relationships using ORM objects.

Conceptually:

Create Michael

↓

Create Backend Project

↓

Set project.user = Michael

↓

Create Task

↓

Set task.user = Michael

↓

Set task.project = Backend Project

This demonstrates one of the major advantages of using an ORM.

I can work naturally with Python objects while SQLAlchemy manages the corresponding foreign-key relationships.

---

# Relationship Cascades During Persistence

Because the Users, Projects and Tasks were connected through SQLAlchemy relationships, adding the parent objects to the Session allowed the connected object graph to become part of the Session through SQLAlchemy's normal relationship cascade behaviour.

Conceptually:

Michael

↓

Backend Project

↓

Study SQLAlchemy

If these transient ORM objects are correctly connected, adding Michael can also cause related objects to be added to the Session.

This is why it was possible to add the Users and commit the connected object graph.

However, I still need to understand which cascade behaviours are configured rather than assuming every relationship operation will always behave identically.

---

# Session Management

One of the main patterns reinforced today was proper Session creation.

The correct pattern is:

Session(engine)

This creates an actual SQLAlchemy Session connected to the database engine.

The important distinction is:

Session

↓

Class

while:

Session(engine)

↓

Session instance

Therefore, database work should use a real Session instance.

This is a recurring concept I need to make automatic.

---

# Session.add() and Session.add_all()

`session.add()` is useful when explicitly adding one ORM object.

`session.add_all()` can be used when explicitly adding multiple ORM objects.

For example:

Multiple Users

↓

add_all()

The objects then become tracked by the Session.

The Session manages pending database changes until the transaction is committed or rolled back.

---

# commit()

`session.commit()` commits the current transaction.

It does not receive individual ORM objects as arguments.

The mental model is:

Create Objects

↓

Add Objects to Session

↓

Session Tracks Changes

↓

commit()

↓

Persist Transaction

This distinction was reinforced because previous exercises exposed confusion between adding objects and committing transactions.

---

# SELECT Queries

The checkpoint required retrieving data using SQLAlchemy's `select()` function.

For example, to retrieve Projects belonging to a specific User, the query conceptually becomes:

SELECT Project

WHERE

Project.user_id equals User ID

This demonstrates that ORM querying still reflects relational database logic.

The Python syntax is different from raw SQL, but the underlying concepts remain:

SELECT

WHERE

JOIN

FILTER

ORDER

RELATIONSHIPS

---

# scalar() vs scalars()

One of the most important corrections from today's checkpoint was understanding:

`session.scalar()`

versus:

`session.scalars()`.

This is currently one of the SQLAlchemy concepts I need to practise until it becomes automatic.

---

## scalar()

`scalar()` is appropriate when I expect one scalar ORM result.

Conceptually:

Query

↓

One User

↓

scalar()

For example:

Find Michael by unique email.

Because the email is unique, the query should return at most one User.

---

## scalars()

`scalars()` is used when the query can return multiple scalar ORM objects.

For example:

Retrieve all Projects belonging to Michael.

Conceptually:

Query

↓

Project A

Project B

Project C

↓

scalars()

↓

all()

Therefore:

One expected object

↓

scalar()

Multiple expected objects

↓

scalars().all()

This distinction is important because attempting:

scalar(...).all()

mixes two incompatible expectations.

---

# ORM Attribute Awareness

The checkpoint also reinforced the importance of knowing which attributes belong to which model.

For example:

Project

contains:

name

while:

Task

contains:

title

Therefore:

project.name

is valid.

But:

project.title

is not part of the current Project model.

As database models grow, I need to remain aware of the domain represented by each ORM class.

---

# Querying by IDs

After creating data, IDs can be captured and used in later queries.

For example:

Michael's ID

can be used to retrieve:

Projects where Project.user_id equals Michael's ID.

Similarly:

Backend Engineering's Project ID

can be used to retrieve:

Tasks where Task.project_id equals the Backend Engineering Project ID.

IDs provide reliable relational identifiers.

---

# JOIN Queries

The checkpoint required retrieving Sarah's Tasks using explicit JOINs.

The relationship path is:

Task

↓

Project

↓

User

Conceptually:

Start with Tasks

↓

JOIN Project

↓

JOIN User

↓

Filter User

This demonstrates that SQLAlchemy relationships can be used when constructing relational JOIN queries.

The important distinction remains:

JOIN

is used to construct query logic.

It should not be confused with relationship loading strategies such as `joinedload()`.

---

# Filtering

The checkpoint required retrieving Tasks where:

priority >= 4

This demonstrated basic filtering using SQLAlchemy.

It also required combining multiple conditions.

For example:

Michael's Tasks

AND

priority >= 4

This becomes conceptually:

Task.user_id == Michael's ID

AND

Task.priority >= 4

Combining filters is fundamental for real API endpoints.

---

# Relationship Traversal

SQLAlchemy relationships allow related objects to be accessed directly.

For example:

Michael

↓

michael.projects

↓

project.tasks

This allows code to traverse:

User

↓

Project

↓

Task

without manually querying each foreign-key value.

For example, the application can conceptually print:

User: Michael

Project: Backend Engineering

Task: Study SQLAlchemy

Task: Practice Alembic

Project: API Project

Task: Build Authentication

Task: Add Rate Limiting

This is convenient, but it introduces an important performance consideration.

Relationship access may trigger additional SQL queries depending on the loading strategy.

---

# Lazy Loading

With lazy loading, related data may not be retrieved until the relationship is accessed.

For example:

Retrieve Michael

↓

Access michael.projects

↓

SQLAlchemy may execute another query

Then:

Access project.tasks

↓

SQLAlchemy may execute additional queries

Lazy loading can be convenient, but repeated relationship access can lead to inefficient query behaviour.

---

# The N+1 Query Problem

The N+1 problem occurs when retrieving a collection of parent objects causes an additional relationship query for each parent.

Conceptually:

1 query

↓

Retrieve Projects

Then:

Project 1

↓

Query Tasks

Project 2

↓

Query Tasks

Project 3

↓

Query Tasks

If there are N Projects, this pattern can become approximately:

1 + N queries

This can become expensive as the dataset grows.

---

# selectinload()

`selectinload()` is an eager-loading strategy.

It can deliberately load related collections in additional batched queries rather than repeatedly querying relationships for each parent.

For the multi-level relationship:

User

↓

Projects

↓

Tasks

the intended loading path can be configured as:

User.projects

↓

Project.tasks

This tells SQLAlchemy that these relationships will be needed.

Conceptually:

Retrieve User

↓

Load Projects deliberately

↓

Load Tasks for those Projects deliberately

This helps avoid accidental N+1 behaviour.

---

# Query Correctness vs Query Performance

One of the important lessons from relationship loading is that:

Correct output

does not automatically mean:

Efficient database access.

A program may correctly print every Project and Task while executing far more SQL queries than necessary.

Therefore, backend engineers must think about:

"What data did I retrieve?"

and:

"How did I retrieve it?"

Using:

echo=True

allows SQLAlchemy-generated SQL to be inspected during development.

---

# Indexes

The schema contains indexes from previous lessons.

For example:

user_id

and:

project_id

are indexed.

There is also a composite index involving:

user_id

and:

completed.

Indexes primarily help database query performance.

They can help the database locate rows more efficiently for suitable query patterns.

However, indexes have costs.

They require:

- additional storage
- maintenance during writes

Therefore, indexes should be based on actual query patterns rather than being added to every column.

---

# Index vs Constraint

The checkpoint reinforced that indexes and constraints have different primary responsibilities.

Index

↓

Performance

Constraint

↓

Data integrity

For example:

An index may help retrieve Tasks belonging to a User.

A CHECK constraint prevents invalid priority values.

A UNIQUE constraint prevents duplicate email values.

A FOREIGN KEY protects relationships.

A NOT NULL constraint prevents NULL values.

These are different responsibilities.

Some database implementations may use indexes internally for certain constraints, but conceptually the purposes remain different.

---

# CHECK Constraint

Task priority is constrained to:

1 through 5.

The rule is:

priority >= 1

AND

priority <= 5

This means values such as:

1

3

5

are valid.

Values such as:

0

6

20

99

are invalid.

The database therefore protects the valid Task priority range even if application-level validation is bypassed.

---

# UNIQUE Constraint

User.email is unique.

This prevents two Users from storing the same email address.

For example:

Michael

michael46@example.com

can exist.

Attempting to create another User with:

michael46@example.com

should cause the database to reject the operation.

This demonstrates that uniqueness is enforced at the database level.

---

# IntegrityError

When a database integrity rule is violated, SQLAlchemy may raise:

IntegrityError

For example:

Duplicate Email

↓

UNIQUE violation

↓

IntegrityError

or:

priority = 20

↓

CHECK violation

↓

IntegrityError

The application can catch this exception and handle the failure.

---

# rollback()

After an integrity failure, the transaction must be rolled back.

Conceptually:

Attempt Commit

↓

Constraint Violation

↓

IntegrityError

↓

Transaction Failed

↓

rollback()

↓

Failed Transaction Cleared

This restores the Session's transactional state so that it can continue to be used appropriately.

This directly connects the constraint lessons with the earlier transaction lessons.

---

# Transaction Atomicity

One of the most important integration exercises today combined:

transactions

with:

database constraints.

The test attempted to insert:

one valid Task

and:

one invalid Task

inside the same transaction.

For example:

Task A

priority = 3

Valid

Task B

priority = 99

Invalid

When the database rejects Task B, the transaction fails.

After rollback, Task A should not remain persisted either.

Conceptually:

Transaction

├── Valid INSERT
└── Invalid INSERT

↓

Constraint Violation

↓

Transaction Failure

↓

Rollback

↓

Neither INSERT Persists

This demonstrates the Atomicity property of ACID.

---

# ACID Atomicity

Atomicity means that a transaction behaves as one logical unit.

Either:

all operations succeed

or:

the transaction does not commit.

This prevents partially completed operations.

For example, imagine transferring money.

It would be dangerous if:

Money removed from Account A

succeeds

but:

Money added to Account B

fails.

Transactions allow related operations to succeed or fail together.

The Task example is smaller, but it demonstrates the same principle.

---

# Alembic Migration Checkpoint

The database schema has evolved over several lessons.

The important concept is that the database did not appear in its current form instantly.

It evolved through migrations.

Conceptually:

Initial Schema

↓

Add Fields

↓

Add Relationships

↓

Add Indexes

↓

Add Projects

↓

Add Constraints

↓

Current Schema

Alembic records this schema evolution.

---

# alembic current

The command:

`alembic current`

shows the migration revision currently applied to the database.

Conceptually:

Database

↓

"What migration state are you currently using?"

↓

Current Revision

This helps determine whether the database is up to date.

---

# alembic history

The command:

`alembic history`

shows the migration revision chain.

This allows the developer to inspect how the schema evolved.

Each migration should connect to another through revision identifiers.

Conceptually:

Revision A

↓

Revision B

↓

Revision C

↓

Revision D

↓

HEAD

The migration chain should represent intentional schema evolution.

---

# ORM Models vs Actual Database Schema

One of the most important concepts from the entire database section is:

Changing Python ORM code does not automatically change an existing database.

For example:

Add UNIQUE to User.email

in Python.

That changes the model definition.

It does not automatically modify the existing physical database table.

The proper workflow is:

Modify ORM Model

↓

Generate Migration

↓

Inspect Migration

↓

Apply Migration

↓

Database Schema Changes

This distinction is fundamental when working with production databases.

---

# Existing Data and Migration Safety

Adding stricter constraints to a populated database can fail if existing rows violate those rules.

For example:

Existing priority = 100

Then add:

CHECK priority between 1 and 5

The existing row violates the new rule.

Similarly:

Duplicate Emails Already Exist

↓

Add UNIQUE(email)

↓

Migration Problem

Therefore, safe schema evolution may require:

Inspect Existing Data

↓

Clean Invalid Data

↓

Apply Migration

This is why database migrations require more thought than simply generating files automatically.

---

# Current Schema Explanation

## users.id

Table:

users

Type:

Primary Key

Purpose:

Uniquely identifies each User.

It can be referenced by foreign keys in other tables.

---

## projects.user_id

Table:

projects

Type:

Foreign Key

References:

users.id

Purpose:

Identifies which User owns the Project.

Relationship:

User

↓

Projects

---

## tasks.user_id

Table:

tasks

Type:

Foreign Key

References:

users.id

Purpose:

Directly associates a Task with a User in the current schema.

---

## tasks.project_id

Table:

tasks

Type:

Nullable Foreign Key

References:

projects.id

Purpose:

Identifies which Project a Task belongs to.

Because it is nullable, a Task can currently exist without belonging to a Project.

---

# User → Project → Task Relationship Path

The first relationship is:

User

↓

Project

This is implemented using:

projects.user_id

↓

users.id

The second relationship is:

Project

↓

Task

This is implemented using:

tasks.project_id

↓

projects.id

Therefore:

User

↓

Project

↓

Task

is possible because of the foreign-key chain:

users.id

↑

projects.user_id

and:

projects.id

↑

tasks.project_id

SQLAlchemy relationships then provide the object-oriented navigation:

user.projects

↓

project.tasks

---

# Important Corrections From My Checkpoint Attempt

The checkpoint exposed several recurring mistakes that I need to eliminate.

---

## Mistake 1 - Missing select Import

I used:

select()

without importing it.

I corrected this by importing `select` from SQLAlchemy.

This was a simple import mistake, but it would prevent the program from running.

---

## Mistake 2 - scalar() vs scalars()

I initially attempted patterns such as:

scalar(...).all()

This was incorrect.

I reinforced:

scalar()

for one expected ORM result.

scalars().all()

for multiple ORM results.

This is one of my main SQLAlchemy areas to practise.

---

## Mistake 3 - Project.name vs Project.title

I attempted to access:

project.title

even though the Project model defines:

name

The Task model contains:

title.

This reinforced the importance of understanding the attributes belonging to each ORM model.

---

## Mistake 4 - Session vs Session(engine)

I again accidentally used:

Session

instead of creating a Session instance bound to the engine.

The correct mental model is:

Session

↓

Class

Session(engine)

↓

Database Session

This needs to become automatic.

---

## Mistake 5 - Query Indentation

I accidentally placed one query inside a previous Task loop.

This would cause the query to execute repeatedly.

This was primarily a Python control-flow issue rather than a SQLAlchemy concept issue.

The correction reinforced that query execution should occur at the intended structural level.

---

## Mistake 6 - Case-Sensitive Data Expectations

I created:

Sarah

but queried:

sarah

It is better not to rely on database-specific collation or case behaviour when exact matching is intended.

Using reliable identifiers such as IDs or unique emails is often preferable.

---

## Mistake 7 - Capturing IDs Clearly

I learned that when IDs will be needed outside a Session block, it is clearer to capture the primitive ID values while working with the active Session.

For example:

michael_id

backend_project_id

These integers can then safely be used in later queries without relying on ORM objects that are no longer associated with the same active Session.

---

# Areas I Performed Well In

The checkpoint also showed clear improvement.

I successfully understood and attempted:

- model definitions
- primary keys
- foreign keys
- relationships
- object graph creation
- assigning relationships using ORM objects
- Session persistence
- filtering
- JOIN structure
- priority queries
- multiple WHERE conditions
- database constraints

My main remaining weaknesses were more specific:

- Session syntax
- scalar vs scalars
- model attribute awareness
- loop indentation
- result handling

This is useful because the weaknesses are becoming narrower rather than being broad misunderstandings of relational databases.

---

# Key Mental Models

## Session

Session

↓

Class

Session(engine)

↓

Usable database Session

---

## Query Result

One Object Expected

↓

scalar()

Multiple Objects Expected

↓

scalars().all()

---

## Foreign Key vs Relationship

project.user_id

↓

Stored database ID

project.user

↓

Related Python ORM object

---

## Relationship Path

User

↓

projects.user_id

↓

Project

↓

tasks.project_id

↓

Task

---

## Constraint

Database Rule

↓

Invalid Data Attempted

↓

Database Rejects It

---

## IntegrityError

Constraint Violation

↓

IntegrityError

↓

rollback()

---

## Atomic Transaction

Multiple Operations

↓

One Fails

↓

Transaction Fails

↓

Rollback

↓

None Commit

---

## ORM Change

Change Python Model

↓

Database Does Not Automatically Change

↓

Alembic Migration Required

---

## Index

Query Pattern

↓

Potential Faster Lookup

---

## selectinload()

Parent Objects

↓

Related Collections Needed

↓

Load Relationships Deliberately

↓

Avoid Repeated Per-Parent Lazy Queries

---

# Day 46 Q&A Review

## 1. Foreign Key Column vs ORM Relationship

A foreign-key column such as:

project.user_id

contains the database identifier of the related User.

An ORM relationship such as:

project.user

provides the related User object.

Foreign key:

Database relationship.

ORM relationship:

Python object navigation.

---

## 2. Why ORM Changes Do Not Automatically Change Existing Databases

SQLAlchemy model definitions describe the application's expected schema.

An existing database already has a physical schema.

Changing the Python class does not automatically alter existing tables.

Alembic migrations are used to deliberately evolve the schema.

---

## 3. What Problem Does selectinload() Help Prevent?

`selectinload()` helps prevent N+1-style query behaviour when related collections are needed.

Instead of executing a relationship query for every parent object, SQLAlchemy can load related collections in batched secondary queries.

---

## 4. Index vs Constraint

An index primarily improves query performance.

A constraint primarily protects data integrity.

Examples of constraints include:

- UNIQUE
- CHECK
- NOT NULL
- FOREIGN KEY

---

## 5. Why rollback() After IntegrityError?

An integrity failure causes the current transaction to fail.

`rollback()` rolls back the failed transaction and resets the Session's transactional state.

---

## 6. Valid and Invalid INSERT in One Transaction

If both operations belong to the same transaction and one violates a constraint, the transaction should fail.

The valid INSERT should also be rolled back.

This demonstrates atomicity.

---

## 7. Why Clean Existing Data Before Adding Constraints?

Existing rows may already violate the new rule.

For example:

duplicate emails

invalid priorities

NULL values

These problems may need to be resolved before stricter constraints can safely be introduced.

---

## 8. User → Project → Task

User to Project is created by:

projects.user_id

referencing:

users.id

Project to Task is created by:

tasks.project_id

referencing:

projects.id

Together they form:

User

↓

Project

↓

Task

---

# Database Section Progress

The recent lessons have built on each other:

Day 32

↓

SQLAlchemy ORM Fundamentals

Day 33

↓

Sessions, INSERT, Commit, Refresh and SELECT

Day 34

↓

Transactions, Rollback, Update and Delete

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

Migration Workflow and Data Safety

Day 42

↓

Indexes and Query Performance

Day 43

↓

Projects and Multi-Level Relationships

Day 44

↓

Relationship Loading, N+1 and Eager Loading

Day 45

↓

Database Constraints and Data Integrity

Day 46

↓

Database Integration Checkpoint

The progression has moved from:

"How do I use SQLAlchemy?"

toward:

"How do I design and operate a relational persistence layer?"

---

# Completion Checklist

## Database Models

- [x] User model
- [x] Project model
- [x] Task model
- [x] Primary keys
- [x] Foreign keys
- [x] Nullable relationships
- [x] ORM relationships

## Dataset

- [x] Created multiple Users
- [x] Created multiple Projects
- [x] Created multiple Tasks
- [x] Connected objects through ORM relationships
- [x] Persisted connected object graph

## Queries

- [x] Queried Projects by User
- [x] Queried Tasks by Project
- [x] Used explicit JOINs
- [x] Filtered by priority
- [x] Combined multiple WHERE conditions
- [x] Reinforced scalar()
- [x] Reinforced scalars().all()

## Relationships

- [x] Traversed User → Projects
- [x] Traversed Project → Tasks
- [x] Understood FK vs relationship()
- [x] Understood multi-level relationships

## Performance

- [x] Reviewed indexes
- [x] Reviewed N+1 problem
- [x] Used selectinload()
- [x] Understood eager loading
- [x] Used echo=True to observe SQL

## Data Integrity

- [x] UNIQUE email
- [x] CHECK priority
- [x] NOT NULL fields
- [x] FOREIGN KEY relationships
- [x] Tested invalid priority
- [x] Tested duplicate email
- [x] Handled IntegrityError
- [x] Used rollback()

## Transactions

- [x] Tested multiple operations in one transaction
- [x] Triggered transaction failure
- [x] Rolled back transaction
- [x] Verified valid operation was also rolled back
- [x] Reinforced ACID atomicity

## Migrations

- [x] Reviewed migration chain
- [x] Understood alembic current
- [x] Understood alembic history
- [x] Reinforced ORM model vs physical schema
- [x] Reinforced migration safety

## Corrections

- [x] Corrected missing select import
- [x] Corrected scalar vs scalars
- [x] Corrected Project.name vs Project.title
- [x] Reinforced Session(engine)
- [x] Corrected query indentation
- [x] Improved identifier usage
- [x] Reinforced capturing primitive IDs when useful

## Knowledge Review

- [x] Completed 8 checkpoint questions
- [x] Explained foreign keys
- [x] Explained relationships
- [x] Explained migrations
- [x] Explained eager loading
- [x] Explained indexes vs constraints
- [x] Explained rollback
- [x] Explained atomicity
- [x] Explained User → Project → Task

---

# Final Review

Day 46 was an integration checkpoint rather than a normal lesson.

The purpose was to determine whether the individual database concepts learned over the previous days could be combined into one coherent system.

The checkpoint showed that I now understand the major architecture of the database layer.

I can model:

User

↓

Project

↓

Task

using foreign keys and ORM relationships.

I can create connected ORM objects, persist them using Sessions, retrieve them with SELECT queries, filter results, perform JOINs and navigate relationships.

I also understand that retrieving correct data is only one part of database engineering.

Performance matters.

This is why indexes and eager-loading strategies such as `selectinload()` are important.

Correctness also matters.

This is why database constraints such as:

UNIQUE

CHECK

NOT NULL

FOREIGN KEY

are important.

Transactions then connect multiple database operations into reliable units of work.

If one operation violates an integrity rule, rollback can prevent the database from being left in a partially updated state.

Alembic provides another important layer by allowing the schema to evolve over time rather than deleting and recreating databases whenever models change.

The checkpoint also identified several recurring implementation weaknesses.

The most important are:

Session vs Session(engine)

scalar() vs scalars()

one ORM object vs a collection of ORM objects

correct model attributes

Python loop indentation

These are narrower implementation issues rather than a lack of understanding of relational database fundamentals.

The next goal is to make these patterns automatic through continued usage.

The most important mental model from the entire checkpoint is:

Model the Domain

↓

Define Relationships

↓

Protect Relationships With Foreign Keys

↓

Persist Through Sessions

↓

Use Transactions

↓

Query Deliberately

↓

Optimise Important Query Paths

↓

Protect Data With Constraints

↓

Evolve Schema With Migrations

↓

Verify Behaviour

This represents the complete database workflow developed throughout this section.

**Day 46: Completed - Week 21 Database Integration Checkpoint**