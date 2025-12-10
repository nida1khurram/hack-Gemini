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
  login: (accessToken: string, refreshToken: string) => void;
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

  const setAuthData = useCallback((accessToken: string, refreshToken: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('refresh_token', refreshToken); // Store refresh token
    }
    setIsAuthenticated(true);
    // User profile will be fetched by useEffect when isAuthenticated becomes true
  }, []); // Removed fetchUserProfile from dependencies

  const clearAuthData = useCallback(() => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token'); // Clear refresh token
    }
    setIsAuthenticated(false);
    setUser(null);
  }, []);

  const fetchUserProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let accessToken = null;
      if (typeof window !== 'undefined') {
        accessToken = localStorage.getItem('access_token');
      }
      if (!accessToken) {
        clearAuthData();
        return;
      }
      const response = await axios.get(`${backendUrl}/user/profile`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        // Access token expired, try to refresh
        const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;
        if (refreshToken) {
          try {
            const refreshResponse = await axios.post(`${backendUrl}/auth/refresh`, {}, {
              headers: {
                Authorization: `Bearer ${refreshToken}`,
              },
            });
            const newAccessToken = refreshResponse.data.access_token;
            const newRefreshToken = refreshResponse.data.refresh_token;
            if (typeof window !== 'undefined') {
              localStorage.setItem('access_token', newAccessToken);
              localStorage.setItem('refresh_token', newRefreshToken);
            }
            // Retry fetching user profile with new access token
            await fetchUserProfile(); // Recursive call, but should resolve with new token
            return;
          } catch (refreshErr) {
            console.error('Failed to refresh token:', refreshErr);
            setError('Session expired. Please log in again.');
            clearAuthData();
          }
        } else {
          setError('Session expired. Please log in again.');
          clearAuthData();
        }
      } else {
        console.error('Failed to fetch user profile:', err);
        setError('Failed to fetch user profile.');
        clearAuthData();
      }
    } finally {
      setLoading(false);
    }
  }, [backendUrl, clearAuthData]);

  useEffect(() => {
    // Only fetch user profile if authenticated or if tokens exist on initial load
    if (isAuthenticated || (typeof window !== 'undefined' && localStorage.getItem('access_token'))) {
      fetchUserProfile();
    }
  }, [isAuthenticated, fetchUserProfile]); // Added isAuthenticated to dependency array

  const login = (accessToken: string, refreshToken: string) => {
    setAuthData(accessToken, refreshToken);
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
