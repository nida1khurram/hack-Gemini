# backend/tests/api/test_auth.py

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

from backend.src.main import app
from backend.src.database import get_db, get_user_db
from backend.src.models.user import User
from backend.src.services.user_service import get_user_manager

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test_auth.db"

# Create a test engine and session
engine = create_engine(TEST_DATABASE_URL)

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine) # Clean up after tests

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session
    def get_user_db_override():
        yield get_user_manager(session)

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_user_db] = get_user_db_override
    app.dependency_overrides[get_user_manager] = lambda: get_user_manager(session) # Override for UserManager

    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear() # Clear overrides

def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password", "username": "testuser"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data

def test_login_user(client: TestClient):
    # First, register a user
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password", "username": "loginuser"},
    )

    # Then, attempt to log in
    response = client.post(
        "/auth/jwt/login", # Matches tokenUrl in BearerAuthentication
        data={"username": "login@example.com", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_read_users_me(client: TestClient):
    # Register and login a user
    client.post(
        "/auth/register",
        json={"email": "me@example.com", "password": "password", "username": "meuser"},
    )
    login_response = client.post(
        "/auth/jwt/login",
        data={"username": "me@example.com", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = login_response.json()["access_token"]

    # Access protected /users/me endpoint
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert data["username"] == "meuser"

# Add tests for:
# - Invalid registration
# - Invalid login
# - Password reset
# - Social login (requires mocking external OAuth providers)
# - Profile update
