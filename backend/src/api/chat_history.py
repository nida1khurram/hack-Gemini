from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID

from ..database import get_db
from ..models.chat_history import ChatHistory
from ..services.chat_history_service import ChatHistoryService

router = APIRouter()

@router.get("/history", response_model=List[ChatHistory])
async def get_user_chat_history(
    db: Annotated[Session, Depends(get_db)]
):
    # For now, return empty list since we removed authentication
    # In a real implementation, you'd need another way to identify the user
    raise HTTPException(
        status_code=501,
        detail="Chat history requires user authentication which has been removed"
    )

@router.delete("/history/{history_id}", response_model=dict)
async def delete_user_chat_history(
    history_id: UUID,
    db: Annotated[Session, Depends(get_db)]
):
    # For now, raise error since we removed authentication
    raise HTTPException(
        status_code=501,
        detail="Deleting chat history requires user authentication which has been removed"
    )