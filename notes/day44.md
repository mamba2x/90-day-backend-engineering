# Day 44 - Relationship Loading, N+1 Queries and Eager Loading

## Overview

Today I moved from simply knowing how to create and query SQLAlchemy relationships to understanding how those relationships are actually loaded from the database.

In previous lessons, I learned how to create relationships such as:

User

↓

Projects

↓

Tasks

I also learned how to navigate those relationships using ORM attributes such as:

`user.projects`

`project.tasks`

`task.project`

However, today I learned that simply accessing a relationship does not mean that SQLAlchemy already retrieved that related data from the database.

The way related data is loaded matters because poorly planned relationship loading can cause an application to execute far more database queries than necessary.

The major concepts covered today were:

- lazy loading
- eager loading
- the N+1 query problem
- `selectinload()`
- `joinedload()`
- relationship loading strategies
- collection relationships
- scalar relationships
- explicit JOINs vs eager-loading JOINs
- multi-level eager loading
- observing generated SQL
- using `echo=True`
- query count awareness
- ORM performance
- class vs object vs collection handling

The most important lesson today was:

A query can be logically correct while still being inefficient.

Therefore, backend development is not only about returning the correct data.

I must also understand how much database work is required to retrieve that data.

---

## Relationship Loading

SQLAlchemy relationships allow me to navigate between related ORM objects.

For example:

`project.tasks`

allows me to retrieve the Tasks associated with a Project.

Likewise:

`task.project`

allows me to retrieve the Project associated with a Task.

However, these relationships represent data stored in different database tables.

For example:

Projects are stored in:

`projects`

while Tasks are stored in:

`tasks`

The relationship exists because:

`tasks.project_id`

references:

`projects.id`

Therefore, when Python accesses:

`project.tasks`

SQLAlchemy may need to perform additional database work to retrieve those Task rows.

This introduced the concept of relationship loading strategies.

---

## Lazy Loading

Lazy loading means that related data is not necessarily retrieved when the original object is first loaded.

Instead, SQLAlchemy waits until the relationship is actually accessed.

Conceptually:

Retrieve Project

↓

Project object exists

↓

Tasks have not necessarily been retrieved

↓

Access `project.tasks`

↓

SQLAlchemy retrieves related Tasks

The word "lazy" therefore means:

Do not retrieve the relationship until it is needed.

This can be convenient because the application does not automatically retrieve related data that it may never use.

For example, if I only need:

`project.name`

then retrieving every Task belonging to the Project may be unnecessary.

Lazy loading allows that extra work to be postponed.

However, this convenience can create serious performance problems when relationships are accessed repeatedly inside loops.

---

## The N+1 Query Problem

The major performance problem introduced today was the N+1 query problem.

Suppose the application retrieves 100 Projects.

The first query retrieves those Projects.

Conceptually:

1 query

↓

Retrieve 100 Projects

Then my Python code loops through those Projects and accesses:

`project.tasks`

for every Project.

If lazy loading causes one additional query for each Project, SQLAlchemy may execute:

1 query for Projects

+

100 queries for Tasks

=

101 queries

This is the N+1 query problem.

The general pattern is:

1 initial query

+

N additional queries

where N represents the number of parent objects.

Therefore:

10 Projects

↓

Approximately 11 queries

100 Projects

↓

Approximately 101 queries

1,000 Projects

↓

Approximately 1,001 queries

This can become extremely expensive as an application's data grows.

---

## Why N+1 Is Dangerous

One reason the N+1 problem is dangerous is that the Python code causing it can look completely normal.

For example:

Loop through Projects

↓

Loop through each Project's Tasks

There is nothing obviously wrong with this logic.

The application may also work perfectly during development when the database contains only a few records.

For example:

3 Projects

may result in only a few additional queries.

The performance problem may therefore be difficult to notice.

However, if the production database later contains:

1,000 Projects

or:

100,000 Projects

the same code can create a huge amount of unnecessary database traffic.

This means backend developers must think about both:

Correctness

and:

Database Efficiency

---

## My Lazy Loading Experiment

Today I deliberately retrieved Projects without specifying an eager-loading strategy.

I then traversed each Project and accessed its Tasks.

The purpose was not simply to print the data.

The purpose was to observe what SQLAlchemy did behind the scenes.

This helped me understand that accessing:

`project.tasks`

can cause database queries.

The experiment also revealed an important mistake in my original code.

I initially placed the Task loop outside the Project loop.

Conceptually, my code behaved like:

Loop through every Project

↓

Finish loop

↓

Take the final Project

↓

Access only that Project's Tasks

This meant I was not actually testing relationship loading across every Project.

After correcting the indentation, the structure became:

For each Project

↓

Print Project

↓

For each Task belonging to that Project

↓

Print Task

This caused the relationship to be accessed for every Project and allowed me to properly observe the potential N+1 behaviour.

---

## Why Indentation Changed the Experiment

Python indentation controls which statements belong to a loop.

This means:

Project Loop

then:

Task Loop outside Project Loop

is completely different from:

Project Loop

↓

Task Loop inside Project Loop

In the first case, the Task relationship is only accessed after the Project loop finishes.

At that point, the `project` variable still refers to the last Project processed.

Therefore, only that Project's Tasks are accessed.

In the corrected version, every Project's Task relationship is accessed.

This was important because the purpose of the experiment was to see how SQLAlchemy behaves when multiple parent relationships are traversed.

---

## Eager Loading

Eager loading is a different relationship-loading strategy.

Instead of waiting until Python accesses a relationship, I can tell SQLAlchemy in advance:

"I know I am going to need this related data."

SQLAlchemy can then retrieve the relationship more deliberately.

Conceptually:

Build Query

↓

Tell SQLAlchemy which relationships are needed

↓

Execute Query

↓

Retrieve Parent Data

+

Related Data

↓

Use Relationships Without Triggering the same N+1 pattern

The goal is to avoid unnecessary repeated queries.

---

## selectinload()

The first eager-loading strategy I learned today was:

`selectinload()`

For example:

`selectinload(Project.tasks)`

means that when Projects are retrieved, SQLAlchemy should also efficiently load their related Tasks.

The basic mental model is:

Query 1

↓

Retrieve Projects

Then:

Query 2

↓

Retrieve Tasks whose `project_id` belongs to those Projects

Conceptually, the second query may behave like:

WHERE project_id IN (...)

This means SQLAlchemy can retrieve Tasks for multiple Projects together rather than issuing one Task query for every individual Project.

For example, instead of:

1 Project query

+

100 Task queries

=

101 queries

the basic `selectinload()` strategy can be closer to:

1 Project query

+

1 related Tasks query

=

2 queries

For very large parent sets, SQLAlchemy may batch the related SELECT operations rather than always producing literally one secondary query, but the important concept remains the same:

`selectinload()` avoids the one-query-per-parent pattern.

---

## Why selectinload() Is Useful for Collections

`Project.tasks` is a collection relationship.

One Project can have many Tasks.

Conceptually:

Project

↓

Task 1

Task 2

Task 3

Task 4

Because multiple parent Projects may each have multiple related Tasks, `selectinload()` can efficiently retrieve the related collections using the parent IDs.

A useful starting mental model is:

One-to-Many Collection

↓

`selectinload()`

is often a strong option

This is not an absolute rule, but it is a useful default idea when learning relationship-loading strategies.

---

## joinedload()

The second eager-loading strategy I learned today was:

`joinedload()`

Instead of retrieving the relationship through a separate SELECT strategy, `joinedload()` can load the related object using a SQL JOIN.

For example:

`joinedload(Task.project)`

means:

Retrieve Tasks

and also:

Load their related Projects

using an eager-loading JOIN.

This is useful because:

`Task.project`

represents one related Project object.

The relationship is:

Many Tasks

↓

One Project

Therefore, retrieving a Task together with its Project can be a reasonable use case for `joinedload()`.

---

## Collection vs Scalar Relationships

Today I reinforced an important distinction between collection relationships and scalar relationships.

For example:

`project.tasks`

represents:

Many Tasks

Therefore it is a collection.

It can be looped over.

Conceptually:

Project

↓

[Task, Task, Task]

However:

`task.project`

represents:

One Project

Therefore it is a scalar relationship.

It is one ORM object, not a collection.

This means:

Looping through `project.tasks`

makes sense.

But:

Looping through `task.project`

does not.

Instead, I access attributes directly:

`task.project.name`

This corrected one of the mistakes in my original code.

---

## Nullable Relationships

My Task model currently allows:

`project_id`

to be nullable.

This was introduced previously for migration safety because older Tasks may not belong to Projects.

Therefore:

`task.project`

can potentially be:

`None`

This means that when accessing:

`task.project.name`

I should account for the possibility that no Project exists.

The mental model is:

If project_id contains a valid Project ID

↓

task.project is a Project object

If project_id is NULL

↓

task.project may be None

This reinforces the connection between database nullability and Python application behaviour.

---

## selectinload() vs joinedload()

Today I learned that neither loading strategy is universally better.

They solve the same broad problem in different ways.

A useful starting mental model is:

Collection relationship:

`Project.tasks`

↓

`selectinload()` is often useful

Single related object:

`Task.project`

↓

`joinedload()` can be useful

However, the correct strategy depends on:

- relationship cardinality
- amount of data
- database engine
- number of parent records
- number of child records
- network/database latency
- query shape
- application workload

Therefore, I should not memorise:

"Always use selectinload."

or:

"Always use joinedload."

Instead, I should understand what SQL each strategy generates and evaluate the result.

---

## Explicit join() vs joinedload()

Today I also learned that:

`join()`

and:

`joinedload()`

are not the same thing.

An explicit JOIN is primarily part of the query logic.

For example, I may JOIN Task to Project because I want to filter Tasks based on information stored in the Project table.

Conceptually:

Retrieve Tasks

↓

JOIN Projects

↓

WHERE Project.name = "API Project"

Here, Project participates in determining which Task rows should be returned.

The JOIN is part of the query logic.

`joinedload()` has a different purpose.

It tells SQLAlchemy:

"I am going to need this relationship, so load it eagerly."

Therefore, my mental model is:

`join()`

↓

Query logic

while:

`joinedload()`

↓

Relationship-loading strategy

The SQL generated internally may involve JOINs in both situations, but their ORM purposes are different.

---

## Multi-Level Eager Loading

Yesterday I built the relationship:

User

↓

Projects

↓

Tasks

Today I learned how to eagerly load relationships across multiple levels.

Conceptually:

Retrieve User

↓

Load User's Projects

↓

Load each Project's Tasks

This can be expressed through chained loading strategies.

The relationship graph is:

User.projects

↓

Project.tasks

This allows SQLAlchemy to know in advance that my application intends to traverse:

User

↓

Project

↓

Task

Instead of blindly traversing relationships and potentially generating repeated lazy-loading queries, I can plan the required object graph before executing the query.

---

## Why Multi-Level Loading Matters

Imagine an API endpoint that returns:

User

↓

Projects

↓

Tasks

Without thinking about relationship loading, serialization could access:

`user.projects`

and then:

`project.tasks`

for every Project.

Depending on the loading configuration, this could generate many additional database queries.

By specifying the required relationships upfront, I can make the database-access strategy more deliberate.

This is particularly important for nested API responses.

---

## Class vs Object vs Collection

One of the major practical mistakes I corrected today was confusing ORM classes, individual ORM objects, and collections of ORM objects.

For example:

`User`

represents the ORM class.

It describes the User model.

Conceptually:

User

↓

Blueprint

After querying the database, I may receive:

`user`

which represents:

One User ORM object

If I retrieve multiple Users:

`users`

represents:

A collection of User ORM objects

Therefore:

User

↓

Class

user

↓

One object

users

↓

Collection of objects

The same applies to Projects:

Project

↓

ORM class

project

↓

One Project object

projects

↓

Collection of Project objects

And Tasks:

Task

↓

ORM class

task

↓

One Task object

tasks

↓

Collection of Task objects

This distinction is important because Python loops require iterable objects.

I cannot simply write:

Loop through User

because `User` is the ORM class.

Instead, I execute a query and receive a collection:

users

Then:

Loop through users

↓

Each item is one user

---

## Nested Loop Structure

The multi-level relationship also helped reinforce how nested loops should reflect the relationship hierarchy.

Conceptually:

Users

↓

For each User

↓

User's Projects

↓

For each Project

↓

Project's Tasks

↓

For each Task

This produces the structure:

User

    Project

        Task
        Task

    Project

        Task
        Task

The indentation of the Python code should mirror this hierarchy.

This is particularly important when working with nested ORM relationships.

---

## SQL Query Construction vs Execution

Today also reinforced the distinction between constructing a SQLAlchemy query and actually executing it.

Creating:

`select(Project)`

does not immediately retrieve Projects.

It creates a SQL statement object.

The mental model is:

Build SELECT Statement

↓

SQL Description Exists

Then:

Execute Through Session

↓

Database Runs Query

Then:

Retrieve Results

↓

ORM Objects

Therefore:

`select(...)`

means:

Construct Query

while:

`session.scalars(...)`

means:

Execute and retrieve scalar ORM results

and:

`.all()`

means:

Collect all returned results

This distinction is important because ORM code separates query construction from database execution.

---

## Session Usage

I also reinforced correct SQLAlchemy Session usage.

The correct mental model is:

`Session`

↓

Session class

while:

`Session(engine)`

↓

Actual Session connected to my database engine

Therefore, database work should happen through a Session instance connected to the engine.

This corrected another mistake in my original attempt where I used the Session class itself rather than constructing a Session.

---

## Using echo=True

One of the most useful tools today was:

`echo=True`

When creating the SQLAlchemy engine with SQL echo enabled, SQLAlchemy prints generated SQL statements to the terminal.

Previously, this mainly helped me see what SQLAlchemy was doing.

Today it became an important performance-learning tool.

I can compare:

Lazy Loading

against:

`selectinload()`

against:

`joinedload()`

and actually observe the SQL being executed.

This means I do not have to rely entirely on assumptions.

I can inspect the ORM's behaviour.

---

## Observing N+1 with echo=True

The lazy-loading experiment allows me to observe a pattern such as:

Retrieve Projects

↓

SQL query

Then:

Access Project 1 Tasks

↓

Another SQL query

Access Project 2 Tasks

↓

Another SQL query

Access Project 3 Tasks

↓

Another SQL query

This makes the N+1 problem visible.

Without observing generated SQL, the Python code may look harmless.

With SQL logging enabled, I can see that relationship access can have database consequences.

This introduced an important backend habit:

Do not judge database performance only by looking at Python code.

Inspect the database operations as well.

---

## Comparing Lazy Loading and selectinload()

The major comparison today was:

Lazy Loading:

Retrieve Projects

↓

Access Project 1 Tasks

↓

Query

Access Project 2 Tasks

↓

Query

Access Project 3 Tasks

↓

Query

and so on.

Compared with:

`selectinload()`

Retrieve Projects

↓

Retrieve related Tasks using Project IDs

↓

Relationships available for traversal

The second approach can significantly reduce query count when many parent objects require the same relationship.

This is why eager loading can be extremely important in APIs.

---

## The 1,000 Project Example

Today's challenge considered:

1,000 Projects

with:

20 Tasks per Project

Using an N+1 pattern could potentially result in approximately:

1 query

for the Projects

plus:

1,000 queries

for their Task collections

giving approximately:

1,001 queries

This demonstrates why N+1 can become extremely expensive at scale.

The number of Tasks per Project does not mean there must be one query per Task.

The N in this example represents the number of parent Projects whose Task relationships are lazily loaded.

---

## Why JOIN Everything Is Not Automatically the Answer

It may seem that the solution to database performance is simply:

JOIN everything.

However, today I learned why that is not necessarily ideal either.

Suppose:

1 Project

has:

20 Tasks

A JOIN between Projects and Tasks can produce rows conceptually like:

Project A + Task 1

Project A + Task 2

Project A + Task 3

...

Project A + Task 20

The Project information may therefore be repeated across many result rows.

With:

1,000 Projects

and:

20 Tasks each

the joined result may contain approximately:

20,000 rows

with parent information repeated across those rows.

This does not mean JOINs are bad.

It means JOINs also have costs.

Therefore:

Avoid N+1

does not mean:

JOIN absolutely everything.

---

## Performance Decisions Should Be Measured

One of today's broader lessons was that database performance decisions should not be based purely on theory.

Useful reasoning can help me choose an initial strategy.

For example:

Collection

↓

Consider `selectinload()`

Scalar Relationship

↓

Consider `joinedload()`

But production decisions should also consider actual evidence.

This can include:

- generated SQL
- query count
- EXPLAIN plans
- indexes
- realistic dataset sizes
- query timings
- database workload
- response times
- memory usage
- amount of transferred data

Therefore, backend optimisation should follow a process such as:

Understand Query Pattern

↓

Choose Reasonable Strategy

↓

Inspect Generated SQL

↓

Measure

↓

Compare Alternatives

↓

Optimise Based on Evidence

---

## Why ORMs Do Not Remove the Need to Understand SQL

SQLAlchemy allows me to work with Python objects instead of manually writing SQL for every operation.

However, the database still executes SQL.

Therefore, using an ORM does not remove concepts such as:

- SELECT
- JOIN
- WHERE
- indexes
- foreign keys
- transactions
- query plans
- query counts
- result-set sizes

An ORM provides an abstraction.

It does not make database behaviour disappear.

This is why understanding SQL remains important even when using SQLAlchemy.

---

## Application Correctness vs Performance

One of the most important mental models from today is:

Correct Endpoint

does not automatically mean:

Efficient Endpoint

An API endpoint can:

- return HTTP 200
- return the correct JSON
- pass its tests
- appear completely functional

while still performing hundreds of unnecessary database queries.

Therefore, production backend engineering requires several dimensions of correctness.

The application should be:

Functionally Correct

and:

Data Correct

and:

Secure

and:

Efficient

Today's lesson focused mainly on the efficiency part.

---

## Connection to Database Indexes

Day 42 focused on indexes.

Indexes help answer the question:

"How can the database execute a particular query more efficiently?"

Day 44 introduced a different question:

"Why is my application executing so many queries in the first place?"

These are different performance problems.

For example:

Problem A:

One query is slow.

Potential solution:

Improve indexing or query design.

Problem B:

Application executes 1,001 queries unnecessarily.

Potential solution:

Improve ORM relationship loading.

Therefore:

Indexes

↓

Improve certain individual query patterns

while:

Eager Loading

↓

Can reduce unnecessary query count

Both are important parts of database performance.

---

## Mistakes I Corrected Today

### Mistake 1 - Incorrect Loop Indentation

My biggest mistake was placing the Task loop outside the Project loop.

This meant I only accessed the Task relationship for the final Project rather than every Project.

I corrected the nesting so that each Project's Tasks are traversed inside the Project loop.

This allowed the N+1 experiment to work correctly.

---

### Mistake 2 - Misinterpreting the Query Count

Because my original loop only accessed the final Project's Tasks, I observed one Task query and concluded that only one query occurred.

After correcting the loop, I understood that the experiment must access every Project's Task collection before I can properly observe the N+1 pattern.

This reinforced the importance of validating experiments before drawing conclusions from them.

---

### Mistake 3 - Not Traversing selectinload() Results

I correctly wrote the `selectinload(Project.tasks)` query, but initially did not traverse the Tasks afterward.

I corrected this by looping through each Project and its Tasks.

This allowed me to compare the eager-loading behaviour against the lazy-loading experiment.

---

### Mistake 4 - Confusing User Results with Project Results

I queried:

User

but stored the returned collection using a misleading Project variable name.

I corrected this by using:

users

for a collection of User objects.

This reinforced:

Class

vs:

Object

vs:

Collection

---

### Mistake 5 - Trying to Iterate Over task.project

I initially treated:

`task.project`

as though it were a collection.

However:

Task

↓

belongs to one Project

Therefore:

`task.project`

is one Project object.

I corrected this by directly accessing:

`task.project.name`

while also accounting for the possibility that the Project is `None`.

---

### Mistake 6 - Incorrect Session Construction

I initially used the Session class directly.

I corrected this by constructing a Session using the database engine.

This reinforced:

Session

↓

Class

Session connected to Engine

↓

Actual database Session

---

### Mistake 7 - Iterating Over ORM Classes

I attempted to loop directly over:

User

Project

and relationship definitions.

I corrected this by understanding that ORM classes are model definitions, not collections of database records.

The correct flow is:

Execute Query

↓

Receive Collection

↓

Loop Through Collection

For example:

User

↓

Class

users

↓

Queried collection

user

↓

One object from collection

---

## Important Mental Models

### Lazy Loading

Parent Retrieved

↓

Relationship Not Yet Needed

↓

Access Relationship

↓

Load Related Data

---

### N+1

1 Parent Query

+

N Relationship Queries

↓

Potential Performance Problem

---

### Eager Loading

Know Relationship Is Needed

↓

Tell SQLAlchemy Upfront

↓

Load Related Data Deliberately

↓

Avoid Repeated Lazy Queries

---

### selectinload()

Retrieve Parents

↓

Collect Parent IDs

↓

Retrieve Related Rows Using Parent IDs

↓

Populate Relationships

---

### joinedload()

Retrieve Main Entity

↓

JOIN Related Entity for Loading

↓

Relationship Available

---

### Collection Relationship

`project.tasks`

↓

Many Tasks

↓

Iterable

---

### Scalar Relationship

`task.project`

↓

One Project or None

↓

Not a collection

---

### ORM Naming

User

↓

Class

user

↓

One User

users

↓

Collection of Users

---

### Multi-Level Loading

User

↓

Projects

↓

Tasks

---

### Explicit JOIN

JOIN

↓

Query Logic

↓

Filter / Sort / Query Across Tables

---

### joinedload()

joinedload

↓

Loading Strategy

↓

Retrieve Related Object Eagerly

---

### Performance Investigation

Application Code

↓

Generated SQL

↓

Query Count

↓

Query Plan / Behaviour

↓

Measurement

↓

Optimisation

---

## Key Concepts Learned

Today I learned and reinforced:

- relationship loading
- lazy loading
- eager loading
- N+1 queries
- query-count awareness
- `selectinload()`
- `joinedload()`
- collection eager loading
- scalar eager loading
- multi-level eager loading
- `User.projects`
- `Project.tasks`
- `Task.project`
- nested relationship traversal
- collection vs scalar relationships
- nullable relationships
- explicit JOIN vs joinedload
- query construction vs execution
- ORM class vs ORM object
- ORM object vs collection
- Session construction
- nested Python loops
- importance of indentation
- SQLAlchemy SQL logging
- `echo=True`
- inspecting generated SQL
- performance measurement
- JOIN row duplication
- avoiding unnecessary relationship loading
- ORM performance in APIs
- database performance at scale

---

## Progress From Day 43 to Day 44

Day 43 focused on creating a richer relational structure:

User

↓

Project

↓

Task

I learned how to:

- create the Project model
- connect User to Projects
- connect Projects to Tasks
- create foreign keys
- create ORM relationships
- query those relationships
- perform multi-level JOINs
- reason about ownership consistency

Day 44 asked the next logical question:

"When I traverse those relationships, how does SQLAlchemy actually retrieve the related data?"

This introduced relationship-loading performance.

The progression is:

Day 37

↓

Create Relationships

Day 38

↓

Create Related Objects

Day 39

↓

Query Relationships and JOINs

Day 40

↓

Manage Schema Changes with Alembic

Day 41

↓

Make Migrations Safer

Day 42

↓

Improve Query Performance with Indexes

Day 43

↓

Build Multi-Level Relationships

Day 44

↓

Load Those Relationships Efficiently

The lessons are now starting to combine database design, ORM behaviour and performance.

---

## Completion Checklist

### Relationship Loading

- [x] Understood relationship loading
- [x] Understood lazy loading
- [x] Understood eager loading
- [x] Understood when related data may require additional SQL

### N+1

- [x] Understood the N+1 query problem
- [x] Understood 1 + N query behaviour
- [x] Understood why N+1 can be difficult to notice
- [x] Understood why N+1 becomes dangerous at scale
- [x] Corrected the lazy-loading experiment

### selectinload()

- [x] Imported selectinload
- [x] Used selectinload(Project.tasks)
- [x] Understood parent query + related SELECT strategy
- [x] Understood why selectinload is useful for collections
- [x] Traversed eagerly loaded Task collections

### joinedload()

- [x] Imported joinedload
- [x] Used joinedload(Task.project)
- [x] Understood joined eager loading
- [x] Understood why Task.project is scalar
- [x] Accounted for nullable Project relationships

### Multi-Level Loading

- [x] Loaded User.projects
- [x] Loaded Project.tasks
- [x] Chained selectinload strategies
- [x] Traversed User → Project → Task
- [x] Understood nested object graphs

### ORM Fundamentals

- [x] Reinforced class vs object
- [x] Reinforced object vs collection
- [x] Reinforced Session construction
- [x] Reinforced query construction
- [x] Reinforced query execution
- [x] Reinforced relationship traversal

### Performance

- [x] Used echo=True
- [x] Observed generated SQL
- [x] Compared lazy and eager-loading strategies
- [x] Understood query count as a performance concern
- [x] Understood that JOINing everything also has costs
- [x] Understood the importance of measuring realistic workloads

### Corrections

- [x] Corrected loop indentation
- [x] Corrected N+1 experiment
- [x] Corrected missing selectinload traversal
- [x] Corrected misleading variable naming
- [x] Corrected scalar relationship iteration
- [x] Corrected Session usage
- [x] Corrected ORM class iteration
- [x] Completed shortened Day 44 Q&A

---

## Overall Review

Day 44 introduced an important shift in how I think about ORM code.

Previously, my main concern was:

"Can I retrieve the correct related objects?"

Now I also need to ask:

"How did SQLAlchemy retrieve those objects?"

This matters because ORM relationship traversal can hide database queries behind ordinary-looking Python attribute access.

A simple expression such as:

`project.tasks`

can potentially cause SQLAlchemy to communicate with the database.

When this happens repeatedly inside a loop, it can create the N+1 query problem.

I learned that eager-loading strategies allow me to plan relationship loading more deliberately.

`selectinload()` can be particularly useful when loading collections such as:

Project

↓

Tasks

while `joinedload()` can be useful when retrieving a scalar related object such as:

Task

↓

Project

I also learned that these are not rigid rules.

Performance decisions depend on the actual workload.

The correct engineering process is not:

Memorise one loading strategy

↓

Use it everywhere

Instead:

Understand Relationship

↓

Understand Query Pattern

↓

Choose Loading Strategy

↓

Inspect Generated SQL

↓

Measure Performance

↓

Optimise Based on Evidence

The practical mistakes I made today were mostly related to Python loop structure and ORM object handling rather than misunderstanding the new SQLAlchemy loading concepts.

I correctly understood and used the important new operations:

`selectinload(Project.tasks)`

`joinedload(Task.project)`

and multi-level loading through:

User.projects

↓

Project.tasks

My biggest correction was understanding that the indentation of nested loops directly affects which relationships are accessed.

I also reinforced the distinction between:

User

as an ORM class,

user

as one ORM object,

and:

users

as a collection of ORM objects.

This distinction is important when working with query results and nested relationships.

The most important performance lesson from today is:

A working endpoint is not automatically an efficient endpoint.

An endpoint may return completely correct data while silently generating hundreds or thousands of unnecessary database queries.

Therefore, understanding the SQL generated by an ORM is an important part of becoming a backend engineer.

Day 42 taught me how to make certain queries faster using indexes.

Day 44 taught me that sometimes the bigger problem is that the application is executing far too many queries in the first place.

These are two different layers of database optimisation, and understanding both will become increasingly important as the applications I build become larger.

**Day 44: Completed after corrections**