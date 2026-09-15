# Day 42 - Database Indexes with SQLAlchemy and Alembic

## Overview

Today I learned how database indexes work and how to manage them properly using SQLAlchemy and Alembic.

I had already encountered indexes while learning raw SQL, but today I connected that knowledge to ORM-based backend development and database migrations.

The main lesson was that indexes are not simply something that should be added everywhere to "make the database faster."

Instead, an index is an additional database structure designed to make certain query patterns more efficient.

Indexes also introduce costs.

They consume additional storage and can make INSERT, UPDATE, and DELETE operations more expensive because the database has to maintain the indexes whenever indexed data changes.

The main mental model from today is:

Identify Common Query

↓

Determine Whether an Index Could Help

↓

Define Index in SQLAlchemy

↓

Generate Alembic Migration

↓

Inspect Migration

↓

Apply Migration

↓

Verify Database Schema

This means index design should always be based on how the application actually queries its data.

---

## Understanding Database Indexes

A database index is an additional data structure that helps the database locate matching rows more efficiently.

Without an appropriate index, the database may sometimes need to examine a large portion of a table to find the requested records.

For example, imagine the `tasks` table contains millions of rows and the application frequently performs:

`WHERE user_id = 10`

Without an appropriate index, the database may have to examine many rows while searching for Tasks belonging to User 10.

An index on `user_id` gives the database another structure that it can potentially use to locate those records more efficiently.

A useful mental model is the index at the back of a textbook.

Instead of reading every page looking for a topic, I can use the index to locate the relevant pages.

Database indexes work on a similar principle.

---

## Indexes Do Not Automatically Make Everything Faster

One of the most important lessons from today was that indexes involve trade-offs.

It would be incorrect to think:

"More indexes = faster database."

Indexes can improve certain read operations, but they also introduce additional work.

Whenever data is inserted, updated, or deleted, the database may also need to update the relevant indexes.

Therefore, an index can provide:

Potentially faster reads

but also:

Additional storage

+

More expensive INSERT operations

+

More expensive UPDATE operations

+

More expensive DELETE operations

+

Additional index maintenance

The better mental model is:

Read Performance

↕

Write Cost + Storage Cost

This means indexes should be created deliberately rather than automatically.

---

## Primary Keys and Indexes

My Task model already contains a primary key:

`id`

Primary keys generally already have an index or an equivalent efficient lookup structure maintained by the database.

This means I normally do not need to create another ordinary index such as:

`INDEX(id)`

just to search by the primary key.

For example, a lookup such as:

`session.get(Task, 42)`

already benefits from the database's primary-key lookup behaviour.

Creating another ordinary index on the same `id` column would usually be unnecessary duplication.

---

## Foreign Keys vs Indexes

Today I reinforced the difference between foreign keys and indexes.

These two concepts solve different problems.

A foreign key provides:

Referential integrity.

An index provides:

Potential query-performance improvement.

For example:

`tasks.user_id`

references:

`users.id`

The foreign key ensures that a Task cannot reference a User that does not exist.

Conceptually:

Foreign Key

↓

Data Integrity

The index serves a different purpose.

If my application frequently performs:

`WHERE user_id = ?`

an index on `user_id` may help the database locate Tasks belonging to that User more efficiently.

Conceptually:

Index

↓

Query Performance

Therefore:

Foreign Key != Index

A foreign key relationship does not exist primarily for performance, and an index does not provide referential integrity.

---

## Why user_id Is a Good Index Candidate

My application frequently needs to retrieve Tasks belonging to a particular User.

For example:

`WHERE user_id = 10`

This is a common and meaningful query pattern.

Because many Tasks can belong to one User, the `tasks` table could eventually contain a very large number of rows.

An index on:

`user_id`

can potentially make retrieving one User's Tasks more efficient.

This is why `user_id` is a reasonable index candidate.

The reason is not simply that `user_id` is a foreign key.

The reason is that the application frequently searches and filters Tasks using `user_id`.

This distinction is important.

Indexes should be designed around query patterns rather than simply around which columns look important.

---

## Defining a Single-Column Index in SQLAlchemy

I learned that SQLAlchemy allows a single-column index to be defined using:

`index=True`

For the `user_id` database column, the index belongs on the mapped column.

Conceptually:

`user_id`

↓

Actual Database Column

↓

ForeignKey

↓

nullable

↓

index

The correct structure is:

`user_id` contains the foreign key, nullability rule, and index configuration.

This is different from the ORM relationship:

`user`

The relationship exists for Python-side ORM navigation.

Conceptually:

`user_id`

↓

Database column

while:

`user`

↓

Related User ORM object

This was an important correction from today's work because I initially attempted to place `index=True` and `nullable=False` on the SQLAlchemy `relationship()`.

Those options belong to the actual database column rather than the ORM navigation relationship.

The correct mental model is:

`user_id`

↓

Database structure and constraints

`user`

↓

ORM object navigation

---

## SQLAlchemy Metadata Does Not Automatically Change the Database

Another important concept reinforced today was that changing the SQLAlchemy model does not automatically change an existing database.

For example, adding:

`index=True`

changes the SQLAlchemy metadata.

However, the existing database does not automatically receive the new index.

The workflow is still:

Change SQLAlchemy Model

↓

Generate Alembic Migration

↓

Inspect Migration

↓

Apply Migration

↓

Database Schema Changes

This is the same schema-evolution principle I learned during Days 40 and 41.

---

## Why Alembic Is Required for Index Changes

Alembic manages the schema change required to introduce the index into the existing database.

After changing the SQLAlchemy model, Alembic can compare the model metadata with the current database schema and generate the appropriate migration.

The migration records the schema change as part of the database's version history.

This means indexes become version-controlled database changes just like:

- tables
- columns
- foreign keys
- constraints
- other schema structures

This is important because database performance structures should also evolve in a controlled and repeatable way.

---

## Index Migration upgrade()

When an index is introduced, the migration's `upgrade()` function should contain the operation that creates the index.

Conceptually:

upgrade()

↓

Create Index

In Alembic this is normally represented using an operation such as:

`op.create_index(...)`

The important distinction I corrected today is that `upgrade()` does not "contain the migration file."

Instead:

The migration file

↓

contains `upgrade()`

and:

`upgrade()`

↓

contains the schema operations required to move the database forward.

For an index migration, one of those operations is creating the index.

---

## Index Migration downgrade()

The `downgrade()` function should reverse the schema change introduced by `upgrade()`.

If:

upgrade()

↓

creates index

then:

downgrade()

↓

drops index

This is normally represented with an operation such as:

`op.drop_index(...)`

This reinforces the migration principle from previous days:

upgrade()

↓

Move Schema Forward

downgrade()

↓

Reverse Schema Change

The purpose of the downgrade function is not merely to say "move to the previous migration."

It contains the actual operations necessary to reverse the current migration.

---

## Understanding Composite Indexes

Today I also learned about composite indexes.

A composite index is one index containing multiple columns.

For example:

`INDEX(user_id, completed)`

contains:

`user_id`

and:

`completed`

inside the same index.

This can be useful when the application frequently filters using those columns together.

For example:

`WHERE user_id = 10 AND completed = false`

A composite index on:

`(user_id, completed)`

is a reasonable candidate for this query pattern.

---

## Defining a Composite Index in SQLAlchemy

Composite indexes can be defined using SQLAlchemy's `Index` object.

At the table level, the Task model can define an index conceptually as:

`INDEX(user_id, completed)`

This creates an index containing both columns.

The important thing is that this is one composite index, not two separate indexes.

Conceptually:

Single-column indexes:

`INDEX(user_id)`

`INDEX(completed)`

are different from:

Composite index:

`INDEX(user_id, completed)`

The composite index is specifically organised using both columns.

---

## Why Composite Index Column Order Matters

Another important concept I learned today was that column order matters in composite indexes.

These two indexes are not necessarily equivalent:

`INDEX(user_id, completed)`

and:

`INDEX(completed, user_id)`

For:

`INDEX(user_id, completed)`

a simplified mental model is:

user_id

↓

completed

The index is organised beginning with `user_id`.

This means the order should be chosen based on actual application query patterns.

For example, if the application frequently retrieves Tasks for one User and then filters those Tasks by completion status, the order:

`(user_id, completed)`

makes sense.

This showed me that composite indexes should not simply contain a random collection of useful columns.

Their structure should reflect how the application accesses its data.

---

## Understanding completed as an Index Candidate

The `completed` field is a boolean.

It has only two possible values:

`True`

or:

`False`

This means it has very low cardinality.

For example, imagine 5 million Tasks where:

3 million are incomplete

and:

2 million are complete.

If I search:

`WHERE completed = false`

a very large percentage of the table may match.

Because the value does not narrow the result set very much, a standalone index on `completed` may provide less benefit than expected.

This does not mean boolean indexes are always useless.

It means they should not automatically be created without considering:

- table size
- value distribution
- query patterns
- database behaviour
- actual query plans

This is another example of why index design requires reasoning rather than simply adding `index=True` everywhere.

---

## Understanding Cardinality and Selectivity

Today I was introduced to an important idea related to indexing:

Cardinality and selectivity.

A column such as:

`completed`

has very few possible values.

This gives it low cardinality.

A column such as:

`user_id`

may contain thousands or millions of different values.

This can make it more selective for certain queries.

For example:

`WHERE user_id = 8721`

may reduce millions of Tasks down to a small number belonging to one User.

Meanwhile:

`WHERE completed = false`

may still match millions of rows.

Therefore, indexes tend to be most useful when they help the database significantly narrow down the records it needs to examine.

---

## Indexes and Write Performance

Indexes are not free.

Suppose a new Task is inserted.

The database must store the new Task row.

If indexes also exist, the database may need to update those index structures as well.

For example:

Insert Task

↓

Write Task Row

↓

Update Primary Key Structure

↓

Update user_id Index

↓

Update Composite Index

The same idea applies to updates.

If `completed` is part of:

`INDEX(user_id, completed)`

then changing:

`completed = false`

to:

`completed = true`

may require the database to update the relevant index structure.

This is particularly important because the Task completion status in my example application may change frequently.

Therefore, index design must consider both reads and writes.

---

## Index Storage Cost

Indexes require additional storage because the database maintains extra structures in addition to the actual table data.

This means creating many unnecessary indexes can increase database storage requirements.

The cost of an index therefore includes:

- storage
- maintenance
- additional work during writes
- additional schema complexity

This corrected my earlier answer where I mentioned "overwrite head" as an index cost.

`head` is an Alembic migration concept and is not an index-performance cost.

---

## The Database Decides Whether to Use an Index

Creating an index does not guarantee that the database will use it for every matching query.

The database has a query planner.

The planner evaluates possible ways to execute the query.

Depending on factors such as:

- table size
- number of matching rows
- available indexes
- data distribution
- query structure

the database may decide that using an index is useful.

In another situation, it may decide that scanning the table is cheaper.

Therefore:

Index Exists

does not guarantee:

Index Used

This connects to my earlier SQL lessons involving `EXPLAIN`.

`EXPLAIN` can help investigate how the database plans to execute a query.

This means production index optimisation should eventually be based on evidence rather than assumptions.

---

## Why Every Column Should Not Be Indexed

A major lesson from today was that indexing every column is not good database design.

Every index has a cost.

If I create indexes on:

- title
- completed
- priority
- description
- user_id
- due_date

without evidence that those indexes help important queries, the database must maintain all those structures even when they provide little benefit.

This can increase:

- storage usage
- INSERT cost
- UPDATE cost
- DELETE cost
- database complexity

Therefore, the better strategy is:

Observe Query Patterns

↓

Identify Important Queries

↓

Consider Candidate Index

↓

Measure Query Behaviour

↓

Keep Useful Indexes

Rather than:

Index Everything

↓

Hope Database Becomes Fast

---

## Query Pattern 1: Tasks for One User

For the query:

`WHERE user_id = 10`

a reasonable index is:

`INDEX(user_id)`

This is because the query searches directly using `user_id`.

The index can potentially help locate the subset of Tasks belonging to the requested User.

---

## Query Pattern 2: Incomplete Tasks for One User

For the query:

`WHERE user_id = 10 AND completed = false`

a reasonable index candidate is:

`INDEX(user_id, completed)`

This matches the query pattern where Tasks are first associated with a particular User and then filtered by completion status.

This was one of the index choices I correctly identified during today's practical work.

---

## Query Pattern 3: All Incomplete Tasks

For:

`WHERE completed = false`

I should not automatically create:

`INDEX(completed)`

because `completed` contains only two possible values.

If a large percentage of the table contains `false`, the index may not narrow the search sufficiently.

The correct approach is to consider the actual workload and verify query performance rather than assuming that every WHERE condition requires an index.

---

## Index Design for a Large Task System

The practical scenario involved a database containing approximately 5 million Tasks.

The common operations were:

1. Find a Task by primary key.
2. Get all Tasks for one User.
3. Get all incomplete Tasks for one User.
4. Create new Tasks frequently.
5. Update Task completion status frequently.

Several possible indexes were considered.

### INDEX(id)

I would normally not create another explicit ordinary index on `id`.

The primary key already provides efficient lookup behaviour.

Therefore, an additional index would usually be unnecessary.

### INDEX(user_id)

This is a reasonable candidate.

The application frequently retrieves Tasks belonging to one User.

Therefore, the index directly supports an important query pattern.

### INDEX(completed)

I would probably not create this standalone index yet.

The column only contains two possible values and may have low selectivity.

Completion status is also updated frequently, which means maintaining this index would introduce write overhead.

### INDEX(priority)

I would not add this yet.

The described workload does not show a common query that frequently filters or sorts using priority.

Without evidence of a useful query pattern, adding this index would introduce cost without a clear benefit.

### INDEX(user_id, completed)

This is a strong candidate.

One of the most common operations is retrieving incomplete Tasks belonging to one particular User.

The composite index directly reflects that query pattern.

Therefore, the strongest candidates from the scenario are:

`INDEX(user_id)`

and:

`INDEX(user_id, completed)`

However, I also learned that indexes can sometimes overlap in usefulness.

In a real production system, I would eventually inspect query plans and benchmark actual workloads before assuming both indexes must remain permanently.

---

## Connection to Previous SQL Index Lessons

Earlier in the course, I learned indexes using raw SQL.

I worked with concepts such as:

- CREATE INDEX
- DROP INDEX
- EXPLAIN
- single-column indexes
- composite indexes
- query filtering
- ORDER BY considerations

Today I connected those concepts to SQLAlchemy and Alembic.

The raw SQL mental model was:

SQL Query

↓

Create Index

↓

Database Index

The ORM/migration mental model is now:

Application Query Pattern

↓

SQLAlchemy Index Definition

↓

Alembic Migration

↓

Database Index

This connection is important because SQLAlchemy does not remove the need to understand SQL and database behaviour.

The ORM gives me another way to define and work with database structures, but the underlying database concepts still matter.

---

## Mistakes I Corrected Today

Today's practical work exposed several important mistakes.

### Mistake 1: Putting index=True on relationship()

I initially placed index configuration on the ORM `user` relationship.

I corrected this and learned that indexes belong to actual database columns.

Therefore:

`user_id`

is the database column and can contain:

- ForeignKey
- nullable
- index

while:

`user`

is the ORM relationship used for object navigation.

---

### Mistake 2: Confusing Foreign Key Purpose With Index Purpose

I initially explained that `user_id` should be indexed because it provides referential integrity.

This was incorrect.

The foreign key provides referential integrity.

The reason to index `user_id` is that the application frequently queries Tasks using that column.

Correct mental model:

Foreign Key

↓

Integrity

Index

↓

Performance

---

### Mistake 3: Misunderstanding upgrade()

I initially described `upgrade()` as containing the migration file.

I corrected this.

The migration file contains:

`upgrade()`

and:

`downgrade()`

The `upgrade()` function contains operations that move the database schema forward.

For today's index migration, that means creating the index.

---

### Mistake 4: Misunderstanding downgrade()

I initially described downgrade mainly as moving to the previous migration.

While that describes the overall result, the `downgrade()` function itself contains the operations required to reverse the current migration.

For an index migration:

upgrade()

↓

Create Index

downgrade()

↓

Drop Index

---

### Mistake 5: Indexing completed Automatically

I initially considered keeping a standalone:

`INDEX(completed)`

I learned that a boolean column has only two possible values and may have low selectivity.

Therefore, I should not automatically create a standalone index on it without evidence that it improves an important query.

---

### Mistake 6: Incomplete Understanding of Index Costs

I correctly identified storage as a cost but incorrectly mentioned "overwrite head."

I corrected this.

The real major costs include:

- additional storage
- index maintenance
- more expensive INSERT operations
- more expensive UPDATE operations
- more expensive DELETE operations

---

## Important Mental Models

### Index Purpose

Query Pattern

↓

Index

↓

Potentially Faster Lookup

---

### Foreign Key vs Index

Foreign Key

↓

Referential Integrity

Index

↓

Query Performance

---

### ORM Relationship vs Database Column

`user_id`

↓

Actual Database Column

↓

ForeignKey / nullable / index

`user`

↓

ORM Navigation

↓

relationship()

---

### Index Migration

Change SQLAlchemy Metadata

↓

Generate Alembic Migration

↓

Inspect upgrade() and downgrade()

↓

Apply Migration

↓

Verify Schema

---

### Index Trade-Off

Potentially Faster Reads

↕

Storage + Write Overhead

---

### Composite Index

`INDEX(user_id, completed)`

↓

First organised around user_id

↓

Then completed

Column order matters.

---

### Index Selection

Common Query Pattern

↓

Candidate Index

↓

Measure Performance

↓

Keep If Useful

---

## Key Concepts Learned

Today I learned and reinforced:

- database indexes
- single-column indexes
- composite indexes
- index selectivity
- column cardinality
- primary-key indexing behaviour
- foreign keys vs indexes
- SQLAlchemy `index=True`
- SQLAlchemy `Index`
- table-level index configuration
- composite index column ordering
- indexing foreign-key columns
- boolean-column indexing limitations
- index storage costs
- index write overhead
- INSERT index maintenance
- UPDATE index maintenance
- DELETE index maintenance
- Alembic index migrations
- `op.create_index()`
- `op.drop_index()`
- migration inspection
- query patterns
- query planner behaviour
- indexes not being guaranteed to be used
- evidence-based database optimisation
- relationship configuration vs column configuration
- avoiding unnecessary indexes
- indexing based on application workload

---

## Progress From Day 41 to Day 42

Day 41 focused on migration safety.

I learned:

- revision chains
- `revision`
- `down_revision`
- nullable migrations
- NOT NULL migration risks
- backfills
- staged constraints
- downgrade data-loss risks
- SQLAlchemy defaults
- database server defaults

Day 42 built on this by introducing performance-related schema changes.

I learned:

- how indexes affect query performance
- how indexes affect writes
- how to define indexes using SQLAlchemy
- how indexes become Alembic migrations
- how single-column indexes differ from composite indexes
- why index column order matters
- why boolean indexes may have low value
- why query patterns should drive index design
- why every column should not be indexed

The migration workflow is therefore becoming broader.

I am no longer only using migrations to change columns.

I can also use migrations to evolve performance-related database structures such as indexes.

---

## Completion Checklist

### SQLAlchemy

- [x] Imported SQLAlchemy `Index`
- [x] Defined a composite Task index
- [x] Understood where `index=True` belongs
- [x] Corrected the relationship/index configuration
- [x] Understood database column vs ORM relationship configuration

### Index Fundamentals

- [x] Understood the purpose of an index
- [x] Understood that indexes do not make every operation faster
- [x] Understood foreign key vs index
- [x] Understood primary-key indexing behaviour
- [x] Understood why `user_id` is a useful index candidate
- [x] Understood single-column indexes
- [x] Understood composite indexes
- [x] Understood composite-index column order
- [x] Understood boolean-column selectivity
- [x] Understood index storage cost
- [x] Understood index write overhead
- [x] Understood why every column should not be indexed

### Query Design

- [x] Identified `INDEX(user_id)` for User Task queries
- [x] Identified `INDEX(user_id, completed)` for User + completion queries
- [x] Reconsidered unnecessary standalone `INDEX(completed)`
- [x] Understood why `INDEX(priority)` is not justified by the current workload
- [x] Understood why a separate `INDEX(id)` is generally unnecessary

### Alembic

- [x] Understood that `index=True` does not automatically modify an existing database
- [x] Understood why Alembic is required for index schema changes
- [x] Understood that `upgrade()` creates the index
- [x] Understood that `downgrade()` removes the index
- [x] Understood that index migrations should be inspected before application

### Corrections

- [x] Corrected Day 42 Q&A
- [x] Corrected the purpose of `user_id` indexing
- [x] Corrected the placement of `index=True`
- [x] Corrected understanding of `upgrade()`
- [x] Corrected understanding of `downgrade()`
- [x] Corrected index-cost reasoning
- [x] Corrected large-database index-selection reasoning

---

## Overall Review

Day 42 introduced another important part of production database engineering: performance-aware schema design.

The biggest lesson was that indexes are not magic performance switches.

An index is an additional database structure designed to help particular query patterns.

This means I should not ask:

"Which columns can I index?"

Instead, I should ask:

"What queries does my application perform frequently?"

Then:

"Which index could potentially make those queries more efficient?"

The strongest example from today's work was the Task/User relationship.

Because the application frequently searches for Tasks belonging to a User:

`WHERE user_id = ?`

an index on:

`user_id`

is a reasonable candidate.

When the application frequently searches:

`WHERE user_id = ? AND completed = false`

a composite index on:

`(user_id, completed)`

becomes another strong candidate.

However, indexing `completed` alone may be less useful because it is a boolean column with very low cardinality.

I also reinforced that index design has costs.

Every additional index consumes storage and may make writes more expensive.

Therefore, production database optimisation requires balancing:

Read Performance

against:

Write Performance + Storage + Maintenance

Another important progression was connecting indexes to the Alembic workflow.

Indexes are part of the database schema.

Therefore, when an index is added to the SQLAlchemy model, the existing database still needs a migration.

The complete mental model is now:

Understand Application Queries

↓

Choose Candidate Index

↓

Define Index in SQLAlchemy

↓

Generate Alembic Migration

↓

Inspect create/drop Operations

↓

Apply Migration

↓

Verify Database

↓

Eventually Measure Real Query Performance

This continues the progression from previous days:

Day 40:

"How do I migrate my database?"

Day 41:

"How do I migrate my database without breaking existing data?"

Day 42:

"How do I evolve my database schema to support important query patterns without creating unnecessary performance costs?"

This is another step toward understanding how production backend databases are designed, evolved, and optimised.

**Day 42: Completed after corrections**