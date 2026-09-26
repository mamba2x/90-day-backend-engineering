from fastapi import Depends, FastAPI,HTTPException
from pydantic import BaseModel, ConfigDict

from sqlalchemy import create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)


DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str]

    priority: Mapped[int] = mapped_column(default=3)


Base.metadata.create_all(engine)


class TaskCreate(BaseModel):
    title: str
    priority: int = 3

class TaskUpdate(BaseModel):
    title: str | None = None
    priority: int | None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    priority: int


def get_session():

    with Session(engine) as session:
        yield session

# TASK Retrieve dependency
def get_task_or_404(
    task_id: int,
    session: Session
):

    task = session.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task

app = FastAPI()


@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    session: Session = Depends(get_session)
):

    return session.scalars(
        select(Task)
    ).all()

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
):

    return get_task_or_404(
        task_id,
        session
    )

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
):

    db_task = Task(
        title=task.title,
        priority=task.priority
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):

    task = get_task_or_404(
        task_id,
        session
    )

    update_data = task_update.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(task, field, value)

    session.commit()
    session.refresh(task)

    return task
@app.delete(
    "/tasks/{task_id}",
    status_code=204
)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):

    task = get_task_or_404(
        task_id,
        session
    )

    session.delete(task)
    session.commit()