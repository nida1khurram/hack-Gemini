from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from pydantic import BaseModel

from ..services.chatbot_service import ChatbotService
from ..vector_db import get_qdrant_client
from qdrant_client import QdrantClient
from ..database import get_db

router = APIRouter()

class ChatbotQuery(BaseModel):
    query: str
    context: str | None = None

@router.post("/query")
async def query_chatbot(
    query: ChatbotQuery,
    qdrant_client: Annotated[QdrantClient, Depends(get_qdrant_client)],
    db: Annotated[Session, Depends(get_db)]
):
    # For now, using a placeholder user ID since we removed authentication
    # In a real implementation, you might use session-based IDs or anonymous IDs
    chatbot_service = ChatbotService(qdrant_client, db, "anonymous_user") # Pass db and anonymous user_id
    response = await chatbot_service.query(query.query, query.context)
    return {"response": response}
