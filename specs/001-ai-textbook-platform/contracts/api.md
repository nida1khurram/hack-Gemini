# API Contracts: AI-Native Textbook Platform

**Date**: 2025-12-10

## Authentication Endpoints (`/auth`)

### POST /auth/register
-   **Description**: Registers a new user.
-   **Request Body**:
    -   `username`: string
    -   `email`: string
    -   `password`: string
-   **Response**:
    -   `access_token`: string
    -   `token_type`: string

### POST /auth/login
-   **Description**: Authenticates a user and returns access tokens.
-   **Request Body**:
    -   `username`: string
    -   `password`: string
-   **Response**:
    -   `access_token`: string
    -   `refresh_token`: string
    -   `token_type`: string

### POST /auth/refresh
-   **Description**: Refreshes an access token using a refresh token.
-   **Request Header**: `Authorization: Bearer <refresh_token>`
-   **Response**:
    -   `access_token`: string
    -   `token_type`: string

## Chatbot Endpoints

### POST /chatbot/query
-   **Description**: Handles general chatbot queries.
-   **Security**: Requires authentication (Bearer Token).
-   **Request Body**:
    -   `query`: string (The user's question)
    -   `context`: string (Optional, additional context provided to the LLM)
-   **Response**:
    -   `response`: string (The chatbot's answer)

### POST /chatbot/selected
-   **Description**: Handles chatbot queries based on selected text from the book.
-   **Security**: Requires authentication (Bearer Token).
-   **Request Body**:
    -   `query`: string (The user's question)
    -   `context`: string (The selected text from the book)
-   **Response**:
    -   `response`: string (The chatbot's answer)

## Translation Endpoint

### POST /translate
-   **Description**: Translates text to a specified target language.
-   **Security**: Requires authentication (Bearer Token).
-   **Request Body**:
    -   `text`: string (The text to be translated)
    -   `target_language`: string (The language code/name to translate to, e.g., 'Urdu', 'es', 'fr')
-   **Response**:
    -   `translated_text`: string (The translated text)

## Module Endpoints (`/modules`)

### POST /modules/
-   **Description**: Creates a new module.
-   **Security**: Requires authentication (Bearer Token).
-   **Request Body**:
    -   `title`: string
    -   `description`: string (Optional)
-   **Response**: `ModuleInDB` object

### GET /modules/
-   **Description**: Retrieves a list of all modules.
-   **Query Parameters**:
    -   `skip`: integer (Optional, default 0)
    -   `limit`: integer (Optional, default 100)
-   **Response**: List of `ModuleInDB` objects

### GET /modules/{module_id}
-   **Description**: Retrieves a single module by ID.
-   **Path Parameters**:
    -   `module_id`: integer
-   **Response**: `ModuleInDB` object

### PUT /modules/{module_id}
-   **Description**: Updates an existing module.
-   **Security**: Requires authentication (Bearer Token).
-   **Path Parameters**:
    -   `module_id`: integer
-   **Request Body**:
    -   `title`: string
    -   `description`: string (Optional)
-   **Response**: `ModuleInDB` object

### DELETE /modules/{module_id}
-   **Description**: Deletes a module.
-   **Security**: Requires authentication (Bearer Token).
-   **Path Parameters**:
    -   `module_id`: integer
-   **Response**: `ModuleInDB` object

## Chapter Endpoints (`/chapters`)

### POST /chapters/
-   **Description**: Creates a new chapter.
-   **Security**: Requires authentication (Bearer Token).
-   **Request Body**:
    -   `module_id`: integer
    -   `title`: string
    -   `content_english`: string
    -   `content_urdu`: string (Optional)
-   **Response**: `ChapterInDB` object

### GET /chapters/
-   **Description**: Retrieves a list of all chapters.
-   **Query Parameters**:
    -   `skip`: integer (Optional, default 0)
    -   `limit`: integer (Optional, default 100)
-   **Response**: List of `ChapterInDB` objects

### GET /chapters/{chapter_id}
-   **Description**: Retrieves a single chapter by ID.
-   **Path Parameters**:
    -   `chapter_id`: integer
-   **Response**: `ChapterInDB` object

### PUT /chapters/{chapter_id}
-   **Description**: Updates an existing chapter.
-   **Security**: Requires authentication (Bearer Token).
-   **Path Parameters**:
    -   `chapter_id`: integer
-   **Request Body**:
    -   `module_id`: integer
    -   `title`: string
    -   `content_english`: string
    -   `content_urdu`: string (Optional)
-   **Response**: `ChapterInDB` object

### DELETE /chapters/{chapter_id}
-   **Description**: Deletes a chapter.
-   **Security**: Requires authentication (Bearer Token).
-   **Path Parameters**:
    -   `chapter_id`: integer
-   **Response**: `ChapterInDB` object

## User Progress Endpoints (`/progress`)

### POST /progress/
-   **Description**: Marks a chapter as complete for the current authenticated user.
-   **Security**: Requires authentication (Bearer Token).
-   **Request Body**:
    -   `chapter_id`: integer
-   **Response**: `UserChapterProgressInDB` object

### GET /progress/
-   **Description**: Retrieves the chapter progress for the current authenticated user.
-   **Security**: Requires authentication (Bearer Token).
-   **Response**: List of `UserChapterProgressInDB` objects

## User Quiz Attempt Endpoints (`/quiz`)

### POST /quiz/attempts/
-   **Description**: Records a quiz attempt for the current authenticated user.
-   **Security**: Requires authentication (Bearer Token).
-   **Request Body**:
    -   `quiz_id`: integer
    -   `score`: float
-   **Response**: `UserQuizAttemptInDB` object

### GET /quiz/attempts/{quiz_id}
-   **Description**: Retrieves all quiz attempts for a specific quiz by the current authenticated user.
-   **Security**: Requires authentication (Bearer Token).
-   **Path Parameters**:
    -   `quiz_id`: integer
-   **Response**: List of `UserQuizAttemptInDB` objects
