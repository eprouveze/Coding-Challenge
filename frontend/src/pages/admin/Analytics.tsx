import { useQuery } from '@tanstack/react-query'
import {
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress
} from '@mui/material'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Bar, Pie } from 'react-chartjs-2'
import { analyticsService } from '@/services/analytics'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
)

export default function Analytics() {
  const { data: eventStats, isLoading: eventsLoading } = useQuery({
    queryKey: ['eventStatistics'],
    queryFn: analyticsService.getEventStatistics,
  })

  const { data: userStats, isLoading: usersLoading } = useQuery({
    queryKey: ['userStatistics'],
    queryFn: analyticsService.getUserStatistics,
  })

  if (eventsLoading || usersLoading) {
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    )
  }

  const categoryData = eventStats ? {
    labels: Object.keys(eventStats.events_by_category),
    datasets: [
      {
        label: 'Events by Category',
        data: Object.values(eventStats.events_by_category),
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)',
          'rgba(255, 159, 64, 0.5)',
          'rgba(199, 199, 199, 0.5)',
        ],
      },
    ],
  } : null

  const roleData = userStats ? {
    labels: Object.keys(userStats.users_by_role),
    datasets: [
      {
        label: 'Users by Role',
        data: Object.values(userStats.users_by_role),
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
        ],
      },
    ],
  } : null

  return (
    <>
      <Typography variant="h5" gutterBottom>
        Analytics Dashboard
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h3" color="primary">
              {eventStats?.total_events || 0}
            </Typography>
            <Typography variant="subtitle1">Total Events</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h3" color="secondary">
              {eventStats?.total_attendees || 0}
            </Typography>
            <Typography variant="subtitle1">Total Attendees</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h3" color="success.main">
              {eventStats?.average_attendance_rate || 0}%
            </Typography>
            <Typography variant="subtitle1">Avg Attendance Rate</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={3}>
          <Paper sx={{ p: 3, textAlign: 'center' }}>
            <Typography variant="h3" color="info.main">
              {userStats?.total_users || 0}
            </Typography>
            <Typography variant="subtitle1">Total Users</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Events by Category
            </Typography>
            {categoryData && (
              <Bar
                data={categoryData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                }}
              />
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Users by Role
            </Typography>
            {roleData && (
              <Pie
                data={roleData}
                options={{
                  responsive: true,
                  plugins: {
                    legend: {
                      position: 'bottom',
                    },
                  },
                }}
              />
            )}
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Event Insights
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Upcoming Events
                  </Typography>
                  <Typography variant="h5">
                    {eventStats?.upcoming_events || 0}
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Most Popular Category
                  </Typography>
                  <Typography variant="h5">
                    {eventStats?.most_popular_category || 'N/A'}
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12} md={4}>
                <Box>
                  <Typography variant="subtitle2" color="text.secondary">
                    Events at Capacity
                  </Typography>
                  <Typography variant="h5">
                    {eventStats?.events_at_capacity || 0}
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </>
  )
}