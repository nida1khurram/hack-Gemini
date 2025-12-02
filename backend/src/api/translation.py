from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..services.translation_service import TranslationService

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str

@router.post("/")
async def translate_text(request: TranslationRequest):
    translation_service = TranslationService()
    translated_text = await translation_service.translate_to_urdu(request.text)
    return {"translated_text": translated_text}
