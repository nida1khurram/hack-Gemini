from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models
from ..middleware.auth import get_current_user, get_db_session

router = APIRouter()

@router.get("/profile", response_model=models.UserInDB)
async def read_user_profile(current_user: Annotated[models.User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db_session)]):
    return current_user
