import axios, { AxiosInstance, AxiosError } from 'axios';
import toast from 'react-hot-toast';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: `${API_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token');
          window.location.href = '/login';
          toast.error('Session expired. Please login again.');
        } else if (error.response?.status === 403) {
          toast.error('You do not have permission to perform this action.');
        } else if (error.response?.status === 500) {
          toast.error('Server error. Please try again later.');
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(username: string, password: string) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await this.api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async register(data: { email: string; username: string; password: string; full_name?: string }) {
    const response = await this.api.post('/auth/register', data);
    return response.data;
  }

  async getCurrentUser() {
    const response = await this.api.get('/auth/me');
    return response.data;
  }

  async updateCurrentUser(data: any) {
    const response = await this.api.put('/auth/me', data);
    return response.data;
  }

  // Event endpoints
  async getEvents(params?: { skip?: number; limit?: number; status?: string; search?: string }) {
    const response = await this.api.get('/events', { params });
    return response.data;
  }

  async getEvent(id: string) {
    const response = await this.api.get(`/events/${id}`);
    return response.data;
  }

  async createEvent(data: any) {
    const response = await this.api.post('/events', data);
    return response.data;
  }

  async updateEvent(id: string, data: any) {
    const response = await this.api.put(`/events/${id}`, data);
    return response.data;
  }

  async deleteEvent(id: string) {
    const response = await this.api.delete(`/events/${id}`);
    return response.data;
  }

  async registerForEvent(eventId: string) {
    const response = await this.api.post(`/events/${eventId}/register`);
    return response.data;
  }

  // Attendee endpoints
  async getAttendees(params?: any) {
    const response = await this.api.get('/attendees', { params });
    return response.data;
  }

  async getAttendee(id: string) {
    const response = await this.api.get(`/attendees/${id}`);
    return response.data;
  }

  async updateAttendee(id: string, data: any) {
    const response = await this.api.put(`/attendees/${id}`, data);
    return response.data;
  }

  async checkInAttendee(id: string) {
    const response = await this.api.post(`/attendees/${id}/check-in`);
    return response.data;
  }

  // Analytics endpoints
  async getDashboardAnalytics(params?: { start_date?: string; end_date?: string }) {
    const response = await this.api.get('/analytics/dashboard', { params });
    return response.data;
  }

  async getEventAnalytics(eventId: string) {
    const response = await this.api.get(`/analytics/events/${eventId}`);
    return response.data;
  }

  async getRevenueAnalytics(params?: any) {
    const response = await this.api.get('/analytics/revenue', { params });
    return response.data;
  }

  async getAttendanceTrends(params?: any) {
    const response = await this.api.get('/analytics/attendance-trends', { params });
    return response.data;
  }
}

export const api = new ApiService();