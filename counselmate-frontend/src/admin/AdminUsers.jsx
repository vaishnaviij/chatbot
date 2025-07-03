import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AdminUsers = ({ admin, onLogout }) => {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (!admin) {
      navigate('/login');
      return;
    }

    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/admin/users', {
          params: { admin_username: admin.username }
        });
        
        if (!response.data.success) {
          throw new Error(response.data.message || 'Failed to fetch users');
        }

        setUsers(response.data.users);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to fetch users');
        console.error('Error fetching users:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [admin, navigate]);

  const filteredUsers = users.filter(user => {
    const username = user.username?.toLowerCase() || '';
    const email = user.email?.toLowerCase() || '';
    const search = searchTerm.toLowerCase();
    return username.includes(search) || email.includes(search);
  });

  const deleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    
    try {
      const response = await axios.delete(`/api/admin/users/${userId}`, {
        data: { admin_username: admin.username }
      });
      
      if (response.data.success) {
        setUsers(users.filter(user => user._id !== userId));
        setError('');
      } else {
        setError(response.data.message || 'Failed to delete user');
      }
    } catch (err) {
      const errorMsg = err.response?.data?.message || 
                     (err.response?.status === 403 ? 
                      'You do not have permission to delete this user' : 
                      'Failed to delete user');
      setError(errorMsg);
      console.error('Delete error:', err);
    }
  };

  if (!admin) return null;
  if (loading) return <div className="loading">Loading users...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="admin-page">
      <header className="admin-header">
        <h1>User Management</h1>
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
      </header>

      <main className="admin-content">
        <div className="user-controls">
          <input
            type="text"
            placeholder="Search users..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="user-list-container">
          <table className="user-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Joined</th>
                <th>Admin</th>
                {/* <th>Actions</th> */}
              </tr>
            </thead>
            <tbody>
              {filteredUsers.map(user => (
                <tr key={user._id}>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td>{user.is_admin ? 'Yes' : 'No'}</td>
                  <td className="actions">
                    {/* <button 
                      onClick={() => deleteUser(user._id)}
                      className="delete-btn"
                      disabled={user.is_admin && !admin.is_super_admin}
                    >
                      Delete
                    </button> */}
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

export default AdminUsers;