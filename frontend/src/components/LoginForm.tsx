import React, { useState, useCallback } from 'react';
import useAuth from '../hooks/useAuth';
import { signIn } from 'next-auth/react'; // For social login redirects

import styles from './LoginForm.module.css';

const LoginForm: React.FC = () => {
  const auth = useAuth();
  const [isRegister, setIsRegister] = useState(false); // Keep for now for UI toggle

  // Form state
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [username, setUsername] = useState<string>(''); // For registration
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleLogin = useCallback(async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await auth.login(email, password);
    } catch (err) {
      setError(err.message || 'Login failed.');
      console.error('Login failed:', err);
    } finally {
      setLoading(false);
    }
  }, [email, password, auth]);
  
  const handleRegister = useCallback(async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await auth.register(email, password, username);
    } catch (err) {
      setError(err.message || 'Registration failed.');
      console.error('Registration failed:', err);
    } finally {
      setLoading(false);
    }
  }, [email, password, username, auth]);

  const handleGoogleLogin = useCallback(() => {
    signIn('google', { callbackUrl: '/' }); // Redirect to homepage after login
  }, []);

  const handleGitHubLogin = useCallback(() => {
    signIn('github', { callbackUrl: '/' }); // Redirect to homepage after login
  }, []);

  const switchForm = () => {
    setIsRegister(!isRegister);
    setError(null);
  };

  if (auth.loading) {
    return <div className={styles.loading}>Loading...</div>;
  }
  
  if (auth.isAuthenticated) {
    return (
      <div className={styles.loginSuccess}>
        <p>You are logged in as {auth.user?.name || auth.user?.email}.</p>
        <button onClick={() => auth.logout()} className={styles.logoutButton}>
          Logout
        </button>
      </div>
    );
  }

  return (
    <div className={styles.loginFormContainer}>
      <form onSubmit={isRegister ? handleRegister : handleLogin} className={styles.loginForm}>
        <h2>{isRegister ? 'Register' : 'Login'}</h2>
        
        {isRegister && (
          <div className={styles.formGroup}>
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
            />
          </div>
        )}
        <div className={styles.formGroup}>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        {error && <div className={styles.errorMessage}>{error}</div>}
        {auth.error && <div className={styles.errorMessage}>{auth.error}</div>}
        
        <button type="submit" disabled={loading} className={styles.loginButton}>
          {loading ? 'Processing...' : (isRegister ? 'Register' : 'Login')}
        </button>

        <div className={styles.socialLogin}>
            <button type="button" onClick={handleGoogleLogin} disabled={loading}>Login with Google</button>
            <button type="button" onClick={handleGitHubLogin} disabled={loading}>Login with GitHub</button>
        </div>

        <div className={styles.switchForm}>
          {isRegister ? (
            <p>Already have an account? <button type="button" onClick={switchForm}>Login</button></p>
          ) : (
            <p>Don't have an account? <button type="button" onClick={switchForm}>Register</button></p>
          )}
        </div>
      </form>
    </div>
  );
};

export default LoginForm;