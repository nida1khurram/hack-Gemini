# backend/src/middleware/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from typing import Annotated

from ..database import settings # Import settings for AUTH_SECRET

# This should be the same secret used by Auth.js in your Node.js backend
AUTH_SECRET = settings.SECRET_KEY # Using SECRET_KEY from Python backend's settings
ALGORITHM = "HS256" # Auth.js uses HS256 by default

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/jwt/login") # This tokenUrl might not be used if Auth.js handles login directly

class TokenData(BaseModel):
    id: str | None = None
    email: str | None = None
    name: str | None = None

async def get_current_user_from_jwt(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT using the shared secret
        payload = jwt.decode(token, AUTH_SECRET, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub") # 'sub' is typically the user ID in Auth.js JWTs
        user_email: str = payload.get("email")
        user_name: str = payload.get("name")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id, email=user_email, name=user_name)
    except JWTError:
        raise credentials_exception
    return token_data
