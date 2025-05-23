import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import EventCard from '@/components/EventCard'
import { Event } from '@/types'

const mockEvent: Event = {
  id: 1,
  title: 'Test Event',
  description: 'Test Description',
  date: '2024-12-25T10:00:00',
  location: 'Test Location',
  capacity: 100,
  category: 'conference',
  created_at: '2024-01-01T00:00:00',
  updated_at: '2024-01-01T00:00:00',
  organizer_id: 1,
  organizer: {
    id: 1,
    email: 'organizer@test.com',
    username: 'organizer',
    role: 'organizer',
    is_active: true,
    created_at: '2024-01-01T00:00:00',
  },
  current_attendees: 50,
  available_spots: 50,
}

describe('EventCard', () => {
  it('renders event information correctly', () => {
    render(
      <BrowserRouter>
        <EventCard event={mockEvent} />
      </BrowserRouter>
    )

    expect(screen.getByText('Test Event')).toBeInTheDocument()
    expect(screen.getByText('Test Description')).toBeInTheDocument()
    expect(screen.getByText('Test Location')).toBeInTheDocument()
    expect(screen.getByText('conference')).toBeInTheDocument()
    expect(screen.getByText('50 / 100')).toBeInTheDocument()
  })

  it('shows FULL chip when no spots available', () => {
    const fullEvent = { ...mockEvent, available_spots: 0 }
    render(
      <BrowserRouter>
        <EventCard event={fullEvent} />
      </BrowserRouter>
    )

    expect(screen.getByText('FULL')).toBeInTheDocument()
  })
})