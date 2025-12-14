# backend/src/models/user.py

from typing import Optional
import enum
import uuid

from sqlmodel import Field, SQLModel, Relationship
from fastapi_users import schemas

class UserBackground(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

class UserProfile(SQLModel, table=True):
    __tablename__ = "userprofile"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    background: UserBackground = Field(default=UserBackground.beginner)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", unique=True) # Changed to uuid.UUID
    user: Optional["User"] = Relationship(back_populates="profile")

class User(SQLModel, table=True):
    __tablename__ = "users" # Changed table name to users
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True) # Changed to UUID
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    
    profile: Optional[UserProfile] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

# Pydantic Schemas for API
class UserRead(schemas.BaseUser[uuid.UUID]): # Changed to uuid.UUID
    username: str
    background: UserBackground
    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    username: str
    background: UserBackground = UserBackground.beginner

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    background: Optional[UserBackground] = None