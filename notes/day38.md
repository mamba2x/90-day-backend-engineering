# Day 38 - Working with SQLAlchemy ORM Relationships

## Overview

Today I built on the SQLAlchemy relationship fundamentals from Day 37 and learned how to actually work with related ORM objects in Python.

Previously, I learned how a foreign key creates a database-level connection between the `User` and `Task` tables and how `relationship()` allows SQLAlchemy ORM objects to navigate that connection.

Today, I went further by learning that I do not always need to manually assign foreign key values such as `user_id=michael.id`. Since SQLAlchemy already understands the relationship between `User` and `Task`, I can work directly with the related Python objects.

The main focus was creating related objects, adding objects through relationships, retrieving related records, and traversing relationships in both directions.

---

## Revisiting the User and Task Relationship

The relationship between User and Task remains a one-to-many relationship.

One User can have many Tasks, while each Task belongs to one User.

Conceptually:

User
↓
Many Tasks

Task
↓
One User

At the database level, the relationship is represented using:

`tasks.user_id → users.id`

At the ORM level, the relationship is represented using:

`User.tasks ↔ Task.user`

This means that the foreign key stores the actual database reference, while the ORM relationship gives Python a convenient way to work with the related objects.

---

## Understanding task.user_id vs task.user

One of the most important concepts I learned today was the difference between `task.user_id` and `task.user`.

`task.user_id` represents the foreign key value stored in the Task table.

For example:

`task.user_id = 1`

means that the Task belongs to the User whose primary key is `1`.

On the other hand:

`task.user`

represents the actual related User ORM object.

Therefore, if the Task belongs to Michael:

`task.user_id`

could return:

`1`

while:

`task.user.name`

could return:

`Michael`

and:

`task.user.email`

could return:

`michael@example.com`

The important mental model is:

`task.user_id` = database identity

`task.user` = related Python ORM object

---

## Creating Related Objects Using ORM Objects

Previously, I created relationships by manually assigning the foreign key.

For example:

`user_id=michael.id`

Today I learned that SQLAlchemy allows me to work directly with ORM objects.

Instead of manually providing the foreign key, I can assign the related User object through the relationship.

Conceptually:

`user=michael`

SQLAlchemy already knows that `Task.user` is connected to `Task.user_id` through the configured relationship and foreign key.

Because Michael is an ORM User object with a primary key, SQLAlchemy can determine which `user_id` should be associated with the Task.

This approach is more ORM-oriented because I am working with Python objects rather than manually managing database IDs.

---

## Adding Tasks Through user.tasks

I also learned that relationships can be managed from the User side.

Since one User can have many Tasks, SQLAlchemy represents the relationship as a collection:

`user.tasks`

A new Task can therefore be added directly to this collection.

Conceptually:

`michael.tasks.append(task)`

This tells SQLAlchemy that the Task belongs to Michael.

SQLAlchemy can then associate the Task with Michael and manage the corresponding foreign key.

This demonstrated that relationships can be worked with from either direction:

Task → User

or:

User → Tasks

---

## Why user.tasks Is a Collection

I reinforced the reason why `user.tasks` behaves like a collection.

Retrieving a specific User does not mean that only one Task exists for that User.

For example, Michael could have:

- Study FastAPI
- Study C++
- Learn SQLAlchemy

Therefore:

`michael.tasks`

must be capable of containing multiple Task objects.

This is why operations such as looping and `.append()` can be used with `michael.tasks`.

By contrast:

`task.user`

represents only one User because each Task belongs to one User.

The mental model is:

`user.tasks` → many Task objects

`task.user` → one User object

---

## Understanding back_populates More Clearly

Today I gained a more practical understanding of `back_populates`.

The relationship is configured on both models:

`User.tasks`

and:

`Task.user`

These represent opposite sides of the same relationship.

`back_populates` tells SQLAlchemy that these attributes belong together.

Conceptually:

`User.tasks ↔ Task.user`

Because the relationship is bidirectional, SQLAlchemy can keep the Python-side relationship synchronized.

For example, when a Task is associated with Michael through the relationship, SQLAlchemy understands that Michael is the Task's User and that the Task belongs to Michael's collection of Tasks.

This is one of the main reasons SQLAlchemy relationships are useful instead of manually managing every connection using IDs.

---

## Retrieving Related Objects

I continued practising `session.get()` to retrieve ORM objects using their primary keys.

For example:

`session.get(User, michael_id)`

retrieves Michael using his primary key.

Once the User has been retrieved, I can access the User's related Tasks through:

`michael.tasks`

Since this is a collection, I can loop through it and access each Task individually.

I also retrieved a specific Task using its primary key.

Once the Task was retrieved, I could access information about its owner through the relationship.

For example:

`task.user.name`

and:

`task.user.email`

This means I can move from a Task object to its related User object without manually performing another user lookup in my application code.

---

## Relationship Traversal

I learned that moving from one ORM object to another through relationship attributes is called relationship traversal.

For example:

`task.user.name`

can be understood as:

Task
↓
User
↓
Name

Another example is:

`user.tasks`

which moves from:

User
↓
Related Tasks

This makes working with connected database records feel much more natural from Python because the application can navigate between related objects.

---

## Working with Object IDs Safely

Today I also corrected an important issue involving IDs across SQLAlchemy sessions.

If I create an object inside one Session and need to retrieve it later in another Session, I can store its primary key before leaving the original Session.

For example, I can store:

`michael_id`

and:

`task_id`

Then, inside another Session, I can retrieve the objects using:

`session.get(User, michael_id)`

or:

`session.get(Task, task_id)`

This is clearer and safer than relying on hardcoded IDs such as `1`, especially as more records are added to the database.

---

## Sarah Relationship Challenge

As the final exercise, I created another User named Sarah.

Sarah was associated with three Tasks:

- Learn Docker - Priority 5
- Practice Testing - Priority 4
- Read Documentation - Priority 3

Instead of manually setting `user_id` on every Task, the Tasks were added through Sarah's ORM relationship.

This demonstrated how multiple related records can be associated with one parent object using the one-to-many relationship.

After committing the data, Sarah could be retrieved from the database and her Tasks accessed through the `tasks` relationship.

This reinforced the idea that SQLAlchemy relationships are not only useful for reading related records but can also be used when creating and associating new records.

---

## ForeignKey vs relationship()

I reinforced the distinction between `ForeignKey` and `relationship()`.

`ForeignKey` works at the database level.

It establishes:

`tasks.user_id → users.id`

`relationship()` works at the ORM level.

It provides:

`task.user`

and:

`user.tasks`

Therefore:

ForeignKey = database-level connection

relationship() = Python/ORM-level navigation

back_populates = connects both sides of the ORM relationship

These three concepts work together but have different responsibilities.

---

## More ORM-Oriented Code

Another important takeaway from today was understanding what it means for code to be more ORM-oriented.

Both of these approaches can associate a Task with a User:

`user_id=michael.id`

and:

`user=michael`

However, `user=michael` is more ORM-oriented because I am working directly with the related Python object.

The ORM then handles translating that object relationship into the appropriate database foreign key.

This allows application code to focus more on relationships between objects rather than manually manipulating IDs everywhere.

---

## Key Concepts Learned

Today I learned and reinforced:

- Creating related objects using ORM relationships
- The difference between `task.user_id` and `task.user`
- Using `user=michael` instead of manually assigning `user_id`
- Adding Tasks through `user.tasks.append()`
- How SQLAlchemy manages foreign keys through relationships
- Working with one-to-many relationships
- Why `User.tasks` is a collection
- Why `Task.user` is a single object
- How `back_populates` connects both sides of a relationship
- Retrieving related objects using `session.get()`
- Saving object IDs for later retrieval
- Relationship traversal
- Navigating from Task to User
- Navigating from User to Tasks
- Creating multiple related Tasks for one User
- The difference between database relationships and ORM relationships

---

## Important Mental Model

The main relationship can now be understood at two levels.

### Database Level

`tasks.user_id → users.id`

The foreign key stores which User owns each Task.

### ORM Level

`User.tasks ↔ Task.user`

The ORM allows Python objects to navigate the same relationship.

Therefore:

`task.user_id`

gives the User's database ID.

`task.user`

gives the User ORM object.

`user.tasks`

gives the collection of Task ORM objects belonging to the User.

---

## Progress From Day 37 to Day 38

Day 37 focused on defining and understanding relationships.

I learned:

ForeignKey → connects tables

relationship() → allows ORM navigation

back_populates → connects both ORM sides

Day 38 focused on actually using those relationships.

I can now:

- Create a Task using a User object
- Add Tasks directly through a User's task collection
- Retrieve a User and access their Tasks
- Retrieve a Task and access its User
- Navigate relationships between ORM objects
- Understand how SQLAlchemy translates object relationships into foreign keys

This means I have moved from simply defining ORM relationships to actively manipulating related objects through SQLAlchemy.

---

## Completion Checklist

- [x] Reviewed the User and Task one-to-many relationship
- [x] Understood `task.user_id`
- [x] Understood `task.user`
- [x] Created a Task using `user=michael`
- [x] Used `michael.tasks.append()`
- [x] Understood how SQLAlchemy determines the foreign key
- [x] Retrieved a User using `session.get()`
- [x] Retrieved a Task using `session.get()`
- [x] Navigated from User to Tasks
- [x] Navigated from Task to User
- [x] Understood relationship traversal
- [x] Understood `back_populates` more deeply
- [x] Used stored IDs across different Sessions
- [x] Created Sarah with multiple related Tasks
- [x] Reinforced ForeignKey vs relationship()
- [x] Completed the Day 38 relationship Q&A

---

## Overall Review

Day 38 strengthened my understanding of SQLAlchemy relationships by moving from relationship definitions into actual relationship operations.

I initially made some mistakes involving retrieving objects, using variables returned from `session.get()`, distinguishing between `task.user` and `task.user_id`, and managing objects across different Sessions. Correcting these issues helped reinforce how SQLAlchemy's ORM works with related objects.

The biggest takeaway from today is that I do not always have to manually work with foreign key IDs. Once the relationship has been correctly configured, I can work naturally with Python ORM objects and allow SQLAlchemy to manage the underlying database relationship.

**Day 38: Completed**