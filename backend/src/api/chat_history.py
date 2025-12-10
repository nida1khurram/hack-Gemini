from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from ..database import get_db
from ..middleware.auth import get_current_user, get_db_session
from ..models.user import User
from ..models.chat_history import ChatHistory
from ..services.chat_history_service import ChatHistoryService

router = APIRouter()

@router.get("/history", response_model=List[ChatHistory])
async def get_user_chat_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db_session)]
):
    chat_history_service = ChatHistoryService(db)
    histories = chat_history_service.get_user_chat_histories(current_user.id)
    return histories

@router.delete("/history/{history_id}", response_model=dict)
async def delete_user_chat_history(
    history_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db_session)]
):
    chat_history_service = ChatHistoryService(db)
    # Ensure the user owns the history they are trying to delete
    history_to_delete = chat_history_service.get_chat_history_by_id(history_id)
    if not history_to_delete or history_to_delete.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat history not found or not authorized")
        
    success = chat_history_service.delete_chat_history(history_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chat history not found")
    return {"message": "Chat history deleted successfully"}