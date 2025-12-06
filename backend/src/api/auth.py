from datetime import timedelta, datetime # Added datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext # Import for hashing refresh tokens

from .. import models # Import models module
from ..database import get_db, Base, engine
from ..middleware.auth import (
    get_db_session, get_password_hash, verify_password,
    create_access_token, create_refresh_token, # Added create_refresh_token
    ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, # Added REFRESH_TOKEN_EXPIRE_MINUTES
    SECRET_KEY, REFRESH_TOKEN_SECRET, verify_refresh_token # Added REFRESH_TOKEN_SECRET, verify_refresh_token
)
import uuid # Import uuid

# Password hashing for refresh token
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()

# User registration
@router.post("/register")
async def register_user(user: models.UserCreate, db: Annotated[Session, Depends(get_db_session)]): # Use models.UserCreate for input
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    
    # Use the SQLAlchemy User model for creating the database object
    new_user = models.User( 
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        background=user.background # This is already an Enum
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id} # Return something meaningful

# User login (token endpoint)
@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db_session)]):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create Access Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Create Refresh Token
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    
    # Hash and store refresh token in DB
    user.hashed_refresh_token = pwd_context.hash(refresh_token)
    user.refresh_token_expires_at = datetime.utcnow() + refresh_token_expires
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60 # seconds
    }

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

@router.post("/refresh")
async def refresh_access_token(refresh_token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_refresh_token(refresh_token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username == username).first()
    
    if user is None or user.hashed_refresh_token is None or user.refresh_token_expires_at is None:
        raise credentials_exception

    # Verify the provided refresh token against the stored hashed one
    if not pwd_context.verify(refresh_token, user.hashed_refresh_token):
        raise credentials_exception
    
    # Check if refresh token has expired
    if datetime.utcnow() > user.refresh_token_expires_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    # Generate a new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Generate a new refresh token (for refresh token rotation)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    new_refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )

    # Store the new hashed refresh token and its expiry in the DB
    user.hashed_refresh_token = pwd_context.hash(new_refresh_token)
    user.refresh_token_expires_at = datetime.utcnow() + refresh_token_expires
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
