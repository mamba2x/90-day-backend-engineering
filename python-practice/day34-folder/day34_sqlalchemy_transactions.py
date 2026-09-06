from sqlalchemy.exc import IntegrityError

from sqlalchemy import (
    create_engine,
    String,
    Boolean,
    Integer,
    select
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session
)


DATABASE_URL = "sqlite:///./tasks.db"


engine = create_engine(
    DATABASE_URL
)


# ------------------------------------
# BASE
# ------------------------------------

class Base(DeclarativeBase):
    pass


# ------------------------------------
# TASK MODEL
# ------------------------------------

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


Base.metadata.create_all(engine)


# ==================================================
# TASK 1 + TASK 2
# CREATE TRANSACTION PRACTICE TASK
# ==================================================

with Session(engine) as session:

    task = Task(
        title="Transaction Practice",
        completed=False,
        priority=3
    )

    session.add(task)

    session.commit()

    session.refresh(task)

    update_id = task.id

    print(
        "Created:",
        task.id,
        task.title,
        task.completed,
        task.priority
    )


# ==================================================
# TASK 3
# UPDATE TASK
# ==================================================

with Session(engine) as session:

    statement = select(Task).where(
        Task.id == update_id
    )

    task = session.scalar(statement)

    if task is None:

        print("Task not found")

    else:

        print(
            "Before:",
            task.completed,
            task.priority
        )

        task.completed = True
        task.priority = 5

        session.commit()

        session.refresh(task)

        print(
            "After:",
            task.completed,
            task.priority
        )


# ==================================================
# TASK 4
# CONFIRM UPDATE USING A NEW SESSION
# ==================================================

with Session(engine) as session:

    statement = select(Task).where(
        Task.id == update_id
    )

    task = session.scalar(statement)

    if task is None:

        print("Updated task not found")

    else:

        print(
            "Confirmed update:",
            task.id,
            task.completed,
            task.priority
        )


# ==================================================
# TASK 5
# CREATE DELETE PRACTICE TASK
# ==================================================

with Session(engine) as session:

    delete_task = Task(
        title="Delete Practice",
        completed=False,
        priority=1
    )

    session.add(delete_task)

    session.commit()

    session.refresh(delete_task)

    delete_id = delete_task.id

    print(
        "Delete practice task created:",
        delete_id
    )


# ==================================================
# TASK 6
# DELETE TASK
# ==================================================

with Session(engine) as session:

    statement = select(Task).where(
        Task.id == delete_id
    )

    task = session.scalar(statement)

    if task is None:

        print("Task not found")

    else:

        session.delete(task)

        session.commit()

        print(
            f"Task {delete_id} deleted"
        )


# ==================================================
# TASK 7
# CONFIRM DELETION
# ==================================================

with Session(engine) as session:

    statement = select(Task).where(
        Task.id == delete_id
    )

    deleted_task = session.scalar(statement)

    if deleted_task is None:

        print("Deletion confirmed")

    else:

        print("Task still exists")


# ==================================================
# TASK 8 + TASK 9
# FAILED TRANSACTION + ROLLBACK
# ==================================================

with Session(engine) as session:

    bad_task = Task(
        title=None,
        completed=False,
        priority=3
    )

    session.add(bad_task)

    try:

        session.commit()

    except IntegrityError:

        session.rollback()

        print(
            "Database rejected invalid task."
        )

        print(
            "Transaction rolled back."
        )

    # Prove that the SAME Session still works
    # after rollback.

    statement = select(Task)

    tasks = session.scalars(
        statement
    ).all()

    print(
        "Session still works."
    )

    print(
        "Number of tasks:",
        len(tasks)
    )


# ==================================================
# FINAL CHALLENGE
# ATOMICITY
# ==================================================

with Session(engine) as session:

    valid_task = Task(
        title="Atomic Valid Task",
        completed=False,
        priority=4
    )

    invalid_task = Task(
        title=None,
        completed=False,
        priority=4
    )

    session.add_all([
        valid_task,
        invalid_task
    ])

    try:

        session.commit()

    except IntegrityError:

        session.rollback()

        print(
            "Atomic transaction failed."
        )

        print(
            "Both INSERT operations were rolled back."
        )


# ==================================================
# FINAL CHALLENGE EXPLANATION
# ==================================================

# Why should the valid task not be permanently
# saved when the invalid task causes the
# transaction to fail?
#
# Answer:
# Both INSERT operations are part of the same
# transaction. Atomicity means all operations in
# the transaction must succeed together.
#
# Since the invalid task causes the transaction
# to fail, rollback() cancels the entire transaction
# so the valid task is not permanently saved either.


# ==================================================
# TASK QUESTION
# ==================================================

# What type of problem can IntegrityError represent?
#
# Answer:
# IntegrityError represents a database operation
# that violates a database integrity constraint.
#
# Examples include:
# - inserting NULL into a NOT NULL column
# - violating a UNIQUE constraint
# - violating a foreign key constraint
# - attempting to create a duplicate primary key


# ==================================================
# DAY 34 QUESTIONS
# ==================================================

# Question 1:
# What is a database transaction?
#
# Answer:
# A database transaction is a unit of work containing
# one or more database operations that are treated
# together.
#
# The operations can either be committed successfully
# or rolled back when something fails.


# Question 2:
# What does session.commit() do?
#
# Answer:
# session.commit() commits the current transaction
# and makes its pending database changes permanent.


# Question 3:
# What does session.rollback() do?
#
# Answer:
# session.rollback() cancels the uncommitted changes
# in the current transaction and returns the Session
# to a usable state after a failed transaction.


# Question 4:
# Why should rollback() normally be called
# after a failed database transaction?
#
# Answer:
# A failed transaction leaves the Session's current
# transaction in a failed state.
#
# rollback() cancels the uncommitted work and resets
# the transaction so the Session can safely perform
# more database operations.


# Question 5:
# What does atomicity mean?
#
# Answer:
# Atomicity means that all operations in a transaction
# succeed together or none of them are permanently
# applied.
#
# It follows an "all or nothing" rule.


# Question 6:
# How do we update an ORM object that was
# loaded through a Session?
#
# Answer:
# We retrieve the ORM object, change its attributes,
# and then call session.commit().
#
# Example:
#
# task.completed = True
# task.priority = 5
# session.commit()


# Question 7:
# Do we need session.add(task) again after
# querying an existing task before updating it?
#
# Answer:
# No.
#
# An ORM object retrieved through the Session is
# already being tracked by that Session.
#
# We can modify its attributes and call commit()
# without calling add() again.


# Question 8:
# What does session.delete(task) do?
#
# Answer:
# session.delete(task) marks the ORM object for
# deletion in the current transaction.
#
# The deletion becomes permanent when
# session.commit() is called.


# Question 9:
# Does session.delete(task) immediately make
# the deletion permanent?
#
# Answer:
# No.
#
# session.delete(task) only marks the object for
# deletion.
#
# session.commit() makes the deletion permanent.


# Question 10:
# If two INSERTs are part of the same
# transaction and one fails, why is rollback
# useful?
#
# Answer:
# rollback() prevents only part of the transaction
# from being saved.
#
# If one INSERT fails, rollback() cancels the
# uncommitted work so neither INSERT becomes
# permanent.
#
# This preserves atomicity and helps keep the
# database consistent.