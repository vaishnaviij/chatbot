import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import AdminUsers from './admin/AdminUsers';
import AdminCareers from './admin/AdminCareers';
import AdminAdmins from './admin/AdminAdmins';
import './styles.css';

// Protected route component for admin routes
const ProtectedAdminRoute = ({ admin, children }) => {
  if (!admin) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  const [user, setUser] = useState(null);
  const [admin, setAdmin] = useState(null);

  useEffect(() => {
    // Check if user is logged in from localStorage
    const savedUser = localStorage.getItem('counselmate_user');
    const savedAdmin = localStorage.getItem('counselmate_admin');
    if (savedUser) setUser(JSON.parse(savedUser));
    if (savedAdmin) setAdmin(JSON.parse(savedAdmin));
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('counselmate_user', JSON.stringify(userData));
  };

  const handleAdminLogin = (adminData) => {
    setAdmin(adminData);
    localStorage.setItem('counselmate_admin', JSON.stringify(adminData));
  };

  const handleLogout = () => {
    setUser(null);
    setAdmin(null);
    localStorage.removeItem('counselmate_user');
    localStorage.removeItem('counselmate_admin');
  };

  return (
    <Router>
      <div className="app">
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Home user={user} admin={admin} onLogout={handleLogout} />} />
          <Route path="/login" element={<Login onLogin={handleLogin} onAdminLogin={handleAdminLogin} />} />
          
          {/* User Dashboard */}
          <Route 
            path="/dashboard" 
            element={
              user ? <Dashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" replace />
            } 
          />
          
          {/* Admin Routes */}
          <Route 
            path="/admin" 
            element={
              <ProtectedAdminRoute admin={admin}>
                <AdminDashboard admin={admin} onLogout={handleLogout} />
              </ProtectedAdminRoute>
            } 
          />
          <Route 
            path="/admin/users" 
            element={
              <ProtectedAdminRoute admin={admin}>
                <AdminUsers admin={admin} onLogout={handleLogout} />
              </ProtectedAdminRoute>
            } 
          />
          <Route 
            path="/admin/careers" 
            element={
              <ProtectedAdminRoute admin={admin}>
                <AdminCareers admin={admin} onLogout={handleLogout} />
              </ProtectedAdminRoute>
            } 
          />
          <Route 
            path="/admin/admins" 
            element={
              <ProtectedAdminRoute admin={admin}>
                {admin?.is_super_admin ? (
                  <AdminAdmins admin={admin} onLogout={handleLogout} />
                ) : (
                  <Navigate to="/admin" replace />
                )}
              </ProtectedAdminRoute>
            } 
          />
          
          {/* Catch-all route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;