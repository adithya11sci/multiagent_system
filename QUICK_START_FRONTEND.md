# 🚀 Quick Reference Card

## Start the System

```powershell
.\start-system.ps1
```

## Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend UI | http://localhost:3000 | Web Interface |
| Backend API | http://localhost:8000 | API Server |
| API Docs | http://localhost:8000/docs | Swagger UI |

## Pages

| Page | Route | Purpose |
|------|-------|---------|
| Dashboard | `/` | System overview |
| Train Delay | `/train-delay` | Report delays |
| Passenger Query | `/passenger-query` | Ask questions |
| Crowd Prediction | `/crowd-prediction` | Predict capacity |
| Alerts | `/alerts` | Send notifications |
| Agents | `/agents` | Monitor agents |

## First Time Setup

```powershell
# 1. Install frontend dependencies
cd frontend
npm install

# 2. Start system
cd ..
.\start-system.ps1
```

## Manual Start

```powershell
# Terminal 1 - Backend
.\venv\Scripts\Activate.ps1
python api\server.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## Stop the System

Press `Ctrl+C` in both terminal windows

## Common Commands

```powershell
# Install dependencies
cd frontend && npm install

# Build frontend
cd frontend && npm run build

# Preview build
cd frontend && npm run preview

# Check health
curl http://localhost:8000/api/health
```

## File Locations

```
📁 Backend API:      api/server.py
📁 Frontend App:     frontend/src/
📁 Configuration:    frontend/.env
📁 Documentation:    FRONTEND_GUIDE.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend not connecting | Check if running on port 8000 |
| Frontend errors | Run `npm install` in frontend/ |
| Port in use | Change port or kill process |
| Build fails | Delete node_modules, reinstall |

## Key Features

✅ 6 Complete Pages  
✅ Real-time Monitoring  
✅ AI Agent Integration  
✅ Responsive Design  
✅ Type-Safe Code  
✅ API Documentation  

## Documentation Files

- `FRONTEND_SETUP.md` - Setup guide
- `FRONTEND_GUIDE.md` - Complete docs (400+ lines)
- `FRONTEND_IMPLEMENTATION.md` - Implementation details
- `INSTALLATION_TESTING_GUIDE.md` - Testing guide
- `FRONTEND_COMPLETE.md` - Summary

## Need Help?

1. Check FRONTEND_GUIDE.md
2. View API docs at /docs
3. Check browser console (F12)
4. Review terminal logs

---

**Your Railway AI System is ready! 🚂✨**
