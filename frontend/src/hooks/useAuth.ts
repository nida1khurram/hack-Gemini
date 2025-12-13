import { useState, useEffect, useCallback } from 'react';
import { authService } from '../services/api';

interface UserProfile {
  id: string;
  username: string;
  email: string;
  background: 'beginner' | 'intermediate' | 'expert';
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
}

interface AuthState {
  isAuthenticated: boolean;
  user: UserProfile | null;
  loading: boolean;
  error: string | null;
  login: (email, password) => Promise<void>;
  register: (email, password, username) => Promise<void>;
  logout: () => void;
}

const useAuth = (): AuthState => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchUserProfile = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const currentUser = await authService.getCurrentUser();
      if (currentUser) {
        setUser(currentUser);
        setIsAuthenticated(true);
      } else {
        setIsAuthenticated(false);
        setUser(null);
        localStorage.removeItem('access_token');
      }
    } catch (err) {
      console.error('Failed to fetch user profile:', err);
      setError('Session expired. Please log in again.');
      setIsAuthenticated(false);
      setUser(null);
      localStorage.removeItem('access_token');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // On initial load, check for a token and fetch the user profile
    if (typeof window !== 'undefined' && localStorage.getItem('access_token')) {
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, [fetchUserProfile]);

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const data = await authService.login(email, password);
      localStorage.setItem('access_token', data.access_token);
      await fetchUserProfile(); // Fetch user profile after successful login
    } catch (err) {
      console.error('Login failed:', err);
      setError('Invalid email or password.');
      throw err; // Re-throw error to be caught in the component
    } finally {
      setLoading(false);
    }
  };
  
  const register = async (email, password, username) => {
    setLoading(true);
    setError(null);
    try {
      await authService.register(email, password, username);
      // After successful registration, log the user in
      await login(email, password);
    } catch (err) {
      console.error('Registration failed:', err);
      setError('Registration failed. Email may already be in use.');
      throw err; // Re-throw error
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await authService.logout();
    } catch (err) {
      console.error('Logout failed:', err);
    } finally {
      localStorage.removeItem('access_token');
      setIsAuthenticated(false);
      setUser(null);
    }
  };

  return {
    isAuthenticated,
    user,
    loading,
    error,
    login,
    register,
    logout,
  };
};

export default useAuth;