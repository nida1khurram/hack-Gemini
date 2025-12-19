from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
import uuid

from .. import models
from ..database import get_db

router = APIRouter()

class ChapterProgressRequest(BaseModel):
    chapter_id: int

@router.post("/", response_model=models.UserChapterProgressInDB)
async def mark_chapter_complete(
    request: ChapterProgressRequest,
    db: Session = Depends(get_db)
):
    # For now, this requires a user ID to be passed differently since auth is removed
    # We'll return a proper response without authentication
    raise HTTPException(
        status_code=501,
        detail="Progress tracking requires user authentication which has been removed"
    )

@router.get("/", response_model=List[models.UserChapterProgressInDB])
async def get_user_progress(
    db: Session = Depends(get_db)
):
    # For now, this requires a user ID to be passed differently since auth is removed
    raise HTTPException(
        status_code=501,
        detail="Progress tracking requires user authentication which has been removed"
    )
