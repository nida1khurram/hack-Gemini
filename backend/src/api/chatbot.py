from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel

from ..services.chatbot_service import ChatbotService
from ..vector_db import get_qdrant_client
from qdrant_client import QdrantClient
from ..middleware.auth import get_current_user, get_db_session # Import get_db_session
from .. import models

router = APIRouter()

class ChatbotQuery(BaseModel):
    query: str
    context: str | None = None

@router.post("/query")
async def query_chatbot(
    query: ChatbotQuery,
    qdrant_client: Annotated[QdrantClient, Depends(get_qdrant_client)],
    db: Annotated[Session, Depends(get_db_session)], # Add db session dependency
    current_user: models.User = Depends(get_current_user)
):
    chatbot_service = ChatbotService(qdrant_client, db, current_user.id) # Pass db and user_id
    response = await chatbot_service.query(query.query, query.context)
    return {"response": response}
