# backend/scripts/migrate_users.py

import os
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine
from passlib.context import CryptContext

# Import the new User and UserProfile models
from backend.src.models.user import User, UserProfile
# Import the old User model to fetch existing data
# from backend.src.models.user_old import OldUser # Assuming an old user model exists

# Load environment variables
load_dotenv()

# Database setup (from backend/src/database.py)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL)

# Password hashing context for fastapi-users
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_db_and_tables():
    # This function is for ensuring tables exist, typically handled by Alembic
    # for production. Keep for local testing convenience.
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def main():
    print("Starting user migration script...")

    # Ensure new tables are created (if not already by alembic)
    # This might be redundant if alembic is used, but good for local testing
    create_db_and_tables()

    with Session(engine) as session:
        # Step 1: Fetch old user data
        # This part assumes you have an "OldUser" model or similar structure
        # for your existing JWT users. You'll need to define it or adapt.
        # Example:
        # old_users = session.query(OldUser).all()
        
        # Placeholder for fetching existing users from your current structure
        # For demonstration, let's assume a list of dicts for old users
        old_users_data = [
            {"id": 1, "username": "old_user1", "email": "old1@example.com", "password_raw": "old_secret_pass1"},
            {"id": 2, "username": "old_user2", "email": "old2@example.com", "password_raw": "old_secret_pass2"},
            # ... add more old users
        ]
        
        migrated_count = 0
        for old_user_data in old_users_data:
            # Check if user already exists to prevent duplicates on re-run
            existing_user = session.query(User).filter(User.email == old_user_data["email"]).first()
            if existing_user:
                print(f"User with email {old_user_data['email']} already exists. Skipping.")
                continue

            # Hash the password for the new User model
            hashed_password = pwd_context.hash(old_user_data["password_raw"])

            # Create UserProfile
            user_profile = UserProfile(
                username=old_user_data["username"],
                # ... other profile data from old_user_data
            )
            session.add(user_profile)
            session.flush() # Ensure profile_id is generated

            # Create new User
            new_user = User(
                email=old_user_data["email"],
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=False,
                is_verified=False,
                profile_id=user_profile.id,
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            session.refresh(user_profile)
            
            user_profile.user_id = new_user.id # Link profile to user
            session.add(user_profile)
            session.commit()
            session.refresh(user_profile)


            print(f"Migrated user: {new_user.email} with profile {user_profile.username}")
            migrated_count += 1
        
        print(f"Migration complete. Total users migrated: {migrated_count}")

if __name__ == "__main__":
    main()
