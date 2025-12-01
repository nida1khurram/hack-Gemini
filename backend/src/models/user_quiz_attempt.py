from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pydantic import BaseModel
import uuid
from datetime import datetime

from .database import Base
from .user import User

class UserQuizAttempt(Base):
    __tablename__ = "user_quiz_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    quiz_id = Column(Integer) # Assuming quiz_id refers to a quiz defined elsewhere, not in DB directly
    score = Column(Float)
    attempted_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

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
