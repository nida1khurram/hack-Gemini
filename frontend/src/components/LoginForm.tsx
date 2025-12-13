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
      setError('Registration failed. Email may already be in use. Please try logging in instead.');
      console.error('Registration failed:', err);
    } finally {
      setLoading(false);
    }
  }, [email, password, username, auth]);

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
        <p>You are logged in as {auth.user?.username || auth.user?.email}.</p>
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
