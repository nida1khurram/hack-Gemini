from sqlmodel import SQLModel, Field
from sqlalchemy import String, DateTime, Column
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
import uuid
import enum
from typing import Optional

class UserBackground(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(sa_column=Column(String, unique=True, index=True))
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    hashed_password: str = Field(sa_column=Column(String))
    hashed_refresh_token: Optional[str] = Field(sa_column=Column(String, nullable=True))  # New field
    refresh_token_expires_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))  # New field
    background: UserBackground = Field(sa_column=Column(String, default=UserBackground.beginner))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), onupdate=func.now()))

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    background: UserBackground = UserBackground.beginner

class UserInDB(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    background: UserBackground
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

