import axios from 'axios';
import { getSession } from 'next-auth/react'; // Import getSession for Auth.js client-side

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
  return 'http://localhost:8000'; // Default Python backend port
};

const NODE_API_URL = getNodeBackendUrl();
const PYTHON_API_URL = getPythonBackendUrl();

// Removed Authentication Service for Node.js Auth.js
// Auth.js provides client-side helper functions (signIn, signOut, getSession)
// So manual axios calls for auth are not needed here.
// export const authService = { ... }


// Helper function to get the JWT from the Auth.js session
const getAuthToken = async (): Promise<string | null> => {
  const session = await getSession();
  if (session && session.jwt) { // Assuming the JWT is stored in session.jwt
    return session.jwt as string;
  }
  return null;
};


// Existing API functions (now pointing to Python backend and using Auth.js session token)
export const chatbotQuery = async (query: string, context?: string) => {
  const token = await getAuthToken(); // Get JWT from Auth.js session
  if (!token) {
    throw new Error('Authentication token not found. Please log in.');
  }

  const response = await axios.post(`${PYTHON_API_URL}/chatbot/query`, { query, context }, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const chatbotQuerySelected = async (query: string, selectedText: string) => {
  const token = await getAuthToken(); // Get JWT from Auth.js session
  if (!token) {
    throw new Error('Authentication token not found. Please log in.');
  }

  const response = await axios.post(`${PYTHON_API_URL}/chatbot/selected`, { query, context: selectedText }, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const getChatHistory = async () => {
  const token = await getAuthToken(); // Get JWT from Auth.js session
  if (!token) {
    throw new Error('Authentication token not found. Please log in.');
  }

  const response = await axios.get(`${PYTHON_API_URL}/chat/history`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};
