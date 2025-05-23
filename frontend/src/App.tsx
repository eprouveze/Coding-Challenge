import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import EventsPage from './pages/EventsPage'
import EventDetailPage from './pages/EventDetailPage'
import AdminDashboard from './pages/AdminDashboard'
import MyEventsPage from './pages/MyEventsPage'
import { useAuthStore } from './store/authStore'

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)

  return (
    <Box sx={{ minHeight: '100vh' }}>
      <Routes>
        <Route path="/login" element={!isAuthenticated ? <LoginPage /> : <Navigate to="/" />} />
        <Route path="/register" element={!isAuthenticated ? <RegisterPage /> : <Navigate to="/" />} />
        
        <Route element={<Layout />}>
          <Route path="/" element={<EventsPage />} />
          <Route path="/events/:id" element={<EventDetailPage />} />
          
          <Route element={<ProtectedRoute />}>
            <Route path="/my-events" element={<MyEventsPage />} />
          </Route>
          
          <Route element={<ProtectedRoute allowedRoles={['admin', 'organizer']} />}>
            <Route path="/admin/*" element={<AdminDashboard />} />
          </Route>
        </Route>
      </Routes>
    </Box>
  )
}

export default App