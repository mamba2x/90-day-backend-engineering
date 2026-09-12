# Day 40 - Database Migrations with Alembic

## Overview

Today I moved from simply defining database structures with SQLAlchemy into managing how an existing database schema changes over time using Alembic migrations.

Previously, I relied mainly on `Base.metadata.create_all()` when creating database tables. This works when tables need to be created for the first time, but it is not a proper solution for changing an existing database schema.

Today I successfully configured Alembic with SQLAlchemy, generated migration revisions, applied migrations to an SQLite database, and evolved the Task schema by adding a new `description` column.

This introduced me to one of the most important database management workflows used in production backend development:

Change ORM Model

↓

Generate Migration

↓

Inspect Migration

↓

Apply Migration

↓

Verify Database Revision

Instead of deleting and recreating the database whenever my models change, I can now evolve the database through controlled, versioned migrations.

---

## Why Database Migrations Are Necessary

An application's database structure will normally change as the application grows.

For example, the original Task model contained fields such as:

- id
- title
- completed
- priority
- user_id

Later, I decided to introduce:

- description

If the application already contains users and tasks, deleting the database and recreating it would destroy the existing information.

Database migrations provide a safer approach.

A migration describes how the database should move from one schema version to another.

Conceptually:

Database Version 1

↓

Migration

↓

Database Version 2

↓

Migration

↓

Database Version 3

This allows the database structure to evolve while maintaining a history of those changes.

---

## Schema Changes vs Normal Data Changes

I reinforced the difference between database data and database schema.

Data refers to the actual records stored inside tables.

Examples include:

- Michael
- Sarah
- Study FastAPI
- Learn Docker

Schema refers to the structure used to store those records.

Examples include:

- tables
- columns
- data types
- primary keys
- foreign keys
- indexes
- constraints

Adding another Task is a data operation.

Adding a new `description` column to the Task table is a schema operation.

Alembic primarily helps manage schema changes.

---

## Why create_all() Is Not Enough

Previously, I used:

`Base.metadata.create_all(engine)`

This is useful for creating database tables that do not already exist.

However, it is not a proper database migration system.

If an existing `tasks` table already contains data and I modify my Task model by adding:

`description`

the existing table is not automatically evolved through a controlled versioned process simply because the Python model changed.

This introduced an important distinction:

ORM Model

does not automatically equal:

Actual Existing Database Schema

The SQLAlchemy model represents what my application expects the schema to look like.

Alembic manages how the real database moves toward that expected schema.

---

## Introduction to Alembic

Alembic is a database migration tool commonly used alongside SQLAlchemy.

SQLAlchemy and Alembic have related but different responsibilities.

SQLAlchemy handles areas such as:

- ORM models
- database queries
- relationships
- sessions
- transactions
- mapping Python objects to database tables

Alembic handles areas such as:

- migration revisions
- schema changes
- migration history
- schema upgrades
- schema downgrades
- database version tracking

A useful mental model is:

SQLAlchemy

↓

Describe and interact with the database

Alembic

↓

Track and apply changes to the database structure

---

## Initialising Alembic

Today I successfully initialised Alembic inside my Day 40 project.

This created an Alembic structure containing important files and directories such as:

`alembic/`

`alembic/versions/`

`alembic/env.py`

`alembic/script.py.mako`

`alembic/README`

`alembic.ini`

The `versions` directory stores the migration revisions created as the database schema evolves.

This means database schema changes can now exist as actual version-controlled files inside the project.

---

## Understanding alembic.ini

I learned that `alembic.ini` contains Alembic configuration.

For today's project, Alembic needed to know which database it should work with.

My application uses:

`sqlite:///./day40.db`

This connects the migration environment to the SQLite database used for Day 40.

A useful mental model is:

`alembic.ini`

↓

Where/configuration for the database

This corrected my earlier misunderstanding where I mixed up the responsibilities of `alembic.ini` and `env.py`.

---

## Understanding env.py

The `env.py` file configures Alembic's migration environment.

One of its most important responsibilities in this project is giving Alembic access to the SQLAlchemy metadata.

My models inherit from the SQLAlchemy declarative Base.

The resulting:

`Base.metadata`

contains information describing the mapped database schema.

Alembic uses this metadata when comparing my SQLAlchemy models against the actual database.

Conceptually:

SQLAlchemy Models

↓

Base.metadata

↓

Alembic env.py

↓

Migration Autogeneration

This allows Alembic to understand what schema my application expects.

---

## Understanding Base.metadata

`Base.metadata` contains SQLAlchemy's understanding of my database schema.

This includes information about:

- users table
- tasks table
- columns
- primary keys
- foreign keys
- column types
- constraints

By exposing this metadata to Alembic through:

`target_metadata = Base.metadata`

Alembic can compare my ORM schema with the actual database schema.

This is what makes migration autogeneration possible.

---

## Understanding target_metadata

The purpose of:

`target_metadata = Base.metadata`

is to tell Alembic which SQLAlchemy metadata it should use when detecting schema differences.

Conceptually:

Current Database Schema

compared with:

Base.metadata

If Alembic detects a difference, it can generate migration operations representing that difference.

For example:

Database:

Task has no description

SQLAlchemy metadata:

Task has description

Alembic can detect that a new column may need to be added.

---

## Creating the Initial Migration

Today I successfully generated the initial migration for the User and Task models.

This created a migration revision inside:

`alembic/versions/`

The initial migration represents the first version of the database schema managed by Alembic.

Conceptually:

Base

↓

Initial Migration

↓

users table

tasks table

This establishes a migration starting point for future schema changes.

---

## Understanding revision --autogenerate

One of the most important Alembic commands I learned was:

`alembic revision --autogenerate`

This command compares:

Current Database Schema

with:

SQLAlchemy Base.metadata

Alembic then attempts to generate a migration file representing the detected differences.

The command does not itself mean that the database has already been changed.

Instead:

`revision --autogenerate`

↓

Generate migration instructions

This distinction is important because migration generation and migration execution are separate operations.

---

## Understanding Migration Files

Migration revisions are stored inside:

`alembic/versions/`

Today my project successfully produced multiple migration files.

The first migration represented the creation of the initial User and Task schema.

A later migration represented adding the new description field.

This created an actual migration history.

Conceptually:

Base

↓

Create Users and Tasks

↓

Add Description to Tasks

↓

Head

This is fundamentally different from simply editing the model and recreating the database.

Alembic now has a history describing how the database reached its current structure.

---

## Understanding upgrade()

Each migration revision contains an `upgrade()` function.

The `upgrade()` function contains the operations required to move the database forward to the new schema version.

For example:

Old Task Schema

↓

upgrade()

↓

Task Schema With Description

An upgrade can perform operations such as:

- creating tables
- adding columns
- creating indexes
- adding foreign keys
- adding constraints

Therefore, `upgrade()` represents moving the database schema forward, not simply "upgrading a table."

---

## Understanding downgrade()

Migration revisions can also contain a `downgrade()` function.

The purpose of `downgrade()` is to define how that migration can be reversed.

For example:

Task With Description

↓

downgrade()

↓

Task Without Description

The mental model is:

`upgrade()`

↓

Forward

`downgrade()`

↓

Backward

This allows Alembic to manage schema history in both directions when appropriate.

---

## Applying Migrations

Generating a migration does not automatically apply it.

This was an important distinction I learned today.

The migration generation stage creates instructions.

The migration application stage executes those instructions against the database.

The important command is:

`alembic upgrade head`

This tells Alembic to move the database to the latest available migration revision.

Therefore:

`revision --autogenerate`

↓

Create migration

while:

`upgrade head`

↓

Apply migration

Today I successfully reached the latest Alembic revision for the Day 40 database.

---

## Understanding Alembic Head

`head` represents the latest migration revision in the current migration chain.

Conceptually:

Base

↓

Initial Migration

↓

Description Migration

↓

HEAD

Running:

`alembic upgrade head`

means:

Move the database to the latest available migration revision.

The terminal output confirmed that my migration state reached a revision marked as:

`(head)`

This means the database migration state was aligned with the latest migration revision available in the project.

---

## Adding the Description Column

After establishing the initial database schema, I modified the Task ORM model by adding:

`description`

The field was configured as an optional string with a maximum length of 500 characters.

Conceptually:

Old Task:

- id
- title
- completed
- priority
- user_id

New Task:

- id
- title
- completed
- priority
- description
- user_id

Instead of deleting the database, I generated another Alembic migration.

The new migration revision represented:

Add description to tasks

This demonstrated the main reason migrations exist.

The database schema could evolve from one version to another through a controlled migration rather than being recreated from scratch.

---

## Multiple Migration Revisions

My Day 40 project now contains multiple migration revisions inside the Alembic `versions` directory.

This demonstrates that Alembic is tracking the history of the schema rather than only storing the current structure.

The migration chain conceptually looks like:

Base

↓

Create Users and Tasks

↓

Add Description to Tasks

↓

Head

Each revision represents a specific schema transition.

This allows developers to understand how the current database schema evolved.

---

## Why Generated Migrations Must Be Inspected

Another important production lesson from today is that automatically generated migrations should always be reviewed.

Alembic's autogeneration feature is powerful, but generated migrations are still code.

They may sometimes be:

- incomplete
- incorrect
- unsafe
- different from the developer's intention

Therefore, the correct workflow is:

Generate Migration

↓

Inspect upgrade()

↓

Inspect downgrade()

↓

Confirm Intended Changes

↓

Apply Migration

This becomes especially important when working with production databases containing important user or business data.

---

## Checking the Current Migration

Alembic provides commands for checking which migration revision is currently applied.

The current revision allows me to determine where the actual database sits within the migration history.

The terminal output from today's work showed a revision marked:

`(head)`

This confirmed that the database had reached the latest available migration revision at that point.

Conceptually:

Migration 1

↓

Migration 2 ← current/head

The current database revision and the latest available revision are therefore aligned.

---

## Understanding Migration History

Alembic maintains a migration chain rather than treating every schema change independently.

Each migration knows its relationship to previous revisions.

Conceptually:

Base

↓

Revision A

↓

Revision B

↓

Revision C

↓

Head

This gives the database schema a history.

That history becomes useful when:

- deploying applications
- upgrading environments
- reproducing schemas
- reviewing database changes
- rolling back certain changes
- collaborating with other developers

Migration files should therefore be treated as an important part of the project's source code.

---

## Understanding downgrade -1

I learned that:

`alembic downgrade -1`

means:

Move backward by one migration revision.

For example:

Initial Migration

↓

Description Migration ← current

Running:

`alembic downgrade -1`

would move the database back to:

Initial Migration

The migration's `downgrade()` function defines the operations required to perform that reversal.

Afterwards:

`alembic upgrade head`

can move the database forward to the latest revision again.

This gives Alembic the ability to move through schema history in a controlled manner.

---

## The Complete Migration Lifecycle

The most important workflow from Day 40 is:

### 1. Define or Modify SQLAlchemy Models

The ORM models represent the schema expected by the application.

### 2. Generate a Migration

Alembic compares the current database with SQLAlchemy metadata and creates migration instructions.

### 3. Inspect the Migration

The generated `upgrade()` and `downgrade()` operations should be reviewed.

### 4. Apply the Migration

Alembic executes the migration against the database.

### 5. Verify the Revision

The current migration revision should be checked to ensure that the database reached the expected state.

The complete mental model is:

Change Model

↓

Generate Migration

↓

Inspect Migration

↓

Apply Migration

↓

Verify Revision

↓

Continue Development

---

## create_all() vs Alembic

One of the biggest conceptual improvements from today was understanding when `create_all()` and Alembic are used.

### Base.metadata.create_all()

Useful for:

- quickly creating missing tables
- simple development environments
- learning SQLAlchemy
- initial experimentation

However, it does not provide proper version-controlled schema evolution.

### Alembic

Useful for:

- evolving existing schemas
- tracking schema versions
- adding columns
- removing columns
- changing tables
- applying upgrades
- defining downgrades
- maintaining migration history
- managing production database changes

The mental model is:

`create_all()`

↓

Create missing structures

Alembic

↓

Track and evolve structures over time

---

## Mistakes I Corrected Today

During Day 40, I initially had several conceptual misunderstandings.

I originally thought database migrations were mainly about migrating new data into tables.

I corrected this understanding and learned that migrations primarily manage changes to database schema.

I initially described `create_all()` as only creating an entirely fresh table.

I learned that it creates missing tables but does not provide the controlled schema evolution and version history required for an existing production database.

I initially mixed up `alembic.ini` and `env.py`.

I corrected this by understanding that `alembic.ini` contains Alembic configuration such as the database connection, while `env.py` configures the migration environment and connects Alembic to SQLAlchemy metadata.

I initially misunderstood `revision --autogenerate` as simply inspecting the database.

I corrected this and learned that it compares the database schema with SQLAlchemy metadata and generates migration instructions.

I also improved my understanding of:

- `upgrade()`
- `downgrade()`
- `head`
- migration revisions
- migration history

Most importantly, I then applied these concepts practically by creating an Alembic environment and generating actual migration revisions.

---

## Important Mental Models

### SQLAlchemy vs Alembic

SQLAlchemy

↓

Define and interact with database models

Alembic

↓

Manage how the schema changes over time

---

### Configuration

`alembic.ini`

↓

Database and Alembic configuration

`env.py`

↓

Migration environment and SQLAlchemy metadata

---

### Metadata

SQLAlchemy Models

↓

Base.metadata

↓

target_metadata

↓

Alembic Autogenerate

---

### Generate vs Apply

`alembic revision --autogenerate`

↓

Generate migration

`alembic upgrade head`

↓

Apply migration

---

### Schema Direction

`upgrade()`

↓

Move forward

`downgrade()`

↓

Move backward

---

### Complete Workflow

Change ORM Model

↓

Generate Migration

↓

Inspect Migration

↓

Apply Migration

↓

Check Current Revision

↓

Database Schema Updated

---

## Key Concepts Learned

Today I learned and reinforced:

- database migrations
- database schema evolution
- Alembic
- SQLAlchemy metadata
- `Base.metadata`
- `target_metadata`
- `alembic.ini`
- `env.py`
- Alembic initialization
- migration directories
- migration revision files
- migration history
- migration autogeneration
- `revision --autogenerate`
- `upgrade()`
- `downgrade()`
- `upgrade head`
- Alembic `head`
- checking current revisions
- adding columns through migrations
- multiple migration revisions
- schema versioning
- `create_all()` versus migrations
- ORM schema versus actual database schema
- reviewing generated migrations
- production database evolution

---

## Completion Checklist

### SQLAlchemy Model Work

- [x] Created the Day 40 SQLAlchemy models
- [x] Configured the SQLite database
- [x] Defined the User model
- [x] Defined the Task model
- [x] Maintained the User/Task relationship
- [x] Added the optional Task description field

### Alembic Setup

- [x] Initialised Alembic
- [x] Generated the Alembic project structure
- [x] Created the `alembic/versions` directory
- [x] Configured `alembic.ini`
- [x] Configured `env.py`
- [x] Connected Alembic to SQLAlchemy metadata
- [x] Created the Day 40 SQLite database

### Migration Work

- [x] Generated the initial User and Task migration
- [x] Created an additional migration for the Task description field
- [x] Stored migration revisions inside `alembic/versions`
- [x] Applied migrations to the database
- [x] Reached the latest Alembic migration revision
- [x] Verified a revision marked as `(head)`
- [x] Established a multi-revision migration history

### Concepts

- [x] Understood why migrations are needed
- [x] Understood schema changes versus data changes
- [x] Understood the limitations of `create_all()`
- [x] Understood Alembic's purpose
- [x] Understood `Base.metadata`
- [x] Understood `target_metadata`
- [x] Understood `alembic.ini`
- [x] Understood `env.py`
- [x] Understood `revision --autogenerate`
- [x] Understood `upgrade head`
- [x] Understood `upgrade()`
- [x] Understood `downgrade()`
- [x] Understood `head`
- [x] Understood why generated migrations should be inspected
- [x] Understood the purpose of `downgrade -1`
- [x] Corrected the Day 40 Q&A

### Remaining Verification

- [ ] Confirm `alembic downgrade -1` was successfully executed
- [ ] Confirm the database was upgraded back to `head` after the downgrade test

---

## Overall Review

Day 40 introduced one of the most important concepts in production database development: controlled schema evolution.

Before today, my SQLAlchemy work focused mainly on defining models, creating tables, storing data, querying data, transactions, and relationships.

Today I successfully moved beyond simply creating database structures and began managing database schema history.

I configured an Alembic environment, connected it to my SQLAlchemy models, created an SQLite database managed through migrations, generated an initial migration, introduced a new Task field, generated another migration for that schema change, and reached the latest Alembic revision.

The biggest takeaway from today is that changing a Python ORM model and changing an existing database are two separate operations.

SQLAlchemy defines what my application expects.

Alembic controls how the real database gets there.

The migration lifecycle I now understand is:

Change Model

↓

Generate Migration

↓

Inspect Migration

↓

Apply Migration

↓

Verify Revision

This represents an important progression toward managing databases the way real backend applications do.

**Day 40 Status: Core Alembic setup and migration workflow completed. Downgrade/restore verification remains.**