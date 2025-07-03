import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { color } from 'framer-motion';

const CareerSuggestions = ({ user }) => {
  const [careers, setCareers] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      fetchCareerSuggestions();
    }
  }, [user]);

  const fetchCareerSuggestions = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await axios.post('/api/careers/suggest', {
        interests: user.interests || [],
        skills: user.skills || [],
        education: user.education_level || null
      });
      
      if (response.data.success) {
        setCareers(response.data.careers);
      } else {
        setError(response.data.message || 'Failed to fetch career suggestions');
      }
    } catch (err) {
      console.error('Error fetching career suggestions:', err);
      setError(err.response?.data?.message || 
               'Error fetching career suggestions. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div className="career-suggestions">
      <h2 style={{ color: 'black' }}>Career Suggestions</h2>
      <p>Based on your profile, here are some careers you might consider:</p>
      
      {isLoading ? (
        <div className="loading">Loading suggestions...</div>
      ) : error ? (
        <div className="error">{error}</div>
      ) : careers.length === 0 ? (
        <div className="no-results">
          No suggestions yet. Please update your profile with more information about your interests and skills.
        </div>
      ) : (
        <div className="careers-list">
          {careers.map((career, index) => (
            <div key={index} className="career-card">
              <h3 style={{ color: 'black' }}>{career.title}</h3>
              <p>{career.description}</p>
              
              <div className="career-details">
                <div className="detail">
                  <strong>Required Skills:</strong>
                  <ul>
                    {career.required_skills.slice(0, 3).map((skill, i) => (
                      <li key={i}>{skill}</li>
                    ))}
                  </ul>
                </div>
                
                <div className="detail">
                  <strong>Education Paths:</strong>
                  <ul>
                    {career.education_paths.slice(0, 2).map((path, i) => (
                      <li key={i}>{path}</li>
                    ))}
                  </ul>
                </div>
                
                <div className="detail">
                  <strong>Salary Range:</strong>
                  <p>{career.avg_salary_range?.entry || 'N/A'} - {career.avg_salary_range?.senior || 'N/A'}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CareerSuggestions;