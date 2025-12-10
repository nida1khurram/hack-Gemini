from qdrant_client import QdrantClient, models
import google.generativeai as genai
from sqlmodel import Session
from uuid import UUID
from ..database import settings
from .embedding_service import EmbeddingService
from .chat_history_service import ChatHistoryService # Import ChatHistoryService

class ChatbotService:
    def __init__(self, qdrant_client: QdrantClient, db: Session, user_id: UUID):
        self.qdrant_client = qdrant_client
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.embedding_service = EmbeddingService()
        self.chat_history_service = ChatHistoryService(db) # Initialize ChatHistoryService
        self.user_id = user_id # Store user_id
        self.collection_name = "ai_textbook_chapters" # This should be configurable

    async def query(self, text: str, context: str | None = None) -> str:
        # First, ensure chat history exists for the user or create a new one
        chat_histories = self.chat_history_service.get_user_chat_histories(self.user_id)
        if not chat_histories:
            current_chat_history = self.chat_history_service.create_chat_history(self.user_id)
        else:
            current_chat_history = chat_histories[0] # Use the most recent chat history for context

        # Add user's query to chat history
        self.chat_history_service.add_message_to_history(current_chat_history.id, "user", text)

        # Build RAG context (fallback when no embeddings available)
        rag_context = ""
        if context:
            rag_context += f"User provided additional context: {context}\n\n"

        # Try to perform semantic search in Qdrant if the method exists
        try:
            # Embed the user's query
            query_embedding = (await self.embedding_service.get_embeddings([text]))[0]

            # Perform semantic search in Qdrant - use the correct method name
            if hasattr(self.qdrant_client, 'search'):
                search_result = self.qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=query_embedding,
                    limit=3  # Retrieve top 3 relevant chunks
                )
            elif hasattr(self.qdrant_client, 'search_points'):
                search_result = self.qdrant_client.search_points(
                    collection_name=self.collection_name,
                    query=query_embedding,
                    limit=3
                )
            else:
                search_result = []

            if search_result:
                retrieved_docs_content = [hit.payload.get('content', '') for hit in search_result if hit.payload and hasattr(hit, 'payload')]
                if retrieved_docs_content:
                    rag_context += "Retrieved documents context:\n" + "\n---\n".join(retrieved_docs_content)
        except Exception as e:
            # Log the error but continue with a basic response
            print(f"Error in Qdrant search: {e}")
            # Continue with empty rag_context to use fallback

        # Prepare prompt for LLM
        prompt = f"Given the following context: {rag_context}\n\nAnswer the question: {text}"

        if not rag_context: # Fallback if no context found
            prompt = f"Answer the question: {text}"

        try:
            model = genai.GenerativeModel(settings.GEMINI_CHAT_MODEL)
            response = model.generate_content(prompt)
            response_text = response.text
        except Exception as e:
            # Fallback response if Gemini API fails
            print(f"Error generating response with Gemini: {e}")
            response_text = f"I understand you're asking: '{text}'. However, I'm currently unable to generate a detailed response. Please try again later or contact support if the issue persists."

        # Add chatbot's response to chat history
        self.chat_history_service.add_message_to_history(current_chat_history.id, "assistant", response_text)

        return response_text
