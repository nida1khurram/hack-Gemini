import React, { useState, useCallback } from 'react';
import axios from 'axios';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useAuth from '../hooks/useAuth'; // Adjust path if necessary

import styles from './LoginForm.module.css'; // Assuming you'll create this for styling

const LoginForm: React.FC = () => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000';
  const auth = useAuth();

  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback(async (event: React.FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Make a POST request to the backend's /auth/token endpoint
      const response = await axios.post(
        `${backendUrl}/auth/token`,
        new URLSearchParams({
          username: username,
          password: password,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      const { access_token } = response.data;
      auth.login(access_token); // Use the login function from useAuth hook
    } catch (err) {
      console.error('Login failed:', err);
      if (axios.isAxiosError(err) && err.response) {
        if (err.response.status === 401) {
          setError('Invalid username or password.');
        } else {
          setError(`Login failed: ${err.response.data.detail || err.message}`);
        }
      } else {
        setError('An unexpected error occurred during login.');
      }
    } finally {
      setLoading(false);
    }
  }, [username, password, backendUrl, auth]);

  if (auth.isAuthenticated) {
    return <div className={styles.loginSuccess}>You are already logged in as {auth.user?.username}.</div>;
  }

  return (
    <div className={styles.loginFormContainer}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} className={styles.loginForm}>
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
        <button type="submit" disabled={loading} className={styles.loginButton}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default LoginForm;
