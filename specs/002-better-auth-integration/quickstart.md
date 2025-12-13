# Quickstart: `fastapi-users` Integration

This guide provides the essential steps to get the new authentication system running locally for development and testing.

## 1. Install Dependencies

Add the following libraries to your `backend/requirements.txt` and install them:

```text
fastapi-users[sqlalchemy]
passlib[bcrypt]
```

Run the following command from the `backend` directory:
```bash
pip install -r requirements.txt
```

## 2. Configure Environment Variables

Add the following variable to your `.env` file. This is a secret key used by `fastapi-users` for signing tokens. You can generate a strong secret using `openssl rand -hex 32`.

```env
# .env
SECRET_KEY="YOUR_SUPER_SECRET_KEY_HERE"
```

## 3. Backend Integration

The following is a minimal example of how to integrate `fastapi-users` into the main application file (`backend/src/main.py`).

```python
# backend/src/main.py

import uvicorn
from fastapi import FastAPI

from backend.src.models.user import UserRead, UserCreate, UserUpdate
from backend.src.services.user_service import get_user_manager, auth_backend

app = FastAPI()

# Include the routers from fastapi-users
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

## 4. Run the Application

Once the dependencies are installed and the code is updated, you can run the backend:

```bash
# From the project root
cd backend
python -m src.main
```

You can now access the interactive API documentation at `http://127.0.0.1:8000/docs` to see and test the new authentication endpoints provided by `fastapi-users`.
