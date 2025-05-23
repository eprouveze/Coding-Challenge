import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Select,
  MenuItem,
  CircularProgress,
  Box,
  Alert
} from '@mui/material'
import { format } from 'date-fns'
import api from '@/services/api'
import { User } from '@/types'
import { useAuthStore } from '@/store/authStore'

export default function UserManagement() {
  const queryClient = useQueryClient()
  const currentUser = useAuthStore(state => state.user)
  
  const { data: users, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await api.get<User[]>('/users/')
      return response.data
    },
  })

  const updateUserMutation = useMutation({
    mutationFn: async ({ userId, role }: { userId: number; role: string }) => {
      const response = await api.put(`/users/${userId}`, { role })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  const handleRoleChange = (userId: number, newRole: string) => {
    if (userId === currentUser?.id) {
      alert("You cannot change your own role")
      return
    }
    updateUserMutation.mutate({ userId, role: newRole })
  }

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return <Alert severity="error">Failed to load users</Alert>
  }

  const getRoleColor = (role: string) => {
    const colors: Record<string, any> = {
      admin: 'error',
      organizer: 'warning',
      attendee: 'default',
    }
    return colors[role] || 'default'
  }

  return (
    <>
      <Typography variant="h5" gutterBottom>
        User Management
      </Typography>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Username</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Full Name</TableCell>
              <TableCell>Role</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Joined</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {users?.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.username}</TableCell>
                <TableCell>{user.email}</TableCell>
                <TableCell>{user.full_name || '-'}</TableCell>
                <TableCell>
                  {currentUser?.role === 'admin' && user.id !== currentUser.id ? (
                    <Select
                      value={user.role}
                      onChange={(e) => handleRoleChange(user.id, e.target.value)}
                      size="small"
                    >
                      <MenuItem value="attendee">Attendee</MenuItem>
                      <MenuItem value="organizer">Organizer</MenuItem>
                      <MenuItem value="admin">Admin</MenuItem>
                    </Select>
                  ) : (
                    <Chip 
                      label={user.role} 
                      color={getRoleColor(user.role)} 
                      size="small" 
                    />
                  )}
                </TableCell>
                <TableCell>
                  <Chip 
                    label={user.is_active ? 'Active' : 'Inactive'} 
                    color={user.is_active ? 'success' : 'default'} 
                    size="small" 
                  />
                </TableCell>
                <TableCell>{format(new Date(user.created_at), 'PP')}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  )
}