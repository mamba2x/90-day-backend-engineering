from sqlalchemy.exc import IntegrityError
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

# Task Update
class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    completed: bool | None = None

    priority: int | None = Field(
        default=None,
        ge=1,
        le=5
    )

# the database session dependency 
def get_Session():
    with Session(engine) as session:
        yield session

# get_task_dependency

def get_task_or_404(session:Session, task_id:int):
    statement = select(Task).where(Task.id==task_id)
    task = session.scalar(statement)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task not found"
        )
    else:
        return task
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
    "/tasks/min_priority",
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
    task = get_task_or_404(session,task_id)

    return task

@app.patch('/tasks/{task_id}', response_model=TaskResponse)
def updated_task(updated_task:TaskUpdate, task_id:int, session:Session=Depends(get_Session)):
    task = get_task_or_404(session,task_id)

    update= updated_task.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    for field, value in update.items():
        setattr(
            task,field,value
        )
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unable to update task"
    )
    return task

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    session: Session = Depends(get_Session)
):

    task= get_task_or_404(session,task_id)
    session.delete(task)

    session.commit()
    
# exclude_unset=True 
# is used to ensure to exclude keys that the user didn't provide value to

# Question 1:
# Why do we use a separate TaskUpdate model
# instead of TaskCreate for PATCH?
#
# Answer:cause we have to make them optional so when using post it wont trow error


# Question 2:
# What does model_dump(exclude_unset=True) do?
#
# Answer:it exclude keys user didn't provide


# Question 3:
# Why is exclude_unset especially useful
# for PATCH requests?
#
# Answer:


# Question 4:
# What does setattr(task, field, value) do?
#
# Answer:it sets the task, key and value 


# Question 5:
# If only "completed" is sent in a PATCH
# request, what should happen to title and
# priority?
#
# Answer:it still remains the same


# Question 6:
# Why can an ORM object retrieved through
# the Session be updated without calling
# session.add() again?
#
# Answer:by using the scalar 


# Question 7:
# What does session.delete(task) do?
#
# Answer:keeps the task to be deleted


# Question 8:
# Why do we call session.commit() after
# session.delete(task)?
#
# Answer: it permanently delete the data


# Question 9:
# Why is get_task_or_404() useful?
#
# Answer:it gets the particular task and also throws error message when called


# Question 10:
# Why should session.rollback() be called
# if commit() raises a database error?
#
# Answer: to cancels the uncommitted change


# Question 11:
# What does HTTP 204 No Content mean?
#
# Answer: no task found


# Question 12:
# After DELETE succeeds, how can we prove
# the task was actually removed?
#
# Answer:we get the task