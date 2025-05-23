import api from './api'
import { LoginCredentials, RegisterData, User } from '@/types'

export const authService = {
  async login(credentials: LoginCredentials) {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    
    const response = await api.post('/users/token', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  },

  async register(data: RegisterData) {
    const response = await api.post('/users/register', data)
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/users/me')
    return response.data
  },

  async updateProfile(data: Partial<User>) {
    const response = await api.put('/users/me', data)
    return response.data
  }
}