from datetime import datetime, timedelta, timezone
from fastapi.middleware.cors import CORSMiddleware
import os
import jwt
from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from pwdlib import PasswordHash

from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)
app = FastAPI()


allowed_origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# for protecting routes with JWT authentication
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

# --------------------------------------------------
# JWT Configuration
# --------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY","dev-secret-only")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# --------------------------------------------------
# Database Models
# --------------------------------------------------

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    email: Mapped[str] = mapped_column(
        unique=True
    )

    hashed_password: Mapped[str]

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str]

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )


Base.metadata.create_all(engine)


# --------------------------------------------------
# Pydantic Schemas
# --------------------------------------------------

class TaskCreate(BaseModel):
    title: str


class TaskResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    title: str
    owner_id: int

class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    email: str

class TaskUpdate(BaseModel):
    title: str | None = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


# --------------------------------------------------
# Password Hashing
# --------------------------------------------------

password_hash = PasswordHash.recommended()


# --------------------------------------------------
# JWT Helper
# --------------------------------------------------

def create_access_token(user_id: int):

    expires_at = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expires_at
    }

    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return access_token


# --------------------------------------------------
# Database Dependency
# --------------------------------------------------

def get_session():

    with Session(engine) as session:
        yield session


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------





# --------------------------------------------------
# Register User
# --------------------------------------------------

@app.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register_user(
    user: UserCreate,
    session: Session = Depends(get_session)
):

    existing_user = session.scalar(
        select(User).where(
            User.email == user.email
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = password_hash.hash(
        user.password
    )

    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


# --------------------------------------------------
# Login User
# --------------------------------------------------

@app.post(
    "/login",
    response_model=LoginResponse
)
def login_user(
    user: UserLogin,
    session: Session = Depends(get_session)
):

    db_user = session.scalar(
        select(User).where(
            User.email == user.email
        )
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_is_valid = password_hash.verify(
        user.password,
        db_user.hashed_password
    )

    if not password_is_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        db_user.id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    db_user = session.get(
        User,
        int(user_id)
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return db_user

@app.get(
    "/me",
    response_model=UserResponse
)
def get_me( 
    current_user: User = Depends(get_current_user)
):

    return current_user

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    db_task = Task(
        title=task.title,
        owner_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

# get the current user's tasks
@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    return session.scalars(
        select(Task).where(
            Task.owner_id == current_user.id
        )
    ).all()

def get_owned_task_or_404(
    task_id: int,
    current_user: User,
    session: Session
):

    task = session.get(
        Task,
        task_id
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not allowed"
        )

    return task

@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    return get_owned_task_or_404(
        task_id,
        current_user,
        session
    )

@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):

    task = get_owned_task_or_404(
        task_id,
        current_user,
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