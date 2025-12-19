#!/usr/bin/env python3
"""
Quick test to verify Cohere embedding service is working properly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database import settings
from src.services.embedding_service import EmbeddingService

def test_embedding():
    print("Testing Cohere embedding service...")

    try:
        # Initialize the embedding service
        embedding_service = EmbeddingService()

        # Test embedding generation
        test_texts = ["What is ROS 2?", "Python publisher example"]
        embeddings = embedding_service.get_embeddings(test_texts)

        print(f"Generated {len(embeddings)} embeddings")
        if embeddings:
            print(f"First embedding dimension: {len(embeddings[0])}")
            print("Embedding service is working correctly!")

        return True
    except Exception as e:
        print(f"Error in embedding service: {e}")
        return False

if __name__ == "__main__":
    test_embedding()