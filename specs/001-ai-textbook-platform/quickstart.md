# Quickstart: AI-Native Textbook Platform

**Date**: 2025-12-10

This guide provides quick steps to get the AI-Native Textbook Platform backend and frontend up and running for local development.

## 1. Prerequisites

Ensure you have the following installed on your system:

-   **Git**: For cloning the repository.
-   **Python 3.11+**: For the backend.
-   **Node.js LTS**: For the frontend.
-   **uv**: A fast Python package installer and dependency manager (`pip install uv`).

## 2. Clone the Repository

```bash
git clone <repository_url>
cd hack-Gemini-cli # Or your project root directory
```

## 3. Backend Setup

1.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```
2.  **Create and activate a Python virtual environment**:
    ```bash
    uv venv
    .\.venv\Scripts\Activate.ps1   # On Windows PowerShell
    # source .venv/bin/activate    # On Linux/macOS Bash/Zsh
    ```
3.  **Install Python dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```
4.  **Configure Environment Variables**:
    *   Create a `.env` file in the project root (`hack-Gemini-cli/.env`).
    *   Fill it with your actual credentials and settings. Example content:
        ```
        DATABASE_URL="postgresql://user:password@host:port/dbname"
        OPENAI_API_KEY="your_openai_api_key"
        TRANSLATION_MODEL="gpt-3.5-turbo"
        GEMINI_API_KEY="your_gemini_api_key"
        GEMINI_CHAT_MODEL="gemini-2.5-flash"
        SECRET_KEY="your_super_secret_key"
        REFRESH_TOKEN_SECRET="another_super_secret_key"
        REFRESH_TOKEN_EXPIRE_MINUTES=10080
        ```
    *   *Note*: Ensure `DATABASE_URL` points to a running PostgreSQL instance (e.g., from Neon.tech).
    *   *Note*: `OPENAI_API_KEY` and `GEMINI_API_KEY` are needed for translation and chatbot services.

5.  **Run the Backend Application**:
    ```bash
    uvicorn src.main:app --reload
    ```
    The backend API will be available at `http://localhost:8000`. You can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## 4. Frontend Setup

1.  **Navigate to the frontend directory**:
    ```bash
    cd ../frontend
    ```
2.  **Install Node.js dependencies**:
    ```bash
    npm install
    # or yarn install
    ```
3.  **Configure Environment Variables**:
    *   Ensure the `.env` file in the project root (`hack-Gemini-cli/.env`) contains `BACKEND_URL`. The frontend `docusaurus.config.ts` will pick this up. If you copied the backend's `.env` to the frontend, you might need to adjust variable names if Docusaurus expects `REACT_APP_BACKEND_URL` instead of `BACKEND_URL`. For now, `process.env.BACKEND_URL` from the root `.env` will be used.
        ```
        BACKEND_URL="http://localhost:8000" # Ensure this matches your backend URL
        ```
4.  **Run the Frontend Application**:
    ```bash
    npm start
    # or yarn start
    ```
    The Docusaurus frontend will typically be available at `http://localhost:3000`.

## 5. Interact with the Platform

### Backend API (via Swagger UI: `http://localhost:8000/docs`)

1.  **Authentication**:
    *   Use `/auth/register` to create a new user.
    *   Use `/auth/login` to log in and obtain `access_token` and `refresh_token`.
    *   Use the "Authorize" button in Swagger UI to provide your `access_token` (Bearer authentication).
2.  **Chatbot**:
    *   Test `/chatbot/query` with general questions.
    *   Test `/chatbot/selected` with text you might manually provide as context.
3.  **Translation**:
    *   Test `/translate` with text and a target language (e.g., 'Urdu').
4.  **Content Management**:
    *   Test CRUD operations for `/modules` and `/chapters`.
5.  **User Data**:
    *   Test `/progress` for marking chapter completion.
    *   Test `/quiz/attempts` for submitting and retrieving quiz scores.

### Frontend Application (`http://localhost:3000`)

1.  **Login**: Navigate to `/login` and log in using the user created via the backend API.
2.  **Chatbot**: Navigate to `/docs/intro` (or any other markdown page where you've embedded `<Chatbot />`).
    *   The chatbot UI should now be visible (after successful login).
    *   Test asking questions.

---
**Troubleshooting**:
-   Ensure both backend and frontend servers are running.
-   Check environment variables in your `.env` file.
-   Refer to browser console for frontend errors and backend terminal for backend logs.
