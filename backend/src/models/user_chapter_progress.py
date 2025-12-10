from sqlmodel import SQLModel, Field
from sqlalchemy import Integer, String, DateTime, Column
from sqlalchemy.sql import func
from pydantic import BaseModel
import uuid
import enum
from datetime import datetime
from typing import Optional

class ProgressStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"

class UserChapterProgress(SQLModel, table=True):
    __tablename__ = "user_chapter_progress"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    chapter_id: int = Field(foreign_key="chapters.id")
    status: ProgressStatus = Field(sa_column=Column(String, default=ProgressStatus.not_started))
    started_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    completed_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=True))

class UserChapterProgressBase(BaseModel):
    user_id: uuid.UUID
    chapter_id: int
    status: ProgressStatus = ProgressStatus.not_started

class UserChapterProgressCreate(UserChapterProgressBase):
    pass

class UserChapterProgressInDB(UserChapterProgressBase):
    id: uuid.UUID
    started_at: datetime
    completed_at: datetime | None = None

    class Config:
        from_attributes = True
