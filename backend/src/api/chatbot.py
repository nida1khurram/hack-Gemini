from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..services.chatbot_service import ChatbotService
from ..vector_db import get_qdrant_client
from qdrant_client import QdrantClient

router = APIRouter()

class ChatbotQuery(BaseModel):
    query: str
    context: str | None = None

@router.post("/query")
async def query_chatbot(query: ChatbotQuery, qdrant_client: Annotated[QdrantClient, Depends(get_qdrant_client)]):
    chatbot_service = ChatbotService(qdrant_client)
    response = await chatbot_service.query(query.query, query.context)
    return {"response": response}
