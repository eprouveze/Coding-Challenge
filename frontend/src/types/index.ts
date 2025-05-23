export interface User {
  id: number
  email: string
  username: string
  full_name?: string
  role: 'admin' | 'organizer' | 'attendee'
  is_active: boolean
  created_at: string
}

export interface Event {
  id: number
  title: string
  description?: string
  date: string
  location: string
  capacity: number
  category: EventCategory
  created_at: string
  updated_at: string
  organizer_id: number
  organizer: User
  current_attendees: number
  available_spots: number
}

export interface EventWithAttendees extends Event {
  attendees: Attendee[]
}

export interface Attendee {
  id: number
  event_id: number
  user_id: number
  status: AttendanceStatus
  registered_at: string
  checked_in_at?: string
  waitlist_position?: number
  user: User
}

export type EventCategory = 
  | 'conference'
  | 'workshop'
  | 'seminar'
  | 'networking'
  | 'social'
  | 'training'
  | 'other'

export type AttendanceStatus = 
  | 'registered'
  | 'checked_in'
  | 'cancelled'
  | 'waitlisted'

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  password: string
  full_name?: string
}

export interface EventCreateData {
  title: string
  description?: string
  date: string
  location: string
  capacity: number
  category: EventCategory
}

export interface EventUpdateData {
  title?: string
  description?: string
  date?: string
  location?: string
  capacity?: number
  category?: EventCategory
}

export interface EventStatistics {
  total_events: number
  total_attendees: number
  average_attendance_rate: number
  events_by_category: Record<string, number>
  upcoming_events: number
  past_events: number
  most_popular_category: string
  events_at_capacity: number
}

export interface UserStatistics {
  total_users: number
  users_by_role: Record<string, number>
  active_users: number
  new_users_this_month: number
}