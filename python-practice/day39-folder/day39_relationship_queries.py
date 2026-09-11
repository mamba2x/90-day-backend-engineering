from sqlalchemy import (
    Boolean,
    Integer,
    String,
    ForeignKey,
    create_engine,
    select
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

DATABASE_URL = "sqlite:///./day39_relationship_queries.db"

engine = create_engine(DATABASE_URL)


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
# Create Michael and tasks
# -----------------------------

with Session(engine) as session:

    michael = User(
        name="Michael",
        email="michael@example.com"
    )

    michael.tasks.append(
        Task(
            title="Study FastAPI",
            completed=False,
            priority=5
        )
    )

    michael.tasks.append(
        Task(
            title="Learn PostgreSQL",
            completed=False,
            priority=4
        )
    )

    michael.tasks.append(
        Task(
            title="Read Documentation",
            completed=False,
            priority=2
        )
    )

    session.add(michael)
    session.commit()
    session.refresh(michael)

    michael_id = michael.id


# -----------------------------
# Create Sarah and tasks
# -----------------------------

with Session(engine) as session:

    sarah = User(
        name="Sarah",
        email="sarah@example.com"
    )

    sarah.tasks.append(
        Task(
            title="Learn Docker",
            completed=False,
            priority=5
        )
    )

    sarah.tasks.append(
        Task(
            title="Practice Testing",
            completed=False,
            priority=4
        )
    )

    sarah.tasks.append(
        Task(
            title="Study GitHub Actions",
            completed=False,
            priority=3
        )
    )

    session.add(sarah)
    session.commit()
    session.refresh(sarah)

    sarah_id = sarah.id


# ==========================================
# QUERY 1
# Retrieve Michael and use relationship traversal
# ==========================================

with Session(engine) as session:

    michael = session.get(User, michael_id)

    if michael is None:
        print("Michael not found")
    else:
        print("\nMichael's Tasks using relationship:")

        for task in michael.tasks:
            print(
                f"{task.title} - "
                f"Priority: {task.priority}"
            )


# ==========================================
# QUERY 2
# Query Michael's tasks explicitly
# ==========================================

with Session(engine) as session:

    statement = select(Task).where(
        Task.user_id == michael_id
    )

    tasks = session.scalars(statement).all()

    print("\nMichael's Tasks using select:")

    for task in tasks:
        print(
            f"{task.title} - "
            f"Priority: {task.priority}"
        )


# ==========================================
# QUERY 3
# Michael's tasks with priority >= 4
# ==========================================

with Session(engine) as session:

    statement = select(Task).where(
        Task.user_id == michael_id,
        Task.priority >= 4
    )

    tasks = session.scalars(statement).all()

    print("\nMichael's High Priority Tasks:")

    for task in tasks:
        print(
            f"{task.title} - "
            f"Priority: {task.priority}"
        )


# ==========================================
# QUERY 4
# Sarah's tasks using JOIN
# ==========================================

with Session(engine) as session:

    statement = (
        select(Task)
        .join(Task.user)
        .where(
            User.name == "Sarah"
        )
    )

    tasks = session.scalars(statement).all()

    print("\nSarah's Tasks using JOIN:")

    for task in tasks:
        print(
            f"{task.title} - "
            f"Priority: {task.priority}"
        )


# ==========================================
# QUERY 5
# Sarah's tasks with priority >= 4 using JOIN
# ==========================================

with Session(engine) as session:

    statement = (
        select(Task)
        .join(Task.user)
        .where(
            User.name == "Sarah",
            Task.priority >= 4
        )
    )

    tasks = session.scalars(statement).all()

    print("\nSarah's High Priority Tasks:")

    for task in tasks:
        print(
            f"{task.title} - "
            f"Priority: {task.priority}"
        )


# ==========================================
# QUERY 6
# Query both User and Task
# ==========================================

with Session(engine) as session:

    statement = (
        select(User, Task)
        .join(User.tasks)
    )

    results = session.execute(statement).all()

    print("\nUsers and their Tasks:")

    for user, task in results:
        print(
            f"{user.name} -> {task.title}"
        )


# ==========================================
# FINAL CHALLENGE
# Michael's tasks with priority >= 4
# using JOIN
# ==========================================

with Session(engine) as session:

    statement = (
        select(Task)
        .join(Task.user)
        .where(
            User.name == "Michael",
            Task.priority >= 4
        )
    )

    tasks = session.scalars(statement).all()

    print("\nFinal Challenge:")

    for task in tasks:
        print(
            f"{task.title} - "
            f"Priority: {task.priority}"
        )


# ==========================================
# DAY 39 QUESTIONS & ANSWERS
# ==========================================


# Question 1:
# What is the difference between user.tasks and
# select(Task).where(Task.user_id == user.id)?
#
# Answer:
# user.tasks uses the ORM relationship to access
# the collection of Task objects related to a User.
#
# select(Task).where(Task.user_id == user.id)
# explicitly creates a database query that searches
# for Task rows whose foreign key matches the User's ID.


# Question 2:
# What does .join(Task.user) tell SQLAlchemy to do?
#
# Answer:
# It tells SQLAlchemy to join the Task table to the
# User table using the configured Task.user relationship.


# Question 3:
# Which columns connect the User and Task tables?
#
# Answer:
# tasks.user_id connects to users.id.
#
# Task.user_id -> User.id


# Question 4:
# Why doesn't SQLAlchemy need us to manually write
# tasks.user_id == users.id when using .join(Task.user)?
#
# Answer:
# SQLAlchemy already knows how the tables are connected
# because the Task model defines ForeignKey("users.id")
# and the ORM relationship Task.user.
#
# Therefore, SQLAlchemy can automatically determine
# the correct JOIN condition.


# Question 5:
# What does this mean?
# .where(User.name == "Sarah")
#
# Answer:
# It filters the query so that only rows associated
# with a User whose name is "Sarah" are returned.


# Question 6:
# How would you query only Sarah's Tasks
# with priority >= 4?
#
# Answer:
#
# statement = (
#     select(Task)
#     .join(Task.user)
#     .where(
#         User.name == "Sarah",
#         Task.priority >= 4
#     )
# )


# Question 7:
# What is the difference between:
# select(Task)
# and
# select(User, Task)?
#
# Answer:
# select(Task) selects only Task ORM entities.
#
# select(User, Task) selects both User and Task
# ORM entities in each result row.


# Question 8:
# Why might we use session.scalars() for
# select(Task) but session.execute() for
# select(User, Task)?
#
# Answer:
# session.scalars() is convenient when the query
# returns one main ORM entity, such as Task.
#
# session.execute() is useful when the query returns
# multiple values or ORM entities in each row,
# such as both User and Task.


# Question 9:
# What does each item contain when we loop through:
# for user, task in results:
#
# Answer:
# Each result contains two ORM objects:
# one User object and one related Task object.


# Question 10:
# What is the difference between relationship traversal
# and an explicit JOIN query?
#
# Answer:
# Relationship traversal means navigating between
# related ORM objects using relationship attributes.
#
# Examples:
# user.tasks
# task.user
#
# An explicit JOIN query uses select() and join()
# to ask the database to combine related tables
# and optionally filter the results.
#
# Example:
# select(Task).join(Task.user)