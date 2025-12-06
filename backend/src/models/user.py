from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pydantic import BaseModel
import uuid
import enum

from .database import Base

class UserBackground(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    hashed_refresh_token = Column(String, nullable=True) # New field
    refresh_token_expires_at = Column(DateTime(timezone=True), nullable=True) # New field
    background = Column(Enum(UserBackground), default=UserBackground.beginner)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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
    created_at: DateTime
    updated_at: DateTime

    class Config:
        from_attributes = True

