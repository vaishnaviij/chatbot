import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AdminCareers = ({ admin, onLogout }) => {
  const navigate = useNavigate();
  const [careers, setCareers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    if (!admin) {
      navigate('/login');
      return;
    }

    const fetchCareers = async () => {
      try {
        const response = await axios.get('/api/admin/careers', {
          params: { admin_username: admin.username }
        });
        
        if (!response.data.success) {
          throw new Error(response.data.message || 'Failed to fetch careers');
        }

        setCareers(response.data.careers);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to fetch careers');
        console.error('Error fetching careers:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCareers();
  }, [admin, navigate]);

  const filteredCareers = careers.filter(career => {
    const title = career.title?.toLowerCase() || '';
    const search = searchTerm.toLowerCase();
    return title.includes(search);
  });

  const handleDeleteCareer = async (careerId) => {
    if (!window.confirm('Are you sure you want to delete this career?')) return;
    
    try {
      const response = await axios.delete(`/api/admin/careers/${careerId}`, {
        data: { admin_username: admin.username }
      });
      
      if (response.data.success) {
        setCareers(careers.filter(career => career._id !== careerId));
        setError('');
      } else {
        setError(response.data.message || 'Failed to delete career');
      }
    } catch (err) {
      const errorMsg = err.response?.data?.message || 
                     (err.response?.status === 403 ? 
                      'You do not have permission to delete this career' : 
                      'Failed to delete career');
      setError(errorMsg);
      console.error('Delete error:', err);
    }
  };

  const handleEditCareer = (careerId) => {
    navigate(`/admin/careers/edit/${careerId}`);
  };

  if (!admin) return null;
  if (loading) return <div className="loading">Loading careers...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="admin-page">
      <header className="admin-header">
        <h1>Career Management</h1>
        <button onClick={onLogout} className="logout-button">
          Logout
        </button>
      </header>

      <main className="admin-content">
        <div className="career-controls">
          <input
            type="text"
            placeholder="Search careers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
          <button 
            onClick={() => navigate('/admin/careers/new')}
            className="add-career-button"
          >
            Add New Career
          </button>
        </div>

        <div className="career-list-container">
          <table className="career-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Required Skills</th>
                <th>Salary Range</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredCareers.map(career => (
                <tr key={career._id}>
                  <td>{career.title}</td>
                  <td>{career.description.substring(0, 50)}...</td>
                  <td>{career.required_skills?.join(', ') || 'N/A'}</td>
                  <td>
                    {career.avg_salary_range?.entry || 'N/A'} - 
                    {career.avg_salary_range?.senior || 'N/A'}
                  </td>
                  <td className="actions">
                    <button 
                      onClick={() => handleEditCareer(career._id)}
                      className="edit-btn"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDeleteCareer(career._id)}
                      className="delete-btn"
                    >
                      Delete
                    </button>
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

export default AdminCareers;