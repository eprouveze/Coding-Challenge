import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { 
  Grid, 
  Typography, 
  TextField, 
  Select, 
  MenuItem, 
  FormControl, 
  InputLabel, 
  Box,
  CircularProgress,
  Alert
} from '@mui/material'
import EventCard from '@/components/EventCard'
import { eventsService } from '@/services/events'
import { EventCategory } from '@/types'

export default function EventsPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState<EventCategory | ''>('')
  
  const { data: events, isLoading, error } = useQuery({
    queryKey: ['events', categoryFilter],
    queryFn: () => eventsService.getEvents({ 
      category: categoryFilter || undefined,
      upcoming_only: true 
    }),
  })

  const filteredEvents = events?.filter(event =>
    event.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    event.location.toLowerCase().includes(searchTerm.toLowerCase())
  ) || []

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return <Alert severity="error">Failed to load events</Alert>
  }

  return (
    <>
      <Typography variant="h4" component="h1" gutterBottom>
        Upcoming Events
      </Typography>
      
      <Box sx={{ mb: 4, display: 'flex', gap: 2 }}>
        <TextField
          label="Search events"
          variant="outlined"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ flexGrow: 1 }}
        />
        
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Category</InputLabel>
          <Select
            value={categoryFilter}
            label="Category"
            onChange={(e) => setCategoryFilter(e.target.value as EventCategory | '')}
          >
            <MenuItem value="">All Categories</MenuItem>
            <MenuItem value="conference">Conference</MenuItem>
            <MenuItem value="workshop">Workshop</MenuItem>
            <MenuItem value="seminar">Seminar</MenuItem>
            <MenuItem value="networking">Networking</MenuItem>
            <MenuItem value="social">Social</MenuItem>
            <MenuItem value="training">Training</MenuItem>
            <MenuItem value="other">Other</MenuItem>
          </Select>
        </FormControl>
      </Box>
      
      {filteredEvents.length === 0 ? (
        <Alert severity="info">No events found</Alert>
      ) : (
        <Grid container spacing={3}>
          {filteredEvents.map((event) => (
            <Grid item xs={12} md={6} lg={4} key={event.id}>
              <EventCard event={event} />
            </Grid>
          ))}
        </Grid>
      )}
    </>
  )
}