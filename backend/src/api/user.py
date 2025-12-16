from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .. import models
from ..middleware.auth import get_current_user, get_db_session # Keep for now, might be removed later
from ..services.user_service import fastapi_users # New import

router = APIRouter()

# Dependency for current active user using fastapi_users
current_active_user = fastapi_users.current_user(active=True)

@router.get("/profile", response_model=models.UserRead) # Changed response_model to UserRead
async def read_user_profile(
    current_user: Annotated[models.User, Depends(current_active_user)], # Use fastapi_users current_user
    db: Annotated[Session, Depends(get_db_session)] # Keep old get_db_session for now
):
    # Retrieve UserProfile data
    user_profile = db.exec(select(models.UserProfile).where(models.UserProfile.user_id == current_user.id)).first()
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    # Combine User and UserProfile data for response
    # This requires some adaptation as UserRead is flat
    # For now, let's return User directly and adapt UserRead later if needed
    # Or, preferably, modify UserRead to include profile fields
    
    # As UserRead now contains username and background from my custom User model,
    # the existing current_user directly returned should map correctly.
    # The UserRead schema itself has been modified in models/user.py to include these.
    return current_user # fastapi-users handles the UserRead mapping


@router.put("/profile", response_model=models.UserRead) # New PUT endpoint
async def update_user_profile(
    profile_update: models.UserUpdate, # Use UserUpdate schema for partial updates
    current_user: Annotated[models.User, Depends(current_active_user)],
    db: Annotated[Session, Depends(get_db_session)]
):
    # Find the user's profile
    user_profile = db.exec(select(models.UserProfile).where(models.UserProfile.user_id == current_user.id)).first()
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )
    
    # Apply updates from profile_update to user_profile
    profile_data = profile_update.dict(exclude_unset=True)
    for key, value in profile_data.items():
        if hasattr(user_profile, key):
            setattr(user_profile, key, value)
    
    db.add(user_profile)
    db.commit()
    db.refresh(user_profile)
    
    # Also update user fields if they are in profile_update and user object
    user_data = profile_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        if hasattr(current_user, key) and key not in ["password", "email", "id"]: # Avoid updating critical auth fields here
            setattr(current_user, key, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    # Return the updated user (which should include refreshed profile data)
    return current_user