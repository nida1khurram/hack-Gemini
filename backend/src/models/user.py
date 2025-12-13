# backend/src/models/user.py

from datetime import datetime
from typing import Optional
import uuid
import enum

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel # Keep BaseModel for now for UserCreate, UserInDB
from fastapi_users import schemas

class UserBackground(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    expert = "expert"

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    background: UserBackground = Field(sa_column=Column(String, default=UserBackground.beginner))
    # Add other profile fields here as needed
    # Link back to User
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", unique=True)
    user: Optional["User"] = Relationship(back_populates="profile")


class User(SQLModel, SQLAlchemyBaseUserTable, table=True): # Inherit from SQLAlchemyBaseUserTable
    # Inherits from SQLModel, SQLAlchemyBaseUserTable for fastapi-users compatibility
    # id field is provided by SQLAlchemyBaseUserTable (int)
    # email field is provided by SQLAlchemyBaseUserTable (str, unique, index)
    # hashed_password field is provided by SQLAlchemyBaseUserTable (str)
    
    # Custom fields from existing User model
    # Note: username and background are moved to UserProfile to maintain clean separation
    # but kept here for initial migration if needed, then moved to profile.
    # For now, let's keep them here as optional fields to facilitate migration
    # and then move to profile in a separate task.

    # These fields are required by FastAPI-Users BaseUserTable
    # They will be explicitly set during migration or new user creation
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

    # Link to UserProfile
    profile_id: Optional[int] = Field(default=None, foreign_key="userprofile.id")
    profile: Optional[UserProfile] = Relationship(back_populates="user")


# Pydantic Schemas for API (fastapi-users compatible)

class UserRead(schemas.BaseUser[int]):
    username: str # Add username to UserRead from profile
    background: UserBackground # Add background to UserRead from profile
    # is_active, is_superuser, is_verified are already in BaseUser
    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    username: str # Add username to UserCreate
    background: UserBackground = UserBackground.beginner # Add background to UserCreate

class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None # Allow updating username
    background: Optional[UserBackground] = None # Allow updating background