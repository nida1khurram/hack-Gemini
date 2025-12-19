from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..services.translation_service import TranslationService

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@router.post("/")
async def translate_text(request: TranslationRequest):
    translation_service = TranslationService()
    translated_text = await translation_service.translate(request.text, request.target_language)
    return {"translated_text": translated_text}
