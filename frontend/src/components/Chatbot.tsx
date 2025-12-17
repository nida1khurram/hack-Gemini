import React, { useState, useEffect, useRef } from 'react'; // Import useRef
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { chatbotQuery } from '../services/api'; // Import the API service without auth

interface ChatbotProps {
  selectedText?: string;
  hideWhenGlobalAvailable?: boolean; // New prop to control visibility when global chatbot is available
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

const Chatbot: React.FC<ChatbotProps> = ({ selectedText, hideWhenGlobalAvailable = false }) => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000';
  console.log('Chatbot: Using backendUrl:', backendUrl);

  // Check if we should hide this inline chatbot when global one is available
  if (hideWhenGlobalAvailable) {
    return null; // Don't render anything if global chatbot is available and we should hide
  }

  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]); // State for current conversation
  const chatHistoryContainerRef = useRef<HTMLDivElement>(null); // Ref for scrolling

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
      e.preventDefault(); // Prevent default form submission
    }
    processQuery();
  };

  const processQuery = async () => {
    if (!query.trim()) return; // Don't send empty queries

    const userMessage: ChatMessage = { role: 'user', content: query };
    setChatHistory((prev) => [...prev, userMessage]); // Add user message to history
    setQuery(''); // Clear input

    setLoading(true);
    setError('');

    try {
      const res = await chatbotQuery(userMessage.content, selectedText);
      const assistantMessage: ChatMessage = { role: 'assistant', content: res.response };
      setChatHistory((prev) => [...prev, assistantMessage]); // Add assistant response
    } catch (err) {
      console.error('Chatbot error:', err);
      setError('Failed to get response from chatbot.');
      setChatHistory((prev) => [...prev, { role: 'assistant', content: 'Error: Could not get a response.' }]); // Add error message to history
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px', margin: '20px 0', display: 'flex', flexDirection: 'column', height: '400px' }}>
      <h3>AI Chatbot</h3>
      {selectedText && (
        <div style={{ marginBottom: '10px', padding: '10px', background: '#f0f0f0', borderRadius: '5px' }}>
          <strong>Context:</strong> {selectedText}
        </div>
      )}
      <div ref={chatHistoryContainerRef} style={{ flexGrow: 1, overflowY: 'auto', marginBottom: '10px', paddingRight: '5px' }}>
        {chatHistory.map((msg, index) => (
          <div key={index} style={{ marginBottom: '5px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
            <span style={{
              display: 'inline-block',
              padding: '8px 12px',
              borderRadius: '15px',
              maxWidth: '80%',
              background: msg.role === 'user' ? '#007bff' : '#e9e9e9',
              color: msg.role === 'user' ? 'white' : 'black',
            }}>
              {msg.content}
            </span>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault(); // Prevent form submission on Enter to avoid duplicate calls
              processQuery(); // Submit the query directly
            }
          }}
          placeholder="Ask a question..."
          style={{ width: 'calc(100% - 80px)', marginRight: '10px', padding: '8px' }}
        />
        <button type="submit" disabled={loading} style={{ padding: '8px 15px' }}>
          {loading ? 'Sending...' : 'Ask'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default Chatbot;