import api from './api'
import { EventStatistics, UserStatistics } from '@/types'

export const analyticsService = {
  async getEventStatistics() {
    const response = await api.get<EventStatistics>('/analytics/events')
    return response.data
  },

  async getUserStatistics() {
    const response = await api.get<UserStatistics>('/analytics/users')
    return response.data
  },

  async getEventSpecificStatistics(eventId: number) {
    const response = await api.get(`/analytics/events/${eventId}/stats`)
    return response.data
  }
}