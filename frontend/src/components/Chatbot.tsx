import React, { useState } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import axios from 'axios'; // Assuming axios is installed

interface ChatbotProps {
  selectedText?: string;
}

const Chatbot: React.FC<ChatbotProps> = ({ selectedText }) => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000'; // Fallback to localhost

  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleQueryChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setQuery(event.target.value);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    setResponse('');
    try {
      const token = localStorage.getItem('access_token'); // Assuming token is stored in localStorage
      if (!token) {
        setError('Please log in to use the chatbot.');
        setLoading(false);
        return;
      }

      const res = await axios.post(
        `${backendUrl}/chatbot/query`,
        { query, context: selectedText },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setResponse(res.data.response);
    } catch (err) {
      console.error('Chatbot error:', err);
      setError('Failed to get response from chatbot.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px', margin: '20px 0' }}>
      <h3>AI Chatbot</h3>
      {selectedText && (
        <div style={{ marginBottom: '10px', padding: '10px', background: '#f0f0f0', borderRadius: '5px' }}>
          <strong>Context:</strong> {selectedText}
        </div>
      )}
      <div>
        <input
          type="text"
          value={query}
          onChange={handleQueryChange}
          placeholder="Ask a question..."
          style={{ width: 'calc(100% - 80px)', marginRight: '10px', padding: '8px' }}
        />
        <button onClick={handleSubmit} disabled={loading} style={{ padding: '8px 15px' }}>
          {loading ? 'Sending...' : 'Ask'}
        </button>
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {response && (
        <div style={{ marginTop: '15px', padding: '10px', background: '#e9e9e9', borderRadius: '5px' }}>
          <strong>Response:</strong> {response}
        </div>
      )}
    </div>
  );
};

export default Chatbot;
