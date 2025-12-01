# Research: AI-Native Textbook on Physical AI & Humanoid Robotics

This document outlines the key decisions and research findings for the project.

## Key Decisions

### Content Depth vs. Breadth
- **Decision**: Focus on implementable projects over deep theoretical dives.
- **Rationale**: The primary goal is to provide a hands-on learning experience. Project-based learning is more engaging and effective for the target audience.
- **Alternatives considered**: A comprehensive theoretical textbook was considered but rejected as it would be less practical and engaging.

### Hardware Emphasis
- **Decision**: Provide both cloud and local paths for simulations and development.
- **Rationale**: This approach ensures accessibility for readers with varying hardware capabilities, aligning with the "Accessibility and Clarity" principle.
- **Alternatives considered**: Focusing only on local setup was rejected as it would exclude users without powerful hardware. Focusing only on cloud setup was rejected as it would introduce costs and dependencies.

### Assessment Approach
- **Decision**: Project-based assessments with code submissions.
- **Rationale**: This aligns with the hands-on, project-based learning approach and provides a more practical way to assess skills.
- **Alternatives considered**: Multiple-choice quizzes were considered but rejected as they do not effectively assess practical skills.

### Translation Quality
- **Decision**: Professional translation for key terms only, with the rest machine-translated.
- **Rationale**: This provides a balance between quality and cost. Key technical terms need to be accurate, while machine translation is sufficient for general text.
- **Alternatives considered**: Full professional translation was rejected due to high cost and time constraints. Full machine translation was rejected due to potential inaccuracies in technical terms.

## Technology Research

### Docusaurus
- **Task**: Research best practices for Docusaurus project structure.
- **Findings**: Docusaurus is well-suited for this project due to its focus on documentation and content-driven websites. The default project structure is a good starting point. We will use plugins for features like search and internationalization.

### FastAPI
- **Task**: Research integrating FastAPI with Neon Postgres and Qdrant.
- **Findings**: FastAPI is a high-performance Python web framework that is easy to learn and use. It has excellent support for asynchronous operations, which is ideal for AI model integration. There are well-documented libraries for connecting to Postgres and Qdrant.

### Better-auth
- **Task**: Research implementing user authentication with Better-auth.
- **Findings**: Better-auth is a secure and feature-rich authentication library for FastAPI. It supports various authentication methods and social logins. It also provides a good foundation for user profile management.

### OpenAI API
- **Task**: Research using OpenAI API for RAG chatbot and translation.
- **Findings**: The OpenAI API provides powerful models for natural language understanding and generation, which are essential for the RAG chatbot. The API also offers translation capabilities. We will need to carefully manage API costs.

### Deployment
- **Task**: Research best practices for deploying FastAPI to Vercel/Heroku.
- **Findings**: Both Vercel and Heroku are good options for deploying FastAPI applications. Vercel offers a seamless deployment experience with a focus on serverless functions, while Heroku is a more traditional PaaS. We will start with Vercel due to its generous free tier and ease of use.
