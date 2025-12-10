import React, { useState, useEffect, useRef } from 'react'; // Import useRef
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useAuth from '../hooks/useAuth'; // Import useAuth hook
import { chatbotQuery, getChatHistory } from '../services/api'; // Import the new API service

interface ChatbotProps {
  selectedText?: string;
}

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatHistoryEntry {
  id: string;
  messages: string | ChatMessage[]; // Can be JSON string or array
}

const Chatbot: React.FC<ChatbotProps> = ({ selectedText }) => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000';
  console.log('Chatbot: Using backendUrl:', backendUrl);

  const { isAuthenticated, loading: authLoading, error: authError, fetchUserProfile } = useAuth(); // Use the auth hook
  console.log('Chatbot: isAuthenticated:', isAuthenticated, 'authLoading:', authLoading);

  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]); // State for current conversation
  const chatHistoryContainerRef = useRef<HTMLDivElement>(null); // Ref for scrolling

  // Fetch chat history on component mount or auth status change
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const histories: ChatHistoryEntry[] = await getChatHistory();
        if (histories && histories.length > 0) {
          // Assuming we display the most recent conversation
          let messages = histories[0].messages;

          // If messages is a string (JSON), parse it to get the array
          if (typeof messages === 'string') {
            try {
              messages = JSON.parse(messages);
            } catch (e) {
              console.error('Failed to parse chat history messages:', e);
              messages = []; // Fallback to empty array
            }
          }

          setChatHistory(messages);
        }
      } catch (err) {
        console.error('Failed to fetch chat history:', err);
        setError('Failed to load chat history.');
      }
    };

    if (isAuthenticated) {
      fetchHistory();
    } else {
      setChatHistory([]); // Clear history if not authenticated
    }
  }, [isAuthenticated]);

  // Scroll to bottom of chat history when messages update
  useEffect(() => {
    if (chatHistoryContainerRef.current) {
      chatHistoryContainerRef.current.scrollTop = chatHistoryContainerRef.current.scrollHeight;
    }
  }, [chatHistory]);


  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevent default form submission
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
      if (err instanceof Error && err.message.includes('Authentication token not found')) {
        setError('Please log in to use the chatbot.');
      }
      setChatHistory((prev) => [...prev, { role: 'assistant', content: 'Error: Could not get a response.' }]); // Add error message to history
    } finally {
      setLoading(false);
    }
  };

  if (authLoading) {
    console.log('Chatbot: Rendering loading authentication message.'); // Debug log
    return <div style={{ margin: '20px 0', padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>Loading authentication...</div>;
  }

  if (!isAuthenticated) {
    console.log('Chatbot: Rendering "Please log in" message.'); // Debug log
    return (
      <div style={{ margin: '20px 0', padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
        <h3>AI Chatbot</h3>
        <p>Please <a href="/docs/login">log in</a> to use the chatbot functionality.</p> {/* TODO: Create a login page */}
        {authError && <p style={{ color: 'red' }}>{authError}</p>}
      </div>
    );
  }

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
      <div>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSubmit();
            }
          }}
          placeholder="Ask a question..."
          style={{ width: 'calc(100% - 80px)', marginRight: '10px', padding: '8px' }}
        />
        <button onClick={handleSubmit} disabled={loading} style={{ padding: '8px 15px' }}>
          {loading ? 'Sending...' : 'Ask'}
        </button>
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default Chatbot;