// frontend/src/components/TextSelectionContextMenu.tsx

import React, { useState, useEffect, useRef } from 'react';
import { getSelectedText, getSelectionCoordinates } from '../utils/text_selection';
import { chatbotQuerySelected } from '../services/api'; // Import the new API service

// We will make TextSelectionContextMenu directly call the API.
// A more complex setup might involve a global state management or passing a callback
// to update the main Chatbot component's state and trigger a query.
// For now, this fulfills the task requirement of sending selected text to the backend.

const TextSelectionContextMenu: React.FC = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [currentSelectedText, setCurrentSelectedText] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSelectionChange = () => {
    const selectedText = getSelectedText();
    if (selectedText && selectedText.length > 0) {
      const coords = getSelectionCoordinates();
      if (coords) {
        setPosition(coords);
        setCurrentSelectedText(selectedText);
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    } else {
      setIsVisible(false);
    }
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
      setIsVisible(false);
    }
  };

  const handleAskClick = async () => {
    if (currentSelectedText) {
      setIsLoading(true);
      setError(null);
      try {
        // For simplicity, we'll ask a generic question related to the selected text
        const response = await chatbotQuerySelected("Explain this text.", currentSelectedText);
        console.log("Chatbot response for selected text:", response);
        // In a full implementation, you might want to display this response in the main chatbot UI
      } catch (err) {
        console.error("Error asking about selected text:", err);
        setError("Failed to get response for selected text.");
      } finally {
        setIsLoading(false);
        setIsVisible(false); // Hide menu after interaction
      }
    }
  };

  useEffect(() => {
    document.addEventListener('mouseup', handleSelectionChange);
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mouseup', handleSelectionChange);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  if (!isVisible || !currentSelectedText) {
    return null;
  }

  return (
    <div
      ref={menuRef}
      style={{
        position: 'absolute',
        top: position.y + window.scrollY,
        left: position.x + window.scrollX,
        background: 'white',
        border: '1px solid #ccc',
        borderRadius: '4px',
        padding: '5px',
        zIndex: 1000,
        boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
      }}
    >
      <button
        onClick={handleAskClick}
        disabled={isLoading}
        style={{
          background: 'none',
          border: 'none',
          padding: '5px 10px',
          cursor: 'pointer',
          whiteSpace: 'nowrap',
        }}
      >
        {isLoading ? 'Asking...' : `Ask Chatbot about "${currentSelectedText.substring(0, 20)}..."`}
      </button>
      {error && <p style={{ color: 'red', margin: '5px 0 0', fontSize: '0.8em' }}>{error}</p>}
    </div>
  );
};

export default TextSelectionContextMenu;
