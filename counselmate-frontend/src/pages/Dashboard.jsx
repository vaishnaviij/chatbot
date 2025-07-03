import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import UserProfile from '../components/UserProfile';
import CareerSuggestions from '../components/CareerSuggestions';
import ChatInterface from '../components/ChatInterface';
import AdminPanel from '../components/AdminPanel';
import './Dashboard.css';

const Dashboard = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState(user?.is_admin ? 'admin' : 'profile');

  if (!user) {
    return (
      <div className="dashboard-container login-prompt">
        <div className="login-card">
          <p className="login-message">Please login to access your dashboard.</p>
          <Link to="/login" className="login-link">Go to Login</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-wrapper">
        <header className="dashboard-header">
          <div className="header-content">
            <h1 className="dashboard-title">
              Welcome {user.name} 
              {user.is_admin && <span className="admin-badge">Admin</span>}
            </h1>
            <button onClick={onLogout} className="logout-button">
              Logout
            </button>
          </div>
          
          <nav className="dashboard-nav">
            {user.is_admin && (
              <button
                className={`nav-item ${activeTab === 'admin' ? 'active' : ''}`}
                onClick={() => setActiveTab('admin')}
              >
                Admin Panel
              </button>
            )}
            <button
              className={`nav-item ${activeTab === 'profile' ? 'active' : ''}`}
              onClick={() => setActiveTab('profile')}
            >
              Profile
            </button>
            <button
              className={`nav-item ${activeTab === 'careers' ? 'active' : ''}`}
              onClick={() => setActiveTab('careers')}
            >
              Career Suggestions
            </button>
            <button
              className={`nav-item ${activeTab === 'chat' ? 'active' : ''}`}
              onClick={() => setActiveTab('chat')}
            >
              Chat with Counselor
            </button>
          </nav>
        </header>

        <main className="dashboard-content">
          {activeTab === 'admin' && <AdminPanel currentUser={user} />}
          {activeTab === 'profile' && <UserProfile user={user} onUpdate={() => window.location.reload()} />}
          {activeTab === 'careers' && <CareerSuggestions user={user} />}
          {activeTab === 'chat' && (
            <div className="chat-section">
              <ChatInterface user={user} />
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;