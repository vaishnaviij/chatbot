// import React, { useState, useEffect } from 'react';
// import axios from 'axios';

// const AdminPanel = ({ currentUser }) => {
//   const [users, setUsers] = useState([]);
//   const [careers, setCareers] = useState([]);
//   const [activeTab, setActiveTab] = useState('users');
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState('');
//   const [newCareer, setNewCareer] = useState({
//     title: '',
//     description: '',
//     required_skills: '',
//     personality_fit: '',
//     education_paths: '',
//     avg_salary_range: { entry: '', senior: '' }
//   });

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         setLoading(true);
//         if (activeTab === 'users') {
//           const usersResponse = await axios.get(`/api/admin/users?username=${currentUser.username}`);
//           if (usersResponse.data.success) {
//             setUsers(usersResponse.data.users);
//           }
//         } else {
//           const careersResponse = await axios.get(`/api/admin/careers?username=${currentUser.username}`);
//           if (careersResponse.data.success) {
//             setCareers(careersResponse.data.careers);
//           }
//         }
//       } catch (err) {
//         setError('Failed to fetch data');
//       } finally {
//         setLoading(false);
//       }
//     };

//     if (currentUser?.is_admin) {
//       fetchData();
//     }
//   }, [currentUser, activeTab]);

//   if (!currentUser?.is_admin) {
//     return <div className="unauthorized">You don't have admin privileges</div>;
//   }

//   const handleAddCareer = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await axios.post('/api/admin/careers', {
//         ...newCareer,
//         admin_username: currentUser.username,
//         required_skills: newCareer.required_skills.split(',').map(s => s.trim()),
//         personality_fit: newCareer.personality_fit.split(',').map(s => s.trim()),
//         education_paths: newCareer.education_paths.split(',').map(s => s.trim())
//       });
      
//       if (response.data.success) {
//         setCareers([...careers, {
//           ...newCareer,
//           _id: response.data.id // Assuming your API returns the new ID
//         }]);
//         setNewCareer({
//           title: '',
//           description: '',
//           required_skills: '',
//           personality_fit: '',
//           education_paths: '',
//           avg_salary_range: { entry: '', senior: '' }
//         });
//       }
//     } catch (err) {
//       setError('Failed to add career');
//     }
//   };

//   const handleDeleteCareer = async (careerId) => {
//     try {
//       const response = await axios.delete(`/api/admin/careers/${careerId}`, {
//         data: { admin_username: currentUser.username }
//       });
      
//       if (response.data.success) {
//         setCareers(careers.filter(c => c._id !== careerId));
//       }
//     } catch (err) {
//       setError('Failed to delete career');
//     }
//   };

//   if (loading) return <div>Loading...</div>;
//   if (error) return <div>Error: {error}</div>;

//   return (
//     <div className="admin-panel">
//       <h2>Admin Dashboard</h2>
      
//       <div className="admin-tabs">
//         <button 
//           className={activeTab === 'users' ? 'active' : ''}
//           onClick={() => setActiveTab('users')}
//         >
//           User Management
//         </button>
//         <button 
//           className={activeTab === 'careers' ? 'active' : ''}
//           onClick={() => setActiveTab('careers')}
//         >
//           Career Management
//         </button>
//       </div>
      
//       {activeTab === 'users' && (
//         <div className="users-management">
//           <h3>User Management</h3>
//           <div className="stats">
//             <p>Total Users: {users.length}</p>
//           </div>
          
//           <table className="users-table">
//             <thead>
//               <tr>
//                 <th>Username</th>
//                 <th>Email</th>
//                 <th>Joined</th>
//                 <th>Last Login</th>
//                 <th>Admin</th>
//                 <th>Actions</th>
//               </tr>
//             </thead>
//             <tbody>
//               {users.map(user => (
//                 <tr key={user._id}>
//                   <td>{user.username}</td>
//                   <td>{user.email}</td>
//                   <td>{new Date(user.created_at).toLocaleDateString()}</td>
//                   <td>{user.last_login ? new Date(user.last_login).toLocaleString() : 'Never'}</td>
//                   <td>{user.is_admin ? 'Yes' : 'No'}</td>
//                   <td>
//                     {!user.is_admin && (
//                       <>
//                         <button 
//                           onClick={() => makeAdmin(user.username)}
//                           className="make-admin-btn"
//                         >
//                           Make Admin
//                         </button>
//                         <button 
//                           onClick={() => deleteUser(user._id)}
//                           className="delete-btn"
//                         >
//                           Delete
//                         </button>
//                       </>
//                     )}
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
      
//       {activeTab === 'careers' && (
//         <div className="careers-management">
//           <h3>Career Management</h3>
//           <div className="stats">
//             <p>Total Careers: {careers.length}</p>
//           </div>
          
//           <div className="add-career-form">
//             <h4>Add New Career</h4>
//             <form onSubmit={handleAddCareer}>
//               <div className="form-group">
//                 <label>Title:</label>
//                 <input
//                   type="text"
//                   value={newCareer.title}
//                   onChange={(e) => setNewCareer({...newCareer, title: e.target.value})}
//                   required
//                 />
//               </div>
              
//               <div className="form-group">
//                 <label>Description:</label>
//                 <textarea
//                   value={newCareer.description}
//                   onChange={(e) => setNewCareer({...newCareer, description: e.target.value})}
//                   required
//                 />
//               </div>
              
//               <div className="form-group">
//                 <label>Required Skills (comma separated):</label>
//                 <input
//                   type="text"
//                   value={newCareer.required_skills}
//                   onChange={(e) => setNewCareer({...newCareer, required_skills: e.target.value})}
//                   required
//                 />
//               </div>
              
//               <div className="form-group">
//                 <label>Personality Fit (comma separated):</label>
//                 <input
//                   type="text"
//                   value={newCareer.personality_fit}
//                   onChange={(e) => setNewCareer({...newCareer, personality_fit: e.target.value})}
//                   required
//                 />
//               </div>
              
//               <div className="form-group">
//                 <label>Education Paths (comma separated):</label>
//                 <input
//                   type="text"
//                   value={newCareer.education_paths}
//                   onChange={(e) => setNewCareer({...newCareer, education_paths: e.target.value})}
//                   required
//                 />
//               </div>
              
//               <div className="form-group">
//                 <label>Entry Salary:</label>
//                 <input
//                   type="text"
//                   value={newCareer.avg_salary_range.entry}
//                   onChange={(e) => setNewCareer({
//                     ...newCareer,
//                     avg_salary_range: {
//                       ...newCareer.avg_salary_range,
//                       entry: e.target.value
//                     }
//                   })}
//                   required
//                 />
//               </div>
              
//               <div className="form-group">
//                 <label>Senior Salary:</label>
//                 <input
//                   type="text"
//                   value={newCareer.avg_salary_range.senior}
//                   onChange={(e) => setNewCareer({
//                     ...newCareer,
//                     avg_salary_range: {
//                       ...newCareer.avg_salary_range,
//                       senior: e.target.value
//                     }
//                   })}
//                   required
//                 />
//               </div>
              
//               <button type="submit">Add Career</button>
//             </form>
//           </div>
          
//           <table className="careers-table">
//             <thead>
//               <tr>
//                 <th>Title</th>
//                 <th>Description</th>
//                 <th>Skills</th>
//                 <th>Actions</th>
//               </tr>
//             </thead>
//             <tbody>
//               {careers.map(career => (
//                 <tr key={career._id}>
//                   <td>{career.title}</td>
//                   <td>{career.description.substring(0, 100)}...</td>
//                   <td>{career.required_skills.join(', ')}</td>
//                   <td>
//                     <button className="edit-btn">Edit</button>
//                     <button 
//                       className="delete-btn"
//                       onClick={() => handleDeleteCareer(career._id)}
//                     >
//                       Delete
//                     </button>
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );

//   // Update the makeAdmin function to use the new endpoint
//   async function makeAdmin(username) {
//     try {
//       const response = await axios.post('/api/admin/grant-super', {
//         target_username: username,
//         requester_username: currentUser.username
//       });
      
//       if (response.data.success) {
//         setUsers(users.map(u => 
//           u.username === username ? {...u, is_super_admin: true} : u
//         ));
//       }
//     } catch (err) {
//       setError('Failed to grant admin privileges');
//     }
//   }
//   async function deleteUser(userId) {
//     try {
//       const response = await axios.delete(`/api/admin/users/${userId}`, {
//         data: { admin_username: currentUser.username }
//       });
      
//       if (response.data.success) {
//         setUsers(users.filter(u => u._id !== userId));
//       }
//     } catch (err) {
//       setError('Failed to delete user');
//     }
//   }
// };

// export default AdminPanel;


import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminPanel.css'; // Import the CSS file


const AdminPanel = ({ currentUser }) => {
  const [users, setUsers] = useState([]);
  const [careers, setCareers] = useState([]);
  const [activeTab, setActiveTab] = useState('users');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newCareer, setNewCareer] = useState({
    title: '',
    description: '',
    required_skills: '',
    personality_fit: '',
    education_paths: '',
    avg_salary_range: { entry: '', senior: '' }
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        if (activeTab === 'users') {
          const usersResponse = await axios.get('/api/admin/users', {
            params: { admin_username: currentUser.username }
          });
          
          if (usersResponse.data.success) {
            setUsers(usersResponse.data.users);
          } else {
            throw new Error(usersResponse.data.message || 'Failed to fetch users');
          }
        } else {
          const careersResponse = await axios.get('/api/admin/careers', {
            params: { admin_username: currentUser.username }
          });
          
          if (careersResponse.data.success) {
            setCareers(careersResponse.data.careers);
          } else {
            throw new Error(careersResponse.data.message || 'Failed to fetch careers');
          }
        }
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    if (currentUser?.is_admin) {
      fetchData();
    }
  }, [currentUser, activeTab]);

  if (!currentUser?.is_admin) {
    return <div className="unauthorized">You don't have admin privileges</div>;
  }

  const handleAddCareer = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/admin/careers', {
        ...newCareer,
        admin_username: currentUser.username,
        required_skills: newCareer.required_skills.split(',').map(s => s.trim()),
        personality_fit: newCareer.personality_fit.split(',').map(s => s.trim()),
        education_paths: newCareer.education_paths.split(',').map(s => s.trim())
      });
      
      if (response.data.success) {
        setCareers([...careers, {
          ...newCareer,
          _id: response.data.id,
          required_skills: newCareer.required_skills.split(',').map(s => s.trim())
        }]);
        setNewCareer({
          title: '',
          description: '',
          required_skills: '',
          personality_fit: '',
          education_paths: '',
          avg_salary_range: { entry: '', senior: '' }
        });
        setError('');
      } else {
        setError(response.data.message || 'Failed to add career');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to add career');
    }
  };

  const handleDeleteCareer = async (careerId) => {
    try {
      const response = await axios.delete(`/api/admin/careers/${careerId}`, {
        data: { admin_username: currentUser.username }
      });
      
      if (response.data.success) {
        setCareers(careers.filter(c => c._id !== careerId));
        setError('');
      } else {
        setError(response.data.message || 'Failed to delete career');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete career');
    }
  };

  const makeAdmin = async (username) => {
    try {
      const response = await axios.post('/api/admin/make-admin', {
        admin_username: currentUser.username,
        user_id: username
      });
      
      if (response.data.success) {
        setUsers(users.map(u => 
          u.username === username ? {...u, is_admin: true} : u
        ));
        setError('');
      } else {
        setError(response.data.message || 'Failed to make admin');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to make admin');
    }
  };

  const deleteUser = async (userId) => {
    try {
      const response = await axios.delete(`/api/admin/users/${userId}`, {
        data: { admin_username: currentUser.username }
      });
      
      if (response.data.success) {
        setUsers(users.filter(u => u._id !== userId));
        setError('');
      } else {
        setError(response.data.message || 'Failed to delete user');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete user');
    }
  };

  if (loading) {
    return (
      <div className="admin-panel">
        <div className="loading">
          <p>Loading admin dashboard...</p>
        </div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="admin-panel">
        <div className="error-message">
          <h3>An error occurred</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-panel">
      <h2>Admin Dashboard</h2>
      
      <div className="admin-tabs">
        <button 
          className={activeTab === 'users' ? 'active' : ''}
          onClick={() => setActiveTab('users')}
        >
          User Management
        </button>
        <button 
          className={activeTab === 'careers' ? 'active' : ''}
          onClick={() => setActiveTab('careers')}
        >
          Career Management
        </button>
      </div>
      
      {activeTab === 'users' && (
        <div className="users-management">
          <h3>User Management</h3>
          <div className="stats">
            <p>Total Users: {users.length}</p>
          </div>
          
          <table className="users-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Joined</th>
                <th>Admin</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user._id}>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td>{user.is_admin ? 'Yes' : 'No'}</td>
                  <td>
                    {!user.is_admin && (
                      <>
                        <button 
                          onClick={() => makeAdmin(user._id)}
                          className="make-admin-btn"
                        >
                          Make Admin
                        </button>
                        <button 
                          onClick={() => deleteUser(user._id)}
                          className="delete-btn"
                        >
                          Delete
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      
      {activeTab === 'careers' && (
        <div className="careers-management">
          <h3>Career Management</h3>
          <div className="stats">
            <p>Total Careers: {careers.length}</p>
          </div>
          
          <div className="add-career-form">
            <h4>Add New Career</h4>
            <form onSubmit={handleAddCareer}>
              <div className="form-group">
                <label>Title:</label>
                <input
                  type="text"
                  value={newCareer.title}
                  onChange={(e) => setNewCareer({...newCareer, title: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Description:</label>
                <textarea
                  value={newCareer.description}
                  onChange={(e) => setNewCareer({...newCareer, description: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Required Skills (comma separated):</label>
                <input
                  type="text"
                  value={newCareer.required_skills}
                  onChange={(e) => setNewCareer({...newCareer, required_skills: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Personality Fit (comma separated):</label>
                <input
                  type="text"
                  value={newCareer.personality_fit}
                  onChange={(e) => setNewCareer({...newCareer, personality_fit: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Education Paths (comma separated):</label>
                <input
                  type="text"
                  value={newCareer.education_paths}
                  onChange={(e) => setNewCareer({...newCareer, education_paths: e.target.value})}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Entry Salary:</label>
                <input
                  type="text"
                  value={newCareer.avg_salary_range.entry}
                  onChange={(e) => setNewCareer({
                    ...newCareer,
                    avg_salary_range: {
                      ...newCareer.avg_salary_range,
                      entry: e.target.value
                    }
                  })}
                  required
                />
              </div>
              
              <div className="form-group">
                <label>Senior Salary:</label>
                <input
                  type="text"
                  value={newCareer.avg_salary_range.senior}
                  onChange={(e) => setNewCareer({
                    ...newCareer,
                    avg_salary_range: {
                      ...newCareer.avg_salary_range,
                      senior: e.target.value
                    }
                  })}
                  required
                />
              </div>
              
              <button type="submit">Add Career</button>
            </form>
          </div>
          
          <table className="careers-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Skills</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {careers.map(career => (
                <tr key={career._id}>
                  <td>{career.title}</td>
                  <td>{career.description.substring(0, 100)}...</td>
                  <td>{career.required_skills.join(', ')}</td>
                  <td>
                    <button className="edit-btn">Edit</button>
                    <button 
                      className="delete-btn"
                      onClick={() => handleDeleteCareer(career._id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;