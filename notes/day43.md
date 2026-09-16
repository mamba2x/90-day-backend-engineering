# Day 43 - Projects, Multi-Level Relationships and Relational Schema Design

## Overview

Today I extended my SQLAlchemy database from a simple User and Task structure into a more realistic multi-level relational model involving Users, Projects, and Tasks.

Before today, the main relationship in my application was:

User

↓

Tasks

Today I introduced a new `Project` model, which changed the structure into:

User

↓

Projects

↓

Tasks

This introduced another one-to-many relationship and allowed me to combine several concepts from previous lessons, including:

- SQLAlchemy ORM models
- foreign keys
- one-to-many relationships
- `relationship()`
- `back_populates`
- database indexes
- Alembic migrations
- migration safety
- nullable foreign keys
- SQLAlchemy Sessions
- persistence
- relationship traversal
- explicit SELECT queries
- JOINs
- multi-level JOINs
- relational schema design
- avoiding duplicated ownership information

The biggest lesson today was that relationships are not simply convenient Python attributes.

They represent actual relationships between tables in the relational database, and the way those relationships are designed can affect data consistency.

The main structure for today's application became:

User

↓

Project

↓

Task

At the database level:

users.id

↑

projects.user_id

and:

projects.id

↑

tasks.project_id

This allows the application to represent a User who owns multiple Projects, with each Project containing multiple Tasks.

---

## Introducing the Project Model

Today I created a new `Project` model.

The Project contains:

- id
- name
- user_id
- user
- tasks

The `id` is the Project's primary key.

The `name` stores the name of the Project.

The `user_id` column identifies which User owns the Project.

The `user` relationship allows Python code to navigate from a Project object to its related User object.

The `tasks` relationship allows Python code to navigate from a Project to all the Tasks belonging to it.

This gave me the structure:

User

1

↓

Many

Projects

This is a one-to-many relationship.

One User can own many Projects, while each Project belongs to one User.

---

## User and Project Relationship

The relationship between User and Project is:

One-to-Many.

Conceptually:

One User

↓

Many Projects

For example:

Michael

├── Backend Engineering
├── API Project
└── E-Commerce Platform

Michael is one User, but he can own several Projects.

At the SQLAlchemy ORM level, the relationship is represented in both directions.

From User:

`user.projects`

This returns the collection of Projects belonging to that User.

From Project:

`project.user`

This returns the single User associated with that Project.

Therefore:

`User.projects`

↓

Collection

while:

`Project.user`

↓

Single object

This is an important distinction in one-to-many relationships.

---

## Project and Task Relationship

I also created another one-to-many relationship between Project and Task.

Conceptually:

One Project

↓

Many Tasks

For example:

Backend Engineering

├── Study SQLAlchemy
└── Practice Alembic

The Backend Engineering Project contains multiple Tasks.

At the ORM level:

`project.tasks`

returns the collection of Tasks associated with that Project.

Meanwhile:

`task.project`

returns the single Project associated with a particular Task.

Therefore:

`Project.tasks`

↓

Collection of Task objects

while:

`Task.project`

↓

Single Project object

This follows the same one-to-many pattern I previously learned with User and Task.

---

## The Complete Relationship Structure

After introducing Projects, the main application relationship became:

User

↓

Projects

↓

Tasks

For example:

Michael

├── Backend Engineering
│   ├── Study SQLAlchemy
│   └── Practice Alembic
│
└── API Project
    ├── Build Authentication
    └── Add Rate Limiting

This represents a much more realistic application structure.

Instead of having all Tasks directly grouped under a User without additional organisation, Projects can now organise Tasks into meaningful groups.

---

## Database-Level Relationship Structure

At the database level, these relationships are implemented using foreign keys.

The Project table contains:

`user_id`

which references:

`users.id`

Therefore:

projects.user_id

↓

users.id

This means every Project can identify the User that owns it.

The Task table now contains:

`project_id`

which references:

`projects.id`

Therefore:

tasks.project_id

↓

projects.id

This means every Task can identify the Project that it belongs to.

Together, the relationship chain becomes:

tasks.project_id

↓

projects.id

projects.user_id

↓

users.id

Therefore, ownership can conceptually be followed through:

Task

↓

Project

↓

User

---

## Foreign Keys vs ORM Relationships

Today I reinforced the difference between foreign-key columns and SQLAlchemy ORM relationships.

For example:

`project_id`

is an actual database column.

It may contain a value such as:

`project_id = 4`

This means that the Task references Project 4.

Meanwhile:

`task.project`

does not simply return the number 4.

It returns the related Project ORM object.

Therefore:

`task.project_id`

↓

Database foreign-key value

while:

`task.project`

↓

Python Project ORM object

The same concept applies to Users.

`project.user_id`

might contain:

`1`

while:

`project.user`

returns the actual User ORM object representing User 1.

This gives me the mental model:

Foreign-Key Column

↓

Stored Database Value

ORM Relationship

↓

Python Object Navigation

---

## Understanding back_populates

I continued using `back_populates` to connect both sides of SQLAlchemy relationships.

For the User and Project relationship:

`User.projects`

is connected to:

`Project.user`

Conceptually:

User.projects

↕

Project.user

For the Project and Task relationship:

`Project.tasks`

is connected to:

`Task.project`

Conceptually:

Project.tasks

↕

Task.project

This allows SQLAlchemy to understand that both attributes represent opposite sides of the same relationship.

For example, if a Project belongs to Michael:

`project.user`

can return Michael.

At the same time:

`michael.projects`

can contain that Project.

The relationship can therefore be navigated from either direction.

---

## Adding project_id to Existing Tasks

One of the most important migration decisions today involved the new `project_id` column.

I defined it as nullable initially.

Conceptually:

`project_id = NULL`

is temporarily allowed.

This was necessary because the database may already contain Task rows that existed before Projects were introduced.

Those existing Tasks do not automatically know which Project they belong to.

If I immediately introduced:

`project_id NOT NULL`

the database could have existing rows without a valid value for the new column.

This could cause the migration to fail or leave existing data violating the new constraint.

Therefore, the safer initial migration is:

Add project_id

↓

Allow NULL

↓

Preserve Existing Tasks

↓

Assign Projects Later If Necessary

↓

Potentially Enforce NOT NULL Later

This directly applied the migration-safety concepts from Day 41.

---

## Connecting Day 41 Migration Safety to Day 43

Day 41 taught me that schema changes must account for existing data.

For example, adding a new required column to a populated table can be dangerous.

Today I applied that principle to a foreign key.

Instead of immediately requiring:

`project_id`

I allowed it to be nullable.

This means old Tasks can continue existing while the database schema evolves.

The important lesson is:

Schema Design

must consider:

Existing Data

not only:

Future Data

This is particularly important in production applications where tables may already contain thousands or millions of records.

---

## Indexing Project.user_id

I added an index to:

`projects.user_id`

The reason is not simply because `user_id` is a foreign key.

The reason is that the application is expected to frequently perform queries such as:

"Give me all Projects belonging to User X."

Conceptually:

WHERE user_id = ?

This makes `user_id` a reasonable index candidate.

The index can potentially help the database locate Projects belonging to a particular User more efficiently.

This applied the main lesson from Day 42:

Indexes should be based on query patterns.

Not simply:

"This column is important."

---

## Indexing Task.project_id

I also added an index to:

`tasks.project_id`

Again, the reason is based on query patterns.

A very common application operation could be:

"Give me every Task belonging to Project X."

Conceptually:

WHERE project_id = ?

Because this query may happen frequently, `project_id` is a reasonable index candidate.

The mental model remains:

Common Query

↓

Identify Filter Column

↓

Consider Index

↓

Define Through SQLAlchemy

↓

Generate Alembic Migration

↓

Inspect Migration

↓

Apply Migration

---

## Schema Evolution with Alembic

Today I continued using Alembic rather than relying on:

`Base.metadata.create_all(engine)`

This is important because my database already exists and has a migration history.

The schema has been evolving over multiple lessons.

Conceptually, my migration history now resembles:

Create Users and Tasks

↓

Add Description

↓

Add Due Date

↓

Add Indexes

↓

Add Projects and Project Relationship

↓

HEAD

This demonstrates why Alembic is important.

Instead of recreating the database every time the schema changes, Alembic records each schema change as part of an ordered migration history.

---

## Migration Inspection

Another important practice reinforced today was inspecting migrations before applying them.

Adding a Project model and Task relationship can require several schema operations.

Conceptually, the migration may need to:

Create Projects Table

↓

Create Project Foreign Key

↓

Create Project Index

↓

Add project_id to Tasks

↓

Create Task Project Index

↓

Create Task Project Foreign Key

This shows that one ORM change can result in several database-level changes.

Therefore, I should never blindly assume that an autogenerated migration is correct.

The workflow remains:

Change ORM Models

↓

Generate Migration

↓

Open Migration File

↓

Inspect upgrade()

↓

Inspect downgrade()

↓

Apply Migration

↓

Verify Current Revision

---

## SQLite Migration Considerations

I am currently using SQLite for these exercises.

SQLite has more restrictions around some schema-alteration operations than databases such as PostgreSQL.

This means Alembic migrations involving foreign keys and table changes may sometimes look different depending on the database engine.

The important skill is not memorising the exact generated migration code.

Instead, I should understand:

What does my database currently contain?

↓

What schema do my ORM models describe?

↓

What changes is Alembic proposing?

↓

Are those changes safe and correct?

This reasoning will remain useful even when I eventually move from SQLite to PostgreSQL.

---

## Creating Related ORM Objects

Today I created a User named Michael.

Michael owns two Projects:

- Backend Engineering
- API Project

Backend Engineering contains:

- Study SQLAlchemy
- Practice Alembic

API Project contains:

- Build Authentication
- Add Rate Limiting

Instead of manually hardcoding foreign-key IDs, I connected these objects using SQLAlchemy relationships.

For example:

Project

↓

`user=michael`

and:

Task

↓

`project=backend_engineering`

This allows SQLAlchemy to understand the relationships between the objects.

I do not need to manually guess or hardcode database-generated IDs.

---

## Why Hardcoding Foreign-Key IDs Is Usually a Bad Learning Pattern

Instead of creating a Project using something like:

`user_id = 1`

I can create it using:

`user = michael`

This is more ORM-oriented.

The same applies to Tasks.

Instead of:

`project_id = 3`

I can use:

`project = backend_engineering`

SQLAlchemy understands the configured relationship and eventually stores the correct foreign-key value when the objects are persisted.

This reduces reliance on assumptions about database-generated IDs.

---

## Object Creation Does Not Mean Persistence

One important mistake I corrected today involved creating Python objects without actually saving them to the database.

For example, creating:

Michael

Backend Engineering

API Project

Study SQLAlchemy

Practice Alembic

does not automatically mean those objects exist permanently in the database.

They initially exist as Python ORM objects.

The objects must become part of a SQLAlchemy Session and eventually be committed.

The mental model is:

Create ORM Object

↓

Python Memory

Then:

Add to Session

↓

SQLAlchemy Tracks Object

Then:

Commit

↓

Database Persistence

This is an important distinction.

---

## Session Creation

I also corrected how SQLAlchemy Sessions are created.

`Session`

itself is the class.

To create a database Session connected to my engine, I use:

`Session(engine)`

Therefore:

Session

↓

Class

while:

Session(engine)

↓

Actual Session connected to database engine

The Session manages the unit of work between my Python application and the database.

---

## Relationship Cascading During Persistence

Because my ORM objects are connected through relationships, adding a parent object such as Michael to the Session can also cause related new objects to be persisted through SQLAlchemy's normal relationship cascade behaviour.

Conceptually:

Michael

↓

Projects

↓

Tasks

If these new objects are connected correctly, SQLAlchemy can understand the entire object graph.

This allows ORM-based persistence to feel much more natural than manually inserting every foreign-key value.

However, I should still understand what is happening underneath.

The database ultimately stores rows and foreign-key values.

The ORM simply gives me a more object-oriented way of working with those relationships.

---

## Database-Generated IDs

I corrected another important issue involving primary-key IDs.

When I first create:

Michael

in Python, Michael may not immediately have a database-generated ID.

Before persistence:

`michael.id`

may be:

`None`

After SQLAlchemy inserts Michael into the database and the database generates the primary key, the ORM object can receive that ID.

Therefore, I should not rely on:

`michael.id`

before the object has actually been persisted.

The mental model is:

Create Michael

↓

ID may be None

↓

INSERT into Database

↓

Database Generates ID

↓

SQLAlchemy Receives ID

↓

michael.id now contains database ID

---

## Query 1 - Projects Belonging to Michael

One of today's tasks was retrieving all Projects belonging to Michael.

The query conceptually asks:

SELECT Projects

WHERE:

Project.user_id = Michael.id

This uses the foreign-key relationship between:

projects.user_id

and:

users.id

The expected results are:

Backend Engineering

API Project

This reinforced the connection between relational schema design and actual application queries.

---

## Query 2 - Relationship Traversal

I also retrieved Tasks through ORM relationship traversal.

Starting with:

Backend Engineering

I can navigate:

`backend_engineering.tasks`

This returns the Task collection associated with that Project.

Conceptually:

Backend Engineering

↓

tasks

↓

Study SQLAlchemy

Practice Alembic

This is relationship traversal.

I already have a Project ORM object and navigate through its configured relationship.

---

## Relationship Traversal vs Explicit Query

Today I reinforced the difference between:

`project.tasks`

and an explicit SQLAlchemy query filtering using `project_id`.

The first:

`project.tasks`

uses ORM relationship traversal.

Conceptually:

Existing Project Object

↓

Follow Relationship

↓

Related Tasks

The second approach constructs an explicit database query.

Conceptually:

SELECT Task

↓

WHERE project_id = Project.id

↓

Execute Through Session

↓

Receive Matching Tasks

Both approaches can retrieve related Tasks, but they represent different ways of interacting with the ORM.

---

## Building a SELECT Statement Does Not Execute It

Another important mistake I corrected today was creating SQLAlchemy SELECT statements without executing them.

Writing a SELECT statement only constructs the query.

Conceptually:

`select(Task)`

↓

Build Query

It does not automatically retrieve records.

The query must then be executed through the Session.

Conceptually:

Build Statement

↓

Execute Through Session

↓

Retrieve Results

This distinction is important because SQLAlchemy separates:

Query Construction

from:

Query Execution

The mental model is:

select(...)

↓

SQL Statement Object

session.scalars(...)

↓

Execute Query

.all()

↓

Collect Results

---

## Querying Tasks Using project_id

One of today's explicit queries retrieved Tasks belonging to Backend Engineering using the foreign-key value.

Conceptually:

SELECT Tasks

WHERE:

Task.project_id = Backend Engineering.id

This is different from relationship traversal because I explicitly instruct the database which records to retrieve.

This reinforced my understanding of how ORM relationships connect back to actual foreign-key queries.

---

## Explicit JOIN Between Task and Project

I also queried Tasks using an explicit JOIN.

The query conceptually asks:

Give me Tasks

↓

JOIN their Projects

↓

Keep rows where Project.name = "API Project"

The relationship path is:

Task

↓

Project

This allows filtering Task records based on information stored in the related Project table.

For example:

Task itself contains:

title

completed

priority

project_id

But:

Project.name

belongs to the Project table.

Therefore, to filter Tasks using the Project's name, I can JOIN the related Project table.

---

## Multi-Level JOIN

One of the most important practical exercises today involved a multi-level JOIN.

The relationship path was:

Task

↓

Project

↓

User

At the ORM level:

Task.project

↓

Project.user

↓

User

At the database level:

tasks.project_id

↓

projects.id

then:

projects.user_id

↓

users.id

This allows the application to ask questions such as:

"Give me all Tasks belonging to Projects owned by Michael."

This query crosses three tables:

tasks

↓

projects

↓

users

This was an important progression from the simpler JOINs I learned earlier.

---

## Understanding Multi-Level Relationships

The Task does not need to contain every piece of information about its Project or User.

Instead, relational databases allow information to be separated into appropriate tables.

For example:

Task stores information about the Task.

Project stores information about the Project.

User stores information about the User.

Foreign keys connect them.

Then JOINs allow the database to combine the information when necessary.

This is one of the core ideas behind relational database design.

---

## The Ownership Problem

The most important schema-design question today involved keeping both:

`Task.user_id`

and:

`Task.project_id`

At first, having both may seem convenient.

A Task can directly reference a User.

It can also directly reference a Project.

However, Project itself already references a User.

Therefore, there are now two possible ownership paths.

Path 1:

Task

↓

User

Path 2:

Task

↓

Project

↓

User

This can create duplicated ownership information.

---

## Example of Inconsistent Ownership

Suppose:

Michael has:

`id = 1`

Sarah has:

`id = 2`

Suppose Project 5 belongs to Sarah.

Therefore:

`Project.user_id = 2`

Now imagine someone creates a Task with:

`Task.user_id = 1`

and:

`Task.project_id = 5`

The direct relationship says:

Task

↓

Michael

But the Project relationship says:

Task

↓

Project 5

↓

Sarah

Now the application has contradictory information.

If I ask:

"Who owns this Task?"

one relationship says Michael.

Another relationship says Sarah.

This is a data-consistency problem.

---

## Why Ordinary Foreign Keys Do Not Automatically Prevent the Ownership Problem

An important lesson was that ordinary foreign keys do not automatically understand application business rules.

The database checks:

Does User 1 exist?

If yes:

`Task.user_id = 1`

is valid.

Then it checks:

Does Project 5 exist?

If yes:

`Task.project_id = 5`

is valid.

Both foreign keys can individually be valid.

But the database does not automatically understand:

"The User referenced directly by the Task must be the same User who owns the Task's Project."

That is a separate business rule.

Therefore:

Valid Foreign Keys

do not necessarily mean:

Valid Business Logic

This distinction is extremely important in backend engineering.

---

## One Source of Truth

If every Task must belong to exactly one Project, and every Project belongs to exactly one User, then the User who owns the Task can already be determined through:

Task

↓

Project

↓

User

Therefore, keeping:

`Task.user_id`

only for ownership may be redundant.

A cleaner design could be:

User

↓

Project

↓

Task

Then Task ownership has one clear path.

This creates a single source of truth.

Instead of asking:

`task.user`

and potentially getting one answer,

while:

`task.project.user`

gives another answer,

the application can consistently use:

`task.project.user`

This reduces the possibility of contradictory data.

---

## When a Direct Task-to-User Relationship Could Still Make Sense

Keeping a User reference on Task is not always wrong.

It depends on what the relationship means.

For example:

Sarah may own the Project.

Michael may be assigned one of the Tasks.

Then:

Project.user_id

could represent:

Project Owner

while:

Task.assignee_id

could represent:

Task Assignee

Now the two relationships represent different business concepts.

Conceptually:

Sarah

↓

Owns Project

↓

Backend Platform

↓

Task assigned to Michael

In that situation, both relationships make sense because they answer different questions.

The important thing is to name and design them clearly.

For example:

Project.user_id

↓

Owner

Task.assignee_id

↓

Person responsible for Task

This is much clearer than having two ambiguous ownership fields.

---

## Redundant Data and Data Consistency

Today introduced me to a broader database-design principle:

Duplicating the same fact in multiple places can create consistency problems.

If Task ownership is already determined by Project ownership, storing that ownership again directly on Task means the same information exists twice.

Whenever information is duplicated, the application must ensure both copies remain synchronised.

If one changes without the other, inconsistent data appears.

Therefore, one useful design question is:

"Can this value already be reliably derived from another relationship?"

If yes, storing another copy may not always be necessary.

This does not mean all duplicated data is automatically bad.

It means duplication should be deliberate and justified.

---

## Query Design and Schema Design Are Connected

Today also showed me that database schema design cannot be separated completely from application queries.

For example, introducing:

Project.user_id

means I can efficiently ask:

"Which Projects belong to Michael?"

Introducing:

Task.project_id

means I can ask:

"Which Tasks belong to Backend Engineering?"

Relationships allow me to navigate:

`user.projects`

and:

`project.tasks`

JOINs allow me to query across:

Task

↓

Project

↓

User

Indexes can support common filtering patterns involving:

user_id

and:

project_id

Therefore, schema design affects:

- application logic
- query design
- query performance
- data consistency
- migration complexity

---

## Mistakes I Corrected Today

### Mistake 1 - Incorrect Session Usage

I initially used the Session class without creating an actual Session connected to the engine.

I corrected this by understanding:

Session

↓

Class

Session(engine)

↓

Actual database Session

The Session is required to interact with the database.

---

### Mistake 2 - Creating Objects Without Persisting Them

I initially created User, Project, and Task ORM objects but did not add them to a Session or commit them.

I corrected this.

Creating an ORM object only creates a Python object.

Persistence requires:

Create Object

↓

Add to Session

↓

Commit

↓

Stored in Database

---

### Mistake 3 - Reading ID Before Persistence

I initially attempted to retrieve Michael's ID immediately after constructing the User object.

I learned that the primary key is normally generated when the database INSERT occurs.

Therefore, before persistence:

`michael.id`

may be:

`None`

After persistence:

`michael.id`

contains the generated primary-key value.

---

### Mistake 4 - Incorrect WHERE Syntax

I initially attempted to use keyword-style syntax inside `where()`.

I corrected this by using SQLAlchemy expressions.

Conceptually:

Column

==

Value

The `where()` method expects SQL expression conditions rather than arbitrary keyword arguments.

---

### Mistake 5 - Selecting the Wrong Entity

When trying to retrieve Michael's Projects, I initially selected User.

However, the requested result was Projects.

Therefore, the query should select:

Project

and filter using:

Project.user_id

This reinforced an important query-design question:

"What object am I actually trying to retrieve?"

That object should normally determine what I select.

---

### Mistake 6 - Constructing Queries Without Executing Them

I correctly constructed some JOIN statements but did not execute them.

I learned that:

select(...)

only creates the SQL statement.

The Session must execute it before records are retrieved.

The corrected mental model is:

Build Query

↓

Execute Query

↓

Retrieve Results

---

### Mistake 7 - Missing Explicit project_id Query

I initially used a JOIN for the Backend Engineering Tasks but did not also perform the required explicit foreign-key query.

I corrected this by understanding both approaches:

Relationship traversal

and:

Explicit project_id filtering

and:

JOIN-based filtering

These are different tools for different situations.

---

### Mistake 8 - Incomplete Foreign-Key Explanations

I initially described `projects.user_id` and `tasks.project_id` too vaguely.

I corrected them precisely.

`projects.user_id`

↓

references `users.id`

`tasks.project_id`

↓

references `projects.id`

Being precise about foreign-key direction is important when reasoning about relational schemas.

---

### Mistake 9 - Incomplete ORM Relationship Explanation

I initially understood that the IDs were foreign keys but did not fully explain the difference between foreign-key values and ORM relationships.

I corrected the distinction:

`task.project_id`

↓

Database value

`task.project`

↓

Project ORM object

---

### Mistake 10 - Incomplete Ownership Reasoning

I initially left the ownership consistency challenge unanswered.

After reviewing it, I learned that storing both:

Task.user_id

and:

Task.project_id

can create contradictory ownership information if Project already determines the User.

This introduced the important idea of maintaining one clear source of truth.

---

## Important Mental Models

### User and Project

User

1

↓

Many

Projects

---

### Project and Task

Project

1

↓

Many

Tasks

---

### Full Relationship

User

↓

Project

↓

Task

---

### Database Foreign Keys

projects.user_id

↓

users.id

tasks.project_id

↓

projects.id

---

### ORM Navigation

user.projects

↓

Collection of Projects

project.user

↓

Single User

project.tasks

↓

Collection of Tasks

task.project

↓

Single Project

---

### Persistence

Create ORM Objects

↓

Add to Session

↓

Commit

↓

Database Rows

---

### Database-Generated ID

Create Object

↓

id = None

↓

Persist Object

↓

Database Generates ID

↓

ORM Receives ID

---

### Query Execution

select(...)

↓

Construct Statement

session.scalars(...)

↓

Execute Statement

.all()

↓

Retrieve Results

---

### Multi-Level JOIN

Task

↓

Project

↓

User

---

### Migration Safety

Existing Tasks

↓

Add Nullable project_id

↓

Preserve Existing Rows

↓

Assign Projects

↓

Potentially Make Required Later

---

### Index Reasoning

Common Query

↓

WHERE project_id = ?

↓

Consider INDEX(project_id)

---

### Ownership Consistency

Bad:

Task ─────────→ User A

Task → Project → User B

Two different ownership answers.

Better when ownership is identical:

Task

↓

Project

↓

User

One source of truth.

---

## Key Concepts Learned

Today I learned and reinforced:

- Project ORM modelling
- User-to-Project one-to-many relationships
- Project-to-Task one-to-many relationships
- multi-level relational models
- foreign-key chains
- `projects.user_id`
- `tasks.project_id`
- `User.projects`
- `Project.user`
- `Project.tasks`
- `Task.project`
- `back_populates`
- database columns vs ORM relationships
- nullable foreign-key migrations
- migration safety with existing data
- indexing foreign-key query patterns
- SQLAlchemy Session creation
- object persistence
- database-generated primary keys
- relationship cascade behaviour
- relationship-based object creation
- avoiding hardcoded foreign-key IDs
- relationship traversal
- explicit SELECT queries
- explicit foreign-key filtering
- JOIN queries
- multi-level JOIN queries
- Task → Project → User traversal
- query construction vs query execution
- schema redundancy
- ownership consistency
- foreign-key limitations
- business rules vs database integrity
- one source of truth
- clear relationship naming
- Project owner vs Task assignee
- schema design based on application meaning

---

## Progress From Day 42 to Day 43

Day 42 focused mainly on database indexes.

I learned how to reason about:

- single-column indexes
- composite indexes
- index selectivity
- index storage costs
- index write overhead
- SQLAlchemy index definitions
- Alembic index migrations
- query patterns
- avoiding unnecessary indexes

Day 43 used those concepts inside a larger relational design.

Instead of discussing indexes by themselves, I used them as part of new relationships.

For example:

Project.user_id

↓

Foreign Key

+

Common Query Column

+

Index Candidate

and:

Task.project_id

↓

Foreign Key

+

Common Query Column

+

Index Candidate

I also combined the migration-safety concepts from Day 41.

The new `project_id` column was introduced as nullable because existing Task records may not have Projects.

Therefore, several previous lessons came together today:

Day 37:

Relationships

↓

Day 38:

Creating Related Objects

↓

Day 39:

Relationship Queries and JOINs

↓

Day 40:

Alembic Migrations

↓

Day 41:

Migration Safety

↓

Day 42:

Indexes

↓

Day 43:

Multi-Level Relational Schema

This means I am no longer learning these concepts independently.

I am starting to combine them into realistic backend database design.

---

## Completion Checklist

### Models

- [x] Created Project model
- [x] Added Project primary key
- [x] Added Project name
- [x] Added Project.user_id foreign key
- [x] Added Project.user relationship
- [x] Added Project.tasks relationship
- [x] Added User.projects relationship
- [x] Added Task.project_id foreign key
- [x] Added Task.project relationship

### Relationships

- [x] Understood User → Project one-to-many
- [x] Understood Project → Task one-to-many
- [x] Understood `User.projects`
- [x] Understood `Project.user`
- [x] Understood `Project.tasks`
- [x] Understood `Task.project`
- [x] Understood collection vs scalar relationships
- [x] Understood multi-level relationship traversal

### Foreign Keys

- [x] Understood `projects.user_id → users.id`
- [x] Understood `tasks.project_id → projects.id`
- [x] Understood foreign-key columns vs ORM relationships
- [x] Understood why foreign keys do not automatically enforce every business rule

### Migration Safety

- [x] Added project_id as nullable
- [x] Understood why existing Tasks require migration consideration
- [x] Connected Day 41 migration safety to relationship migrations
- [x] Continued using Alembic instead of create_all()
- [x] Understood migration inspection requirements

### Indexes

- [x] Indexed Project.user_id
- [x] Indexed Task.project_id
- [x] Applied Day 42 query-pattern reasoning
- [x] Understood that foreign key and index solve different problems

### Persistence

- [x] Corrected Session creation
- [x] Understood Session(engine)
- [x] Added ORM objects to the Session
- [x] Committed related objects
- [x] Understood database-generated IDs
- [x] Avoided relying on IDs before persistence
- [x] Used relationships instead of hardcoded foreign-key IDs

### Queries

- [x] Queried Projects belonging to Michael
- [x] Traversed Project.tasks
- [x] Queried Tasks using project_id
- [x] Queried Tasks using Project JOIN
- [x] Queried Tasks using Task → Project → User JOIN
- [x] Understood query construction vs execution
- [x] Understood relationship traversal vs explicit querying

### Schema Design

- [x] Identified duplicated ownership risk
- [x] Understood why two valid foreign keys can still produce invalid business data
- [x] Understood one source of truth
- [x] Considered removing redundant Task.user_id
- [x] Understood when a separate Task-to-User relationship may still be valid
- [x] Understood clearer naming such as assignee_id

### Corrections

- [x] Corrected Session usage
- [x] Corrected persistence flow
- [x] Corrected premature ID access
- [x] Corrected WHERE syntax
- [x] Corrected selected entity
- [x] Corrected missing query execution
- [x] Corrected foreign-key explanations
- [x] Completed multi-level JOIN
- [x] Completed ownership challenge
- [x] Completed Day 43 Q&A

---

## Overall Review

Day 43 was an important step because the database structure became significantly more realistic.

Previously, I mainly worked with a direct User-to-Task relationship.

Today I introduced Projects and created the structure:

User

↓

Project

↓

Task

This required me to think about more than simply writing SQLAlchemy models.

I had to consider:

- how the tables relate
- where foreign keys belong
- which ORM relationships should exist
- which relationships return collections
- which relationships return single objects
- how existing data affects migrations
- which foreign keys are reasonable index candidates
- how objects are persisted
- how relationships can be traversed
- how explicit database queries work
- how JOINs cross multiple relationships
- how duplicated relationships can create inconsistent data

The most important schema-design lesson was the ownership problem.

If every Task belongs to a Project and every Project belongs to one User, then the Task's owner can already be determined through:

Task

↓

Project

↓

User

Adding another direct ownership field to Task may duplicate information.

That duplication can lead to contradictory data where:

Task.user

and:

Task.project.user

refer to different Users.

Ordinary foreign keys do not automatically prevent this because each foreign key can independently reference a valid record.

This taught me an important distinction:

Database Integrity

is not always the same as:

Business-Rule Integrity

A schema can contain technically valid foreign keys while still representing logically invalid application data.

This introduced the idea of designing around a single source of truth.

If ownership is determined through the Project, then storing ownership again directly on Task may not be necessary.

However, a direct User relationship could still make sense if it represents something different, such as the Task assignee.

In that situation, clear naming becomes important.

For example:

Project.user_id

↓

Project Owner

Task.assignee_id

↓

Task Assignee

This makes the meaning of each relationship explicit.

Day 43 therefore moved beyond simply learning SQLAlchemy syntax.

It introduced deeper relational database design thinking.

The progression is now:

Day 37:

"How do ORM relationships work?"

Day 38:

"How do I create related objects?"

Day 39:

"How do I query across relationships?"

Day 40:

"How do I evolve the database with migrations?"

Day 41:

"How do I evolve the database safely?"

Day 42:

"How do I design indexes around query patterns?"

Day 43:

"How do I combine relationships, migrations, indexes, queries, and data consistency into a realistic relational schema?"

This represents a significant step toward building production-style database-backed backend applications.

**Day 43: Completed after corrections**