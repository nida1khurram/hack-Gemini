// frontend/src/theme/Root.tsx - Updated to include global chatbot

import React from 'react';
import ChatbotProvider from '../components/ChatbotProvider';

// Root component with global chatbot toggle
function Root({children}) {
  return (
    <>
      {children}
      <ChatbotProvider />
    </>
  );
}

export default Root;
