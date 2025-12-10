from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from .. import models # Import models module
from ..database import get_db, Base, engine, settings, SessionLocal # Import SessionLocal

# Dependency for database session (needed by get_current_user)
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Password hashing - Configure for Windows compatibility
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt", "plaintext"],
    deprecated="auto",
    bcrypt__rounds=12,
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # Truncate password to 72 bytes to comply with bcrypt limitation
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)

# JWT settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

REFRESH_TOKEN_SECRET = settings.REFRESH_TOKEN_SECRET
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token") # Corrected tokenUrl

def create_token(data: dict, secret_key: str, expires_delta: timedelta | None = None, token_type: str = "access"):
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

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    return create_token(data, SECRET_KEY, expires_delta, token_type="access")

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    return create_token(data, REFRESH_TOKEN_SECRET, expires_delta, token_type="refresh")

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        token_type: str = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate refresh token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db_session)]):
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
