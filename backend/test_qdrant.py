#!/usr/bin/env python3
"""
Quick test to verify Qdrant vector database has content
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.vector_db import get_qdrant_client
from src.database import settings
from src.services.embedding_service import EmbeddingService
import asyncio

async def test_qdrant():
    print("Testing Qdrant vector database...")

    try:
        # Get Qdrant client
        qdrant_client = get_qdrant_client()

        # Check if collection exists and has points
        collections = qdrant_client.get_collections()
        print(f"Available collections: {[col.name for col in collections.collections]}")

        # Check our specific collection
        try:
            collection_info = qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)
            print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' info:")
            print(f"  Points count: {collection_info.points_count}")
            print(f"  Vector size: {collection_info.config.params.vectors.size}")
        except Exception as e:
            print(f"Collection '{settings.QDRANT_COLLECTION_NAME}' not found: {e}")
            return

        # Test embedding generation
        embedding_service = EmbeddingService()
        query_embedding = (await embedding_service.get_embeddings(["What is ROS 2?"]))[0]
        print(f"Generated embedding with dimension: {len(query_embedding)}")

        # Try to search in the collection using the correct method
        if hasattr(qdrant_client, 'search'):
            search_result = qdrant_client.search(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                query_vector=query_embedding,
                limit=3
            )
        elif hasattr(qdrant_client, 'search_points'):
            search_result = qdrant_client.search_points(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                query=query_embedding,
                limit=3
            )
        else:
            print("No search method available on Qdrant client")
            return

        print(f"Search returned {len(search_result)} results:")
        for i, hit in enumerate(search_result):
            print(f"  Result {i+1}:")
            print(f"    Score: {hit.score}")
            print(f"    Content preview: {hit.payload.get('content', '')[:100]}...")
            print(f"    Title: {hit.payload.get('title', 'N/A')}")

    except Exception as e:
        print(f"Error in Qdrant test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_qdrant())