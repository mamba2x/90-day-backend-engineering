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
    DATABASE_URL,
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
Base.metadata.create_all(engine)


with Session(engine) as session:
    new_task = Task(
    title="Study SQLAlchemy",
    completed=False,
    priority=4
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    
    # print(
    #     new_task.id,
    #     new_task.title,
    #     new_task.completed,
    #     new_task.priority
    # )

with Session(engine) as session:

    statement = select(Task)

    result = session.scalars(statement)

    all_tasks = result.all()

    for task in all_tasks:
        print(
            task.id,
            task.title,
            task.completed,
            task.priority
        )
    statement = select(Task).where(
    Task.priority >= 4
)
    result = session.scalars(statement)
    all_high_priority_tasks = result.all()
    for task in all_high_priority_tasks:
        print(
            task.id,
            task.title,
            task.completed,
            task.priority
        )
    statement = select(Task).where(
        Task.id == 1)
    task = session.scalar(statement)

    if task is None:
        print("Task not found")
    else:
        print(task.title)


    # What is the purpose of Session?
#
# Answer:it is to create a database session for engine

# Is new_task already permanently stored
# in SQLite at this point?
#
# Answer:NO 

# Does session.add() permanently save the
# task immediately?
#
# Answer:NO, it just know about the new task 

# What changes after commit()?
#
# Answer:it permanently saves the new task to the database 

# Why did we call refresh() after commit()?
#
# Answer:to update the task object with the latest values from the database

# Why did the ID increase instead of
# restarting from 1?
#
# Answer:it is because the previous task was still stored in the database and the ID is auto-incremented

# final task

with Session(engine) as session:
    first_task = Task(
        title="Final Task",
        completed=False,
        priority=2
    )
    second_task = Task(
        title="Second Task",
        completed=False,
        priority=4
    )
    third_task = Task(
        title="Third Task",
        completed=False,
        priority=5
    )
    session.add_all([first_task, second_task, third_task])
    session.commit()

with Session(engine) as session:
    statement = select(Task)
    tasks = session.scalars(statement).all()
    for task in tasks:
        print(
            task.id,
            task.title,
            task.completed,
            task.priority
        )

    statement =select(Task).where(Task.priority >= 4)
    high_priority = session.scalars(statement).all()
    for task in high_priority:
        print(
            task.id,
            task.title,
            task.completed,
            task.priority
        )
    chosen_id = 3
    statement  =select(Task).where(Task.id == chosen_id)
    chosen_task = session.scalar(statement)
    if chosen_task:
        print(
            chosen_task.id,
            chosen_task.title,
            chosen_task.completed,
            chosen_task.priority
        )    


# Question 1:
# What is a SQLAlchemy Session?
#
# Answer:it is used to create sessions for querying and persisting objects to the database. It is a workspace for your objects and allows you to interact with the database in a transactional manner.


# Question 2:
# What is the difference between the engine
# and a Session?
#
# Answer: The engine is the core interface for connecting to the database, while a Session is used to create transactions and interact with the database in a more object-oriented way.


# Question 3:
# Does creating Task(...) immediately insert
# a row into the database?
#
# Answer:No


# Question 4:
# What does session.add() do?
#
# Answer:it makes the session aware of the new object and marks it for insertion into the database when commit() is called.


# Question 5:
# What does session.commit() do?
#
# Answer:it saves all the changes made to the objects in the session to the database.


# Question 6:
# What does session.refresh() do?
#
# Answer:it updates the object with the latest values from the database.


# Question 7:
# Why don't we need max(id) + 1 anymore?
#
# Answer:because SQLAlchemy automatically handles the ID generation for us.


# Question 8:
# What does select(Task) roughly mean in SQL?
#
# Answer:it selects all columns from the tasks table.


# Question 9:
# What is the difference between:
#
# session.scalars(statement)
#
# and:
#
# session.scalar(statement)
#
# Answer: it retrieves the data from the table


# Question 10:
# Why do we use task.title instead of
# task["title"] now?
#
# Answer: Because we are working with SQLAlchemy objects, which have attributes that can be accessed using dot notation.