from sqlalchemy import (
    create_engine,
    String,
    Boolean,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
    relationship
)


# -----------------------------
# Database setup
# -----------------------------

DATABASE_URL = "sqlite:///./relationship.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# -----------------------------
# Base class
# -----------------------------

class Base(DeclarativeBase):
    pass


# -----------------------------
# User model
# -----------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user"
    )


# -----------------------------
# Task model
# -----------------------------

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    priority: Mapped[int] = mapped_column(
        Integer,
        default=3,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )


# -----------------------------
# Create tables
# -----------------------------

Base.metadata.create_all(engine)


# -----------------------------
# Create users and tasks
# -----------------------------

with Session(engine) as session:

    user_1 = User(
        name="John",
        email="john@example.com"
    )

    user_2 = User(
        name="David",
        email="david@example.com"
    )

    session.add_all([
        user_1,
        user_2
    ])

    session.commit()


    task_1 = Task(
        title="Learn Relationships",
        completed=False,
        priority=5,
        user_id=user_1.id
    )

    task_2 = Task(
        title="Learn SQL",
        completed=False,
        priority=5,
        user_id=user_1.id
    )

    task_3 = Task(
        title="Learn C++",
        completed=False,
        priority=5,
        user_id=user_2.id
    )

    session.add_all([
        task_1,
        task_2,
        task_3
    ])

    session.commit()


# -----------------------------
# Retrieve John and his tasks
# -----------------------------

with Session(engine) as session:

    user = session.get(User, 1)

    if user is None:
        print("User not found")
    else:
        print(f"User: {user.name}")

        print("Tasks:")

        for task in user.tasks:
            print(
                f"- {task.title} "
                f"(Priority: {task.priority})"
            )


# -----------------------------
# Retrieve a task and its user
# -----------------------------

with Session(engine) as session:

    task = session.get(Task, 1)

    if task is None:
        print("Task not found")
    else:
        print(f"Task: {task.title}")
        print(f"Owner: {task.user.name}")


# ==========================================
# DAY 37 QUESTIONS & ANSWERS
# ==========================================


# Question 1:
# What problem does a foreign key solve?
#
# Answer:
# A foreign key creates a database-level link between
# rows in two tables and helps maintain referential integrity.
# In this project, Task.user_id references User.id.


# Question 2:
# What does ForeignKey("users.id") mean?
#
# Answer:
# It means that the user_id column in the tasks table
# references the id column in the users table.


# Question 3:
# What is the difference between a ForeignKey
# and relationship()?
#
# Answer:
# ForeignKey creates the relationship at the database level.
# relationship() creates the relationship at the ORM level
# and allows Python objects to navigate between related objects.


# Question 4:
# What does User.tasks represent?
#
# Answer:
# User.tasks represents the collection of Task objects
# belonging to a particular User.


# Question 5:
# What does Task.user represent?
#
# Answer:
# Task.user represents the User object that owns
# or is associated with that Task.


# Question 6:
# What type of relationship do we have
# between User and Task?
#
# Answer:
# We have a one-to-many relationship.
# One User can have many Tasks, while each Task
# belongs to one User.


# Question 7:
# Why shouldn't we store the user's name
# directly inside every Task row?
#
# Answer:
# Storing the user's name in every Task would create
# unnecessary data duplication and could cause
# inconsistent data when the user's name changes.
# Instead, the Task stores user_id and references
# the User record.


# Question 8:
# What happens when a Task has user_id = 1?
#
# Answer:
# It means that the Task references the User whose
# primary key id is 1.


# Question 9:
# What does session.get(User, 1) do?
#
# Answer:
# It retrieves the User whose primary key is 1.
# If no User with that ID exists, it returns None.


# Question 10:
# Why can't create_all() be treated as
# a proper migration system?
#
# Answer:
# create_all() can create tables that do not exist,
# but it does not properly manage changes to existing
# table structures. A migration tool such as Alembic
# is used to safely evolve an existing database schema.