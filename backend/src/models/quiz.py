from sqlmodel import SQLModel, Field
from sqlalchemy import Integer, String, Text, DateTime, Column
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Quiz(SQLModel, table=True):
    __tablename__ = "quizzes"

    id: int = Field(default=None, primary_key=True)
    module_id: int = Field(foreign_key="modules.id")  # Foreign key to Module
    title: str = Field(sa_column=Column(String, index=True))
    description: Optional[str] = Field(sa_column=Column(Text, nullable=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), onupdate=func.now()))

class QuizBase(BaseModel):
    module_id: int
    title: str
    description: str | None = None

class QuizCreate(QuizBase):
    pass

class QuizInDB(QuizBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True