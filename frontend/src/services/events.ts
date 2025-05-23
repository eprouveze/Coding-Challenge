import api from './api'
import { Event, EventWithAttendees, EventCreateData, EventUpdateData, EventCategory } from '@/types'

export const eventsService = {
  async getEvents(params?: { category?: EventCategory; upcoming_only?: boolean }) {
    const response = await api.get<Event[]>('/events/', { params })
    return response.data
  },

  async getEvent(id: number) {
    const response = await api.get<EventWithAttendees>(`/events/${id}`)
    return response.data
  },

  async createEvent(data: EventCreateData) {
    const response = await api.post<Event>('/events/', data)
    return response.data
  },

  async updateEvent(id: number, data: EventUpdateData) {
    const response = await api.put<Event>(`/events/${id}`, data)
    return response.data
  },

  async deleteEvent(id: number) {
    await api.delete(`/events/${id}`)
  },

  async registerForEvent(eventId: number) {
    const response = await api.post('/attendees/register', { event_id: eventId })
    return response.data
  },

  async cancelRegistration(attendeeId: number) {
    const response = await api.put(`/attendees/${attendeeId}/cancel`)
    return response.data
  },

  async checkInAttendee(attendeeId: number) {
    const response = await api.put(`/attendees/${attendeeId}/check-in`)
    return response.data
  },

  async getMyRegistrations() {
    const response = await api.get('/attendees/my-registrations')
    return response.data
  },

  async getEventAttendees(eventId: number) {
    const response = await api.get(`/attendees/event/${eventId}`)
    return response.data
  }
}