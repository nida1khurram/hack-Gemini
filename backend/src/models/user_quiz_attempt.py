from sqlmodel import SQLModel, Field
from sqlalchemy import Integer, Float, DateTime, Column
from sqlalchemy.sql import func
from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

class UserQuizAttempt(SQLModel, table=True):
    __tablename__ = "user_quiz_attempts"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    quiz_id: int  # Assuming quiz_id refers to a quiz defined elsewhere, not in DB directly
    score: float = Field(sa_column=Column(Float))
    attempted_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))

class UserQuizAttemptBase(BaseModel):
    user_id: uuid.UUID
    quiz_id: int
    score: float

class UserQuizAttemptCreate(UserQuizAttemptBase):
    pass

class UserQuizAttemptInDB(UserQuizAttemptBase):
    id: uuid.UUID
    attempted_at: datetime

    class Config:
        from_attributes = True
