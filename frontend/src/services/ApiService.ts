import axios, {
  AxiosInstance,
  AxiosError,
  InternalAxiosRequestConfig,
  AxiosRequestConfig,
} from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

interface UserData {
  email: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
}

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.api.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem("accessToken");
        if (token) {
          config.headers["Authorization"] = `Bearer ${token}`;
        }
        return config;
      },
      (error: AxiosError) => {
        console.error("Request interceptor error:", error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (!error.config) {
          console.error("No config attached to error");
          return Promise.reject(error);
        }

        const originalRequest = error.config as AxiosRequestConfig & {
          _retry?: boolean;
        };
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;
          try {
            await this.refreshToken();
            return this.api(originalRequest);
          } catch (refreshError) {
            this.logout();
            return Promise.reject(refreshError);
          }
        }
        return Promise.reject(error);
      }
    );
  }

  async signup(userData: UserData): Promise<void> {
    try {
      await this.api.post("/register/", userData);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  async login(userData: UserData): Promise<LoginResponse> {
    try {
      const response = await this.api.post<LoginResponse>("/token/", userData);
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      return response.data;
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  logout(): void {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
  }

  private async refreshToken(): Promise<void> {
    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
      throw new Error("No refresh token available");
    }
    try {
      const response = await this.api.post<{ access: string }>(
        "/token/refresh/",
        { refresh: refreshToken }
      );
      localStorage.setItem("accessToken", response.data.access);
    } catch (error) {
      this.handleError(error);
      throw error;
    }
  }

  private handleError(error: unknown): void {
    if (axios.isAxiosError(error)) {
      console.error("API Error:", error.response?.data);
      // TODO: add more specific error handling here?
    } else {
      console.error("An unexpected error occurred:", error);
    }
  }
}

export const apiService = new ApiService();
