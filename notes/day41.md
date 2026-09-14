# Day 41 - Alembic Migration Workflow, Revision Chains and Data Safety

## Overview

Today I went deeper into database migrations and learned that generating and applying migrations is only one part of the process.

The more important production concern is understanding how a schema change affects existing data.

In Day 40, I learned the basic Alembic workflow:

Change ORM Model

↓

Generate Migration

↓

Inspect Migration

↓

Apply Migration

↓

Verify Database Revision

Today, I built on that by learning how migration revisions form a dependency chain, how nullable and non-nullable columns affect existing rows, how backfilling works, and why downgrades can still cause data loss even when they run successfully.

This moved my understanding from simply knowing Alembic commands to thinking about migration safety.

---

## Continuing From the Existing Migration History

My project already had an Alembic migration history from Day 40.

Conceptually, the migration chain looked like:

Base

↓

Create Users and Tasks

↓

Add Description to Tasks

↓

Head

Today, I extended the schema again by adding a new `due_date` field to the Task model.

The updated Task structure conceptually became:

- id
- title
- completed
- priority
- description
- user_id
- due_date

This allowed me to practise adding another schema change on top of an existing migration history instead of starting from a fresh database.

---

## Understanding Migration Revisions

One of the main concepts I learned today was the meaning of a migration `revision`.

Every Alembic migration has its own unique identifier.

For example:

`revision = "abc123"`

This identifier represents that specific migration revision.

It does not compare the database schema or perform the migration itself.

It simply identifies that migration inside Alembic's migration history.

This is similar to how a Git commit has a unique identifier.

A useful mental model is:

Git commit ID

↓

Identifies a specific code version

Alembic revision ID

↓

Identifies a specific database schema migration

---

## Understanding down_revision

I also learned the purpose of:

`down_revision`

This identifies the migration that comes immediately before the current migration.

For example:

`revision = "bbb222"`

`down_revision = "aaa111"`

means:

`aaa111`

↓

`bbb222`

This creates a dependency relationship between migrations.

The current migration knows which previous migration must already exist before it can be applied.

---

## Why Migration Dependency Chains Matter

Alembic migration revisions form a dependency chain.

For example:

A

↓

B

↓

C

If C is the latest migration, then:

B comes before C

and:

A comes before B

This order matters because later migrations often depend on database structures created earlier.

For example, a migration cannot add a new column to the `tasks` table if the `tasks` table has not yet been created.

Therefore, Alembic needs revision history so it knows:

- which migration comes first
- which migration comes next
- which migrations must be applied
- which migrations must be reversed during downgrade

The migration chain gives structure and order to database schema evolution.

---

## Adding the due_date Column

Today I added a new optional field to the Task model:

`due_date`

The field was configured as a nullable string.

Conceptually:

`due_date: string or NULL`

The important part was:

`nullable=True`

This was intentional because the database may already contain existing Task records.

Those existing rows do not already have a due date.

Allowing NULL means the database can safely accept the new column without requiring every existing record to immediately contain a value.

---

## Why Nullable Columns Are Safer for Existing Data

Suppose the database already contains:

Task 1

Task 2

Task 3

Task 4

Task 5

None of these Tasks previously had a `due_date`.

If I add:

`due_date`

with:

`nullable=True`

then existing rows can safely contain:

`due_date = NULL`

This is valid.

However, if I immediately add:

`due_date`

with:

`nullable=False`

then every existing Task must immediately contain a valid value.

The database may reject the migration because the old rows do not have values for the new required column.

This helped me understand why nullable columns are often easier to introduce into populated tables.

---

## The Danger of NOT NULL on Existing Tables

Today I learned an important migration safety issue.

If I add a new required column to a table that already contains data, the existing rows may violate the new constraint.

For example:

Existing rows:

Task 1

Task 2

Task 3

Then I introduce:

`status NOT NULL`

The database asks:

What value should the old rows have?

If no value is provided, the migration may fail.

The existing records cannot satisfy the new NOT NULL rule.

This means schema design must consider the data that already exists, not only the structure I want for future records.

---

## Understanding Backfills

I learned that a backfill is the process of populating existing rows with values for a newly introduced field or corrected data.

For example:

Before backfill:

Task 1 → status = NULL

Task 2 → status = NULL

Task 3 → status = NULL

After backfill:

Task 1 → status = "pending"

Task 2 → status = "pending"

Task 3 → status = "pending"

This allows existing data to become compatible with a future constraint.

Backfills are especially important when introducing required fields into databases that already contain records.

---

## Safe Migration Strategy for Required Columns

One of the most important patterns I learned today was the safe migration strategy for adding a new required column.

The pattern is:

### Step 1: Add the column as nullable

This allows the schema change to succeed even though existing rows do not yet have values.

### Step 2: Backfill existing rows

Populate the new column for all existing records.

For example:

`status = "pending"`

### Step 3: Enforce NOT NULL

Once all rows contain valid values, the column can safely be changed to:

`nullable=False`

The mental model is:

Add safely

↓

Populate old records

↓

Tighten constraint

This approach reduces the risk of migration failure.

---

## Understanding Migration Safety

Today I learned that a technically correct schema change is not automatically a safe production migration.

Before applying a migration, I should think about:

- existing rows
- NULL values
- required constraints
- defaults
- data loss
- downgrade behaviour
- migration ordering
- application compatibility

This means migration design is not only about changing table structure.

It is also about preserving data integrity.

---

## Understanding upgrade()

The `upgrade()` function represents the operations required to move the database schema forward.

For example:

Old schema:

Task has no due_date

↓

upgrade()

↓

New schema:

Task has due_date

The upgrade function may perform operations such as:

- creating tables
- adding columns
- adding constraints
- creating indexes
- modifying schema structures

It represents forward schema evolution.

---

## Understanding downgrade()

The `downgrade()` function represents the reverse migration.

For example:

Current schema:

Task has due_date

↓

downgrade()

↓

Previous schema:

Task has no due_date

However, I learned today that a successful downgrade does not automatically mean that no data was lost.

This was one of the most important corrections from today's work.

---

## Downgrades Can Cause Data Loss

I initially thought Alembic protected all data during downgrades.

This was incorrect.

Alembic tracks migration operations, not all application data.

For example, imagine the `due_date` column contains:

- 2026-09-20
- 2026-09-25
- 2026-10-01

If the downgrade removes the `due_date` column, those values are also removed.

The downgrade may execute successfully while still destroying data.

Therefore:

Successful downgrade

does not mean:

No data loss

It only means the downgrade operations completed successfully.

This is a very important production lesson.

---

## Understanding alembic downgrade -1

I reinforced the meaning of:

`alembic downgrade -1`

The `-1` means:

Move backward by one migration revision.

For example:

A

↓

B

↓

C ← current

Running:

`alembic downgrade -1`

moves the database back to:

B

This executes the `downgrade()` function of the current migration.

The command changes the schema version, but whether data is preserved depends on what the downgrade operations actually do.

---

## Understanding A -> B -> C

I also corrected my understanding of migration chains.

If the migration history is:

A -> B -> C

and C is head,

then B represents the previous migration revision immediately before C.

It does not represent migrated data.

It represents a schema version.

Conceptually:

C.down_revision = B

This means C depends directly on B.

---

## SQLAlchemy default vs server_default

Another important concept introduced today was the difference between:

`default`

and:

`server_default`

A SQLAlchemy `default` is usually applied on the Python or SQLAlchemy side when a row is inserted through the application.

A `server_default` is defined at the database level.

The database itself supplies the value.

A useful mental model is:

`default`

↓

Application / SQLAlchemy side

`server_default`

↓

Database side

This distinction becomes important during migrations because existing rows already live in the database.

A Python-side default does not automatically populate old database rows.

Database-side behaviour must be considered separately.

---

## Why server_default Matters in Migrations

Suppose I add:

`status`

to an existing table.

If I only define a Python-side default:

`default="pending"`

that may help when future rows are created through SQLAlchemy.

However, existing rows already stored in the database may still need to be handled.

A database-level default or explicit migration backfill may be required.

This showed me that model defaults and migration safety are related but are not the same thing.

---

## Inspecting upgrade() and downgrade()

I reinforced the importance of manually reviewing generated migrations.

Autogeneration can help create migration operations, but generated migration code should never be trusted blindly.

Before applying a migration, I should inspect:

`upgrade()`

and:

`downgrade()`

and ask:

- Is this the schema change I intended?
- Could this remove data?
- Could existing rows violate a new constraint?
- Is the downgrade destructive?
- Are defaults handled correctly?
- Does the migration depend on an earlier revision?

This review process is especially important in production systems.

---

## Adding due_date Safely

Today's actual schema change was adding:

`due_date`

to Task.

The field was intentionally nullable.

This means existing Task records can remain valid even if they do not yet contain due dates.

Conceptually:

Old Task:

- id
- title
- completed
- priority
- description
- user_id

New Task:

- id
- title
- completed
- priority
- description
- user_id
- due_date

Old rows can contain:

`due_date = NULL`

while future records can optionally contain values.

This is a relatively safe schema evolution compared with immediately enforcing NOT NULL.

---

## Final Migration Safety Scenario

The final scenario involved a table containing many existing Task records.

The new requirement was:

`status`

must eventually be required.

The unsafe approach would be:

Add `status NOT NULL` immediately

This could fail because existing Tasks do not contain status values.

The safer approach is:

### Step 1

Add `status` as nullable.

This allows the migration to succeed without violating existing rows.

### Step 2

Backfill all existing Tasks.

For example:

`status = "pending"`

This gives every old record a valid status.

### Step 3

Change the column to NOT NULL.

At this point, every existing record satisfies the constraint.

Future records must also provide a value.

This pattern demonstrated how schema constraints should be introduced gradually when existing data is involved.

---

## Mistakes I Corrected Today

During today's work, I made several conceptual mistakes that helped reinforce the migration concepts.

I initially thought `revision` was related to comparing SQLAlchemy metadata with the database.

I corrected this and learned that `revision` is the unique identifier of a migration.

I initially thought `down_revision` meant moving the head backward.

I corrected this and learned that it identifies the migration that comes immediately before the current one.

I initially left the migration dependency question unanswered.

I learned that revision chains allow Alembic to apply and reverse migrations in the correct order.

I initially described backfilling too generally as populating a table.

I corrected this and learned that backfilling means populating existing records with values for new or corrected fields.

My biggest mistake was believing that a successful downgrade guarantees no data loss.

I corrected this and learned that downgrades can remove columns, tables, and stored values.

I also learned the difference between SQLAlchemy `default` and database `server_default`.

These corrections significantly improved my understanding of migration safety.

---

## Important Mental Models

### Revision Chain

A

↓

B

↓

C

Each migration points back to the migration before it.

---

### revision

Unique migration identifier.

---

### down_revision

Previous migration dependency.

---

### Safe Required Column Migration

Add nullable column

↓

Backfill existing rows

↓

Enforce NOT NULL

---

### Migration Safety

Schema change

↓

Ask what happens to existing data

↓

Design safe migration

↓

Generate migration

↓

Inspect migration

↓

Apply migration

↓

Verify result

---

### Upgrade vs Downgrade

upgrade()

↓

Move schema forward

downgrade()

↓

Move schema backward

But:

Downgrade may still destroy data.

---

### Defaults

SQLAlchemy `default`

↓

Application-side value

Database `server_default`

↓

Database-side value

---

## Key Concepts Learned

Today I learned and reinforced:

- Alembic revision IDs
- `revision`
- `down_revision`
- migration dependency chains
- migration order
- migration history
- nullable columns
- non-nullable columns
- NOT NULL constraints
- existing-row compatibility
- migration failures
- backfills
- safe schema evolution
- staged constraint introduction
- `upgrade()`
- `downgrade()`
- `alembic downgrade -1`
- downgrade data loss
- migration reversibility
- migration safety
- SQLAlchemy `default`
- database `server_default`
- inspecting migration code
- schema changes with existing production data
- designing migrations around existing records

---

## Progress From Day 40 to Day 41

Day 40 focused on learning how to use Alembic.

I learned how to:

- initialise Alembic
- configure the database
- connect Alembic to SQLAlchemy metadata
- generate migration revisions
- apply migrations
- inspect migration history
- reach head

Day 41 focused on understanding how to make those migrations safer.

I learned how to:

- understand revision dependencies
- reason about existing rows
- introduce nullable columns safely
- understand NOT NULL migration problems
- backfill existing data
- stage schema constraints
- understand downgrade risk
- distinguish SQLAlchemy defaults from database defaults
- think about data preservation before applying schema changes

This moved my migration knowledge from basic tooling toward practical migration engineering.

---

## Completion Checklist

### Schema Work

- [x] Continued from the existing Alembic migration history
- [x] Added the `due_date` field to the Task model
- [x] Made `due_date` nullable for migration safety
- [x] Preserved the existing User and Task relationship structure

### Migration Concepts

- [x] Understood `revision`
- [x] Understood `down_revision`
- [x] Understood migration dependency chains
- [x] Understood why migration order matters
- [x] Understood nullable vs non-nullable schema changes
- [x] Understood NOT NULL migration risks
- [x] Understood backfilling
- [x] Understood staged constraint introduction
- [x] Understood `upgrade()`
- [x] Understood `downgrade()`
- [x] Understood `alembic downgrade -1`
- [x] Understood that successful downgrade can still cause data loss
- [x] Understood SQLAlchemy `default`
- [x] Understood database `server_default`
- [x] Understood why migrations must be inspected before applying

### Migration Safety Scenario

- [x] Identified the unsafe NOT NULL migration problem
- [x] Added the column safely as nullable
- [x] Understood how to backfill existing rows
- [x] Understood when to enforce NOT NULL
- [x] Explained why each step is necessary
- [x] Corrected the Day 41 Q&A

---

## Overall Review

Day 41 was focused on understanding the difference between simply running migrations and designing migrations safely.

The most important thing I learned is that database schema changes must always consider the data that already exists.

A model change that looks simple in Python can become dangerous when millions of existing database rows are involved.

For example, adding a nullable column is usually straightforward because old rows can temporarily contain NULL.

Adding a required column is more complicated because every existing row must satisfy the new constraint.

The safe pattern I learned is:

Add Column Safely

↓

Backfill Existing Data

↓

Enforce Constraint

Another major lesson was understanding that Alembic tracks schema history, not all application data.

A migration can successfully downgrade while still deleting important values.

Because of this, `upgrade()` and `downgrade()` must always be reviewed carefully.

The biggest conceptual progression from today is:

Day 40:

"How do I create and apply migrations?"

Day 41:

"How do I design migrations that do not break or destroy existing data?"

This is an important step toward managing database changes in real production backend systems.

**Day 41: Completed**