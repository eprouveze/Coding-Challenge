import { useQuery } from '@tanstack/react-query'
import { 
  Typography, 
  Box,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  Chip,
  Paper
} from '@mui/material'
import { format } from 'date-fns'
import { eventsService } from '@/services/events'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function MyEventsPage() {
  const navigate = useNavigate()
  const [tabValue, setTabValue] = useState(0)
  
  const { data: registrations, isLoading, error } = useQuery({
    queryKey: ['myRegistrations'],
    queryFn: () => eventsService.getMyRegistrations(),
  })

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return <Alert severity="error">Failed to load your events</Alert>
  }

  const upcomingEvents = registrations?.filter((r: any) => 
    new Date(r.event.date) >= new Date() && r.status !== 'cancelled'
  ) || []
  
  const pastEvents = registrations?.filter((r: any) => 
    new Date(r.event.date) < new Date() && r.status !== 'cancelled'
  ) || []

  const getStatusChip = (status: string, waitlistPosition?: number) => {
    const statusColors: Record<string, any> = {
      registered: 'success',
      checked_in: 'info',
      waitlisted: 'warning',
      cancelled: 'error',
    }
    
    const label = status === 'waitlisted' && waitlistPosition 
      ? `Waitlist #${waitlistPosition}` 
      : status.replace('_', ' ')
    
    return <Chip label={label} color={statusColors[status]} size="small" />
  }

  return (
    <>
      <Typography variant="h4" component="h1" gutterBottom>
        My Events
      </Typography>
      
      <Paper sx={{ mt: 3 }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label={`Upcoming (${upcomingEvents.length})`} />
          <Tab label={`Past (${pastEvents.length})`} />
        </Tabs>
        
        <Box sx={{ p: 2 }}>
          {tabValue === 0 && (
            <>
              {upcomingEvents.length === 0 ? (
                <Alert severity="info">You have no upcoming events</Alert>
              ) : (
                <List>
                  {upcomingEvents.map((registration: any) => (
                    <ListItem
                      key={registration.id}
                      sx={{ cursor: 'pointer' }}
                      onClick={() => navigate(`/events/${registration.event.id}`)}
                    >
                      <ListItemText
                        primary={registration.event.title}
                        secondary={
                          <>
                            {format(new Date(registration.event.date), 'PPP')} • {registration.event.location}
                          </>
                        }
                      />
                      {getStatusChip(registration.status, registration.waitlist_position)}
                    </ListItem>
                  ))}
                </List>
              )}
            </>
          )}
          
          {tabValue === 1 && (
            <>
              {pastEvents.length === 0 ? (
                <Alert severity="info">You have no past events</Alert>
              ) : (
                <List>
                  {pastEvents.map((registration: any) => (
                    <ListItem
                      key={registration.id}
                      sx={{ cursor: 'pointer' }}
                      onClick={() => navigate(`/events/${registration.event.id}`)}
                    >
                      <ListItemText
                        primary={registration.event.title}
                        secondary={
                          <>
                            {format(new Date(registration.event.date), 'PPP')} • {registration.event.location}
                          </>
                        }
                      />
                      {getStatusChip(registration.status)}
                    </ListItem>
                  ))}
                </List>
              )}
            </>
          )}
        </Box>
      </Paper>
    </>
  )
}