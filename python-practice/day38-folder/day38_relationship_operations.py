from sqlalchemy import (
    Boolean,
    Integer,
    String,
    ForeignKey,
    create_engine
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

DATABASE_URL = "sqlite:///./day38_relationships.db"

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
# Create Michael and first task
# using task.user
# -----------------------------

with Session(engine) as session:

    michael = User(
        name="Michael",
        email="michael@example.com"
    )

    session.add(michael)
    session.commit()
    session.refresh(michael)

    task_1 = Task(
        title="Study FastAPI",
        completed=False,
        priority=4,
        user=michael
    )

    session.add(task_1)
    session.commit()
    session.refresh(task_1)

    michael_id = michael.id
    task_1_id = task_1.id

    print("Task user_id:", task_1.user_id)
    print("Task user id:", task_1.user.id)


# -----------------------------
# Add another task through
# michael.tasks.append()
# -----------------------------

with Session(engine) as session:

    michael = session.get(User, michael_id)

    if michael is None:
        print("Michael not found")
    else:
        michael.tasks.append(
            Task(
                title="Study C++",
                completed=False,
                priority=2
            )
        )

        session.commit()


# -----------------------------
# Retrieve Michael
# and print all his tasks
# -----------------------------

with Session(engine) as session:

    michael = session.get(User, michael_id)

    if michael is None:
        print("Michael not found")
    else:
        print("\nMichael's Tasks:")

        for task in michael.tasks:
            print(
                f"{task.title} - "
                f"Priority: {task.priority}"
            )


# -----------------------------
# Retrieve one task
# and navigate to its user
# -----------------------------

with Session(engine) as session:

    task = session.get(Task, task_1_id)

    if task is None:
        print("Task not found")
    else:
        print("\nTask Details:")
        print("Title:", task.title)
        print("Owner:", task.user.name)
        print("Owner Email:", task.user.email)
        print("user_id:", task.user_id)
        print("task.user.id:", task.user.id)


# -----------------------------
# Final challenge: Sarah
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
            title="Read Documentation",
            completed=False,
            priority=3
        )
    )

    session.add(sarah)
    session.commit()
    session.refresh(sarah)

    sarah_id = sarah.id


# -----------------------------
# Retrieve Sarah and print tasks
# -----------------------------

with Session(engine) as session:

    sarah = session.get(User, sarah_id)

    if sarah is None:
        print("Sarah not found")
    else:
        print("\nSarah's Tasks:")

        for task in sarah.tasks:
            print(
                f"{task.title} - "
                f"Priority: {task.priority}"
            )


# ==========================================
# DAY 38 QUESTIONS & ANSWERS
# ==========================================


# Question 1:
# What is the difference between
# task.user_id and task.user?
#
# Answer:
# task.user_id contains the foreign key value,
# such as 1 or 3.
#
# task.user contains the related User ORM object.
#
# For example:
# task.user_id -> 1
# task.user -> User object for user with id 1


# Question 2:
# If michael.id is 3 and I create a Task
# with user=michael, what should the Task's
# user_id eventually become?
#
# Answer:
# The Task's user_id should become 3 because
# Michael's primary key is 3.


# Question 3:
# Why can SQLAlchemy determine the foreign key
# when we use user=michael?
#
# Answer:
# SQLAlchemy knows that Task.user is connected
# to Task.user_id through the relationship and
# ForeignKey configuration.
#
# Therefore, when user=michael is assigned,
# SQLAlchemy can use Michael's primary key as
# the Task's foreign key.


# Question 4:
# What happens when we do:
# michael.tasks.append(task)?
#
# Answer:
# The Task is added to Michael's tasks collection,
# and SQLAlchemy associates that Task with Michael
# through the ORM relationship.


# Question 5:
# After michael.tasks.append(task),
# what should task.user represent?
#
# Answer:
# task.user should represent the Michael User
# object because Michael owns that Task.


# Question 6:
# Why is michael.tasks a collection
# but task.user is not?
#
# Answer:
# Because User and Task have a one-to-many
# relationship.
#
# One User can have many Tasks, so michael.tasks
# is a collection.
#
# Each Task belongs to one User, so task.user
# is a single User object.


# Question 7:
# What does back_populates help SQLAlchemy
# keep synchronized?
#
# Answer:
# back_populates connects both sides of the
# relationship.
#
# It helps SQLAlchemy keep User.tasks and
# Task.user synchronized because they represent
# the same relationship from opposite directions.


# Question 8:
# Which approach is more ORM-oriented:
# user_id=michael.id or user=michael?
# Why?
#
# Answer:
# user=michael is more ORM-oriented because
# it works directly with the related User object
# instead of manually assigning the foreign key ID.


# Question 9:
# If task.user_id is 4,
# what does that value represent?
#
# Answer:
# It means that the Task belongs to the User
# whose primary key id is 4.


# Question 10:
# What is relationship traversal?
# Give one example.
#
# Answer:
# Relationship traversal means moving from one
# related ORM object to another through a
# relationship attribute.
#
# Example:
# task.user.name
#
# This moves from:
# Task -> User -> name
#
# Another example:
# user.tasks
#
# This moves from:
# User -> related Tasks