import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AdminAdmins = ({ admin, onLogout }) => {
  const navigate = useNavigate();
  const [admins, setAdmins] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (!admin || !admin.is_super_admin) {
      navigate('/login');
      return;
    }

    const fetchAdmins = async () => {
      try {
        const response = await axios.get('/api/admin/admins', {
          params: { admin_username: admin.username }
        });
        
        if (!response.data.success) {
          throw new Error(response.data.message || 'Failed to fetch admins');
        }

        setAdmins(response.data.admins);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to fetch admins');
        console.error('Error fetching admins:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAdmins();
  }, [admin, navigate]);

  const filteredAdmins = admins.filter(admin => {
    const username = admin.username?.toLowerCase() || '';
    const email = admin.email?.toLowerCase() || '';
    const search = searchTerm.toLowerCase();
    return username.includes(search) || email.includes(search);
  });

  const handleDemoteAdmin = async (adminId) => {
    if (!window.confirm('Are you sure you want to demote this admin to regular user?')) return;
    
    try {
      const response = await axios.post('/api/admin/demote-admin', {
        admin_username: admin.username,
        admin_id: adminId
      });
      
      if (response.data.success) {
        setAdmins(admins.filter(admin => admin._id !== adminId));
        setError('');
      } else {
        setError(response.data.message || 'Failed to demote admin');
      }
    } catch (err) {
      const errorMsg = err.response?.data?.message || 
                     (err.response?.status === 403 ? 
                      'You do not have permission to demote this admin' : 
                      'Failed to demote admin');
      setError(errorMsg);
      console.error('Demote error:', err);
    }
  };

  if (!admin || !admin.is_super_admin) return null;
  if (loading) return <div className="loading">Loading admins...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="admin-page">
      <header className="admin-header">
        <h1>Admin Management</h1>
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
      </header>

      <main className="admin-content">
        <div className="admin-controls">
          <input
            type="text"
            placeholder="Search admins..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="admin-list-container">
          <table className="admin-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Created At</th>
                <th>Role</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredAdmins.map(admin => (
                <tr key={admin._id}>
                  <td>{admin.username}</td>
                  <td>{admin.email}</td>
                  <td>{new Date(admin.created_at).toLocaleDateString()}</td>
                  <td>
                    {admin.is_super_admin ? 'Super Admin' : 'Admin'}
                  </td>
                  <td className="actions">
                    {!admin.is_super_admin && (
                      <button 
                        onClick={() => handleDemoteAdmin(admin._id)}
                        className="demote-btn"
                      >
                        Demote to User
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
};

export default AdminAdmins;