import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box
} from '@mui/material'
import { Edit, Delete } from '@mui/icons-material'
import { format } from 'date-fns'
import { useForm, Controller } from 'react-hook-form'
import { eventsService } from '@/services/events'
import { EventCreateData } from '@/types'
import { useAuthStore } from '@/store/authStore'

export default function EventManagement() {
  const queryClient = useQueryClient()
  const { user } = useAuthStore()
  const [openDialog, setOpenDialog] = useState(false)
  const [editingEvent, setEditingEvent] = useState<any>(null)
  
  const { data: events } = useQuery({
    queryKey: ['adminEvents'],
    queryFn: () => eventsService.getEvents({ upcoming_only: false }),
  })

  const createMutation = useMutation({
    mutationFn: eventsService.createEvent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['adminEvents'] })
      setOpenDialog(false)
      reset()
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => 
      eventsService.updateEvent(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['adminEvents'] })
      setOpenDialog(false)
      setEditingEvent(null)
      reset()
    },
  })

  const deleteMutation = useMutation({
    mutationFn: eventsService.deleteEvent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['adminEvents'] })
    },
  })

  const { control, handleSubmit, reset, setValue } = useForm<EventCreateData>()

  const onSubmit = (data: EventCreateData) => {
    if (editingEvent) {
      updateMutation.mutate({ id: editingEvent.id, data })
    } else {
      createMutation.mutate(data)
    }
  }

  const handleEdit = (event: any) => {
    setEditingEvent(event)
    setValue('title', event.title)
    setValue('description', event.description || '')
    setValue('date', event.date.slice(0, 16))
    setValue('location', event.location)
    setValue('capacity', event.capacity)
    setValue('category', event.category)
    setOpenDialog(true)
  }

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this event?')) {
      deleteMutation.mutate(id)
    }
  }

  const filteredEvents = user?.role === 'admin' 
    ? events 
    : events?.filter(e => e.organizer_id === user?.id)

  return (
    <>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">Event Management</Typography>
        <Button
          variant="contained"
          onClick={() => {
            setEditingEvent(null)
            reset()
            setOpenDialog(true)
          }}
        >
          Create Event
        </Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Date</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Capacity</TableCell>
              <TableCell>Attendees</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredEvents?.map((event) => (
              <TableRow key={event.id}>
                <TableCell>{event.title}</TableCell>
                <TableCell>{format(new Date(event.date), 'PPP')}</TableCell>
                <TableCell>{event.category}</TableCell>
                <TableCell>{event.capacity}</TableCell>
                <TableCell>{event.current_attendees}</TableCell>
                <TableCell>
                  <IconButton onClick={() => handleEdit(event)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(event.id)} color="error">
                    <Delete />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogTitle>{editingEvent ? 'Edit Event' : 'Create Event'}</DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
              <Controller
                name="title"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <TextField {...field} label="Title" fullWidth required />
                )}
              />
              
              <Controller
                name="description"
                control={control}
                render={({ field }) => (
                  <TextField {...field} label="Description" multiline rows={3} fullWidth />
                )}
              />
              
              <Controller
                name="date"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <TextField {...field} type="datetime-local" label="Date" fullWidth required InputLabelProps={{ shrink: true }} />
                )}
              />
              
              <Controller
                name="location"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <TextField {...field} label="Location" fullWidth required />
                )}
              />
              
              <Controller
                name="capacity"
                control={control}
                rules={{ required: true, min: 1 }}
                render={({ field }) => (
                  <TextField {...field} type="number" label="Capacity" fullWidth required />
                )}
              />
              
              <Controller
                name="category"
                control={control}
                rules={{ required: true }}
                render={({ field }) => (
                  <FormControl fullWidth required>
                    <InputLabel>Category</InputLabel>
                    <Select {...field} label="Category">
                      <MenuItem value="conference">Conference</MenuItem>
                      <MenuItem value="workshop">Workshop</MenuItem>
                      <MenuItem value="seminar">Seminar</MenuItem>
                      <MenuItem value="networking">Networking</MenuItem>
                      <MenuItem value="social">Social</MenuItem>
                      <MenuItem value="training">Training</MenuItem>
                      <MenuItem value="other">Other</MenuItem>
                    </Select>
                  </FormControl>
                )}
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button type="submit" variant="contained">
              {editingEvent ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </>
  )
}