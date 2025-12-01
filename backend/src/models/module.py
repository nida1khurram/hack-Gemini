from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from pydantic import BaseModel
from .database import Base
from datetime import datetime

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ModuleBase(BaseModel):
    title: str
    description: str | None = None

class ModuleCreate(ModuleBase):
    pass

class ModuleInDB(ModuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
