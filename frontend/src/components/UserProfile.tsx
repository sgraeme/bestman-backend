import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { apiService } from "../services/ApiService";
import { UserProfileData } from "../types";

const UserProfile: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [profileData, setProfileData] = useState<UserProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedBio, setEditedBio] = useState("");

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const data = await apiService.getUserProfile();
        setProfileData(data);
        setEditedBio(data.bio);
      } catch (err) {
        setError("Failed to fetch profile data");
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    if (isAuthenticated) {
      fetchProfileData();
    }
  }, [isAuthenticated]);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditedBio(profileData?.bio || "");
  };

  const handleSave = async () => {
    if (!profileData || editedBio === profileData.bio) {
      setIsEditing(false);
      return;
    }

    try {
      const updatedProfile = await apiService.updateUserProfile({
        bio: editedBio,
      });
      setProfileData(updatedProfile);
      setIsEditing(false);
    } catch (err) {
      setError("Failed to update profile");
      console.error(err);
    }
  };

  if (!isAuthenticated) {
    return <div>Please log in to view your profile.</div>;
  }

  if (isLoading) {
    return <div>Loading profile...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>User Profile</h1>
      {profileData && (
        <div>
          <p>Email: {profileData.email}</p>
          {isEditing ? (
            <div>
              <p>Bio: {profileData.bio}</p>
              <textarea
                value={editedBio}
                onChange={(e) => setEditedBio(e.target.value)}
                rows={4}
                cols={50}
              />
              <br />
              <button onClick={handleSave}>Save</button>
              <button onClick={handleCancel}>Cancel</button>
            </div>
          ) : (
            <div>
              <p>Bio: {profileData.bio}</p>
              <button onClick={handleEdit}>Edit Bio</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default UserProfile;
