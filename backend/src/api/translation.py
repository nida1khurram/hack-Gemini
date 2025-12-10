from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..services.translation_service import TranslationService
from ..middleware.auth import get_current_user
from .. import models

router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    target_language: str

@router.post("/")
async def translate_text(request: TranslationRequest, current_user: models.User = Depends(get_current_user)):
    translation_service = TranslationService()
    translated_text = await translation_service.translate(request.text, request.target_language)
    return {"translated_text": translated_text}
