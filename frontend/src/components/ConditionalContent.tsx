import React from 'react';

interface ConditionalContentProps {
  allowedBackgrounds: ('beginner' | 'intermediate' | 'expert')[];
  children: React.ReactNode;
}

const ConditionalContent: React.FC<ConditionalContentProps> = ({ allowedBackgrounds, children }) => {
  // For now, show content to all users (removed authentication requirement)
  // In the future, this could be based on user preferences or other non-auth factors
  return <>{children}</>;
};

export default ConditionalContent;
