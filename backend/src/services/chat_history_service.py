from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from ..models.chat_history import ChatHistory, ChatMessage

class ChatHistoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_chat_history(self, user_id: UUID) -> ChatHistory:
        chat_history = ChatHistory(user_id=user_id, messages='[]')
        self.db.add(chat_history)
        self.db.commit()
        self.db.refresh(chat_history)
        return chat_history

    def get_user_chat_histories(self, user_id: UUID) -> List[ChatHistory]:
        statement = select(ChatHistory).where(ChatHistory.user_id == user_id).order_by(ChatHistory.created_at.desc())
        result = self.db.execute(statement)
        return result.scalars().all()
    
    def get_chat_history_by_id(self, chat_history_id: UUID) -> Optional[ChatHistory]:
        statement = select(ChatHistory).where(ChatHistory.id == chat_history_id)
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def add_message_to_history(self, chat_history_id: UUID, role: str, content: str) -> Optional[ChatHistory]:
        import json
        chat_history = self.get_chat_history_by_id(chat_history_id)
        if chat_history:
            # Parse the JSON string to get the messages list
            messages_list = json.loads(chat_history.messages) if chat_history.messages else []
            # Add the new message to the list
            new_message = {"role": role, "content": content}
            messages_list.append(new_message)
            # Convert back to JSON string and update the field
            chat_history.messages = json.dumps(messages_list)

            self.db.add(chat_history) # Add to session to mark as dirty
            self.db.commit()
            self.db.refresh(chat_history)
        return chat_history
    
    def delete_chat_history(self, chat_history_id: UUID) -> bool:
        chat_history = self.get_chat_history_by_id(chat_history_id)
        if chat_history:
            self.db.delete(chat_history)
            self.db.commit()
            return True
        return False
