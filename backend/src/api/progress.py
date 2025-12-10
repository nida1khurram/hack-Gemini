from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
import uuid

from .. import models
from ..database import get_db
from ..middleware.auth import get_current_user

router = APIRouter()

class ChapterProgressRequest(BaseModel):
    chapter_id: int

@router.post("/", response_model=models.UserChapterProgressInDB)
async def mark_chapter_complete(
    request: ChapterProgressRequest, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    progress = db.query(models.UserChapterProgress).filter(
        models.UserChapterProgress.user_id == current_user.id,
        models.UserChapterProgress.chapter_id == request.chapter_id
    ).first()

    if progress:
        progress.status = models.ProgressStatus.completed
        progress.completed_at = models.func.now()
    else:
        progress = models.UserChapterProgress(
            user_id=current_user.id,
            chapter_id=request.chapter_id,
            status=models.ProgressStatus.completed,
            completed_at=models.func.now()
        )
        db.add(progress)

    db.commit()
    db.refresh(progress)
    return progress

@router.get("/", response_model=List[models.UserChapterProgressInDB])
async def get_user_progress(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    progress = db.query(models.UserChapterProgress).filter(
        models.UserChapterProgress.user_id == current_user.id
    ).all()
    return progress
