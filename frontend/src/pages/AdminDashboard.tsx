import { Routes, Route, Link, useLocation } from 'react-router-dom'
import { Box, Tabs, Tab, Paper } from '@mui/material'
import EventManagement from './admin/EventManagement'
import Analytics from './admin/Analytics'
import UserManagement from './admin/UserManagement'

export default function AdminDashboard() {
  const location = useLocation()
  const currentTab = location.pathname.split('/').pop() || 'events'

  return (
    <Box>
      <Paper sx={{ mb: 3 }}>
        <Tabs value={currentTab}>
          <Tab label="Events" value="events" component={Link} to="/admin/events" />
          <Tab label="Analytics" value="analytics" component={Link} to="/admin/analytics" />
          <Tab label="Users" value="users" component={Link} to="/admin/users" />
        </Tabs>
      </Paper>
      
      <Routes>
        <Route path="/" element={<EventManagement />} />
        <Route path="/events" element={<EventManagement />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/users" element={<UserManagement />} />
      </Routes>
    </Box>
  )
}