export interface UserData {
  email: string;
  password: string;
}

export interface LoginResponse {
  access: string;
  refresh: string;
}

export interface UserProfileData {
  email: string;
  bio: string;
}
