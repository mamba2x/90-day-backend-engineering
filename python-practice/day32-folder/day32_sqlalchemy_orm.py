from sqlalchemy import (
    create_engine,
    String,
    Boolean,
    Integer
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


DATABASE_URL = "sqlite:///./tasks.db"


engine = create_engine(
    DATABASE_URL,
    echo=True
)


class Base(DeclarativeBase):
    pass


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


class Category(Base):

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


Base.metadata.create_all(engine)


# ------------------------------------
# TASK ANSWERS
# ------------------------------------

# What database are we using?
#
# Answer:
# SQLite


# What file will store our data?
#
# Answer:
# tasks.db


# What is the purpose of the engine?
#
# Answer:
# The engine is SQLAlchemy's main interface for
# communicating with the database and managing
# database connections.


# Why will our ORM models inherit from Base?
#
# Answer:
# Inheriting from Base allows SQLAlchemy to recognize
# the classes as ORM models and register their table
# metadata.


# Did SQLAlchemy create another tasks table
# when the script ran again?
#
# Answer:
# No.


# Why not?
#
# Answer:
# create_all() checks whether the table already exists
# and only creates tables that are missing.


# ------------------------------------
# ROUGH SQL EQUIVALENT
# ------------------------------------

# CREATE TABLE tasks (
#     id INTEGER PRIMARY KEY,
#     title VARCHAR(100) NOT NULL,
#     completed BOOLEAN NOT NULL,
#     priority INTEGER NOT NULL
# );


# ------------------------------------
# QUESTIONS
# ------------------------------------

# Question 1:
# What does ORM stand for?
#
# Answer:
# Object-Relational Mapping.


# Question 2:
# What problem does an ORM solve?
#
# Answer:
# An ORM maps Python classes and objects to relational
# database tables and rows, allowing application code
# to work with database data using Python objects.


# Question 3:
# Does using an ORM mean SQL is no longer important?
#
# Answer:
# No. SQL is still important for understanding
# relational databases, queries, performance and
# transactions.


# Question 4:
# What is the SQLAlchemy engine?
#
# Answer:
# The engine is SQLAlchemy's main interface for
# communicating with the database.


# Question 5:
# What is the purpose of DeclarativeBase?
#
# Answer:
# DeclarativeBase provides the base class that ORM
# models inherit from so SQLAlchemy can register
# their table mappings and metadata.


# Question 6:
# What does __tablename__ define?
#
# Answer:
# It defines the name of the database table mapped
# to the ORM model.


# Question 7:
# What does primary_key=True mean?
#
# Answer:
# It marks the column as the table's primary key,
# uniquely identifying each row.


# Question 8:
# What does nullable=False mean?
#
# Answer:
# The database column cannot contain NULL.


# Question 9:
# What is the difference between TaskCreate and
# the SQLAlchemy Task model?
#
# Answer:
# TaskCreate is a Pydantic schema used to validate
# API input. Task is a SQLAlchemy ORM model used to
# represent data stored in the database.


# Question 10:
# What does Base.metadata.create_all(engine) do?
#
# Answer:
# It creates tables for registered ORM models that
# do not already exist in the database.