import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ChatbotContextType {
  isGlobalChatbotAvailable: boolean;
  setIsGlobalChatbotAvailable: (available: boolean) => void;
}

const ChatbotContext = createContext<ChatbotContextType | undefined>(undefined);

export const ChatbotProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isGlobalChatbotAvailable, setIsGlobalChatbotAvailable] = useState(true);

  return (
    <ChatbotContext.Provider value={{ isGlobalChatbotAvailable, setIsGlobalChatbotAvailable }}>
      {children}
    </ChatbotContext.Provider>
  );
};

export const useChatbotContext = () => {
  const context = useContext(ChatbotContext);
  if (context === undefined) {
    throw new Error('useChatbotContext must be used within a ChatbotProvider');
  }
  return context;
};