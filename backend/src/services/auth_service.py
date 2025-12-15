from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
from sqlmodel import Session
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from authlib.integrations.starlette_client import OAuth

from .. import models
from ..database import get_db
from ..database import settings


# Password hashing
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt", "plaintext"],
    deprecated="auto",
    bcrypt__rounds=12,
)

# JWT settings (maintaining compatibility with existing system)
SECRET_KEY = settings.SECRET_KEY
REFRESH_TOKEN_SECRET = settings.REFRESH_TOKEN_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


class AuthService:
    def __init__(self):
        self.oauth = OAuth()
        
        # Register OAuth providers (Google, GitHub)
        if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
            self.oauth.register(
                name='google',
                server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                client_kwargs={
                    'scope': 'openid email profile'
                }
            )
        
        if settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET:
            self.oauth.register(
                name='github',
                server_metadata_url='https://github.com/.well-known/openid_configuration',
                client_id=settings.GITHUB_CLIENT_ID,
                client_secret=settings.GITHUB_CLIENT_SECRET,
                client_kwargs={
                    'scope': 'user:email'
                }
            )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password using the configured context."""
        # Truncate password to 72 bytes to comply with bcrypt limitation
        truncated_password = password[:72] if len(password) > 72 else password
        return pwd_context.hash(truncated_password)

    def create_token(self, data: dict, secret_key: str, expires_delta: Optional[timedelta] = None, token_type: str = "access"):
        """Create a JWT token with specified parameters."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            # Default expiry based on token type if not provided
            if token_type == "access":
                expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            elif token_type == "refresh":
                expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
            else:
                raise ValueError("Invalid token_type")
        to_encode.update({"exp": expire, "type": token_type})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
        return encoded_jwt

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create an access token."""
        return self.create_token(data, SECRET_KEY, expires_delta, token_type="access")

    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a refresh token."""
        return self.create_token(data, REFRESH_TOKEN_SECRET, expires_delta, token_type="refresh")

    def verify_refresh_token(self, token: str):
        """Verify a refresh token."""
        try:
            payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
            token_type: str = payload.get("type")
            if token_type != "refresh":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
            return payload
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate refresh token")

    def get_current_user(self, token: str, db: Session):
        """Get the current user from the token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            token_type: str = payload.get("type")
            if username is None or token_type != "access":
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            raise credentials_exception
        return user

    def authenticate_user(self, db: Session, username: str, password: str):
        """Authenticate a user with username and password."""
        user = db.query(models.User).filter(models.User.username == username).first()
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def register_user(self, db: Session, user_create: models.UserCreate):
        """Register a new user."""
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.username == user_create.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        existing_email = db.query(models.User).filter(models.User.email == user_create.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password
        hashed_password = self.get_password_hash(user_create.password)
        
        # Create the new user
        new_user = models.User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            background=user_create.background
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user

    def refresh_access_token(self, refresh_token: str, db: Session):
        """Refresh an access token using a refresh token."""
        # Verify the refresh token
        payload = self.verify_refresh_token(refresh_token)
        username: str = payload.get("sub")
        
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        # Get the user from the database
        user = db.query(models.User).filter(models.User.username == username).first()
        
        if not user or not user.hashed_refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        # Verify the provided refresh token against the stored hashed one
        if not self.verify_password(refresh_token, user.hashed_refresh_token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        # Check if refresh token has expired
        if datetime.utcnow() > user.refresh_token_expires_at:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
        
        # Generate a new access token
        new_access_token = self.create_access_token(
            data={"sub": user.username}
        )
        
        # Generate a new refresh token (for refresh token rotation)
        new_refresh_token = self.create_refresh_token(
            data={"sub": user.username}
        )

        # Store the new hashed refresh token and its expiry in the DB
        user.hashed_refresh_token = self.get_password_hash(new_refresh_token)
        user.refresh_token_expires_at = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }


# Global instance of AuthService
auth_service = AuthService()