from qdrant_client import QdrantClient, models
from typing import List, Dict, Any
from .database import settings
import logging

# Try to connect to Qdrant server, fallback to in-memory if not available
try:
    client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, api_key=settings.QDRANT_API_KEY)
    # Test the connection
    client.get_collections()
except Exception as e:
    logging.warning(f"Could not connect to Qdrant server: {e}. Using in-memory storage for development.")
    client = QdrantClient(":memory:")

def get_qdrant_client():
    return client

async def recreate_qdrant_collection(collection_name: str, vector_size: int = 768):
    """
    Creates or recreates a Qdrant collection with the specified name and vector size.
    """
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
    )

async def upsert_vectors_to_collection(collection_name: str, points: List[models.PointStruct]):
    """
    Inserts or updates vectors and their payloads into a Qdrant collection.
    """
    client.upsert(
        collection_name=collection_name,
        wait=True,
        points=points
    )
