import React, { useState } from 'react';

const ProfilePage = () => {
  const [user, setUser] = useState({
    name: 'John Doe',
    email: 'johndoe@example.com',
    bio: 'Software developer with a passion for open-source projects.',
  });

  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState({ ...user });

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
    setEditedUser({ ...user });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedUser({
      ...editedUser,
      [name]: value,
    });
  };

  const handleSave = () => {
    setUser({ ...editedUser });
    setIsEditing(false);
  };

  return (
    <div className="profile-container">
      <h2>User Profile</h2>
      <div className="profile-info">
        <label>Name:</label>
        {isEditing ? (
          <input
            type="text"
            name="name"
            value={editedUser.name}
            onChange={handleChange}
          />
        ) : (
          <p>{user.name}</p>
        )}
      </div>
      <div className="profile-info">
        <label>Email:</label>
        {isEditing ? (
          <input
            type="email"
            name="email"
            value={editedUser.email}
            onChange={handleChange}
          />
        ) : (
          <p>{user.email}</p>
        )}
      </div>
      <div className="profile-info">
        <label>Bio:</label>
        {isEditing ? (
          <textarea
            name="bio"
            value={editedUser.bio}
            onChange={handleChange}
          />
        ) : (
          <p>{user.bio}</p>
        )}
      </div>
      <div className="profile-actions">
        {isEditing ? (
          <>
            <button onClick={handleSave} className="btn save-btn">
              Save
            </button>
            <button onClick={handleEditToggle} className="btn cancel-btn">
              Cancel
            </button>
          </>
        ) : (
          <button onClick={handleEditToggle} className="btn edit-btn">
            Edit Profile
          </button>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;