import axios from 'axios';

// For Docusaurus, we need to handle the backend URL differently
// Since process.env is not available in the browser, we'll use a global variable
// that can be set during the build process or fall back to a default
declare global {
  var BACKEND_URL: string;
}

// Get backend URL - first try global, then fallback
const getBackendUrl = () => {
  // In Docusaurus, we can set this via the config
  if (typeof window !== 'undefined' && (window as any).BACKEND_URL) {
    return (window as any).BACKEND_URL;
  }
  // For development, fallback to default
  return 'http://localhost:8000';
};

const API_URL = getBackendUrl();

export const chatbotQuery = async (query: string, context?: string) => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Authentication token not found. Please log in.');
  }

  const response = await axios.post(`${API_URL}/chatbot/query`, { query, context }, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const chatbotQuerySelected = async (query: string, selectedText: string) => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Authentication token not found. Please log in.');
  }

  const response = await axios.post(`${API_URL}/chatbot/selected`, { query, context: selectedText }, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const getChatHistory = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    throw new Error('Authentication token not found. Please log in.');
  }

  const response = await axios.get(`${API_URL}/chat/history`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

// Add other API functions here as needed
