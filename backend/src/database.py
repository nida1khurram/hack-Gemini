from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# New imports for fastapi-users
from fastapi_users.db import SQLAlchemyUserDatabase
from .models.user import User # Assuming User model is in .models.user

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REFRESH_TOKEN_SECRET: str
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    OPENAI_API_KEY: str
    TRANSLATION_MODEL: str
    GEMINI_API_KEY: str
    GEMINI_CHAT_MODEL: str
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_API_KEY: str
    QDRANT_URL: str = "http://localhost:6333"  # Default value
    Qdrant_END_POINT: str  # This is the variable name in your .env
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = "backend/.env"

settings = Settings()

# Configure the engine based on the database type
if settings.DATABASE_URL.startswith("sqlite"):
    # For SQLite, we need to disable check_same_thread for async operations
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # For other databases (PostgreSQL, MySQL, etc.)
    engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = SQLModel

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for fastapi-users to get a user database instance
def get_user_db(db: SessionLocal):
    yield SQLAlchemyUserDatabase(db, User)
