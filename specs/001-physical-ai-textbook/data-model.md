# Data Model: AI-Native Textbook on Physical AI & Humanoid Robotics

This document defines the data model for the project.

## User
Represents a reader of the textbook.

**Attributes**:
- `id`: (UUID, Primary Key) Unique identifier for the user.
- `username`: (String, Unique) The user's chosen username.
- `email`: (String, Unique) The user's email address.
- `hashed_password`: (String) The user's hashed password.
- `background`: (Enum: "beginner", "intermediate", "expert") The user's self-reported background.
- `created_at`: (Timestamp) The timestamp when the user was created.
- `updated_at`: (Timestamp) The timestamp when the user was last updated.

## Chapter
Represents a chapter in the textbook.

**Attributes**:
- `id`: (Integer, Primary Key) Unique identifier for the chapter.
- `module_id`: (Integer, Foreign Key) The ID of the module this chapter belongs to.
- `title`: (String) The title of the chapter.
- `content_english`: (Text) The content of the chapter in English.
- `content_urdu`: (Text) The content of the chapter in Urdu.

## Module
Represents a module in the textbook.

**Attributes**:
- `id`: (Integer, Primary Key) Unique identifier for the module.
- `title`: (String) The title of the module.
- `description`: (Text) A brief description of the module.

## UserChapterProgress
Tracks a user's progress through the chapters.

**Attributes**:
- `id`: (UUID, Primary Key)
- `user_id`: (UUID, Foreign Key to User)
- `chapter_id`: (Integer, Foreign Key to Chapter)
- `status`: (Enum: "not_started", "in_progress", "completed") The user's progress status for the chapter.
- `started_at`: (Timestamp)
- `completed_at`: (Timestamp, nullable)

## UserQuizAttempt
Tracks a user's attempt at a quiz.

**Attributes**:
- `id`: (UUID, Primary Key)
- `user_id`: (UUID, Foreign Key to User)
- `quiz_id`: (Integer) The ID of the quiz.
- `score`: (Float) The user's score on the quiz.
- `attempted_at`: (Timestamp)
