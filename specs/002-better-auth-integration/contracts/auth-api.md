# Auth API Contracts

This document outlines the existing API contracts that must be maintained after the migration to `fastapi-users`. The `fastapi-users` library provides these endpoints out-of-the-box, but they will be configured to match these existing paths and schemas.

## Endpoints

### 1. Register

-   **Endpoint**: `POST /auth/register`
-   **Description**: Creates a new user.
-   **Request Body**:
    ```json
    {
      "email": "user@example.com",
      "password": "yourpassword"
    }
    ```
-   **Response Body (Success)**:
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "is_active": true,
      "is_superuser": false,
      "is_verified": false
    }
    ```
-   **Response (Failure)**: `400 Bad Request` if email is invalid or already exists.

### 2. Login

-   **Endpoint**: `POST /auth/login`
-   **Description**: Authenticates a user and returns an access token.
-   **Request Body**: `application/x-www-form-urlencoded`
    ```
    username=user@example.com&password=yourpassword
    ```
-   **Response Body (Success)**:
    ```json
    {
      "access_token": "...",
      "token_type": "bearer"
    }
    ```
-   **Response (Failure)**: `401 Unauthorized` for invalid credentials.

### 3. Logout

-   **Endpoint**: `POST /auth/logout`
-   **Description**: Logs out the user. This will be handled by `fastapi-users` by deleting the authentication cookie.
-   **Request Body**: None
-   **Response Body (Success)**: `200 OK`
-   **Response (Failure)**: `401 Unauthorized` if not logged in.

### 4. Get Current User

-   **Endpoint**: `GET /users/me`
-   **Description**: Retrieves the profile of the currently authenticated user.
-   **Request Body**: None
-   **Response Body (Success)**:
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "is_active": true,
      "is_superuser": false,
      "is_verified": false
    }
    ```
-   **Response (Failure)**: `401 Unauthorized` if not authenticated.

### 5. Update Current User

-   **Endpoint**: `PUT /users/me`
-   **Description**: Updates the password of the currently authenticated user.
-   **Request Body**:
    ```json
    {
      "password": "current_password",
      "new_password": "new_secure_password"
    }
    ```
-   **Response Body (Success)**: `200 OK` with the updated user object.
-   **Response (Failure)**: `401 Unauthorized` or `400 Bad Request`.
