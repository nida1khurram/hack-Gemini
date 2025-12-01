from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pydantic import BaseModel
import uuid
import enum
from datetime import datetime

from .database import Base
from .user import User
from .chapter import Chapter

class ProgressStatus(str, enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"

class UserChapterProgress(Base):
    __tablename__ = "user_chapter_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    status = Column(Enum(ProgressStatus), default=ProgressStatus.not_started)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User")
    chapter = relationship("Chapter")

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
