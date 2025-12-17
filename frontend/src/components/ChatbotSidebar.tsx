import React, { useState, useEffect, useRef } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { chatbotQuery } from '../services/api';
import './ChatbotSidebar.css';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatbotSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatbotSidebar: React.FC<ChatbotSidebarProps> = ({ isOpen, onClose }) => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000';
  console.log('ChatbotSidebar: Using backendUrl:', backendUrl);

  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const chatHistoryContainerRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of chat history when messages update
  useEffect(() => {
    if (chatHistoryContainerRef.current) {
      chatHistoryContainerRef.current.scrollTop = chatHistoryContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) {
      e.preventDefault();
    }
    processQuery();
  };

  const processQuery = async () => {
    if (!query.trim()) return;

    const userMessage: ChatMessage = { role: 'user', content: query };
    setChatHistory((prev) => [...prev, userMessage]);
    setQuery('');

    setLoading(true);
    setError('');

    try {
      const res = await chatbotQuery(userMessage.content, undefined); // No selected text for sidebar
      const assistantMessage: ChatMessage = { role: 'assistant', content: res.response };
      setChatHistory((prev) => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chatbot error:', err);
      setError('Failed to get response from chatbot.');
      setChatHistory((prev) => [...prev, { role: 'assistant', content: 'Error: Could not get a response.' }]);
    } finally {
      setLoading(false);
    }
  };

  // Handle Enter key press in the input field
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      processQuery();
    }
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="chatbot-sidebar-overlay" onClick={onClose}>
      <div className="chatbot-sidebar" onClick={(e) => e.stopPropagation()}>
        <div className="chatbot-header">
          <h3>AI Chatbot</h3>
          <button className="close-button" onClick={onClose} aria-label="Close chatbot">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div ref={chatHistoryContainerRef} className="chat-history-container">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`} style={{ textAlign: msg.role === 'user' ? 'right' : 'left' }}>
              <span className={`message-bubble ${msg.role}`}>
                {msg.content}
              </span>
            </div>
          ))}
        </div>

        <form className="chat-input-form" onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={handleQueryChange}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question..."
            className="chat-input"
            autoFocus
          />
          <button type="submit" disabled={loading} className="send-button">
            {loading ? 'Sending...' : 'Send'}
          </button>
        </form>

        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default ChatbotSidebar;