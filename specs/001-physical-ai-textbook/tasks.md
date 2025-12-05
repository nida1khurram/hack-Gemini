# Tasks: AI-Native Textbook on Physical AI & Humanoid Robotics

**Input**: Design documents from `specs/001-physical-ai-textbook/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Initialize Docusaurus frontend project in `frontend/`
- [X] T002 [P] Initialize FastAPI backend project in `backend/`
- [X] T003 [P] Configure linting and formatting tools for both projects

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T004 [P] Create database models in `backend/src/models/` based on `data-model.md`
- [X] T005 [P] Configure database connection to Neon Postgres in `backend/src/database.py`
- [X] T006 [P] Configure vector database connection to Qdrant in `backend/src/vector_db.py`
- [X] T007 Implement user registration and login endpoints in `backend/src/api/auth.py`
- [X] T008 [P] Implement user authentication middleware using Better-auth in `backend/src/middleware/auth.py`
- [X] T009 [P] Set up basic API routes and middleware structure in `backend/src/main.py`

---

## Phase 3: User Story 1 - Read the AI Textbook (Priority: P1) 🎯 MVP

**Goal**: Readers can access and read the textbook content.

**Independent Test**: The textbook is deployed on GitHub Pages and can be accessed and read.

### Implementation for User Story 1

- [X] T010 [P] [US1] Create Docusaurus pages for the 4 modules in `frontend/docs/`
- [X] T011 [P] [US1] Create Docusaurus pages for the 15 chapters in `frontend/docs/`
- [X] T012 [P] [US1] Add placeholder content for each chapter
- [X] T013 [US1] Implement navigation between chapters and modules in `frontend/sidebars.js`

---

## Phase 4: User Story 2 - Ask Questions with RAG Chatbot (Priority: P1)

**Goal**: Readers can ask questions to a RAG chatbot.

**Independent Test**: The RAG chatbot is available and responds to questions about the textbook content.

### Implementation for User Story 2

- [X] T014 [P] [US2] Implement the RAG chatbot service in `backend/src/services/chatbot_service.py`
- [X] T015 [US2] Create the `/chatbot/query` API endpoint in `backend/src/api/chatbot.py`
- [X] T016 [P] [US2] Develop the frontend chatbot component in `frontend/src/components/Chatbot.js`
- [X] T017 [US2] Integrate the chatbot component with the textbook pages

---

## Phase 5: User Story 3 - Personalized Learning Experience (Priority: P2)

**Goal**: The content is personalized based on the user's background.

**Independent Test**: The content of the textbook is adapted based on the user's profile.

### Implementation for User Story 3

- [X] T018 [P] [US3] Implement the personalization rules engine in `backend/src/services/personalization_service.py`
- [X] T019 [US3] Create the `/user/profile` API endpoint in `backend/src/api/user.py`
- [X] T020 [US3] Dynamically render content in Docusaurus based on user background

---

## Phase 6: User Story 4 - Translate Content to Urdu (Priority: P3)

**Goal**: The content can be translated to Urdu.

**Independent Test**: The content can be translated to Urdu.

### Implementation for User Story 4

- [X] T021 [P] [US4] Implement the translation service using OpenAI API in `backend/src/services/translation_service.py`
- [X] T022 [US4] Create the `/translate` API endpoint in `backend/src/api/translation.py`
- [X] T023 [P] [US4] Add a "Translate to Urdu" button to the frontend

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T024 Write the actual content for the textbook
- [X] T025 Add code examples and simulations
- [X] T026 Complete the capstone project
- [X] T027 Perform testing and quality validation
- [ ] T028 Deploy the frontend and backend
