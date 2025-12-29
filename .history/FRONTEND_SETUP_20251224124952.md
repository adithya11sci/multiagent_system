# Frontend Setup and Run Guide

## Quick Start

### 1. Install Dependencies

```powershell
cd frontend
npm install
```

### 2. Start Development Server

```powershell
npm run dev
```

The application will be available at **http://localhost:3000**

## Full System Startup

### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - Backend:**
```powershell
# From project root
cd d:\multiagent
.\venv\Scripts\Activate.ps1
python api\server.py
```

**Terminal 2 - Frontend:**
```powershell
# From project root
cd d:\multiagent\frontend
npm run dev
```

### Option 2: Quick Start Script

Create a file `start-system.ps1` in the project root:

```powershell
# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python api\server.py"

# Wait for backend to start
Start-Sleep -Seconds 5

# Start frontend
cd frontend
npm run dev
```

Then run:
```powershell
.\start-system.ps1
```

## Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## Troubleshooting

### Backend not responding

1. Check if backend is running on port 8000
2. Verify `.env` file has correct API URL
3. Check terminal for error messages

### Frontend build errors

```powershell
# Clear cache and reinstall
Remove-Item -Recurse -Force node_modules, package-lock.json
npm install
```

### Port already in use

If port 3000 is busy, Vite will automatically use the next available port (3001, 3002, etc.)

## Production Build

```powershell
cd frontend
npm run build
```

Output will be in `frontend/dist/` directory.
