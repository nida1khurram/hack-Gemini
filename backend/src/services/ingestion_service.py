from typing import List, Dict, Any
import re
from .embedding_service import EmbeddingService

class IngestionService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Chunks text into smaller pieces with a specified overlap.
        Simple word-based chunking for now.
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
