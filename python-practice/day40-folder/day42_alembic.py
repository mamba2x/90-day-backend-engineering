from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
    create_engine,
    Index
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)


DATABASE_URL = "sqlite:///./day40.db"

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


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


class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
    Index(
        "ix_tasks_user_id_completed",
        "user_id",
        "completed"
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
        index= True
    )

    due_date: Mapped[str | None] = mapped_column(
    String(20),
    nullable=True
)

    user: Mapped["User"] = relationship(
        back_populates="tasks",

    )

# SELECT *
# FROM tasks
# WHERE user_id = 10;

# INDEX(user_id)

# SELECT *
# FROM tasks
# WHERE user_id = 10
# AND completed = false;
# INDEX(user_id,completed)



# this are the ones i will keep
# INDEX(user_id)
# 1. What problem does a database index solve?
# An index provides an additional data structure that can help the
# database locate matching rows more efficiently instead of scanning
# a large portion of the table.


# 2. Does an index make every database operation faster?
# No. Indexes can improve certain read queries, but INSERT, UPDATE,
# and DELETE operations can become more expensive because the
# database must also maintain the indexes.


# 3. What is the difference between a foreign key and an index?
# A foreign key provides referential integrity between tables.
# An index is primarily used to improve the performance of
# appropriate query patterns.


# 4. Why is user_id a reasonable column to index?
# Our application frequently retrieves Tasks belonging to a specific
# User using WHERE user_id = ?. An index on user_id can potentially
# make this lookup more efficient.


# 5. Does index=True automatically modify an existing database?
# No. It changes SQLAlchemy's model metadata, but the existing
# database still needs a schema migration.


# 6. Why do we still need Alembic?
# Alembic generates, tracks, and applies the schema migration that
# creates the index in the existing database.


# 7. What should upgrade() contain?
# It should contain the operation that creates the new index,
# normally using op.create_index(...).


# 8. What should downgrade() generally do?
# It should reverse the schema change by removing the index,
# normally using op.drop_index(...).


# 9. What is a composite index?
# A composite index is one index containing multiple columns,
# such as INDEX(user_id, completed).


# 10. Why can column order matter?
# Composite indexes are ordered by their columns. An index such as
# (user_id, completed) is organised beginning with user_id, so index
# order should be chosen based on actual query patterns.


# 11. Why might an index on completed be less useful?
# completed is a boolean with only two possible values. Many rows may
# have the same value, so the index may have low selectivity and may
# not reduce the amount of data the database needs to examine enough
# to justify using it.


# 12. What costs do indexes introduce?
# Indexes require additional storage and maintenance. INSERT, UPDATE,
# and DELETE operations may become more expensive because relevant
# indexes must also be updated.


# 13. Does creating an index guarantee it will be used?
# No. The database query planner decides whether using an index or
# another strategy is more efficient for a particular query.


# 14. Why shouldn't we index every column?
# Every index requires storage and write maintenance, and some indexes
# may provide little performance benefit. Indexes should therefore be
# based on actual query patterns.


# 15. What index would I consider for:
# WHERE user_id = ? AND completed = false?
#
# I would consider INDEX(user_id, completed) because the application
# frequently filters using these columns together.