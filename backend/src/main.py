from dotenv import load_dotenv

from fastapi import FastAPI, Depends 
from .database import Base, engine 
from .api import auth 
from .api import chatbot 
from .api import user 
from .api import translation # Import the translation router
from .middleware.auth import get_current_user 
from . import models 
from typing import Annotated 

load_dotenv()

app = FastAPI()

# Create database tables
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"]) 
app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"]) 
app.include_router(user.router, prefix="/user", tags=["user"]) 
app.include_router(translation.router, prefix="/translate", tags=["translation"]) # Include the translation router

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI-Native Textbook Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Example of a protected route
@app.get("/users/me")
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user