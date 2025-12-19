import React, { useState, useEffect } from 'react';
import './FloatingChatbotToggle.css';

interface FloatingChatbotToggleProps {
  onToggle: () => void;
  isOpen: boolean;
}

const FloatingChatbotToggle: React.FC<FloatingChatbotToggleProps> = ({ onToggle, isOpen }) => {
  const [isVisible, setIsVisible] = useState(false);

  // Show the toggle button after a short delay to avoid flashing on initial load
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 300); // 300ms delay to show the button after page load

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`floating-chatbot-toggle ${!isVisible ? 'hidden' : ''} ${isOpen ? 'open' : ''}`}>
      <button
        className="toggle-button"
        onClick={onToggle}
        aria-label={isOpen ? "Close chatbot" : "Open chatbot"}
        title={isOpen ? "Close chatbot" : "Open chatbot"}
      >
        {isOpen ? (
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        )}
      </button>
    </div>
  );
};

export default FloatingChatbotToggle;