import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

interface UserProfile {
  id: string;
  username: string;
  email: string;
  background: 'beginner' | 'intermediate' | 'expert';
}

interface AuthState {
  isAuthenticated: boolean;
  user: UserProfile | null;
  loading: boolean;
  error: string | null;
  login: (token: string) => void;
  logout: () => void;
  fetchUserProfile: () => void;
}

const useAuth = (): AuthState => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000';

  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const setAuthData = useCallback((token: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
    setIsAuthenticated(true);
    // Fetch user profile immediately after login
    fetchUserProfile();
  }, [fetchUserProfile]);

  const clearAuthData = useCallback(() => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    setIsAuthenticated(false);
    setUser(null);
  }, []);

  const fetchUserProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let token = null;
      if (typeof window !== 'undefined') {
        token = localStorage.getItem('access_token');
      }
      if (!token) {
        clearAuthData();
        return;
      }
      const response = await axios.get(`${backendUrl}/user/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (err) {
      console.error('Failed to fetch user profile:', err);
      setError('Failed to fetch user profile.');
      clearAuthData();
    } finally {
      setLoading(false);
    }
  }, [backendUrl, clearAuthData]);

  useEffect(() => {
    fetchUserProfile();
  }, [fetchUserProfile]);

  const login = (token: string) => {
    setAuthData(token);
  };

  const logout = () => {
    clearAuthData();
  };

  return {
    isAuthenticated,
    user,
    loading,
    error,
    login,
    logout,
    fetchUserProfile,
  };
};

export default useAuth;
