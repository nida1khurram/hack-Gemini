import React from 'react';
import useAuth from '../hooks/useAuth';

interface ConditionalContentProps {
  allowedBackgrounds: ('beginner' | 'intermediate' | 'expert')[];
  children: React.ReactNode;
}

const ConditionalContent: React.FC<ConditionalContentProps> = ({ allowedBackgrounds, children }) => {
  const { user, loading: authLoading } = useAuth();

  if (authLoading) {
    return <p>Loading personalized content...</p>;
  }

  if (!user || !allowedBackgrounds.includes(user.background)) {
    return null; // Don't render if user is not authenticated or background not allowed
  }

  return <>{children}</>;
};

export default ConditionalContent;
