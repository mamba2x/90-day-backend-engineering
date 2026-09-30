from datetime import datetime, timedelta, timezone

import jwt

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from pwdlib import PasswordHash

from sqlalchemy import create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
)


# --------------------------------------------------
# JWT Configuration
# --------------------------------------------------

SECRET_KEY = "change-this-secret-in-production"
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


Base.metadata.create_all(engine)


# --------------------------------------------------
# Pydantic Schemas
# --------------------------------------------------

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

app = FastAPI()


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