

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '@google/model-viewer';
import './Login.css'; 


const Login = ({ onLogin, onAdminLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isAdminLogin, setIsAdminLogin] = useState(false);
  const [modelLoadError, setModelLoadError] = useState(false);
  const navigate = useNavigate();

  const handleModelError = () => {
    console.error('Failed to load 3D model');
    setModelLoadError(true);
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      if (isLogin) {
        const endpoint = isAdminLogin ? '/api/admin/auth/login' : '/api/auth/login';
        
        const requestData = isAdminLogin 
          ? { username, password }
          : { identifier: username, password };
        
        const response = await axios.post(endpoint, requestData);
        
        if (response.data.success) {
          if (isAdminLogin) {
            onAdminLogin(response.data.admin);
            navigate('/admin');
          } else {
            onLogin(response.data.user);
            navigate('/dashboard');
          }
        } else {
          setError(response.data.message || 'Invalid credentials');
        }
      } else {
        if (isAdminLogin) {
          setError('Admin registration is not allowed here');
          return;
        }
        
        const response = await axios.post('/api/auth/register', {
          username,
          email,
          password
        });
        
        if (response.data.success) {
          setError('Registration successful! Please login.');
          setIsLogin(true);
          setUsername('');
          setPassword('');
        } else {
          setError(response.data.message || 'Registration failed');
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="welcome-section">
        <div className="welcome-image-container">
          {modelLoadError ? (
            <div className="model-error-fallback">
              <p>Unable to load 3D model</p>
            </div>
          ) : (
            <model-viewer 
              src="/bot.glb"  // Use public folder path
              alt="3D Robot" 
              auto-rotate 
              camera-controls 
              style={{ 
                width: '100%', 
                maxWidth: '500px', 
                height: '400px' 
              }}
              loading="eager"
              exposure="0.5"
              shadow-intensity="1"
              ar
              ar-modes="webxr scene-viewer quick-look"
              onError={handleModelError}
            >
              <div slot="error" className="model-error-fallback">
                <p>Failed to load 3D model</p>
              </div>
            </model-viewer>
          )}
        </div>
      </div>

      <div className="login-section">
        <div className="login-content">
          <div className="login-header">
            <h2>{isLogin ? (isAdminLogin ? 'Admin Login' : 'Welcome Back') : 'Create Account'}</h2>
            <p className="subtitle">
              {isLogin 
                ? (isAdminLogin 
                    ? 'Enter your admin credentials' 
                    : 'Sign in to continue to your account')
                : 'Join our platform today'}
            </p>
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          <div className="login-type-toggle">
            <button 
              type="button"
              className={!isAdminLogin ? 'active' : ''}
              onClick={() => setIsAdminLogin(false)}
            >
              User Login
            </button>
            <button 
              type="button"
              className={isAdminLogin ? 'active' : ''}
              onClick={() => setIsAdminLogin(true)}
            >
              Admin Login
            </button>
          </div>
          
          <form onSubmit={handleSubmit}>
            {!isLogin && !isAdminLogin && (
              <div className="form-group">
                <label>Email Address</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="Enter your email"
                />
              </div>
            )}
            
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                placeholder="Choose a username"
              />
            </div>
            
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength="6"
                placeholder="Enter your password"
              />
            </div>
            
            <button 
              type="submit" 
              disabled={isLoading}
              className="submit-btn"
            >
              {isLoading ? 'Processing...' : isLogin ? 'Sign In' : 'Register'}
            </button>
          </form>
          
          {!isAdminLogin && (
            <div className="toggle-mode">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button 
                type="button" 
                onClick={() => {
                  setIsLogin(!isLogin);
                  setError('');
                }}
              >
                {isLogin ? 'Register' : 'Login'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Login;