from fastapi import FastAPI, Depends, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis
from starlette.responses import JSONResponse
import logging
from dotenv import load_dotenv

from .database import engine, settings # Import settings
from sqlmodel import SQLModel
# from .api import auth # Removed
from .api import chatbot
from .api import user # This will be changed or removed later if fastapi-users handles user management
from .api import translation # Import the translation router
# from .middleware.auth import get_current_user # Removed
from .models.user import UserRead, UserCreate, UserUpdate # New import for fastapi-users schemas
from .services.user_service import auth_backend, fastapi_users, google_oauth_client, github_oauth_client # New import for fastapi-users instance and OAuth clients

from . import models
from typing import Annotated

load_dotenv()

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

origins = [
    "http://localhost",
    "http://localhost:3000",  # Frontend URL
    "http://localhost:3001",  # Frontend URL
    "http://localhost:3002",  # Frontend URL
    "http://localhost:3003",  # Frontend URL
    # Add other origins as needed for deployment
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiter setup
@app.on_event("startup")
async def startup_event():
    # SQLModel.metadata.create_all(bind=engine) # This is now handled by Alembic
    # Initialize FastAPI-Limiter with Redis
    try:
        redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis)
        logger.info("Redis connected successfully for rate limiting")
    except Exception as e:
        logger.warning(f"Could not connect to Redis: {e}. Rate limiting will be disabled.")
        # Set a flag to indicate Redis is not available
        app.state.redis_available = False

@app.exception_handler(Exception)
async def rate_limit_exceeded_handler(request: Request, exc: Exception):
    if "RateLimitExceeded" in str(type(exc)):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded"},
        )
    # Re-raise if it's not a rate limit exception
    raise exc

from .api import translation, module, chapter, progress, quiz, chat_history

# Integrate fastapi-users routers
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt", # Using /auth/jwt for login to match contract, or /auth/bearer for bearer auth
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Integrate Google OAuth2 router
app.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend),
    prefix="/auth/google", # Consistent with redirect_url in user_service.py
    tags=["auth"],
)

# Integrate GitHub OAuth2 router
app.include_router(
    fastapi_users.get_oauth_router(github_oauth_client, auth_backend),
    prefix="/auth/github", # Consistent with redirect_url in user_service.py
    tags=["auth"],
)


# Existing routers (auth.router removed)
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(translation.router, prefix="/translate", tags=["translation"])
app.include_router(module.router, prefix="/modules", tags=["modules"])
app.include_router(chapter.router, prefix="/chapters", tags=["chapters"])
app.include_router(progress.router, prefix="/progress", tags=["progress"])
app.include_router(quiz.router, prefix="/quiz", tags=["quiz"])
app.include_router(chat_history.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI-Native Textbook Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Old protected route removed as fastapi-users provides its own /users/me
# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
#     return current_user