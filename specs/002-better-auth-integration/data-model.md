# Data Model: Better Auth Integration

This document outlines the data models required for the `fastapi-users` integration. The models are designed to be compatible with the existing user profile data while adhering to the requirements of the `fastapi-users` library.

## Core Models (as required by `fastapi-users`)

These models will be defined in `backend/src/models/user.py`.

### 1. `User` Model

This is the core user model that will be stored in the database. It inherits from `SQLModel` and `BaseUser`.

```python
# backend/src/models/user.py

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)

    # Foreign key to the user profile table
    profile_id: int = Field(default=None, foreign_key="userprofile.id")
```

### 2. `UserProfile` Model

This model will hold the application-specific user profile data. This separation ensures that the core authentication model (`User`) remains clean and only contains data required by `fastapi-users`.

```python
# backend/src/models/user.py (or a new profile.py)

from sqlmodel import SQLModel, Field

class UserProfile(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    full_name: str = Field(index=True)
    # Add other profile fields here as needed
```

## Schema Models (Pydantic Schemas for API)

These Pydantic schemas are used by `fastapi-users` for request and response validation.

### 1. `UserRead` Schema

Defines the user data that is safe to be returned in an API response.

```python
# backend/src/models/user.py

from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    pass

```

### 2. `UserCreate` Schema

Defines the data required to create a new user.

```python
# backend/src/models/user.py

class UserCreate(schemas.BaseUserCreate):
    pass
```

### 3. `UserUpdate` Schema

Defines the data that can be updated by a user.

```python
# backend/src.models/user.py

class UserUpdate(schemas.BaseUserUpdate):
    pass
```

## Relationships

- The `User` model will have a one-to-one relationship with the `UserProfile` model. This is handled via the `profile_id` foreign key. This design keeps the authentication schema separate from the application's profile schema, which is a good practice.
- The existing user table will need to be migrated to this new structure. A migration script will be required to:
    1. Create the new `User` and `UserProfile` tables.
    2. Transfer data from the old user table into these new tables.
    3. Hash passwords using the format expected by `fastapi-users`.
