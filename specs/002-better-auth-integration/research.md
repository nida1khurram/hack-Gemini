# Research: Defining "Better-Auth"

**Status**: Completed

This document outlines the research required to resolve the critical unknown identified in the implementation plan: the specific nature of "Better-Auth".

## 1. Research Task: What is "Better-Auth"?

The term "Better-Auth" is used in the project requirements, but it does not map to a standard, well-known authentication service, library, or platform. The entire implementation strategy depends on this definition.

### Initial Findings & Roadblock

- **Finding**: The user-provided URL `https://www.better-auth.com/` refers to a **TypeScript library** designed for Node.js environments.
- **Conclusion**: It is **not compatible** with the project's Python/FastAPI backend. A new decision was required.

### Decision

- **Decision**: The project will use the **`fastapi-users`** library.

### Rationale

- **Rationale**: `fastapi-users` is a dedicated, open-source authentication library specifically designed for FastAPI. It provides all the required features out-of-the-box (email/password auth, social auth, password reset) and integrates directly into the existing application, which aligns with the goal of having a self-contained solution without relying on external managed services. This choice minimizes external dependencies and costs while providing a secure and maintainable solution.

### Alternatives Considered

| Option | Type | Description |
| :--- | :--- | :--- |
| **A** | **Managed Service** | **Auth0 / Okta**: A leading identity-as-a-service platform. |
| **B** | **Managed Service** | **Firebase Authentication**: Part of the Google Firebase suite. |
| **C** | **Self-Hosted** | **Keycloak**: An open-source Identity and Access Management solution. |
| **D** | **Library** | **fastapi-users**: A library for FastAPI that provides a robust, out-of-the-box authentication system. |
