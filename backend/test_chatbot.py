#!/usr/bin/env python3
"""
Test script to verify chatbot functionality
"""

import asyncio
from qdrant_client import QdrantClient
from sqlmodel import Session, create_engine
from src.database import settings
from src.services.chatbot_service import ChatbotService
from uuid import UUID


async def test_chatbot():
    print("Testing chatbot functionality...")

    # Check if API key is properly loaded
    print(f"Gemini API Key loaded: {bool(settings.GEMINI_API_KEY)}")
    print(f"Gemini API Key length: {len(settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else 0}")
    print(f"Gemini Chat Model: {settings.GEMINI_CHAT_MODEL}")

    # Create a mock DB session
    engine = create_engine(settings.DATABASE_URL)
    db = Session(engine)

    # Try to connect to Qdrant
    print(f"Qdrant Host: {settings.QDRANT_HOST}")
    print(f"Qdrant Port: {settings.QDRANT_PORT}")
    print(f"Qdrant URL: {settings.QDRANT_URL}")

    try:
        # For cloud Qdrant, we use the URL and API key
        qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
            timeout=10
        )

        print("Attempting to connect to Qdrant...")
        # Try to get collection info to verify connection
        collections = qdrant_client.get_collections()
        print(f"Connected to Qdrant successfully. Collections: {collections}")
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        # If cloud connection fails, try localhost
        try:
            print("Trying localhost connection...")
            qdrant_client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT,
                api_key=settings.QDRANT_API_KEY,
                timeout=10
            )
            collections = qdrant_client.get_collections()
            print(f"Connected to Qdrant (localhost) successfully. Collections: {collections}")
        except Exception as e2:
            print(f"Error connecting to Qdrant (localhost): {e2}")
            # Create a mock client for testing
            qdrant_client = None
            print("Using mock Qdrant client for testing")

    # Create chatbot service
    user_id = "123e4567-e89b-12d3-a456-426614174000"  # Mock UUID
    if qdrant_client:
        chatbot_service = ChatbotService(qdrant_client, db, user_id)

        # Test the query function
        try:
            print("\nTesting chatbot query...")
            response = await chatbot_service.query("Hello, how are you?")
            print(f"Response: {response}")

            if "requires a valid Google Gemini API key" in response:
                print("\\n[X] The chatbot is not using the Gemini API properly")
            else:
                print("\\n[OK] The chatbot is working with Gemini API")

        except Exception as e:
            print(f"Error during query: {e}")
    else:
        print("Cannot test chatbot service without Qdrant connection")


if __name__ == "__main__":
    asyncio.run(test_chatbot())