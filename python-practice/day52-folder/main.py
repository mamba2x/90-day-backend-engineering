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


DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# --------------------------------------------------
# Database
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


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    email: str


# --------------------------------------------------
# Password Hashing
# --------------------------------------------------

password_hash = PasswordHash.recommended()


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