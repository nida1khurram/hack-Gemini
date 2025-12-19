from qdrant_client import QdrantClient, models
from typing import List, Dict, Any
from .database import settings
import logging

# Try to connect to Qdrant server, fallback to local persistent storage if not available
try:
    # Try connecting with URL first (for cloud instances)
    client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    # Test the connection
    client.get_collections()
    logging.info("Connected to remote Qdrant server successfully.")
except Exception as e:
    try:
        # If URL fails, try with host/port
        client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, api_key=settings.QDRANT_API_KEY)
        # Test the connection
        client.get_collections()
        logging.info("Connected to remote Qdrant server successfully.")
    except Exception as e2:
        logging.warning(f"Could not connect to Qdrant server: {e2}. Using local persistent storage for development.")
        # Use local persistent storage instead of in-memory to preserve data between runs
        client = QdrantClient(path="./qdrant_local")  # Local persistent storage

def get_qdrant_client():
    return client

async def recreate_qdrant_collection(collection_name: str, vector_size: int = 1024):
    """
    Creates or recreates a Qdrant collection with the specified name and vector size.
    For Cohere embeddings, use 1024 dimensions.
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
