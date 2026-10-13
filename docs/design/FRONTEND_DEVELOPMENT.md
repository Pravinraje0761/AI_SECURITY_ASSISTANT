# Frontend Development
## AI-Powered Digital Bodyguard for Intelligent Cyber Threat Detection and Prevention

**Version:** 1.0  
**Date:** July 14, 2026  

---

## 1. FRONTEND OVERVIEW

This document provides complete implementation details for the React Dashboard frontend.

### 1.1 Frontend Purpose

Provide a modern, responsive web interface for:
- User authentication
- Real-time threat monitoring
- URL and file scanning
- Alert management
- Security score visualization
- Threat intelligence dashboard
- User behavior analysis

### 1.2 Technology Stack

- **Framework**: React 18
- **Language**: TypeScript
- **State Management**: Redux Toolkit
- **Routing**: React Router v6
- **UI Components**: Material-UI (MUI)
- **Charts**: Recharts
- **HTTP Client**: Axios
- **WebSocket**: Socket.io-client
- **Forms**: React Hook Form
- **Validation**: Zod
- **Styling**: Tailwind CSS

### 1.3 Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Loading.tsx
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── dashboard/
│   │   │   ├── SecurityScore.tsx
│   │   │   ├── ThreatChart.tsx
│   │   │   ├── AlertFeed.tsx
│   │   │   └── QuickActions.tsx
│   │   ├── scanning/
│   │   │   ├── URLScanner.tsx
│   │   │   ├── FileScanner.tsx
│   │   │   └── ScanResults.tsx
│   │   ├── alerts/
│   │   │   ├── AlertList.tsx
│   │   │   ├── AlertCard.tsx
│   │   │   └── AlertFilters.tsx
│   │   └── monitoring/
│   │       ├── ProcessMonitor.tsx
│   │       ├── ResourceMonitor.tsx
│   │       └── NetworkMonitor.tsx
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Scan.tsx
│   │   ├── Alerts.tsx
│   │   ├── Monitoring.tsx
│   │   ├── Settings.tsx
│   │   └── Profile.tsx
│   ├── store/
│   │   ├── index.ts
│   │   ├── authSlice.ts
│   │   ├── alertSlice.ts
│   │   ├── threatSlice.ts
│   │   └── scanSlice.ts
│   ├── services/
│   │   ├── api.ts
│   │   ├── authService.ts
│   │   ├── scanService.ts
│   │   ├── alertService.ts
│   │   └── websocketService.ts
│   ├── types/
│   │   ├── auth.ts
│   │   ├── alert.ts
│   │   ├── threat.ts
│   │   └── scan.ts
│   ├── utils/
│   │   ├── validators.ts
│   │   ├── formatters.ts
│   │   └── constants.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useWebSocket.ts
│   │   └── useAlerts.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

---

## 2. PROJECT SETUP

### 2.1 Package.json

```json
{
  "name": "digital-bodyguard-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0",
    "@mui/icons-material": "^5.14.0",
    "@mui/material": "^5.14.0",
    "@mui/x-charts": "^6.0.0",
    "@reduxjs/toolkit": "^1.9.0",
    "axios": "^1.6.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.47.0",
    "react-redux": "^8.1.0",
    "react-router-dom": "^6.18.0",
    "recharts": "^2.10.0",
    "socket.io-client": "^4.6.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx"
  }
}
```

### 2.2 Vite Config

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      },
    },
  },
})
```

### 2.3 Tailwind Config

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        danger: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
        },
        success: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e',
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
        },
      },
    },
  },
  plugins: [],
}
```

---

## 3. MAIN APPLICATION

### 3.1 App.tsx

```typescript
// src/App.tsx
import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Provider } from 'react-redux'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { store } from './store'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Scan from './pages/Scan'
import Alerts from './pages/Alerts'
import Monitoring from './pages/Monitoring'
import Settings from './pages/Settings'
import Profile from './pages/Profile'
import Layout from './components/common/Layout'

const theme = createTheme({
  palette: {
    primary: {
      main: '#0ea5e9',
    },
    secondary: {
      main: '#6366f1',
    },
  },
})

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="scan" element={<Scan />} />
              <Route path="alerts" element={<Alerts />} />
              <Route path="monitoring" element={<Monitoring />} />
              <Route path="settings" element={<Settings />} />
              <Route path="profile" element={<Profile />} />
            </Route>
          </Routes>
        </Router>
      </ThemeProvider>
    </Provider>
  )
}

export default App
```

### 3.2 main.tsx

```typescript
// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

---

## 4. REDUX STORE

### 4.1 Store Configuration

```typescript
// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit'
import authReducer from './authSlice'
import alertReducer from './alertSlice'
import threatReducer from './threatSlice'
import scanReducer from './scanSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    alerts: alertReducer,
    threats: threatReducer,
    scans: scanReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
```

### 4.2 Auth Slice

```typescript
// src/store/authSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import authService from '../services/authService'

interface AuthState {
  user: any
  token: string
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token') || '',
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  error: null,
}

export const login = createAsyncThunk(
  'auth/login',
  async (credentials: { email: string; password: string }) => {
    const response = await authService.login(credentials)
    localStorage.setItem('token', response.access_token)
    return response
  }
)

export const register = createAsyncThunk(
  'auth/register',
  async (userData: any) => {
    const response = await authService.register(userData)
    return response
  }
)

export const logout = createAsyncThunk('auth/logout', async () => {
  localStorage.removeItem('token')
  return true
})

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false
        state.token = action.payload.access_token
        state.isAuthenticated = true
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Login failed'
      })
      .addCase(logout.fulfilled, (state) => {
        state.user = null
        state.token = ''
        state.isAuthenticated = false
      })
  },
})

export default authSlice.reducer
```

### 4.3 Alert Slice

```typescript
// src/store/alertSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import alertService from '../services/alertService'

interface AlertState {
  alerts: any[]
  loading: boolean
  error: string | null
}

const initialState: AlertState = {
  alerts: [],
  loading: false,
  error: null,
}

export const fetchAlerts = createAsyncThunk('alerts/fetch', async () => {
  const response = await alertService.getAlerts()
  return response
})

export const acknowledgeAlert = createAsyncThunk(
  'alerts/acknowledge',
  async (alertId: string) => {
    await alertService.acknowledgeAlert(alertId)
    return alertId
  }
)

const alertSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    addAlert: (state, action) => {
      state.alerts.unshift(action.payload)
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAlerts.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchAlerts.fulfilled, (state, action) => {
        state.loading = false
        state.alerts = action.payload
      })
      .addCase(acknowledgeAlert.fulfilled, (state, action) => {
        const alert = state.alerts.find((a) => a.id === action.payload)
        if (alert) {
          alert.status = 'acknowledged'
        }
      })
  },
})

export const { addAlert } = alertSlice.actions
export default alertSlice.reducer
```

---

## 5. API SERVICES

### 5.1 API Client

```typescript
// src/services/api.ts
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

### 5.2 Auth Service

```typescript
// src/services/authService.ts
import api from './api'

export const authService = {
  async login(credentials: { email: string; password: string }) {
    const formData = new FormData()
    formData.append('username', credentials.email)
    formData.append('password', credentials.password)
    
    const response = await api.post('/api/v1/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  async register(userData: any) {
    const response = await api.post('/api/v1/auth/register', userData)
    return response.data
  },

  async logout() {
    const response = await api.post('/api/v1/auth/logout')
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/api/v1/auth/me')
    return response.data
  },
}
```

### 5.3 Scan Service

```typescript
// src/services/scanService.ts
import api from './api'

export const scanService = {
  async scanURL(url: string) {
    const response = await api.post('/api/v1/scan/url', {
      type: 'phishing',
      target: url,
    })
    return response.data
  },

  async scanFile(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/api/v1/scan/file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  async getScanHistory() {
    const response = await api.get('/api/v1/scan/history')
    return response.data
  },
}
```

### 5.4 WebSocket Service

```typescript
// src/services/websocketService.ts
import { io, Socket } from 'socket.io-client'

class WebSocketService {
  private socket: Socket | null = null
  private listeners: Map<string, Function[]> = new Map()

  connect() {
    const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
    this.socket = io(WS_URL)

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })

    this.socket.on('new_alert', (data) => {
      this.notify('new_alert', data)
    })

    this.socket.on('threat_detected', (data) => {
      this.notify('threat_detected', data)
    })
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, [])
    }
    this.listeners.get(event)!.push(callback)
  }

  off(event: string, callback: Function) {
    const callbacks = this.listeners.get(event)
    if (callbacks) {
      const index = callbacks.indexOf(callback)
      if (index > -1) {
        callbacks.splice(index, 1)
      }
    }
  }

  private notify(event: string, data: any) {
    const callbacks = this.listeners.get(event)
    if (callbacks) {
      callbacks.forEach((callback) => callback(data))
    }
  }
}

export default new WebSocketService()
```

---

## 6. PAGES

### 6.1 Login Page

```typescript
// src/pages/Login.tsx
import React from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
} from '@mui/material'
import { useDispatch } from 'react-redux'
import { login } from '../store/authSlice'
import { useNavigate } from 'react-router-dom'

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(6, 'Password must be at least 6 characters'),
})

type LoginFormData = z.infer<typeof loginSchema>

const Login: React.FC = () => {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data: LoginFormData) => {
    try {
      await dispatch(login(data) as any)
      navigate('/dashboard')
    } catch (error) {
      console.error('Login failed:', error)
    }
  }

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          mt: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography component="h1" variant="h5" align="center" gutterBottom>
            AI Digital Bodyguard
          </Typography>
          <Typography variant="subtitle1" align="center" color="textSecondary">
            Sign in to your account
          </Typography>
          <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 3 }}>
            <TextField
              margin="normal"
              fullWidth
              label="Email"
              autoComplete="email"
              autoFocus
              {...register('email')}
              error={!!errors.email}
              helperText={errors.email?.message}
            />
            <TextField
              margin="normal"
              fullWidth
              label="Password"
              type="password"
              autoComplete="current-password"
              {...register('password')}
              error={!!errors.password}
              helperText={errors.password?.message}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  )
}

export default Login
```

### 6.2 Dashboard Page

```typescript
// src/pages/Dashboard.tsx
import React, { useEffect } from 'react'
import { Box, Grid, Typography } from '@mui/material'
import { useDispatch, useSelector } from 'react-redux'
import SecurityScore from '../components/dashboard/SecurityScore'
import ThreatChart from '../components/dashboard/ThreatChart'
import AlertFeed from '../components/dashboard/AlertFeed'
import QuickActions from '../components/dashboard/QuickActions'
import { fetchAlerts } from '../store/alertSlice'
import websocketService from '../services/websocketService'

const Dashboard: React.FC = () => {
  const dispatch = useDispatch()
  const { alerts } = useSelector((state: any) => state.alerts)

  useEffect(() => {
    dispatch(fetchAlerts() as any)
    websocketService.connect()

    return () => {
      websocketService.disconnect()
    }
  }, [dispatch])

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <SecurityScore />
        </Grid>
        <Grid item xs={12} md={8}>
          <ThreatChart />
        </Grid>
        <Grid item xs={12} md={6}>
          <AlertFeed />
        </Grid>
        <Grid item xs={12} md={6}>
          <QuickActions />
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard
```

### 6.3 Scan Page

```typescript
// src/pages/Scan.tsx
import React, { useState } from 'react'
import { Box, Typography, Tabs, Tab } from '@mui/material'
import URLScanner from '../components/scanning/URLScanner'
import FileScanner from '../components/scanning/FileScanner'

const Scan: React.FC = () => {
  const [tabValue, setTabValue] = useState(0)

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue)
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Scan
      </Typography>
      <Tabs value={tabValue} onChange={handleTabChange}>
        <Tab label="URL Scanner" />
        <Tab label="File Scanner" />
      </Tabs>
      <Box sx={{ mt: 3 }}>
        {tabValue === 0 && <URLScanner />}
        {tabValue === 1 && <FileScanner />}
      </Box>
    </Box>
  )
}

export default Scan
```

---

## 7. COMPONENTS

### 7.1 Layout Component

```typescript
// src/components/common/Layout.tsx
import React, { useState } from 'react'
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Divider,
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
  Security as SecurityIcon,
  Warning as WarningIcon,
  Monitor as MonitorIcon,
  Settings as SettingsIcon,
  Menu as MenuIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material'
import { useNavigate, useLocation } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { logout } from '../../store/authSlice'

const drawerWidth = 240

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/dashboard' },
  { text: 'Scan', icon: <SecurityIcon />, path: '/scan' },
  { text: 'Alerts', icon: <WarningIcon />, path: '/alerts' },
  { text: 'Monitoring', icon: <MonitorIcon />, path: '/monitoring' },
  { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
]

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()
  const dispatch = useDispatch()

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen)
  }

  const handleLogout = () => {
    dispatch(logout() as any)
    navigate('/login')
  }

  const drawer = (
    <div>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          Digital Bodyguard
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem
            button
            key={item.text}
            selected={location.pathname === item.path}
            onClick={() => navigate(item.path)}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
        <Divider />
        <ListItem button onClick={handleLogout}>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Lout" />
        </ListItem>
      </List>
    </div>
  )

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            AI Digital Bodyguard
          </Typography>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {children}
      </Box>
    </Box>
  )
}

export default Layout
```

### 7.2 Security Score Component

```typescript
// src/components/dashboard/SecurityScore.tsx
import React from 'react'
import {
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  useTheme,
} from '@mui/material'

const SecurityScore: React.FC = () => {
  const theme = useTheme()
  const score = 85 // This would come from API

  const getScoreColor = (score: number) => {
    if (score >= 80) return theme.palette.success.main
    if (score >= 60) return theme.palette.warning.main
    return theme.palette.error.main
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Security Score
        </Typography>
        <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
          <Box sx={{ position: 'relative', display: 'inline-flex' }}>
            <CircularProgress
              variant="determinate"
              value={score}
              size={120}
              thickness={8}
              sx={{ color: getScoreColor(score) }}
            />
            <Box
              sx={{
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
                position: 'absolute',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Typography variant="h4" component="div" color="textPrimary">
                {score}
              </Typography>
            </Box>
          </Box>
        </Box>
        <Typography variant="body2" color="textSecondary" align="center">
          Your system is secure
        </Typography>
      </CardContent>
    </Card>
  )
}

export default SecurityScore
```

### 7.3 Threat Chart Component

```typescript
// src/components/dashboard/ThreatChart.tsx
import React from 'react'
import {
  Card,
  CardContent,
  Typography,
  Box,
} from '@mui/material'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const data = [
  { name: 'Mon', threats: 4 },
  { name: 'Tue', threats: 3 },
  { name: 'Wed', threats: 2 },
  { name: 'Thu', threats: 5 },
  { name: 'Fri', threats: 4 },
  { name: 'Sat', threats: 2 },
  { name: 'Sun', threats: 1 },
]

const ThreatChart: React.FC = () => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Threat Trends
        </Typography>
        <Box sx={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="threats"
                stroke="#ef4444"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  )
}

export default ThreatChart
```

### 7.4 URL Scanner Component

```typescript
// src/components/scanning/URLScanner.tsx
import React, { useState } from 'react'
import {
  Box,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Card,
  CardContent,
} from '@mui/material'
import { useDispatch } from 'react-redux'
import scanService from '../../services/scanService'

const URLScanner: React.FC = () => {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const dispatch = useDispatch()

  const handleScan = async () => {
    if (!url) return

    setLoading(true)
    try {
      const response = await scanService.scanURL(url)
      setResult(response)
    } catch (error) {
      console.error('Scan failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        URL Scanner
      </Typography>
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <TextField
          fullWidth
          label="Enter URL to scan"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
        />
        <Button
          variant="contained"
          onClick={handleScan}
          disabled={loading}
          sx={{ minWidth: 120 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Scan'}
        </Button>
      </Box>

      {result && (
        <Alert
          severity={result.is_phishing ? 'error' : 'success'}
          sx={{ mb: 2 }}
        >
          {result.is_phishing
            ? `Phishing detected! Probability: ${(result.probability * 100).toFixed(2)}%`
            : `URL is safe. Probability: ${(result.probability * 100).toFixed(2)}%`}
        </Alert>
      )}
    </Box>
  )
}

export default URLScanner
```

---

## 8. HOOKS

### 8.1 Use Auth Hook

```typescript
// src/hooks/useAuth.ts
import { useSelector, useDispatch } from 'react-redux'
import { RootState, AppDispatch } from '../store'

export const useAuth = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { user, token, isAuthenticated } = useSelector(
    (state: RootState) => state.auth
  )

  return {
    user,
    token,
    isAuthenticated,
    dispatch,
  }
}
```

### 8.2 Use WebSocket Hook

```typescript
// src/hooks/useWebSocket.ts
import { useEffect, useCallback } from 'react'
import websocketService from '../services/websocketService'

export const useWebSocket = (event: string, callback: Function) => {
  useEffect(() => {
    websocketService.on(event, callback)

    return () => {
      websocketService.off(event, callback)
    }
  }, [event, callback])
}
```

---

## 9. TYPES

### 9.1 Auth Types

```typescript
// src/types/auth.ts
export interface User {
  id: string
  email: string
  first_name?: string
  last_name?: string
  role: string
  is_active: boolean
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  first_name?: string
  last_name?: string
}
```

### 9.2 Alert Types

```typescript
// src/types/alert.ts
export interface Alert {
  id: string
  user_id: string
  type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  title: string
  message?: string
  data?: any
  status: 'new' | 'acknowledged' | 'dismissed'
  created_at: string
}
```

---

## 10. DEPLOYMENT

### 10.1 Dockerfile

```dockerfile
# Build stage
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 10.2 Nginx Config

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 10.3 Docker Compose

```yaml
version: '3.8'

services:
  frontend:
    build: .
    ports:
      - "3000:80"
    depends_on:
      - backend
```

---

## 11. CONCLUSION

This document provides complete implementation for the React Dashboard frontend including:

- **Project Setup**: Vite, TypeScript, Tailwind CSS configuration
- **Redux Store**: State management with Redux Toolkit
- **API Services**: Axios-based API client with interceptors
- **WebSocket**: Real-time updates with Socket.io
- **Pages**: Login, Dashboard, Scan, Alerts, Monitoring
- **Components**: Layout, Security Score, Threat Chart, URL Scanner
- **Hooks**: Custom hooks for auth and WebSocket
- **Types**: TypeScript type definitions
- **Deployment**: Docker and Nginx configuration

**Next Steps:**
1. Install dependencies
2. Configure environment variables
3. Connect to backend API
4. Implement remaining components
5. Test all features
6. Deploy to production

---

## APPENDICES

### Appendix A: Environment Variables

```env
# .env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Appendix B: Build Commands

```bash
# Development
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### Appendix C: Material-UI Theme Customization

```typescript
// src/theme.ts
import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    primary: {
      main: '#0ea5e9',
    },
    secondary: {
      main: '#6366f1',
    },
    background: {
      default: '#f8fafc',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
      },
    },
  },
})

export default theme
```
