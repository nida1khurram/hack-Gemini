import os
from qdrant_client import QdrantClient
from openai import OpenAI

class ChatbotService:
    def __init__(self, qdrant_client: QdrantClient):
        self.qdrant_client = qdrant_client
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # TODO: Load API key securely
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "ai_textbook_chapters") # TODO: Define collection name

    async def query(self, text: str, context: str | None = None) -> str:
        # TODO: Implement retrieval from Qdrant based on text/context
        # For now, a simple placeholder
        retrieved_docs = [] # Placeholder for documents retrieved from Qdrant

        prompt = f"Given the following context: {context}\n\nAnswer the question: {text}"
        if retrieved_docs:
            prompt = f"Given the following documents: {retrieved_docs}\nAnd the context: {context}\n\nAnswer the question: {text}"

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo", # TODO: Make model configurable
            messages=[
                {"role": "system", "content": "You are a helpful assistant for an AI-Native Textbook."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
