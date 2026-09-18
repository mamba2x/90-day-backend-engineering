from sqlalchemy import (
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    create_engine,
    Index,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)

from sqlalchemy.exc import IntegrityError


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = "sqlite:///./day40.db"

engine = create_engine(
    DATABASE_URL,
    echo=True
)


# ============================================================
# BASE MODEL
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# USER MODEL
# ============================================================

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
        nullable=False,
        unique=True
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user"
    )

    projects: Mapped[list["Project"]] = relationship(
        back_populates="user"
    )


# ============================================================
# PROJECT MODEL
# ============================================================

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="projects"
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project"
    )


# ============================================================
# TASK MODEL
# ============================================================

class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        Index(
            "ix_tasks_user_id_completed",
            "user_id",
            "completed"
        ),

        CheckConstraint(
            "priority >= 1 AND priority <= 5",
            name="ck_tasks_priority_range"
        ),
    )

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

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    due_date: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )

    project: Mapped["Project | None"] = relationship(
        back_populates="tasks"
    )


# ============================================================
# PART A - TEST VALID DATA
# ============================================================

print("\n========== VALID PRIORITY TEST ==========\n")

with Session(engine) as session:

    michael = User(
        name="Michael",
        email="michael.day45@example.com"
    )

    backend_project = Project(
        name="Backend Engineering",
        user=michael
    )

    valid_task = Task(
        title="Study Database Constraints",
        priority=4,
        user=michael,
        project=backend_project
    )

    try:
        session.add_all([
            michael,
            backend_project,
            valid_task
        ])

        session.commit()

        print("Valid data successfully stored.")
        print(f"Task: {valid_task.title}")
        print(f"Priority: {valid_task.priority}")

    except IntegrityError as error:
        session.rollback()

        print("Valid data unexpectedly failed.")
        print(error)


# ============================================================
# PART B - TEST INVALID PRIORITY
# ============================================================

print("\n========== INVALID PRIORITY TEST ==========\n")

with Session(engine) as session:

    # Retrieve the existing Michael created above.
    michael = session.get(User, 1)

    if michael is not None:

        # Use one of Michael's existing projects.
        backend_project = michael.projects[0]

        invalid_task = Task(
            title="Impossible Priority",
            priority=100,
            user=michael,
            project=backend_project
        )

        try:
            session.add(invalid_task)

            session.commit()

            print("ERROR: Invalid priority was accepted.")

        except IntegrityError as error:
            session.rollback()

            print(
                "Database rejected invalid priority."
            )

            print(error)

    else:
        print("Michael was not found.")


# ============================================================
# PART C - TEST DUPLICATE EMAIL
# ============================================================

print("\n========== DUPLICATE EMAIL TEST ==========\n")

with Session(engine) as session:

    first_user = User(
        name="Sarah",
        email="duplicate@example.com"
    )

    try:
        session.add(first_user)
        session.commit()

        print("First user successfully created.")

    except IntegrityError as error:
        session.rollback()

        print(
            "The first user could not be created."
        )

        print(error)


with Session(engine) as session:

    second_user = User(
        name="John",
        email="duplicate@example.com"
    )

    try:
        session.add(second_user)

        session.commit()

        # We should NOT reach this point if the UNIQUE
        # constraint is working.
        print(
            "ERROR: Duplicate email was accepted."
        )

    except IntegrityError as error:
        session.rollback()

        print(
            "Database rejected duplicate email."
        )

        print(error)


# ============================================================
# FINAL CHALLENGE
# ============================================================

# Rule:
# User email must be unique.
#
# Database mechanism:
# UNIQUE


# Rule:
# Task priority must be between 1 and 5.
#
# Database mechanism:
# CHECK


# Rule:
# Task title must exist and cannot be NULL.
#
# Database mechanism:
# NOT NULL


# Rule:
# Task.project_id must reference an existing Project
# whenever project_id is not NULL.
#
# Database mechanism:
# FOREIGN KEY


# Why still use application/Pydantic validation?
#
# Application validation allows invalid input to be rejected
# before it reaches the database.
#
# This gives the client clearer error messages and avoids
# unnecessary database operations.
#
# Database constraints provide another layer of protection.
# They guarantee that invalid data cannot be stored even if
# application validation is bypassed or contains a bug.
#
# Therefore:
#
# Application validation
#     ↓
# Protects the application/API boundary
#
# Database constraints
#     ↓
# Protect the integrity of stored data


# ============================================================
# DAY 45 Q&A
# ============================================================


# 1. What is a database constraint?
#
# A database constraint is a rule enforced by the database
# that restricts what data can be stored.
#
# It helps protect the integrity and consistency of the
# database.
#
# Examples include:
#
# PRIMARY KEY
# FOREIGN KEY
# UNIQUE
# NOT NULL
# CHECK


# 2. What is the difference between UNIQUE and NOT NULL?
#
# UNIQUE prevents duplicate values from being stored in a
# column or constrained set of columns.
#
# NOT NULL prevents a column from containing NULL.
#
# They solve different problems.
#
# For example:
#
# email = NULL
#
# is prevented by NOT NULL.
#
# Two rows containing:
#
# michael@example.com
#
# can be prevented by UNIQUE.
#
# Important:
#
# NOT NULL does not necessarily prevent an empty string "".
#
# NULL and "" are different values.


# 3. What does:
#
# CHECK(priority >= 1 AND priority <= 5)
#
# protect against?
#
# It prevents the database from storing priority values
# outside the allowed range.
#
# Valid:
#
# 1
# 2
# 3
# 4
# 5
#
# Invalid:
#
# 0
# -1
# 6
# 100


# 4. Why should email uniqueness be enforced by the database
#    even if the application checks whether an email already
#    exists?
#
# Because application-level checking alone may not be enough,
# especially when multiple requests happen concurrently.
#
# Two requests could check for the same email at almost the
# same time.
#
# Both could initially see that the email does not exist.
#
# Without a database UNIQUE constraint, both requests could
# then attempt to insert the same email.
#
# The UNIQUE constraint makes the database the final authority
# and prevents duplicate email values from being stored.


# 5. What is the difference between application validation
#    and database constraints?
#
# Application validation checks whether incoming data is
# acceptable before the application attempts to store it.
#
# For example, Pydantic could reject:
#
# priority = 100
#
# before SQLAlchemy performs an INSERT.
#
# Database constraints are rules enforced by the database
# itself.
#
# They protect the stored data even if application validation
# is bypassed, forgotten or contains a bug.
#
# Mental model:
#
# Application validation
#     ↓
# "Should this input be accepted by my application?"
#
# Database constraint
#     ↓
# "Is this data ever allowed to exist in my database?"


# 6. Why can adding a new constraint to an existing database
#    cause a migration to fail?
#
# Because existing rows may already violate the new rule.
#
# For example, imagine the database already contains:
#
# priority = 100
#
# and we later introduce:
#
# CHECK(priority >= 1 AND priority <= 5)
#
# The existing value violates the new constraint.
#
# Similarly, if duplicate emails already exist, adding a
# UNIQUE constraint to email may fail until those duplicates
# are resolved.
#
# Therefore, existing data should be inspected and cleaned
# before stricter constraints are introduced.


# 7. What exception can SQLAlchemy raise when the database
#    rejects an INSERT because of an integrity constraint?
#
# IntegrityError
#
# It can occur when database integrity rules are violated,
# such as:
#
# UNIQUE
# CHECK
# NOT NULL
# FOREIGN KEY
#
# depending on the database and operation.


# 8. Why should session.rollback() be called after a failed
#    commit caused by an IntegrityError?
#
# When the commit fails, the current database transaction has
# failed.
#
# rollback() rolls back the failed transaction and resets the
# Session's transactional state so that it can be used again.
#
# Mental model:
#
# Attempt INSERT
#     ↓
# Constraint violated
#     ↓
# commit() fails
#     ↓
# IntegrityError
#     ↓
# session.rollback()
#     ↓
# Failed transaction is cleared
#     ↓
# Session can continue being used