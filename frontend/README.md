# Railway Intelligence Multi-Agent System - Frontend

A modern React-based frontend for the Railway Intelligence Multi-Agent System, providing an intuitive interface to interact with AI-powered railway management agents.

## 🚀 Features

- **Dashboard** - Real-time system overview and quick actions
- **Train Delay Management** - Handle train delays with automated AI responses
- **Passenger Query Assistant** - RAG-powered customer service
- **Crowd Prediction** - AI-driven capacity optimization
- **Multi-Channel Alerts** - SMS, Email, and Push notifications
- **Agent Status Monitoring** - Track all 5 specialized AI agents

## 🛠️ Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - API communication
- **Heroicons** - Icon library
- **React Hot Toast** - Notifications

## 📦 Installation

### Prerequisites

- Node.js 18+ or npm/yarn
- Python backend server running (see parent directory)

### Setup Steps

1. **Navigate to frontend directory**
   ```powershell
   cd frontend
   ```

2. **Install dependencies**
   ```powershell
   npm install
   ```

3. **Configure environment**
   ```powershell
   cp .env.example .env
   ```
   
   Edit `.env` if your backend runs on a different port:
   ```
   VITE_API_URL=http://localhost:8000
   ```

4. **Start development server**
   ```powershell
   npm run dev
   ```

   The frontend will be available at http://localhost:3000

## 🏗️ Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable components
│   │   └── Layout.tsx   # Main layout with navigation
│   ├── pages/           # Page components
│   │   ├── Dashboard.tsx
│   │   ├── TrainDelay.tsx
│   │   ├── PassengerQuery.tsx
│   │   ├── CrowdPrediction.tsx
│   │   ├── Alerts.tsx
│   │   └── Agents.tsx
│   ├── services/        # API services
│   │   └── api.ts       # API client
│   ├── App.tsx          # Root component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

## 🎯 Usage

### Starting the Complete System

1. **Start the backend API server** (from parent directory):
   ```powershell
   cd ..
   python api/server.py
   ```

2. **Start the frontend dev server** (in frontend directory):
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Key Features Guide

#### 1. Dashboard
- System health monitoring
- Quick access to all features
- Agent status overview
- Real-time statistics

#### 2. Train Delay Management
- Report train delays
- Get AI-powered recommendations
- Automated passenger notifications
- Cascading impact analysis

#### 3. Passenger Query Assistant
- Ask questions in natural language
- RAG-powered accurate responses
- Policy and refund information
- Alternative route suggestions

#### 4. Crowd Prediction
- Predict overcrowding
- Capacity optimization
- Historical pattern analysis
- Proactive recommendations

#### 5. Multi-Channel Alerts
- Send SMS via Twilio
- Email notifications via SMTP
- Push notifications
- Bulk recipient management

#### 6. Agent Status
- Monitor all 5 AI agents
- Real-time status updates
- Agent capabilities overview
- Workflow visualization

## 🔧 Development

### Available Scripts

```powershell
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Code Style

- TypeScript for type safety
- Functional React components with hooks
- Tailwind CSS for styling
- ESLint and Prettier for code quality

### Adding New Features

1. Create new page component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation item in `src/components/Layout.tsx`
4. Add API method in `src/services/api.ts` if needed

## 🚀 Production Build

```powershell
# Build optimized production bundle
npm run build

# Output will be in dist/ directory
# Serve with any static file server
```

## 🐛 Troubleshooting

### Backend Connection Issues

If you see "Failed to connect to backend":

1. Ensure backend server is running:
   ```powershell
   python api/server.py
   ```

2. Check backend URL in `.env`:
   ```
   VITE_API_URL=http://localhost:8000
   ```

3. Verify CORS settings in backend `api/server.py`

### Port Conflicts

If port 3000 is in use, Vite will suggest an alternative port. Update your browser URL accordingly.

### Build Errors

Clear node_modules and reinstall:
```powershell
Remove-Item -Recurse -Force node_modules
npm install
```

## 📱 Responsive Design

The frontend is fully responsive and works on:
- Desktop (1920x1080+)
- Laptop (1366x768+)
- Tablet (768x1024)
- Mobile (375x667+)

## 🎨 Customization

### Theme Colors

Edit `tailwind.config.js` to customize colors:

```javascript
theme: {
  extend: {
    colors: {
      primary: { /* your colors */ },
      railway: { /* your colors */ }
    }
  }
}
```

### API Endpoints

Modify `src/services/api.ts` to add/change endpoints.

## 📄 License

Part of the Railway Intelligence Multi-Agent System project.

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📞 Support

For issues or questions, please refer to the main project documentation in the parent directory.
