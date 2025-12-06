# Personal Health Record Dashboard

A comprehensive Personal Health Record Dashboard designed to help users manage their health data, track progress, and gain insights through advanced AI features. It aims to provide a personalized and interactive experience for learning and self-improvement in health-related topics.

## Features

*   **Intuitive UI:** A user-friendly interface built with Docusaurus, offering a clean and responsive design.
*   **Smart Content Analysis:** Auto-detect content complexity, identify subject areas, extract key concepts, and generate learning objectives.
*   **Personalization:** Adapt to learning styles, adjust quiz difficulty, track user progress, and generate custom study plans.
*   **Enhanced Quiz Features:** Timed quizzes, question banks, adaptive testing, and peer comparison.
*   **Export & Integration:** Anki Deck export, Google Classroom Integration, API Endpoints, and batch processing.
*   **Performance Optimization:** Caching, async processing for large files, efficient memory management, and real-time progress updates.
*   **Production Ready Features:** Comprehensive error logging, user analytics, A/B testing, and detailed documentation.
*   **Chatbot Integration:** Interactive chatbot for queries and assistance.
*   **Multi-language Support:** Translation capabilities.

## Technologies Used

*   **Frontend:** Docusaurus (React, TypeScript)
*   **Backend:** FastAPI (Python)
*   **Database:** (Assumed, based on project structure)
*   **Vector Database:** Used for efficient data retrieval and semantic search capabilities.

## Project Structure

```
.
├── backend/                  # FastAPI backend services, APIs, and business logic
│   ├── src/                  # Source code for the backend application
│   │   ├── api/              # API endpoints (auth, chatbot, translation, user)
│   │   ├── models/           # Database models (user, chapter, module, progress, quiz)
│   │   ├── services/         # Business logic and AI services (chatbot, personalization, translation)
│   │   ├── database.py       # Database connection and session management
│   │   ├── main.py           # Main FastAPI application entry point
│   │   └── vector_db.py      # Vector database integration
│   └── ...                   # Other backend-related files (venv, requirements, etc.)
└── frontend/                 # Docusaurus-based user interface
    ├── docs/                 # Markdown documentation files and learning content
    ├── src/                  # React components, pages, and styling
    │   ├── components/       # Reusable UI components (Chatbot, LoginForm, PythonRunner, TranslateButton, etc.)
    │   ├── pages/            # Main application pages
    │   └── hooks/            # Custom React hooks
    └── ...                   # Docusaurus configuration, assets, etc.
```

## Setup and Installation

**1. Clone the repository:**

```bash
git clone <repository_url>
cd hack-Gemini-cli
```

**2. Backend Setup:**

Navigate to the `backend` directory, create a virtual environment, install dependencies, and start the server.

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # On Windows
# source .venv/bin/activate    # On macOS/Linux
pip install -r requirements.txt
python -m uvicorn src.main:app --reload
```

*Ensure you have `uvicorn` installed (`pip install uvicorn`)*.

**3. Frontend Setup:**

Navigate to the `frontend` directory, install dependencies, and start the development server.

```bash
cd frontend
npm install
npm start
```

The frontend application should now be running, typically accessible at `http://localhost:3000`.

## Usage

Access the dashboard through your web browser. Explore the documentation, interact with the chatbot, track your progress, and utilize the various AI-powered features for a personalized health learning experience.