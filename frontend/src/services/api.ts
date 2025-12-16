import axios from 'axios';

// For Docusaurus, we need to handle the backend URL differently
// Since process.env is not available in the browser, we'll use a global variable
// that can be set during the build process or fall back to a default
declare global {
  var NODE_BACKEND_URL: string; // New variable for Node.js backend
  var PYTHON_BACKEND_URL: string; // Existing Python backend
}

// Get backend URLs
const getNodeBackendUrl = () => {
  if (typeof window !== 'undefined' && (window as any).NODE_BACKEND_URL) {
    return (window as any).NODE_BACKEND_URL;
  }
  return 'http://localhost:3001'; // Default Node.js backend port
};

const getPythonBackendUrl = () => {
  if (typeof window !== 'undefined' && (window as any).PYTHON_BACKEND_URL) {
    return (window as any).PYTHON_BACKEND_URL;
  }
  return 'http://localhost:8003'; // Default Python backend port
};

const PYTHON_API_URL = getPythonBackendUrl();

// API functions without authentication
export const chatbotQuery = async (query: string, context?: string) => {
  const response = await axios.post(`${PYTHON_API_URL}/chatbot/query`, { query, context });
  return response.data;
};

export const chatbotQuerySelected = async (query: string, selectedText: string) => {
  const response = await axios.post(`${PYTHON_API_URL}/chatbot/selected`, { query, context: selectedText });
  return response.data;
};

export const getChatHistory = async () => {
  const response = await axios.get(`${PYTHON_API_URL}/chat/history`);
  return response.data;
};
