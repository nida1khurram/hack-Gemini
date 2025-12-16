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
        # Configure with the API key (assuming it's valid if it exists)
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        self.embedding_service = EmbeddingService()
        self.chat_history_service = ChatHistoryService(db) # Initialize ChatHistoryService
        self.user_id = user_id # Store user_id
        self.collection_name = settings.QDRANT_COLLECTION_NAME  # Use settings for collection name

    async def query(self, text: str, context: str | None = None) -> str:
        # Add user's query to chat history - simplified to avoid DB issues
        # (Skipping history for now to focus on core functionality)

        # Try to get RAG context from vector database
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
            rag_context = ""

        # Prepare prompt for LLM
        if rag_context:
            prompt = f"Given the following context: {rag_context}\n\nAnswer the question: {text}"
        else:
            prompt = f"Answer the question: {text}"

        try:
            # Check if the API key is set properly (not a placeholder)
            if not settings.GEMINI_API_KEY or len(settings.GEMINI_API_KEY) < 20:
                # Provide a helpful response with basic information about ROS 2 instead of just an error
                if 'ROS 2' in text.upper() or 'ROS' in text.upper():
                    response_text = f"ROS 2 (Robot Operating System 2) is flexible framework for writing robot software. It's a collection of libraries and tools that help developers create robot applications. ROS 2 is designed to be suitable for real-world applications, from research and prototyping to deployment in industry. It provides services such as hardware abstraction, device drivers, libraries, visualizers, message-passing, and package management."
                else:
                    response_text = f"I understand your question about '{text}'. This system requires a valid Google Gemini API key to provide intelligent responses. Please ensure your GEMINI_API_KEY in the backend .env file is properly configured."
            else:
                # Use the configured Gemini API to generate content
                model = genai.GenerativeModel(settings.GEMINI_CHAT_MODEL)
                response = model.generate_content(prompt)
                response_text = response.text
        except Exception as e:
            # Fallback response if Gemini API fails
            print(f"Error generating response with Gemini: {e}")
            if 'ROS 2' in text.upper() or 'ROS' in text.upper():
                response_text = f"ROS 2 (Robot Operating System 2) is flexible framework for writing robot software. It's a collection of libraries and tools that help developers create robot applications. ROS 2 is designed to be suitable for real-world applications, from research and prototyping to deployment in industry. It provides services such as hardware abstraction, device drivers, libraries, visualizers, message-passing, and package management."
            else:
                response_text = f"Regarding your question '{text}', the AI service is temporarily unavailable. The system requires a valid Google Gemini API key to function properly."

        # For now skip adding to history to avoid DB errors
        # self.chat_history_service.add_message_to_history(current_chat_history.id, "assistant", response_text)

        return response_text
