import React, { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { apiService } from "../services/ApiService";
import { UserProfileData } from "../types";

const UserProfile: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [profileData, setProfileData] = useState<UserProfileData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const data = await apiService.getUserProfile();
        setProfileData(data);
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
          <p>Bio: {profileData.bio}</p>
        </div>
      )}
    </div>
  );
};

export default UserProfile;
