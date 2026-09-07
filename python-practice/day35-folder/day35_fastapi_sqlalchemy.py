from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status,
    Query
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

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

app = FastAPI()

DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread":False
    }
)

class Base(DeclarativeBase):
    pass    


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

# task create pydantic
class Task_create(BaseModel):
    title: str = Field(
        min_length = 3,
        max_length= 100,
    )
    completed:bool =False
    priority :int =Field(
        default =3,
        le=5,
        ge=1
    )

# task response
class TaskResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    title: str
    completed: bool
    priority: int

# the database session dependency 
def get_Session():
    with Session(engine) as session:
        yield session

# injecting the session into route
@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    session: Session = Depends(get_Session)
):
    statement = select(Task)
    task = session.scalars(statement).all()

    return task

@app.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskResponse
)
def create_task(
    task_create: Task_create,
    session: Session = Depends(get_Session)
):

    task = Task(
        title=task_create.title,
        completed=task_create.completed,
        priority=task_create.priority
    )

    session.add(task)

    session.commit()

    session.refresh(task)

    return task



@app.get(
    "/tasks/filtered_task",
    response_model=list[TaskResponse]
)
def get_high_priority_task(session: Session = Depends(get_Session)
):
    statement = select(Task).where(
    Task.priority >= 4
)
    task = session.scalars(statement).all()
    return task

# final challenge
@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    min_priority: int | None = Query(
        default=None,
        ge=1,
        le=5
    ),
    session: Session = Depends(get_Session)
):

    statement = select(Task)

    if min_priority is not None:

        statement = statement.where(
            Task.priority >= min_priority
        )

    tasks = session.scalars(
        statement
    ).all()

    return tasks

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    session: Session = Depends(get_Session)
):

    statement = select(Task).where(
        Task.id == task_id
    )

    task = session.scalar(statement)

    if task is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


# Why does get_session() use yield
# instead of simply returning the Session?
#
# Answer: cause the program would still need to continue. and using yield allows the program to continue working after yield

# Did the task survive the FastAPI restart?
#
# Answer:YES


# Why?
#
# Answer:cause the sqlite stores the data and keeps it permanently even when the system crashes



# Question 1:
# What role does SQLAlchemy now play
# inside the FastAPI application?
#
# Answer:it's main role here is permanently storing data 


# Question 2:
# Why don't we need a Python tasks list
# anymore?
#
# Answer:cause we have sqlite that stores data in database


# Question 3:
# What does Depends(get_session) give
# a route?
#
# Answer: it gives a route the session that was created 


# Question 4:
# Why does get_session() use yield?
#
# Answer: cause it wants the program to continue to run after it has been called


# Question 5:
# What does ConfigDict(
# from_attributes=True
# ) allow TaskResponse to do?
#
# Answer:it allows pydantic models to be able to read ORM objects


# Question 6:
# What is the flow from incoming JSON to
# a database row in POST /tasks?
#
# Answer:its data is validated by the pydantic models then the sessions are created which is then used in create route by using dependency 


# Question 7:
# Why don't we manually generate task IDs
# anymore?
#
# Answer:cause sqlite generate it for us


# Question 8:
# Why is database filtering generally
# preferable to loading all records and
# filtering them in Python?
#
# Answer: it is more simpler and easier


# Question 9:
# What does session.scalar(statement)
# return when the requested task does
# not exist?
#
# Answer:not found


# Question 10:
# Why does a newly created task survive
# after the FastAPI server restarts?
#
# Answer:cause the data is stored in a sqlite database