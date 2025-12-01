from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime

from .database import Base

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String, index=True)
    content_english = Column(Text)
    content_urdu = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    module = relationship("Module")

class ChapterBase(BaseModel):
    module_id: int
    title: str
    content_english: str
    content_urdu: str | None = None

class ChapterCreate(ChapterBase):
    pass

class ChapterInDB(ChapterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
