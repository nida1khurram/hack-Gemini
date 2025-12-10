# Feature Specification: AI-Native Textbook Platform

**Feature Branch**: `001-ai-textbook-platform`  
**Created**: 2025-12-10  
**Status**: Draft  
**Input**: User description: "✅ Phase 1: Project Setup aur Infrastructure (Aaj se Week 1 tak) Iss phase mein, aap saari external services ko setup karenge aur aapka development environment ready hoga. Task Details / Implementation Guide 1. OpenAI Account & API Key Banayein OpenAI dashboard se ek API key generate karein. Yeh aapke LLM (e.g., gpt-4o-mini) aur embeddings (text-embedding-3-small) ke liye zaroori hai. OPENAI_API_KEY ko aapke .env file mein save karein. 2. Neon (Postgres) Database Create Karein Neon.tech par jayein aur Free Tier ka account banayein. Ek new project aur uske andar ek database create karein. Connection String ko note karein. Yeh string aise dikhegi: postgresql://user:pass@ep-cool-breeze-123456.us-east-2.aws.neon.tech/dbname. Isse .env file mein DATABASE_URL variable ke roop mein save karein. 3. Qdrant Cloud Free Cluster Setup Karein Qdrant Cloud par jayein aur free tier cluster create karein. Apna Cluster URL aur API Key generate karein aur note karein. Inhe bhi .env file mein save karein: QDRANT_URL, QDRANT_API_KEY. 4. Local Development Environment Setup Karein Ek dedicated project folder banayein aur requirements.txt file create karein. Ye recommended packages install karein: openai, fastapi, uvicorn, qdrant-client, psycopg2-binary, langchain-openai, python-multipart, pydantic. Fir pip install -r requirements.txt command run karein. ✅ Phase 2: Backend Development (Week 1 & 2) Iss phase mein, aap FastAPI backend banayenge jisme document processing, database interactions, aur chat endpoint shamil honge. Task Implementation Steps aur Code Snippets 1. Core FastAPI Application aur Main Dependencies Initialize Karein Ek file main.py create karein aur iske andar FastAPI app aur basic dependencies define karein. 2. Document Processing aur Ingestion Pipeline Banayein Chunking: Apne book ke text ko paragraphs ya sentences mein break karein (e.g., 300-500 words ke chunks). Yeh step langchain.text_splitter use kar ke automate ho sakta hai. Embedding Generation: Har chunk ke liye OpenAI ke text-embedding-3-small model se embedding vector generate karein. Storage: Har chunk ko uski embedding, original text, aur source metadata (e.g., page number) ke saath Qdrant mein store karein. 3. Core RAG Query Logic Implement Karein Aapka /chat POST endpoint ye kaam karega: 1. User Query Embed: User ke sawaal ka embedding generate karein. 2. Semantic Search: Us embedding ko Qdrant mein query karein aur top k relevant chunks retrieve karein. 3. Context Build: Retrieve kiye gaye chunks ko ek context string mein combine karein. 4. LLM Call: Context aur user query ko ek system prompt ke saath OpenAI ke chat completion API ko send karein jawab generate karne ke liye. 4. "Selected Text" Feature Implement Karein Ek dedicated endpoint (e.g., /chat/selected) banayein jo user ke highlighted text ko directly context ke roop mein accept kare. Isse temporary context milta hai jo sirf usi conversation ke liye relevant hai, general vector search bypass karte hue. 5. Pydantic Models Define Karein (Type Safety ke liye) Request/response structures ko define karne ke liye Pydantic models use karein. Example: QueryRequest, QueryResponse, SelectedTextRequest. 6. Database Connection aur Session Handling Setup Karein Neon Postgres database se connect karne ke liye code likhein. Session History: Har user conversation ke messages aur metadata ko store karein taake context maintain rahe. ✅ Phase 3: Testing aur Frontend Integration (Week 3)Backend ko test karne aur usse connect karne ke liye ek simple frontend ya testing interface banayein. Task Testing & Integration Guide 1. Backend Endpoints ko Test Karein FastAPI automatic Swagger UI provide karta hai http://127.0.0.1:8000/docs par. Isse aap apne /chat aur /chat/selected endpoints manually test kar sakte hain. 2. Book ke Andar Embeddable Chat Widget Design Karein Aapka chatbot published book (e.g., eBook, web-based book) ke andar embed hoga. Embedding Strategy: Ek minimal, non-intrusive chat interface design karein (e.g., bottom-right corner mein ek button). Isse user kisi bhi page par sawaal pooch sakta hai. Context Awareness: Widget ko current page number ya chapter title jaise metadata backend ko bhejna chahiye taake search results refine ho saken. 3. Frontend-Backend Communication Setup Karein Frontend (book) se backend tak API calls handle karne ke liye JavaScript code likhein. Example Fetch Call: 4. "Select Text to Ask" Feature Implement Karein Book reader ko text highlight/select karne aur context menu se "Ask about this" option dene ka functionality add karein. Selected text ko backend ke /chat/selected endpoint par bhejein. ✅ Phase 4: Deployment aur Final Polish (Week 4) Backend ko production environment mein deploy karein aur final integration aur testing complete karein. Task Deployment Steps 1. Backend Server ko Deploy Karein Aapka FastAPI backend kisi bhi platform par deploy ho sakta hai jo Python support karta hai (e.g., Railway, Render, Google Cloud Run). Key Steps: 1. requirements.txt aur runtime.txt (Python version specify karne ke liye) files project mein honi chahiye. 2. Deployment platform par saare environment variables (OPENAI_API_KEY, DATABASE_URL, etc.) set karein. 3. Platform ke deployment command mein uvicorn main:app --host=0.0.0.0 --port=$PORT specify karein. 2. CORS (Cross-Origin Resource Sharing) Configure Karein Jab aapka frontend (book) aur backend alag-alag domains par honge, tab CORS enable karna zaroori hai. FastAPI mein CORSMiddleware add karein aur frontend book ke domain ko allow karein. 3. Security Best Practices Implement Karein API Key Protection: Kabhi bhi API keys ko frontend code mein hard-code na karein. Sab keys backend environment variables mein rahein. Request Limiting (Rate Limiting): Public endpoints par rate limiting laga dein taake misuse na ho. 4. End-to-End Testing aur Quality Check Puri workflow test karein: 1. Book se general question poochna. 2. Text select karke uspar specific sawaal karna. 3. Chat history across sessions check karna. 4. Response time aur answer accuracy verify karna. 🚀 Next Steps aur Additional RecommendationsAsynchronous Operations: FastAPI ki async/await features ka faida uthayein, khaas kar database aur external API calls ke liye, taake performance behtar ho. Error Handling aur Logging: Har possible error case (e.g., API failure, empty search results) ke liye robust error handling implement karein. Saari activities ko log karein debugging ke liye. Scalability: Agar book ki size badi hai, to document ingestion pipeline ko background jobs (e.g., using Celery) mein daalne ka soch sakte hain taike main application block na ho. Metadata aur Filtering: Qdrant mein chunks ko store karte waqt metadata (jaise page_number, chapter) bhi save karein. Baad mein aap retrieval ko current page ke hisaab se filter kar sakte hain, jisse answers aur bhi relevant ho jaayein."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask General Questions (Priority: P1)

Users should be able to ask general questions about the book content through an embedded chat widget and receive relevant answers.

**Why this priority**: Core functionality of the AI-Native Textbook.

**Independent Test**: Can be fully tested by asking a question in the chat widget and verifying a relevant response.

**Acceptance Scenarios**:

1.  **Given** the user is viewing a book page and the chat widget is visible, **When** the user types a general question into the chat input and submits it, **Then** the chatbot displays a relevant answer.
2.  **Given** the user asks a question, **When** the backend processes the query using LLM call with context, **Then** the response is accurate and coherent.

### User Story 2 - Ask About Selected Text (Priority: P1)

Users should be able to select text within the book and ask specific questions related to the highlighted content using a context menu option.

**Why this priority**: Enhances interactivity and provides context-aware assistance.

**Independent Test**: Can be fully tested by highlighting text, using the "Ask about this" option, and verifying a relevant response from the chatbot.

**Acceptance Scenarios**:

1.  **Given** the user is viewing a book page and selects a portion of text, **When** the user activates the "Ask about this" feature (e.g., via a context menu), **Then** the selected text is sent to the backend's `/chat/selected` endpoint.
2.  **Given** the selected text is sent to the backend, **When** the chatbot processes the query using the selected text as direct context, **Then** the chatbot displays an answer highly relevant to the selected text.

### User Story 3 - Maintain Chat History (Priority: P2)

The system should store user conversation messages and metadata to maintain context across sessions.

**Why this priority**: Improves user experience by allowing seamless continuation of conversations.

**Independent Test**: Can be fully tested by initiating a conversation, closing and reopening the book/app, and verifying the previous chat history is loaded.

**Acceptance Scenarios**:

1.  **Given** a user has engaged in a conversation with the chatbot, **When** the user returns to the book later, **Then** their previous chat history is displayed in the chat widget.
2.  **Given** a user logs out and then logs back in, **When** they access the chatbot, **Then** their historical conversations are available.

### User Story 4 - Local Development Environment Setup (Priority: P3)

Developers should be able to set up a local development environment with all necessary tools and configurations to work on the project.

**Why this priority**: Enables efficient development and collaboration.

**Independent Test**: Can be fully tested by following the setup guide and verifying all dependencies are installed and the application runs locally.

**Acceptance Scenarios**:

1.  **Given** a developer has a fresh machine, **When** they follow the provided setup instructions, **Then** their development environment is ready with all required tools (OpenAI API key, Neon DB, Qdrant Cloud, Python packages).

### Edge Cases

- What happens if the OpenAI/Gemini API key is invalid or missing? (Backend should return an appropriate error, frontend should display an error message)
- How does the system handle very large text selections for the "Ask about this" feature? (Backend should handle chunking or truncation gracefully)
- What happens if the Qdrant query returns no relevant chunks? (LLM should indicate lack of specific information or provide a general answer)
- How does the system handle network failures during API calls? (Frontend should display loading/error states, backend should handle exceptions gracefully)
- What if a user tries to access the chatbot without logging in? (Frontend should prompt for login, backend endpoints should reject unauthenticated requests)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST integrate with OpenAI (or Gemini) for LLM and embeddings.
- **FR-002**: System MUST use Neon (Postgres) for database storage.
- **FR-003**: System MUST use Qdrant Cloud for vector database storage.
- **FR-004**: Backend MUST be implemented using FastAPI.
- **FR-005**: System MUST implement document chunking (e.g., 300-500 words per chunk).
- **FR-006**: System MUST generate embeddings for each text chunk.
- **FR-007**: System MUST store text chunks with embeddings, original text, and source metadata (e.g., page number) in Qdrant.
- **FR-008**: Backend MUST provide a `/chat` POST endpoint for general queries.
- **FR-009**: The `/chat` endpoint MUST embed the user query, perform a semantic search in Qdrant, build context from retrieved chunks, and call the LLM to generate a response.
- **FR-010**: Backend MUST provide a `/chat/selected` POST endpoint for queries on selected text.
- **FR-011**: The `/chat/selected` endpoint MUST use the provided selected text directly as context for the LLM call.
- **FR-012**: System MUST define Pydantic models for request/response structures (e.g., `QueryRequest`, `QueryResponse`, `SelectedTextRequest`).
- **FR-013**: System MUST handle database connection and session management for Neon Postgres.
- **FR-014**: System MUST store user conversation messages and metadata to maintain session history.
- **FR-015**: Frontend MUST provide an embeddable, minimal, and non-intrusive chat interface within the book.
- **FR-016**: Chat widget MUST send current page number or chapter title as metadata to the backend for context refinement.
- **FR-017**: Frontend MUST handle API calls to the backend.
- **FR-018**: Frontend MUST implement a "Select Text to Ask" feature, sending selected text to `/chat/selected`.
- **FR-019**: Backend MUST be deployable on Python-supporting platforms (e.g., Railway, Render, Google Cloud Run).
- **FR-020**: System MUST use `requirements.txt` and `runtime.txt` for deployment.
- **FR-021**: Deployment platform MUST have environment variables (OPENAI_API_KEY, DATABASE_URL, etc.) configured.
- **FR-022**: Backend MUST configure CORS middleware to allow frontend book domain access.
- **FR-023**: System MUST protect API keys by storing them in backend environment variables, not hardcoding in frontend.
- **FR-024**: Public endpoints MUST have rate limiting to prevent misuse.
- **FR-025**: System MUST implement end-to-end testing for general questions, selected text questions, and chat history across sessions.
- **FR-026**: System MUST verify response time and answer accuracy.
- **FR-027**: Backend MUST utilize FastAPI's async/await for performance optimization.
- **FR-028**: System MUST implement robust error handling and logging for all possible error cases.
- **FR-029**: System SHOULD consider background jobs for document ingestion if the book size is large.
- **FR-030**: Qdrant storage MUST include metadata (page_number, chapter) for retrieval filtering.

### Key Entities *(include if feature involves data)*

- **User**: Interacts with the chatbot, generates queries, selects text.
- **Book Content**: Text to be processed, chunked, embedded, and queried.
- **Text Chunk**: A segment of book content with its embedding, original text, and source metadata.
- **Query**: User's question, either general or related to selected text.
- **Chat History**: Stored messages and metadata for a user's conversation with the chatbot.
- **Module**: A logical grouping of chapters within the textbook.
- **Chapter**: A section of content within a module, potentially with English and Urdu versions.
- **UserChapterProgress**: Tracks a user's progress on a specific chapter (e.g., not_started, in_progress, completed).
- **UserQuizAttempt**: Records a user's attempt at a quiz, including score and associated quiz ID.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of general user queries are answered accurately and relevantly by the chatbot.
- **SC-002**: 98% of queries on selected text receive answers highly relevant to the highlighted content.
- **SC-003**: Chat history is successfully retrieved for 100% of returning users across sessions.
- **SC-004**: Backend API response time for chatbot queries (general and selected text) is under 500ms for 90% of requests.
- **SC-005**: All external services (OpenAI/Gemini, Neon DB, Qdrant) are successfully integrated and functional.
- **SC-006**: The local development environment can be set up within 30 minutes following the provided guide.
- **SC-007**: Frontend-backend communication functions without CORS-related errors.
- **SC-008**: Sensitive API keys are not exposed in frontend code.
- **SC-009**: Public endpoints are protected by rate limiting, preventing more than 30 requests per minute per user.
- **SC-010**: All end-to-end tests pass, covering general questions, selected text, and chat history.
- **SC-011**: Error handling mechanisms gracefully manage 100% of simulated API failures or empty search results, providing informative feedback to the user.
