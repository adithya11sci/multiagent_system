# 🎯 Railway Intelligence Multi-Agent System - Complete Frontend Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Running the System](#running-the-system)
5. [Features Walkthrough](#features-walkthrough)
6. [API Integration](#api-integration)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

The frontend is a modern, responsive web application built with React and TypeScript that provides an intuitive interface to interact with the Railway Intelligence Multi-Agent System.

### Key Highlights
- **Modern Stack**: React 18, TypeScript, Vite, Tailwind CSS
- **Real-time**: WebSocket support for live updates
- **Responsive**: Works on desktop, tablet, and mobile
- **Type-Safe**: Full TypeScript implementation
- **Fast**: Vite for instant hot module replacement

---

## 🏗️ Architecture

### Frontend Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout.tsx          # Main layout with sidebar navigation
│   ├── pages/
│   │   ├── Dashboard.tsx       # System overview & quick actions
│   │   ├── TrainDelay.tsx      # Train delay management
│   │   ├── PassengerQuery.tsx  # RAG-powered queries
│   │   ├── CrowdPrediction.tsx # Capacity optimization
│   │   ├── Alerts.tsx          # Multi-channel notifications
│   │   └── Agents.tsx          # Agent status monitoring
│   ├── services/
│   │   └── api.ts              # Axios-based API client
│   ├── App.tsx                 # Root component with routing
│   └── main.tsx                # Application entry point
├── public/                     # Static assets
├── index.html                  # HTML template
├── package.json                # Dependencies
├── vite.config.ts              # Vite configuration
├── tailwind.config.js          # Tailwind CSS config
└── tsconfig.json               # TypeScript config
```

### Backend API

```
api/
└── server.py                   # FastAPI server with REST endpoints
```

### Integration Flow

```
┌─────────────┐      HTTP/REST      ┌─────────────┐
│   React     │ ◄─────────────────► │   FastAPI   │
│   Frontend  │                     │   Backend   │
│  (Port 3000)│      WebSocket      │  (Port 8000)│
└─────────────┘ ◄─────────────────► └─────────────┘
                                            │
                                            ▼
                                    ┌─────────────┐
                                    │  LangGraph  │
                                    │ Orchestrator│
                                    └─────────────┘
                                            │
                        ┌───────────────────┼───────────────────┐
                        ▼                   ▼                   ▼
                   ┌─────────┐        ┌─────────┐        ┌─────────┐
                   │Operations│        │Passenger│        │  Crowd  │
                   │  Agent  │        │  Agent  │        │  Agent  │
                   └─────────┘        └─────────┘        └─────────┘
```

---

## 📦 Installation

### Prerequisites

1. **Node.js** (v18 or higher)
   - Download from: https://nodejs.org/
   - Verify: `node --version`

2. **Python Backend** (must be set up first)
   - See main project README

### Step-by-Step Setup

#### 1. Navigate to Frontend Directory

```powershell
cd d:\multiagent\frontend
```

#### 2. Install Dependencies

```powershell
npm install
```

This installs:
- React & React Router
- TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Axios (HTTP client)
- Heroicons (icons)
- React Hot Toast (notifications)

#### 3. Configure Environment

The `.env` file is already created with default settings:

```env
VITE_API_URL=http://localhost:8000
```

Change this if your backend runs on a different port.

---

## 🚀 Running the System

### Method 1: Automated Startup (Recommended)

From the project root directory:

```powershell
.\start-system.ps1
```

This will:
1. Start the backend API server (Port 8000)
2. Start the frontend dev server (Port 3000)
3. Open two PowerShell windows

### Method 2: Manual Startup

**Terminal 1 - Backend:**
```powershell
cd d:\multiagent
.\venv\Scripts\Activate.ps1
python api\server.py
```

**Terminal 2 - Frontend:**
```powershell
cd d:\multiagent\frontend
npm run dev
```

### Access Points

Once started, access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Interactive Swagger UI)

---

## 🎯 Features Walkthrough

### 1. Dashboard (`/`)

**Purpose**: System overview and quick access to all features

**Features**:
- System health status
- Active agents count
- RAG system status
- Quick action cards
- Agent status overview
- System information

**Screenshot Flow**:
```
┌─────────────────────────────────────────┐
│  🚂 Railway Intelligence System         │
│  AI-powered multi-agent system...       │
└─────────────────────────────────────────┘

┌──────────┐  ┌──────────┐  ┌──────────┐
│ Active   │  │ System   │  │   RAG    │
│ Agents   │  │ Status   │  │  System  │
│   5/5    │  │ Healthy  │  │  Active  │
└──────────┘  └──────────┘  └──────────┘

Quick Actions:
┌──────────────┐ ┌──────────────┐
│ 🕐 Report    │ │ 👥 Passenger │
│ Train Delay  │ │    Query     │
└──────────────┘ └──────────────┘
```

### 2. Train Delay Management (`/train-delay`)

**Purpose**: Handle train delays with AI automation

**Features**:
- Delay information input form
- AI-powered analysis
- Automated recommendations
- Passenger notifications
- Cascading impact analysis

**Usage Flow**:
1. Enter train number (e.g., 12627)
2. Enter delay minutes (e.g., 45)
3. Enter current location (e.g., Katpadi Junction)
4. Optional: Affected passenger count
5. Click "Process Delay"
6. AI agents analyze and provide:
   - Operations analysis
   - Recommended actions
   - Automated alerts sent
   - Impact assessment

### 3. Passenger Query Assistant (`/passenger-query`)

**Purpose**: RAG-powered customer service

**Features**:
- Natural language query input
- Knowledge base retrieval
- Accurate policy information
- Alternative suggestions
- Example queries

**Usage Flow**:
1. Type your question (or click example)
2. Click "Get Answer"
3. AI searches knowledge base (RAG)
4. Provides accurate, sourced answer

**Example Queries**:
- "What is the refund policy for cancelled trains?"
- "How do I book a ticket from Chennai to Bangalore?"
- "What are the train timings for route Chennai-Mumbai?"

### 4. Crowd Prediction (`/crowd-prediction`)

**Purpose**: AI-driven capacity optimization

**Features**:
- Crowd level prediction
- Historical pattern analysis
- Capacity recommendations
- Proactive suggestions

**Usage Flow**:
1. Enter train number
2. Enter route (e.g., Chennai-Bangalore)
3. Optional: Select time
4. Click "Predict Crowd"
5. Get predictions and recommendations

### 5. Multi-Channel Alerts (`/alerts`)

**Purpose**: Send notifications through multiple channels

**Features**:
- SMS notifications (Twilio)
- Email alerts (SMTP)
- Push notifications
- Bulk recipients
- Pre-defined scenarios

**Usage Flow**:
1. Write alert message
2. Enter recipients (comma-separated)
3. Select channels (SMS, Email, Push)
4. Click "Send Alert"
5. View delivery status

**Common Scenarios**:
- Train delays
- Platform changes
- Cancellations
- Emergency alerts

### 6. Agent Status (`/agents`)

**Purpose**: Monitor AI agents

**Features**:
- Real-time agent status
- Agent capabilities overview
- Workflow visualization
- Technical details

**Agents Overview**:
1. **Planner Agent** 🧠 - Master coordinator
2. **Operations Agent** ⚙️ - Train management
3. **Passenger Agent** 👥 - Customer service
4. **Crowd Agent** 📊 - Capacity optimization
5. **Alert Agent** 🔔 - Notifications

---

## 🔌 API Integration

### API Service (`src/services/api.ts`)

The frontend communicates with the backend through a centralized API service:

```typescript
// Example usage in a component
import apiService from '../services/api'

// Handle train delay
const result = await apiService.handleTrainDelay({
  train_number: '12627',
  delay_minutes: 45,
  current_location: 'Katpadi',
  affected_passengers: 850
})

// Passenger query
const answer = await apiService.passengerQuery('What is the refund policy?')

// Get agent status
const agents = await apiService.getAgentsStatus()
```

### Available API Methods

```typescript
// Health check
healthCheck(): Promise<HealthResponse>

// Main orchestration
orchestrate(request: string, context?: any): Promise<Response>

// Train delay
handleTrainDelay(data: TrainDelayRequest): Promise<Response>

// Passenger query
passengerQuery(query: string, passenger_id?: string): Promise<Response>

// Crowd prediction
predictCrowd(data: CrowdPredictionRequest): Promise<Response>

// Send alert
sendAlert(data: AlertRequest): Promise<Response>

// Agent status
getAgentsStatus(): Promise<AgentStatusResponse>

// RAG query
queryRAG(query: string): Promise<RAGResponse>

// Demo scenarios
getDemoScenarios(): Promise<ScenariosResponse>

// WebSocket
createWebSocket(): WebSocket
```

### API Response Format

All API responses follow this structure:

```typescript
{
  success: boolean
  data?: {
    final_response: { summary: string }
    operations_result: any[]
    passenger_result: any[]
    crowd_result: any[]
    alert_result: any[]
  }
  error?: string
  timestamp: string
}
```

---

## 🎨 Customization

### Changing Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        500: '#3b82f6',  // Change primary blue
        // ... other shades
      },
      railway: {
        blue: '#003087',    // Railway brand blue
        red: '#FF0000',     // Alert red
        green: '#00A651',   // Success green
        orange: '#FF6B35',  // Warning orange
      }
    }
  }
}
```

### Adding New Pages

1. **Create page component** in `src/pages/NewPage.tsx`:
```tsx
export default function NewPage() {
  return (
    <div>
      <h1>New Page</h1>
    </div>
  )
}
```

2. **Add route** in `src/App.tsx`:
```tsx
<Route path="/new-page" element={<NewPage />} />
```

3. **Add navigation** in `src/components/Layout.tsx`:
```tsx
const navigation = [
  // ... existing items
  { name: 'New Page', href: '/new-page', icon: SomeIcon },
]
```

### Modifying API Endpoints

Edit `src/services/api.ts`:

```typescript
async customEndpoint(data: any) {
  const response = await this.api.post('/api/custom', data)
  return response.data
}
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. "Failed to connect to backend"

**Problem**: Frontend can't reach backend API

**Solutions**:
- Verify backend is running: http://localhost:8000
- Check `.env` file has correct URL
- Ensure no firewall blocking port 8000
- Check backend terminal for errors

#### 2. "Module not found" errors

**Problem**: Missing dependencies

**Solution**:
```powershell
Remove-Item -Recurse -Force node_modules
npm install
```

#### 3. Port 3000 already in use

**Problem**: Another app using port 3000

**Solution**: Vite will auto-suggest alternative port (3001, 3002, etc.)
Or manually specify:
```powershell
npm run dev -- --port 3001
```

#### 4. Build fails

**Problem**: TypeScript or build errors

**Solutions**:
```powershell
# Clear cache
Remove-Item -Recurse -Force node_modules .vite
npm install

# Check for TypeScript errors
npm run build
```

#### 5. Styling doesn't work

**Problem**: Tailwind CSS not loading

**Solution**:
```powershell
# Rebuild Tailwind
npx tailwindcss -i ./src/index.css -o ./dist/output.css
```

#### 6. WebSocket connection fails

**Problem**: Real-time updates not working

**Solutions**:
- Check backend WebSocket endpoint: ws://localhost:8000/ws
- Verify backend has WebSocket support
- Check browser console for connection errors

### Debug Mode

Enable verbose logging:

```typescript
// In src/services/api.ts
constructor() {
  // ... existing code
  
  // Add response logging
  this.api.interceptors.response.use(
    (response) => {
      console.log('API Response:', response)  // Debug log
      return response
    }
  )
}
```

---

## 📈 Performance Tips

### Production Build

```powershell
npm run build
```

Optimizations:
- Code splitting
- Minification
- Tree shaking
- Asset optimization

### Lazy Loading

Add lazy loading for routes:

```tsx
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>
```

---

## 🔒 Security Notes

1. **API Keys**: Never commit API keys to frontend code
2. **Environment Variables**: Use `.env` for configuration
3. **CORS**: Backend has CORS configured for development
4. **Production**: Use environment-specific `.env` files

---

## 📱 Mobile Responsiveness

The UI is fully responsive:
- **Desktop**: Full sidebar, expanded cards
- **Tablet**: Collapsible sidebar, optimized layout
- **Mobile**: Hidden sidebar, mobile menu, stacked cards

Test on different screens:
- Chrome DevTools (F12 → Device Toolbar)
- Browser zoom levels
- Actual devices

---

## 🚀 Deployment

### Building for Production

```powershell
npm run build
```

Output in `dist/` directory.

### Serving Production Build

```powershell
npm run preview
```

Or use any static file server:
```powershell
npx serve dist
```

### Deploy to Hosting

Options:
- **Vercel**: `vercel deploy`
- **Netlify**: Drag & drop `dist/` folder
- **Azure Static Web Apps**: GitHub integration
- **AWS S3**: Upload `dist/` contents

---

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

---

## ✅ Checklist

Before running:
- [ ] Node.js 18+ installed
- [ ] Backend API running on port 8000
- [ ] Frontend dependencies installed (`npm install`)
- [ ] `.env` file configured
- [ ] No port conflicts

---

## 🎉 Success!

If everything is working, you should see:
- ✅ Backend API running on http://localhost:8000
- ✅ Frontend UI on http://localhost:3000
- ✅ Dashboard showing system status
- ✅ All 5 agents showing as "active"
- ✅ No errors in browser console

Enjoy your Railway Intelligence Multi-Agent System! 🚂✨
