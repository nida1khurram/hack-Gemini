from typing import Optional
import uuid
import enum

from sqlmodel import Field, SQLModel, Column, String
from pydantic import BaseModel # Keep BaseModel for now for UserCreate, UserInDB

class UserBackground(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

# Reverted to a simpler User model
class User(SQLModel, table=True):
    __tablename__ = "users" # Keep the table name as "users" for existing foreign keys
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(sa_column=Column(String, unique=True, index=True))
    email: str = Field(sa_column=Column(String, unique=True, index=True))
    # Removed hashed_password, is_active, is_superuser, is_verified as they are handled by Node.js auth
    background: UserBackground = Field(sa_column=Column(String, default=UserBackground.beginner))

# UserCreate schema (for creating users, maybe for chatbot internal use if needed)
class UserCreate(BaseModel):
    username: str
    email: str
    background: UserBackground = UserBackground.beginner

# No need for UserRead, UserUpdate, UserProfile if not directly managed by this backend
