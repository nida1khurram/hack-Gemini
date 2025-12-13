import React, { useState, useCallback } from 'react';
import useAuth from '../hooks/useAuth';

import styles from './LoginForm.module.css';

const LoginForm: React.FC = () => {
  const auth = useAuth();
  const [isRegister, setIsRegister] = useState(false);

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
      setError('Invalid email or password.');
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
      setError('Registration failed. Email may already be in use.');
      console.error('Registration failed:', err);
    } finally {
      setLoading(false);
    }
  }, [email, password, username, auth]);


  if (auth.loading) {
    return <div className={styles.loading}>Loading...</div>;
  }
  
  if (auth.isAuthenticated) {
    return (
      <div className={styles.loginSuccess}>
        <p>You are logged in as {auth.user?.username || auth.user?.email}.</p>
        <button onClick={() => auth.logout()} className={styles.logoutButton}>
          Logout
        </button>
      </div>
    );
  }

  return (
    <div className={styles.loginFormContainer}>
      <div className={styles.tabs}>
        <button onClick={() => setIsRegister(false)} className={!isRegister ? styles.activeTab : ''}>Login</button>
        <button onClick={() => setIsRegister(true)} className={isRegister ? styles.activeTab : ''}>Register</button>
      </div>

      <form onSubmit={isRegister ? handleRegister : handleLogin} className={styles.loginForm}>
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
      </form>
    </div>
  );
};

export default LoginForm;