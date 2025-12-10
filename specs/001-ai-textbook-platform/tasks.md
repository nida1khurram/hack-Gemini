# Tasks for AI-Native Textbook Platform

**Feature Branch**: `001-ai-textbook-platform`
**Date**: 2025-12-10
**Spec**: specs/1-ai-textbook-platform/spec.md
**Plan**: specs/1-ai-textbook-platform/plan.md

## Dependencies

-   User Story 1 (Ask General Questions) is a prerequisite for User Story 2 (Ask About Selected Text).
-   User Story 3 (Maintain Chat History) can be implemented in parallel with other stories but relies on existing user authentication and chatbot functionality.

## Parallel Execution Opportunities

-   Frontend UI development for the chat widget (related to US1 & US2) can start once backend API contracts are stable.
-   Deployment setup and initial configurations can run in parallel with early backend development.
-   `User Story 4 - Local Development Environment Setup` tasks are mostly documentation and verification, which can happen alongside other development.

---

## Phase 1: Setup and Environment Configuration

*Goal*: Establish the core development environment and infrastructure connections.

- [x] T001 Create Python virtual environment and install backend dependencies (openai, fastapi, uvicorn, qdrant-client, psycopg2-binary, langchain-openai, python-multipart, pydantic, pydantic-settings, sqlalchemy, sqlmodel, google-generativeai) backend/requirements.txt
- [x] T002 Configure backend `.env` file with `DATABASE_URL`, `OPENAI_API_KEY`, `GEMINI_API_KEY`, `TRANSLATION_MODEL`, `GEMINI_CHAT_MODEL`, `SECRET_KEY`, `REFRESH_TOKEN_SECRET`, `REFRESH_TOKEN_EXPIRE_MINUTES` in project root .env
- [x] T003 Initialize Node.js environment and install frontend dependencies frontend/package.json
- [x] T004 Configure frontend `.env` with `BACKEND_URL` in frontend/.env

## Phase 2: Foundational Backend Components

*Goal*: Implement core backend services and database connections that are prerequisites for all main features.

- [x] T005 Create database connection and session handling for Neon Postgres backend/src/database.py
- [x] T006 Define Pydantic models for request/response structures (e.g., QueryRequest, QueryResponse, SelectedTextRequest) backend/src/models/
- [x] T007 Implement basic FastAPI application structure with main dependencies backend/src/main.py
- [x] T008 Implement middleware for authentication and authorization backend/src/middleware/auth.py
- [x] T009 Implement user authentication API endpoints (`/auth/register`, `/auth/login`, `/auth/refresh`) backend/src/api/auth.py
- [x] T010 Implement user profile API endpoints (`/user/profile`) backend/src/api/user.py
- [x] T011 Implement CORS middleware configuration backend/src/main.py

## Phase 3: User Story 1 - Ask General Questions [US1] (Priority: P1)

*Goal*: Enable users to ask general questions and receive relevant answers from the chatbot.
*Independent Test*: Asking a general question in the chat widget and verifying a relevant response.

- [x] T012 [P] [US1] Implement document chunking logic backend/src/services/ingestion_service.py (new file)
- [x] T013 [P] [US1] Implement embedding generation using LLM backend/src/services/embedding_service.py (new file)
- [x] T014 [P] [US1] Implement storage of text chunks with embeddings and metadata in Qdrant backend/src/vector_db.py
- [x] T015 [US1] Create `/chatbot/query` POST endpoint for general queries backend/src/api/chatbot.py
- [x] T016 [US1] Implement RAG query logic in ChatbotService to embed user query, search Qdrant, build context, and call LLM backend/src/services/chatbot_service.py
- [x] T017 [P] [US1] Design and implement embeddable chat widget UI component frontend/src/components/Chatbot.tsx
- [x] T018 [P] [US1] Integrate chat widget into a Docusaurus markdown page (e.g., /docs/intro.md) frontend/docs/intro.md
- [x] T019 [P] [US1] Implement frontend-backend communication for `/chatbot/query` endpoint frontend/src/services/api.ts (new file)

## Phase 4: User Story 2 - Ask About Selected Text [US2] (Priority: P1)

*Goal*: Allow users to ask specific questions about selected book content.
*Independent Test*: Highlighting text, using "Ask about this" option, and verifying a relevant chatbot response.

- [x] T020 [US2] Create `/chatbot/selected` POST endpoint for selected text queries backend/src/api/chatbot.py
- [x] T021 [US2] Modify ChatbotService to use selected text directly as context for LLM call backend/src/services/chatbot_service.py
- [x] T022 [P] [US2] Implement frontend functionality to highlight/select text frontend/src/utils/text_selection.ts (new file)
- [x] T023 [P] [US2] Add "Ask about this" context menu option for selected text frontend/src/components/TextSelectionContextMenu.tsx (new file)
- [x] T024 [P] [US2] Send selected text to backend's `/chatbot/selected` endpoint via frontend-backend communication frontend/src/services/api.ts

## Phase 5: User Story 3 - Maintain Chat History [US3] (Priority: P2)

*Goal*: Store and retrieve user conversation history across sessions.
*Independent Test*: Initiating a conversation, closing and reopening the app, and verifying chat history is loaded.

- [x] T024.1 [US3] Create `GET /chat/history` and `DELETE /chat/history/{history_id}` API endpoints backend/src/api/chat_history.py
- [x] T025 [US3] Define `Chat History` entity in data model backend/src/models/chat_history.py (new file)
- [x] T026 [US3] Implement database logic to store chat messages and metadata backend/src/services/chat_history_service.py (new file)
- [x] T027 [US3] Integrate chat history storage into ChatbotService for `/chatbot/query` and `/chatbot/selected` backend/src/services/chatbot_service.py
- [x] T028 [P] [US3] Implement frontend display and retrieval of chat history in the chat widget frontend/src/components/Chatbot.tsx

## Phase 6: User Story 4 - Local Development Environment Setup [US4] (Priority: P3)

*Goal*: Ensure developers can efficiently set up their local environment.
*Independent Test*: Following the setup guide and verifying all dependencies are installed and the application runs locally.

- [x] T029 [US4] Review and refine `quickstart.md` documentation for clarity and completeness specs/1-ai-textbook-platform/quickstart.md
- [x] T030 [US4] Verify all prerequisites and installation steps in `quickstart.md` specs/1-ai-textbook-platform/quickstart.md

## Phase 7: Polish & Cross-Cutting Concerns

*Goal*: Ensure the application is production-ready, secure, and performant.

- [x] T031 Implement robust error handling and logging for backend services and API endpoints backend/src/ (various files)
- [x] T032 Implement rate limiting for public endpoints (30 requests/minute/user) backend/src/main.py
- [x] T033 Implement end-to-end tests for core user flows tests/e2e/ (new files)
- [x] T034 Optimize backend async operations for database and external API calls backend/src/services/ (various files)
- [x] T035 Implement background jobs for document ingestion (if book size is large) backend/src/services/ingestion_service.py (if required, conditional)
- [x] T036 Enhance Qdrant storage with metadata for retrieval filtering backend/src/vector_db.py
- [x] T037 Prepare deployment scripts and configurations for chosen platform (e.g., Render, Railway) deploy/ (new directory)

---

## Implementation Strategy

The implementation will follow an MVP-first approach, iteratively delivering features based on priority. User Story 1 and 2 are P1 and will be prioritized for initial development to establish core chatbot functionality. Subsequent user stories will be built upon this foundation. Parallel execution opportunities will be leveraged where task dependencies allow, particularly between frontend and backend development once API contracts are stable.