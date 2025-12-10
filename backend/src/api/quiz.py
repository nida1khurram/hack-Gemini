from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel

from .. import models
from ..database import get_db
from ..middleware.auth import get_current_user

router = APIRouter()

class QuizAttemptRequest(BaseModel):
    quiz_id: int
    score: float

@router.post("/attempts/", response_model=models.UserQuizAttemptInDB)
async def submit_quiz_attempt(
    request: QuizAttemptRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    attempt = models.UserQuizAttempt(
        user_id=current_user.id,
        quiz_id=request.quiz_id,
        score=request.score
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

@router.get("/attempts/{quiz_id}", response_model=List[models.UserQuizAttemptInDB])
async def get_quiz_attempts(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    attempts = db.query(models.UserQuizAttempt).filter(
        models.UserQuizAttempt.user_id == current_user.id,
        models.UserQuizAttempt.quiz_id == quiz_id
    ).all()
    return attempts
