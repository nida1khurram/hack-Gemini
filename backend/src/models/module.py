from sqlmodel import SQLModel, Field
from sqlalchemy import String, Text, DateTime, Column
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Module(SQLModel, table=True):
    __tablename__ = "modules"

    id: int = Field(default=None, primary_key=True)
    title: str = Field(sa_column=Column(String, index=True))
    description: Optional[str] = Field(sa_column=Column(Text, nullable=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), onupdate=func.now()))

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
