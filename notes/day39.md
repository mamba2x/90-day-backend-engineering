# Day 39 - SQLAlchemy Relationship Queries and JOINs

## Overview

Today I moved from simply creating and navigating SQLAlchemy relationships into actually querying related data using `select()`, `where()`, and `join()`.

In the previous days, I learned how `User` and `Task` are connected using a one-to-many relationship, how `ForeignKey` creates the database-level connection, and how `relationship()` allows ORM objects to navigate between related records.

Today, I focused on using those relationships in real database queries.

The main goal was to understand the difference between:

- accessing related objects through ORM relationship attributes such as `user.tasks`
- explicitly querying related rows with `select()` and `where()`
- combining related tables using SQLAlchemy `JOIN`
- retrieving one ORM entity versus multiple ORM entities in the same query result

This helped connect the raw SQL JOIN knowledge I learned earlier with SQLAlchemy ORM syntax.

---

## Revisiting the User and Task Relationship

The database still uses the same one-to-many relationship.

One User can own many Tasks.

Each Task belongs to one User.

At the database level:

`tasks.user_id -> users.id`

At the ORM level:

`User.tasks <-> Task.user`

This relationship allows SQLAlchemy to understand how the two models are connected.

Because the models already define the connection, SQLAlchemy can use that relationship when performing joins.

---

## Relationship Traversal

The first query method I practised was relationship traversal.

After retrieving Michael from the database using:

`session.get(User, michael_id)`

I could access his related Tasks through:

`michael.tasks`

This works because `tasks` is the relationship attribute on the User model.

The important idea is that once I have a User ORM object, I can navigate directly to the related Task objects.

For example:

`michael.tasks`

returns a collection of Task ORM objects belonging to Michael.

This is different from writing an explicit query because I am navigating through an already configured ORM relationship.

---

## Explicit Task Queries

I also learned how to query Tasks directly using `select()`.

Instead of retrieving a User first and then using:

`user.tasks`

I can query the Task table itself.

For example:

`select(Task).where(Task.user_id == michael_id)`

asks the database to return Task rows where the `user_id` matches Michael's primary key.

This reinforced the difference between relationship traversal and explicit querying.

Relationship traversal:

`michael.tasks`

Explicit query:

`select(Task).where(Task.user_id == michael_id)`

Both can return Michael's Tasks, but they approach the problem differently.

---

## Filtering Related Data

I practised adding additional conditions to queries.

For example, I wanted only Michael's Tasks where the priority was 4 or higher.

This required combining conditions.

Conceptually:

`Task belongs to Michael`

AND

`Task priority >= 4`

The query filters the Task table before returning the results.

This is useful because the database performs the filtering instead of loading every Task and filtering later in Python.

The general mental model is:

`select(Task)`

then:

`where(condition)`

then:

`session.scalars(...).all()`

---

## Introduction to SQLAlchemy JOIN

The main new concept today was SQLAlchemy JOINs.

A JOIN allows related tables to be combined in a query.

For example, instead of finding Sarah's ID first and then querying Tasks by `user_id`, I can join the Task table to the User table and filter using Sarah's name.

Conceptually:

`Task`

JOIN

`User`

WHERE

`User.name == "Sarah"`

The ORM version uses the configured relationship.

For example:

`.join(Task.user)`

This tells SQLAlchemy to join the Task table to the User table using the `Task.user` relationship.

Because SQLAlchemy already knows the relationship between:

`Task.user_id`

and:

`User.id`

I do not need to manually write the SQL join condition.

---

## Connecting SQLAlchemy JOINs to Raw SQL

One of the most important things I reinforced today is that SQLAlchemy JOINs are still based on normal SQL concepts.

In raw SQL, the relationship would conceptually look like:

`tasks.user_id = users.id`

In SQLAlchemy ORM, the same relationship can be represented using:

`.join(Task.user)`

The ORM already knows the connection because the models contain:

`ForeignKey("users.id")`

and:

`relationship()`

This showed me that SQLAlchemy does not remove the need to understand SQL.

It simply gives me a Python-based way of expressing the same database operations.

---

## Querying Sarah's Tasks With a JOIN

I practised retrieving Tasks belonging to Sarah using a JOIN.

Instead of directly querying by a known `user_id`, I used the User model in the query condition.

The logic was:

- select Task objects
- join Task to User
- filter where User.name is Sarah

This is useful in situations where the filtering condition comes from the related table rather than the Task table itself.

For example:

finding Tasks by User name

finding Orders by Customer email

finding Posts by Author name

The same relational idea can be applied to many backend systems.

---

## Combining JOINs With Additional Filters

I also combined a JOIN with another condition.

For example:

Sarah's Tasks

with:

priority >= 4

This required filtering using columns from both related models.

The query conceptually used:

User condition:

`User.name == "Sarah"`

Task condition:

`Task.priority >= 4`

This demonstrated how relational queries can filter across multiple tables at the same time.

---

## Selecting Multiple ORM Entities

Another new concept was querying both User and Task in the same query.

Instead of:

`select(Task)`

I used:

`select(User, Task)`

This changes the result structure.

With:

`select(Task)`

each result represents one Task ORM object.

With:

`select(User, Task)`

each result row contains:

`User object + Task object`

This allowed me to print output such as:

`Michael -> Study FastAPI`

`Sarah -> Learn Docker`

This is useful when the application needs information from both sides of a relationship.

---

## session.scalars() vs session.execute()

Today I gained a better understanding of when to use `session.scalars()` and when to use `session.execute()`.

When the query selects one main ORM entity:

`select(Task)`

I can use:

`session.scalars(statement).all()`

This gives me Task objects directly.

The mental model is:

Query:

`Task`

Result:

`Task`

`Task`

`Task`

However, if the query selects multiple ORM entities:

`select(User, Task)`

I use:

`session.execute(statement).all()`

The result contains rows with multiple objects.

The mental model becomes:

`(User, Task)`

`(User, Task)`

`(User, Task)`

This is why I can write:

`for user, task in results`

Each result row is unpacked into one User ORM object and one Task ORM object.

---

## Important Difference Between Entity and Column

I also corrected an important misunderstanding today.

`select(User, Task)` does not mean that I am selecting two columns.

I am selecting two ORM entities.

A User entity represents the User model and its mapped columns.

A Task entity represents the Task model and its mapped columns.

Therefore:

`select(User, Task)`

returns both ORM objects in each result row.

This is different from selecting individual columns such as:

`select(User.name, Task.title)`

which would return individual values instead of complete ORM objects.

---

## Why .join(Task.user) Works

I learned why SQLAlchemy can automatically determine the JOIN condition.

The Task model defines:

`ForeignKey("users.id")`

This tells SQLAlchemy that:

`Task.user_id`

references:

`User.id`

The model also defines:

`Task.user`

through `relationship()`.

Therefore, when I write:

`.join(Task.user)`

SQLAlchemy already knows which tables and columns should be connected.

I do not need to manually write:

`Task.user_id == User.id`

every time.

---

## Relationship Traversal vs Explicit JOIN

Today I clearly separated two concepts that initially felt similar.

Relationship traversal means navigating through ORM objects.

Examples:

`user.tasks`

`task.user`

This is useful when I already have one ORM object and want to access its related data.

An explicit JOIN means building a database query that combines related tables.

Example concept:

`select(Task).join(Task.user)`

This is useful when I want the database to search, combine, and filter data across related tables.

The mental model is:

Relationship traversal:

`Object -> related object`

Explicit JOIN:

`Database query -> combine related tables`

Neither approach is always better.

The correct choice depends on what the application is trying to do.

---

## Querying With Related Table Conditions

One major improvement from today was understanding that JOINs become especially useful when the filtering condition comes from another table.

For example:

If I already know Michael's ID:

`Task.user_id == michael_id`

is simple and direct.

But if I only know:

`User.name == "Michael"`

then a JOIN makes more sense.

The query can connect User and Task, then filter using the User's name.

This is a common pattern in real backend applications.

---

## Final Challenge

The final challenge combined all the main concepts from today.

The requirement was to find:

all Tasks with priority 4 or higher

belonging to:

Michael

using a JOIN.

This required:

- selecting Task
- joining Task to User
- filtering the User by name
- filtering Task by priority

This exercise showed how conditions from multiple related tables can be combined in one query.

---

## Mistakes I Corrected Today

I initially made several mistakes while writing the relationship queries.

I wrote queries that selected User when the requirement was to return Task objects.

I also wrote priority filters without including the correct User condition.

Some JOIN queries were created but never executed.

I initially used:

`select(User).join(User.tasks)`

when some tasks specifically required:

`select(Task).join(Task.user)`

I also misunderstood `select(User, Task)` as selecting two table columns instead of selecting two ORM entities.

Another issue was not properly distinguishing between relationship traversal and explicit database queries.

Correcting these mistakes helped reinforce the purpose of each query structure.

---

## Key Query Patterns Learned

### Relationship Traversal

`user.tasks`

Use when I already have the User ORM object and want its related Tasks.

---

### Explicit Foreign Key Filtering

`select(Task).where(Task.user_id == user.id)`

Use when I want to directly query Tasks using the related User's ID.

---

### Relationship JOIN

`select(Task).join(Task.user)`

Use when I need to query Tasks while also using information from the User table.

---

### JOIN With Related Table Filter

Conceptually:

Task JOIN User

WHERE User.name matches a value

This allows filtering Task rows based on User information.

---

### Selecting Multiple Entities

`select(User, Task)`

Use when I need both User and Task ORM objects in each result.

---

## Important Mental Model

The key relationship remains:

`tasks.user_id -> users.id`

SQLAlchemy maps that relationship into:

`Task.user`

and:

`User.tasks`

From there:

`user.tasks`

means:

navigate from User to related Tasks

`task.user`

means:

navigate from Task to related User

`select(Task).join(Task.user)`

means:

ask the database to combine Task and User using their configured relationship

`select(User, Task)`

means:

return both ORM entities in each result row

---

## Progress From Day 38 to Day 39

Day 38 focused on creating and manipulating related ORM objects.

I learned how to:

- assign a User directly to a Task
- append Tasks to a User's task collection
- navigate from User to Tasks
- navigate from Task to User
- understand `user_id` versus `user`

Day 39 focused on querying those relationships.

I can now:

- retrieve related Tasks using `user.tasks`
- explicitly query Tasks using `user_id`
- apply multiple filters
- perform SQLAlchemy JOINs
- filter using fields from related tables
- select multiple ORM entities
- understand `session.scalars()` versus `session.execute()`
- distinguish relationship traversal from database JOIN queries

This moves my SQLAlchemy knowledge closer to real backend database operations.

---

## Key Concepts Learned

Today I learned and reinforced:

- SQLAlchemy `select()`
- SQLAlchemy `where()`
- SQLAlchemy `join()`
- relationship traversal
- explicit foreign key filtering
- querying related data
- combining multiple query conditions
- filtering across related tables
- selecting one ORM entity
- selecting multiple ORM entities
- `session.scalars()`
- `session.execute()`
- result row unpacking
- User and Task JOINs
- ORM entities versus individual columns
- relationship-based join inference
- applying SQL knowledge inside SQLAlchemy ORM

---

## Completion Checklist

- [x] Retrieved Michael using `session.get()`
- [x] Accessed Michael's Tasks using `michael.tasks`
- [x] Queried Michael's Tasks using `select(Task)`
- [x] Filtered Tasks using `Task.user_id`
- [x] Queried Michael's Tasks with priority >= 4
- [x] Used `.join(Task.user)`
- [x] Queried Sarah's Tasks through a JOIN
- [x] Combined User and Task filtering conditions
- [x] Queried Sarah's Tasks with priority >= 4
- [x] Used `select(User, Task)`
- [x] Used `session.execute()`
- [x] Unpacked User and Task result rows
- [x] Understood `session.scalars()` vs `session.execute()`
- [x] Completed the JOIN final challenge
- [x] Corrected the Day 39 Q&A
- [x] Reinforced raw SQL JOIN concepts through SQLAlchemy

---

## Overall Review

Day 39 was mainly about turning my SQLAlchemy relationship knowledge into actual database queries.

The most important thing I learned is that ORM relationships are not only useful for navigating objects such as `user.tasks` and `task.user`. They can also be used to build relational database queries through SQLAlchemy JOINs.

I also gained a clearer understanding of when to query using a foreign key directly and when a JOIN is more appropriate.

The biggest improvement today was connecting my earlier SQL knowledge with ORM syntax.

Raw SQL concepts such as:

JOIN

WHERE

foreign keys

and filtering across tables

still exist in SQLAlchemy.

SQLAlchemy simply allows me to express those ideas using Python objects and relationships.

**Day 39: Completed**