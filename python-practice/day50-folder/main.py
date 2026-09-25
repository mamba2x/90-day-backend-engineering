from fastapi import Depends, FastAPI
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


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    priority: int


def get_session():

    with Session(engine) as session:
        yield session


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