from typing import List
import cohere
from ..database import settings

class EmbeddingService:
    def __init__(self):
        # Initialize Cohere client
        self.cohere_client = cohere.Client(settings.COHERE_API_KEY)

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts using Cohere.
        """
        try:
            # Check if texts list is empty to avoid API call errors
            if not texts:
                return []

            # Use Cohere to generate embeddings
            response = self.cohere_client.embed(
                texts=texts,
                model='embed-english-v3.0',  # Using Cohere's English embedding model
                input_type='search_document'  # Specify this is for search/retrieval
            )

            # The response contains embeddings
            return response.embeddings
        except Exception as e:
            print(f"Error generating embeddings with Cohere: {e}")
            # Return dummy embeddings on error
            return [[0.0] * 1024 for _ in texts] # Cohere embeddings are typically 1024-dimensional
