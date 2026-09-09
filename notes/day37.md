# Day 37 - SQLAlchemy Relationships Fundamentals

## Overview

Today I learned how to model relationships between different database tables using SQLAlchemy ORM. The main focus was understanding how a User and a Task can be connected using a foreign key and SQLAlchemy relationships.

The main concept I learned today is that database relationships have two important layers. The `ForeignKey` establishes the actual relationship at the database level, while SQLAlchemy's `relationship()` allows the Python ORM objects to navigate between those related records.

For this task, I created a one-to-many relationship between Users and Tasks. One User can have multiple Tasks, while each Task belongs to one User.

---

## Database Relationship

I created two ORM models:

- User
- Task

The User model contains basic information such as an ID, name, and email.

The Task model contains an ID, title, completion status, priority, and a `user_id` field.

The `user_id` field is the important part because it connects the Task table to the User table.

The relationship is:

User → many Tasks

This means one user can own multiple tasks.

For example, John could have:

- Learn SQL
- Learn Python
- Learn FastAPI

while each individual task belongs to only one user.

---

## Foreign Keys

I learned that a foreign key creates a database-level connection between two tables.

In the Task model, the `user_id` column references the `id` column of the Users table.

Conceptually:

Task.user_id → User.id

If a task has `user_id = 1`, that means the task belongs to the User whose primary key is `1`.

The foreign key also helps maintain referential integrity because the database can enforce that referenced users actually exist.

---

## SQLAlchemy relationship()

I learned that `relationship()` provides the ORM-level representation of a relationship.

The User model has a `tasks` relationship, while the Task model has a `user` relationship.

This allows me to navigate between related Python objects without manually writing another query every time.

From the User side:

`user.tasks`

returns the collection of tasks belonging to that user.

From the Task side:

`task.user`

returns the User who owns that task.

This is an important distinction because `user.tasks` represents multiple Task objects, while `task.user` represents one User object.

---

## Understanding Mapped["User"]

I also learned what the following SQLAlchemy declaration means:

`user: Mapped["User"] = relationship(back_populates="tasks")`

The `user` part is the name of the attribute on the Task object.

`Mapped["User"]` tells SQLAlchemy that this attribute represents a User ORM object.

`relationship()` tells SQLAlchemy that this attribute represents an ORM relationship to another model.

The `back_populates="tasks"` part connects this relationship to the `tasks` relationship on the User model.

Therefore, the two sides are connected like this:

User.tasks ↔ Task.user

This allows SQLAlchemy to understand that they are two sides of the same relationship.

---

## Why User.tasks Is Plural

One important thing I clarified today was why I cannot simply use something like:

`user.task.title`

after retrieving a specific User.

When I do:

`user = session.get(User, 1)`

I have retrieved a specific User, but that User can still have multiple Tasks.

For example:

User #1 could have:

- Task #1: Learn Relationships
- Task #2: Learn SQL

Therefore, SQLAlchemy exposes the relationship as:

`user.tasks`

because it is a collection of Task objects.

If I want a specific task, I need to select that task, access an item from the collection, or query it directly.

For example, `user.tasks[0].title` accesses the first task in the collection.

On the other hand, a Task has only one User, so:

`task.user.name`

works because `task.user` represents one User object.

The mental model I learned is:

User → many Tasks → `user.tasks`

Task → one User → `task.user`

---

## back_populates

I learned that `back_populates` connects both sides of a SQLAlchemy relationship.

The User model defines:

`tasks = relationship(back_populates="user")`

while the Task model defines:

`user = relationship(back_populates="tasks")`

The two attributes point back to each other.

This tells SQLAlchemy that:

- User.tasks is the collection of Tasks associated with a User.
- Task.user is the User associated with a Task.

Therefore:

User.tasks ↔ Task.user

represents the same relationship from opposite directions.

---

## Creating Related Records

I created two users:

- John
- David

I then created three tasks:

- Learn Relationships
- Learn SQL
- Learn C++

John owns the first two tasks, while David owns the third task.

The relationship can therefore be visualized as:

John
- Learn Relationships
- Learn SQL

David
- Learn C++

This helped me understand how the foreign key connects individual Task rows to specific User rows.

---

## session.get()

I also reinforced how `session.get()` works.

`session.get(User, 1)` retrieves the User whose primary key is `1`.

The result needs to be stored in a variable if I want to work with it.

For example:

`user = session.get(User, 1)`

I also learned that I should pass the ORM class to `session.get()`, not an existing model instance.

Therefore:

`session.get(User, 1)`

is correct.

Passing an existing User object instead of the User class is incorrect.

---

## create_all() and Migrations

I reinforced my understanding of `Base.metadata.create_all(engine)`.

`create_all()` can create tables that do not already exist based on the SQLAlchemy models.

However, it should not be treated as a proper database migration system.

If an existing table needs to be changed, such as adding a new column or changing a constraint, `create_all()` does not safely manage those schema changes.

A migration tool such as Alembic is used for properly evolving an existing database schema.

This will become important later in the database migration part of Week 21.

---

## Key Concepts Learned

Today I learned and reinforced:

- One-to-many database relationships
- Foreign keys
- SQLAlchemy `ForeignKey()`
- SQLAlchemy `relationship()`
- `back_populates`
- `Mapped["User"]`
- `User.tasks`
- `Task.user`
- `session.get()`
- Navigating relationships through ORM objects
- Why one side of a relationship can be a list while the other side is a single object
- Why user names should not be duplicated across every Task row
- The difference between database-level relationships and ORM-level relationships
- Why `create_all()` is not a proper migration system

---

## Important Mental Model

The most important thing I learned today is:

ForeignKey = database-level connection

relationship() = ORM-level navigation

back_populates = connects both sides of the ORM relationship

For this project:

User
↓
`tasks`
↓
Many Task objects

Task
↓
`user`
↓
One User object

And at the database level:

`tasks.user_id → users.id`

---

## Day 37 Status

Completed the fundamentals of SQLAlchemy relationships and successfully modelled a one-to-many relationship between Users and Tasks.

I now understand how foreign keys connect tables at the database level and how SQLAlchemy relationships allow me to navigate those connections through Python objects.

### Completion Checklist

- [x] Understand foreign keys
- [x] Understand one-to-many relationships
- [x] Create User and Task ORM models
- [x] Connect Task to User with a foreign key
- [x] Use SQLAlchemy `relationship()`
- [x] Understand `back_populates`
- [x] Access a user's tasks through `user.tasks`
- [x] Access a task's owner through `task.user`
- [x] Use `session.get()` correctly
- [x] Understand why `user.tasks` is a collection
- [x] Understand why `task.user` is a single object
- [x] Understand why `create_all()` is not a migration system

## Overall Review

Day 37 was mainly about understanding relationships rather than building a large application. I initially had some mistakes with the foreign key reference, `session.get()`, and treating `task.user` as a list, but correcting those mistakes helped clarify how SQLAlchemy relationships actually work.

The biggest takeaway is that a foreign key handles the database connection, while `relationship()` gives the Python application a convenient way to navigate that connection.

**Day 37: Completed**