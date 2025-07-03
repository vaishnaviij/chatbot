import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminDashboard.css';

const AdminDashboard = ({ admin, onLogout }) => {
  const navigate = useNavigate();

  if (!admin) {
    navigate('/login');
    return null;
  }

  return (
    <div className="admin-dashboard-container">
      <header className="admin-dashboard-header">
        <div className="header-content">
          <h1>Admin Dashboard</h1>
          <button onClick={onLogout} className="logout-button">
            Logout
          </button>
        </div>
      </header>

      <main className="admin-dashboard-content">
        <div className="admin-stats">
          <h2>Welcome, {admin.username}</h2>
           
        </div>

        <div className="admin-actions">
          <button 
            className="admin-button" 
            onClick={() => navigate('/admin/users')}
          >
            Manage Users
          </button>
          <button 
            className="admin-button" 
            onClick={() => navigate('/admin/careers')}
          >
            Manage Careers
          </button>
          {admin.is_super_admin && (
            <button 
              className="admin-button" 
              onClick={() => navigate('/admin/admins')}
            >
              Manage Admins
            </button>
          )}
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;