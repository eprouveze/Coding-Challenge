import { Card, CardContent, CardActions, Typography, Button, Chip, Box } from '@mui/material'
import { Event } from '@/types'
import { format } from 'date-fns'
import { useNavigate } from 'react-router-dom'

interface EventCardProps {
  event: Event
}

export default function EventCard({ event }: EventCardProps) {
  const navigate = useNavigate()

  const getCategoryColor = (category: string) => {
    const colors: Record<string, any> = {
      conference: 'primary',
      workshop: 'secondary',
      seminar: 'success',
      networking: 'info',
      social: 'warning',
      training: 'error',
      other: 'default',
    }
    return colors[category] || 'default'
  }

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h5" component="div">
          {event.title}
        </Typography>
        
        <Box sx={{ mb: 2 }}>
          <Chip 
            label={event.category} 
            color={getCategoryColor(event.category)} 
            size="small" 
            sx={{ mr: 1 }}
          />
          {event.available_spots === 0 && (
            <Chip label="FULL" color="error" size="small" />
          )}
        </Box>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          {event.description || 'No description available'}
        </Typography>
        
        <Typography variant="body2">
          <strong>Date:</strong> {format(new Date(event.date), 'PPP')}
        </Typography>
        
        <Typography variant="body2">
          <strong>Location:</strong> {event.location}
        </Typography>
        
        <Typography variant="body2">
          <strong>Available Spots:</strong> {event.available_spots} / {event.capacity}
        </Typography>
      </CardContent>
      
      <CardActions>
        <Button size="small" onClick={() => navigate(`/events/${event.id}`)}>
          View Details
        </Button>
      </CardActions>
    </Card>
  )
}