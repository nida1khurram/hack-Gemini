from qdrant_client import QdrantClient

# TODO: Replace with your actual Qdrant connection details (host, port, api_key)
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_API_KEY = None # Set to your API key if using Qdrant Cloud

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT, api_key=QDRANT_API_KEY)

def get_qdrant_client():
    return client
