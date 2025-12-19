from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel

from .. import models
from ..database import get_db

router = APIRouter()

class QuizAttemptRequest(BaseModel):
    quiz_id: int
    score: float

@router.post("/attempts/", response_model=models.UserQuizAttemptInDB)
async def submit_quiz_attempt(
    request: QuizAttemptRequest,
    db: Session = Depends(get_db)
):
    # For now, this requires a user ID to be passed differently since auth is removed
    raise HTTPException(
        status_code=501,
        detail="Quiz attempts require user authentication which has been removed"
    )

@router.get("/attempts/{quiz_id}", response_model=List[models.UserQuizAttemptInDB])
async def get_quiz_attempts(
    quiz_id: int,
    db: Session = Depends(get_db)
):
    # For now, this requires a user ID to be passed differently since auth is removed
    raise HTTPException(
        status_code=501,
        detail="Quiz attempts require user authentication which has been removed"
    )
