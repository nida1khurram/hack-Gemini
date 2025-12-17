import React from 'react';
import OriginalChatbot from './Chatbot';

// This component is used in MDX files and will be hidden when global chatbot is available
const InlineChatbot: React.FC = () => {
  // Since we now have a global floating chatbot, we hide the inline one
  return null; // This will hide the inline chatbot when global one is available
};

export default InlineChatbot;