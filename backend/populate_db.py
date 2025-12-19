#!/usr/bin/env python3
"""
Script to populate the database with book content from documentation files.
This will extract content from the frontend documentation and add it to the
database so the chatbot can use it for RAG (Retrieval-Augmented Generation).
"""

import os
import sys
import re
from pathlib import Path

# Add src to path so we can import the models
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import cohere
from sqlmodel import SQLModel, Session, create_engine
from src.models import Module, Chapter
from src.database import settings
from src.vector_db import get_qdrant_client, upsert_vectors_to_collection, recreate_qdrant_collection
from qdrant_client import models
from uuid import uuid4
import asyncio

def extract_content_from_markdown(file_path):
    """Extract content from markdown file, removing frontmatter and code blocks"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter (content between --- lines)
    lines = content.split('\n')
    frontmatter_removed = []
    in_frontmatter = False
    for line in lines:
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            continue
        if not in_frontmatter:
            frontmatter_removed.append(line)

    content = '\n'.join(frontmatter_removed)

    # Remove code blocks (content between ``` pairs)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Remove image references and other markdown syntax that might not be useful for RAG
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)  # Remove image tags
    content = re.sub(r'\[.*?\]\(.*?\)', '', content)   # Remove links

    # Clean up multiple newlines
    content = re.sub(r'\n\s*\n', '\n\n', content)

    return content.strip()

def chunk_text(text, chunk_size=500, overlap=50):
    """Chunk text into smaller pieces with overlap"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():  # Only add non-empty chunks
            chunks.append(chunk)
    return chunks

def main():
    print("Starting database population with documentation content...")

    # Initialize Cohere client
    cohere_client = cohere.Client(settings.COHERE_API_KEY)

    # Use the local SQLite database instead of the PostgreSQL one
    local_db_path = "ai_textbook.db"
    local_db_url = f"sqlite:///{local_db_path}"
    engine = create_engine(local_db_url, connect_args={"check_same_thread": False})

    # Create tables if they don't exist
    from src.models import Base
    Base.metadata.create_all(bind=engine)

    # Connect to database
    db = Session(bind=engine)

    try:
        # Create modules and chapters from documentation files
        doc_path = Path("../frontend/docs")

        # Create a main module for the book
        main_module = Module(
            title="Physical AI & Humanoid Robotics",
            description="Comprehensive guide to Physical AI and Humanoid Robotics",
            order=1
        )
        db.add(main_module)
        db.commit()
        db.refresh(main_module)

        print(f"Created module: {main_module.title}")

        # Process each markdown file as a chapter
        markdown_files = list(doc_path.rglob("*.md"))

        for i, file_path in enumerate(markdown_files):
            print(f"Processing: {file_path.name}")

            # Extract title from filename or first H1 in content
            content = extract_content_from_markdown(file_path)
            title = file_path.stem.replace('_', ' ').replace('-', ' ').title()

            # Try to find a more specific title from the content
            lines = content.split('\n')
            for line in lines[:10]:  # Check first 10 lines for H1
                if line.strip().startswith('# '):
                    title = line.strip()[2:]  # Remove '# ' prefix
                    break

            # Create the main chapter with the full content
            chapter = Chapter(
                module_id=main_module.id,
                title=title,
                content_english=content
            )
            db.add(chapter)
            db.commit()
            db.refresh(chapter)

            print(f"  Created chapter: {chapter.title}")

            # Create chunks for vector database indexing
            chunks = chunk_text(content)
            print(f"  Created {len(chunks)} chunks for vector indexing")

            # Index chunks into Qdrant vector database
            qdrant_client = get_qdrant_client()

            # Recreate the collection to start fresh
            asyncio.run(recreate_qdrant_collection(settings.QDRANT_COLLECTION_NAME))

            points = []
            for j, chunk in enumerate(chunks):
                if len(chunk.strip()) > 10:  # Only index substantial chunks
                    try:
                        # Generate embedding for the chunk using Cohere
                        response = cohere_client.embed(
                            texts=[chunk],
                            model='embed-english-v3.0',
                            input_type='search_document'
                        )
                        embedding = response.embeddings[0]

                        # Create a Qdrant point
                        point = models.PointStruct(
                            id=str(uuid4()),
                            vector=embedding,
                            payload={
                                "content": chunk,
                                "title": title,
                                "chapter_id": chapter.id,
                                "module_id": main_module.id,
                                "source_file": str(file_path)
                            }
                        )
                        points.append(point)

                        print(f"    Generated embedding for chunk {j+1}")
                    except Exception as e:
                        print(f"    Error generating embedding for chunk {j+1}: {e}")

            if points:
                # Upsert all points to the collection
                asyncio.run(upsert_vectors_to_collection(settings.QDRANT_COLLECTION_NAME, points))
                print(f"  Indexed {len(points)} chunks to vector database")

        print(f"\nSuccessfully populated database with {len(markdown_files)} documentation files")
        print(f"Created 1 module and {len(markdown_files)} chapters")
        print(f"Indexed content into Qdrant collection: {settings.QDRANT_COLLECTION_NAME}")

    except Exception as e:
        print(f"Error during population: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()