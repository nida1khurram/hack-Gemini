---
id: "003"
title: "Implement Refresh Tokens for Better Auth"
stage: "general"
date: "2025-12-05"
surface: "agent"
model: "gemini-1.5-pro"
feature: "better-auth"
branch: "main"
user: "user"
command: "yes prceed"
labels: ["authentication", "security", "jwt", "refresh-tokens", "backend", "frontend"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "backend/src/models/user.py"
  - ".env"
  - "backend/src/middleware/auth.py"
  - "backend/src/api/auth.py"
  - "frontend/src/hooks/useAuth.ts"
  - "frontend/src/components/LoginForm.tsx"
tests_yaml: []
prompt_text: |
  yes prceed
response_text: |
  I have completed the implementation of refresh tokens for "better auth" on both the backend and the frontend.

  Here's a summary of the changes:

  **Backend:**
  *   **`models/user.py`**: Added `hashed_refresh_token` and `refresh_token_expires_at` columns to the `User` model.
  *   **`.env`**: Added `REFRESH_TOKEN_SECRET` and `REFRESH_TOKEN_EXPIRE_MINUTES`.
  *   **`middleware/auth.py`**:
      *   Added logic to load `REFRESH_TOKEN_SECRET` and `REFRESH_TOKEN_EXPIRE_MINUTES`.
      *   Refactored token creation into a generic `create_token` function.
      *   Implemented `create_access_token` and `create_refresh_token` using the generic function.
      *   Added `verify_refresh_token` function.
      *   Modified `get_current_user` to ensure it validates an access token.
  *   **`api/auth.py`**:
      *   Modified the `/auth/token` endpoint to issue both an access token and a refresh token upon successful login. The refresh token is hashed and stored in the database with its expiry.
      *   Added a new `/auth/refresh` endpoint to exchange a valid refresh token for new access and refresh tokens (implementing refresh token rotation).

  **Frontend:**
  *   **`frontend/src/hooks/useAuth.ts`**:
      *   Modified `setAuthData` to store both `access_token` and `refresh_token`.
      *   Modified `clearAuthData` to remove both tokens.
      *   Implemented an auto-refresh mechanism within `fetchUserProfile` to use the refresh token when the access token expires.
      *   Modified the `login` function to accept and pass both access and refresh tokens to `setAuthData`.
  *   **`frontend/src/components/LoginForm.tsx`**: Modified the `handleSubmit` function to retrieve both `access_token` and `refresh_token` from the backend response and pass them to `auth.login()`.

  The backend server has been restarted and is running with these new changes. You will need to build and run your Docusaurus frontend to see these changes in action.

  Please let me know if you have any further instructions.
outcome: "Refresh token implementation completed for both backend and frontend."
evaluation: "User's request to implement 'better auth' using refresh tokens was fully completed, with both backend and frontend modified accordingly."
---
