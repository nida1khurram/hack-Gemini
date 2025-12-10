from typing import List
import google.generativeai as genai
from ..database import settings

class EmbeddingService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embeddings for a list of texts using the configured LLM (Gemini).
        """
        try:
            # Check if texts list is empty to avoid API call errors
            if not texts:
                return []
                
            # Gemini's embed_content takes a list of strings and returns a list of embeddings
            result = genai.embed_content(
                model='models/embedding-001', # Using a specific Gemini embedding model
                content=texts,
                task_type="RETRIEVAL_DOCUMENT"
            )
            # The result object contains an 'embedding' key which is a list of embeddings
            # Each embedding is a list of floats
            return result['embedding']
        except Exception as e:
            print(f"Error generating embeddings with Gemini: {e}")
            # Return dummy embeddings on error or raise an exception
            return [[0.0] * 768 for _ in texts] # Example: 768-dimensional dummy embeddings
