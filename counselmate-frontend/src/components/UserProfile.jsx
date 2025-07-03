import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserProfile = ({ user, onUpdate }) => {
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [education, setEducation] = useState(user?.education_level || '');
  const [interests, setInterests] = useState(user?.interests?.join(', ') || '');
  const [skills, setSkills] = useState(user?.skills?.join(', ') || '');
  const [isEditing, setIsEditing] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (user) {
      setName(user.name || '');
      setEmail(user.email || '');
      setEducation(user.education_level || '');
      setInterests(user.interests?.join(', ') || '');
      setSkills(user.skills?.join(', ') || '');
    }
  }, [user]);

  const handleSave = async () => {
    try {
      if (!user || !user._id) {
        throw new Error('User information is incomplete');
      }
      
      const updatedData = {
        name,
        email,
        education_level: education,
        interests: interests.split(',').map(i => i.trim()).filter(i => i),
        skills: skills.split(',').map(s => s.trim()).filter(s => s)
      };
  
      const response = await axios.put(`/api/user/${user._id}`, updatedData);

      if (response.data.success) {
        setMessage('Profile updated successfully!');
        onUpdate && onUpdate();
        setIsEditing(false);
        setTimeout(() => setMessage(''), 3000);
      }
    } catch (error) {
      console.error('Error updating profile:', error);
      setMessage(error.response?.data?.message || 'Failed to update profile. Please try again.');
    }
  };

  if (!user) return null;

  return (
    <div className="user-profile">
      <h2>Your Profile</h2>
      {message && <div className="message">{message}</div>}
      
      <div className="profile-field">
        <label>Name:</label>
        {isEditing ? (
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
        ) : (
          <span>{name}</span>
        )}
      </div>
      
      <div className="profile-field">
        <label>Email:</label>
        {isEditing ? (
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        ) : (
          <span>{email || 'Not provided'}</span>
        )}
      </div>
      
      <div className="profile-field">
        <label>Education Level:</label>
        {isEditing ? (
          <input type="text" value={education} onChange={(e) => setEducation(e.target.value)} />
        ) : (
          <span>{education || 'Not provided'}</span>
        )}
      </div>
      
      <div className="profile-field">
        <label>Interests:</label>
        {isEditing ? (
          <textarea 
            value={interests} 
            onChange={(e) => setInterests(e.target.value)}
            placeholder="Enter interests separated by commas"
          />
        ) : (
          <span>{interests || 'Not provided'}</span>
        )}
      </div>
      
      <div className="profile-field">
        <label>Skills:</label>
        {isEditing ? (
          <textarea 
            value={skills} 
            onChange={(e) => setSkills(e.target.value)}
            placeholder="Enter skills separated by commas"
          />
        ) : (
          <span>{skills || 'Not provided'}</span>
        )}
      </div>
      
      <div className="profile-actions">
        {isEditing ? (
          <>
            <button onClick={handleSave}>Save</button>
            <button onClick={() => setIsEditing(false)}>Cancel</button>
          </>
        ) : (
          <button onClick={() => setIsEditing(true)}>Edit Profile</button>
        )}
      </div>
    </div>
  );
};

export default UserProfile;