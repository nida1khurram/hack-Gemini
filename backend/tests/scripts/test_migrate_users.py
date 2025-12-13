# backend/tests/scripts/test_migrate_users.py

import pytest
from sqlmodel import Session, SQLModel, create_engine
from passlib.context import CryptContext

# Import the migration script and models
from backend.scripts.migrate_users import main as migrate_main
from backend.src.models.user import User, UserProfile
from backend.src.database import settings # For DATABASE_URL

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine) # Clean up after tests

def test_migration_script(session: Session):
    # This is a placeholder test.
    # In a real scenario, you would:
    # 1. Populate the old user table with test data.
    # 2. Run the migrate_users.py script.
    # 3. Assert that the new User and UserProfile tables contain the migrated data.
    # 4. Assert that passwords are correctly hashed and users can log in.

    # Example: Assert that no users exist initially
    users_before_migration = session.query(User).all()
    assert len(users_before_migration) == 0

    # Simulate running the migration script (e.g., call the main function directly or via subprocess)
    # For now, we will just call the main function with a mock environment if needed.
    # We need to temporarily override the DATABASE_URL for the script
    original_db_url = settings.DATABASE_URL
    settings.DATABASE_URL = TEST_DATABASE_URL

    try:
        migrate_main() # This will attempt to connect to TEST_DATABASE_URL
    finally:
        settings.DATABASE_URL = original_db_url # Restore original DB URL

    # Assert that users have been migrated
    users_after_migration = session.query(User).all()
    assert len(users_after_migration) > 0 # Expecting some users from the placeholder data

    # Further assertions:
    # - Check specific user data
    # - Verify hashed passwords (e.g., by trying to authenticate a test user)
    # - Check UserProfile data
