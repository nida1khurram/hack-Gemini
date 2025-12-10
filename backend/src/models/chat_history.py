from typing import Optional
import datetime
import uuid

from sqlmodel import Field, SQLModel
from sqlalchemy import Text, Column, DateTime
from sqlalchemy.sql import func
import json

# Re-using the User from existing models for relationship
# from .user import User

class ChatMessage(SQLModel):
    role: str
    content: str

class ChatHistory(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id") # Foreign key to User model
    # conversation_id: uuid.UUID = Field(default_factory=uuid.uuid4, index=True) # If multiple conversations per user
    messages: str = Field(default='[]', sa_column=Column(Text))  # Store as JSON string
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, sa_column=Column(DateTime(timezone=True), default=func.now()))
    updated_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow, sa_column=Column(DateTime(timezone=True), onupdate=func.now()))

    # Example of a relationship (requires appropriate setup in main.py if used)
    # user: User = Relationship(back_populates="chat_histories")
