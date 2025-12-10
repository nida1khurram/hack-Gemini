# Research: AI-Native Textbook Platform - Technology Choices

**Date**: 2025-12-10

## Key Technology Decisions and Rationale

### Backend Framework: FastAPI

-   **Decision**: FastAPI
-   **Rationale**: FastAPI was chosen for its modern, fast (built on Starlette and Pydantic), and intuitive framework for building APIs with Python. Its key advantages for this project include:
    -   **High Performance**: Leveraging asynchronous programming (`async/await`) makes it highly efficient for I/O-bound tasks like database queries and external LLM API calls.
    -   **Ease of Use & Developer Experience**: Excellent documentation, automatic interactive API documentation (Swagger UI), and strong type hints reduce development time and improve code quality.
    -   **Pydantic Integration**: Seamless integration with Pydantic for data validation and serialization ensures robust and safe API contracts.
    -   **Scalability**: Suitable for deploying on various platforms that support Python.

### Relational Database: PostgreSQL (via Neon.tech)

-   **Decision**: PostgreSQL, managed by Neon.tech
-   **Rationale**: PostgreSQL is a powerful, open-source object-relational database system known for its reliability, feature richness, and performance. Neon.tech provides a serverless PostgreSQL offering that simplifies database management and scaling.
    -   **Robustness & Data Integrity**: Ideal for storing structured application data such as user profiles, module/chapter information, user progress, and chat history.
    -   **Scalability**: Neon.tech's serverless architecture allows for automatic scaling, which is beneficial for fluctuating workloads.
    -   **Managed Service**: Reduces operational overhead for database setup and maintenance.

### Vector Database: Qdrant Cloud

-   **Decision**: Qdrant Cloud
-   **Rationale**: Qdrant is an open-source vector similarity search engine, and its cloud offering provides a managed service. It is critical for implementing the Retrieval Augmented Generation (RAG) pattern in the chatbot.
    -   **Efficient Vector Search**: Enables fast and accurate retrieval of relevant text chunks based on semantic similarity to user queries.
    -   **Metadata Filtering**: Supports filtering search results by metadata (e.g., page number, chapter), which is essential for context-aware responses in the chatbot.
    -   **Managed Cloud Service**: Simplifies deployment, scaling, and maintenance of the vector database.

### Large Language Models (LLM) and Embeddings: OpenAI / Google Gemini

-   **Decision**: Integration with both OpenAI and Google Gemini APIs.
-   **Rationale**: Utilizing external LLM providers offers access to state-of-the-art models for both text generation (chatbot responses) and text embeddings (converting text into numerical vectors).
    -   **Advanced AI Capabilities**: Provides powerful language understanding and generation abilities for the chatbot.
    -   **Flexibility**: Supporting both providers offers redundancy and allows the project to leverage the strengths of different models or switch providers based on performance, cost, or feature availability.
    -   **Embeddings**: Essential for transforming book content and user queries into vector representations that can be efficiently stored and searched in Qdrant.

### Frontend Framework: Docusaurus

-   **Decision**: Docusaurus
-   **Rationale**: Docusaurus is a static site generator specifically designed for building documentation websites.
    -   **Markdown-First Content**: Naturally suited for creating a textbook, allowing content to be written and managed in Markdown.
    -   **React-based**: Allows for the creation and embedding of interactive UI components (like the chatbot widget) directly within the documentation pages, enhancing the learning experience.
    -   **Extensibility**: Provides plugins and themes for customization.
    -   **Deployment**: Easy to deploy as a static site (e.g., to GitHub Pages).
