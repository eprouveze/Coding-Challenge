import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  Paper, 
  Typography, 
  Button, 
  Box, 
  Chip,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material'
import { CheckCircle } from '@mui/icons-material'
import { format } from 'date-fns'
import { eventsService } from '@/services/events'
import { useAuthStore } from '@/store/authStore'

export default function EventDetailPage() {
  const { id } = useParams<{ id: string }>()
  const queryClient = useQueryClient()
  const { user, isAuthenticated } = useAuthStore()
  const [openDialog, setOpenDialog] = useState(false)
  
  const { data: event, isLoading, error } = useQuery({
    queryKey: ['event', id],
    queryFn: () => eventsService.getEvent(Number(id)),
    enabled: !!id,
  })

  const { data: myRegistrations } = useQuery({
    queryKey: ['myRegistrations'],
    queryFn: () => eventsService.getMyRegistrations(),
    enabled: isAuthenticated,
  })

  const registerMutation = useMutation({
    mutationFn: () => eventsService.registerForEvent(Number(id)),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['event', id] })
      queryClient.invalidateQueries({ queryKey: ['myRegistrations'] })
    },
  })

  const cancelMutation = useMutation({
    mutationFn: (attendeeId: number) => eventsService.cancelRegistration(attendeeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['event', id] })
      queryClient.invalidateQueries({ queryKey: ['myRegistrations'] })
      setOpenDialog(false)
    },
  })

  const checkInMutation = useMutation({
    mutationFn: (attendeeId: number) => eventsService.checkInAttendee(attendeeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['event', id] })
    },
  })

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    )
  }

  if (error || !event) {
    return <Alert severity="error">Failed to load event details</Alert>
  }

  const myRegistration = myRegistrations?.find((r: any) => r.event_id === event.id)
  const isOrganizer = user?.id === event.organizer_id || user?.role === 'admin'

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        {event.title}
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <Chip 
          label={event.category} 
          color="primary" 
          sx={{ mr: 1 }}
        />
        {event.available_spots === 0 && (
          <Chip label="FULL" color="error" />
        )}
      </Box>
      
      <Typography variant="body1" paragraph>
        {event.description || 'No description available'}
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <Typography variant="body1">
          <strong>Date:</strong> {format(new Date(event.date), 'PPP')}
        </Typography>
        <Typography variant="body1">
          <strong>Location:</strong> {event.location}
        </Typography>
        <Typography variant="body1">
          <strong>Capacity:</strong> {event.current_attendees} / {event.capacity} attendees
        </Typography>
        <Typography variant="body1">
          <strong>Organizer:</strong> {event.organizer.full_name || event.organizer.username}
        </Typography>
      </Box>
      
      {isAuthenticated && !isOrganizer && (
        <Box sx={{ mb: 3 }}>
          {!myRegistration ? (
            <Button
              variant="contained"
              onClick={() => registerMutation.mutate()}
              disabled={registerMutation.isPending || event.available_spots === 0}
            >
              {event.available_spots === 0 ? 'Join Waitlist' : 'Register'}
            </Button>
          ) : (
            <>
              <Alert severity="success" sx={{ mb: 2 }}>
                You are registered for this event
                {myRegistration.status === 'waitlisted' && ` (Waitlist position: ${myRegistration.waitlist_position})`}
              </Alert>
              <Button
                variant="outlined"
                color="error"
                onClick={() => setOpenDialog(true)}
              >
                Cancel Registration
              </Button>
            </>
          )}
        </Box>
      )}
      
      {registerMutation.isError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {(registerMutation.error as any)?.response?.data?.detail || 'Registration failed'}
        </Alert>
      )}
      
      {registerMutation.isSuccess && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {registerMutation.data?.message}
        </Alert>
      )}
      
      {isOrganizer && event.attendees && (
        <>
          <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
            Attendees ({event.attendees.length})
          </Typography>
          <List>
            {event.attendees.map((attendee) => (
              <ListItem key={attendee.id}>
                <ListItemText
                  primary={attendee.user.full_name || attendee.user.username}
                  secondary={`${attendee.user.email} - Status: ${attendee.status}`}
                />
                <ListItemSecondaryAction>
                  {attendee.status === 'registered' && (
                    <IconButton
                      edge="end"
                      aria-label="check in"
                      onClick={() => checkInMutation.mutate(attendee.id)}
                    >
                      <CheckCircle color="success" />
                    </IconButton>
                  )}
                </ListItemSecondaryAction>
              </ListItem>
            ))}
          </List>
        </>
      )}
      
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Cancel Registration</DialogTitle>
        <DialogContent>
          Are you sure you want to cancel your registration for this event?
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>No</Button>
          <Button 
            onClick={() => myRegistration && cancelMutation.mutate(myRegistration.id)}
            color="error"
            disabled={cancelMutation.isPending}
          >
            Yes, Cancel
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  )
}