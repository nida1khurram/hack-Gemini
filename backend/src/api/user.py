from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .. import models
from ..database import get_db

router = APIRouter()

@router.get("/profile", response_model=models.UserRead) # Changed response_model to UserRead
async def read_user_profile(
    db: Annotated[Session, Depends(get_db)]
):
    # For now, return a default user profile without authentication
    # In a real implementation, you might want to pass user_id as a parameter
    # or have other ways to identify the user without JWT
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User profile access requires authentication which has been removed"
    )


@router.put("/profile", response_model=models.UserRead) # New PUT endpoint
async def update_user_profile(
    db: Annotated[Session, Depends(get_db)]
):
    # For now, return a default user profile without authentication
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User profile update requires authentication which has been removed"
    )