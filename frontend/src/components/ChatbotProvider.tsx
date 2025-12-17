import React, { useState } from 'react';
import FloatingChatbotToggle from './FloatingChatbotToggle';
import ChatbotSidebar from './ChatbotSidebar';

const ChatbotProvider: React.FC = () => {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  const handleToggle = () => {
    setIsChatbotOpen(!isChatbotOpen);
  };

  const handleClose = () => {
    setIsChatbotOpen(false);
  };

  return (
    <>
      <FloatingChatbotToggle
        onToggle={handleToggle}
        isOpen={isChatbotOpen}
      />
      <ChatbotSidebar
        isOpen={isChatbotOpen}
        onClose={handleClose}
      />
    </>
  );
};

export default ChatbotProvider;