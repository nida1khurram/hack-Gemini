# backend/src/services/user_service.py

import os
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import BearerAuthentication, AuthenticationBackend
from fastapi_users.authentication.oauth2 import GoogleOAuth2, GitHubOAuth2 # New import for GitHubOAuth2

from backend.src.models.user import User, UserCreate, UserUpdate, UserRead
from backend.src.database import get_user_db, settings

SECRET = settings.SECRET_KEY

class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None):
        print(f"Verification requested for user {user.id}. Verification token: {token}")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

bearer_transport = BearerAuthentication(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_user_manager=get_user_manager,
)

# Google OAuth2 integration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
google_oauth_client = GoogleOAuth2(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, redirect_url="/auth/google/callback", name="google")

# GitHub OAuth2 integration
GITHUB_CLIENT_ID = os.getenv("GITHUB_OAUTH_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_OAUTH_CLIENT_SECRET")
github_oauth_client = GitHubOAuth2(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, redirect_url="/auth/github/callback", name="github")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend, google_oauth_client, github_oauth_client], # Add github_oauth_client here
)