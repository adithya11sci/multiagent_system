# 🚀 Quick Start Guide - Frontend Installation & Testing

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Virtual environment set up (`venv` folder exists)
- [ ] Backend dependencies installed
- [ ] GEMINI_API_KEY configured in `.env`

## Step-by-Step Installation

### Step 1: Install Backend Dependencies

```powershell
# Navigate to project root
cd d:\multiagent

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install/update backend dependencies
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

```powershell
# Navigate to frontend directory
cd frontend

# Install all npm packages
npm install
```

This will install:
- React 18.2.0
- TypeScript 5.3.3
- Vite 5.0.8
- Tailwind CSS 3.4.0
- And all other dependencies

### Step 3: Verify Installation

```powershell
# Check Node.js version
node --version
# Should show v18.x.x or higher

# Check npm version
npm --version
# Should show 9.x.x or higher

# Check Python version
python --version
# Should show Python 3.9.x or higher
```

## 🎯 Starting the System

### Option 1: Automated Start (Recommended)

```powershell
# From project root (d:\multiagent)
.\start-system.ps1
```

This opens two PowerShell windows:
1. **Backend Window** - API Server on port 8000
2. **Frontend Window** - Dev Server on port 3000

### Option 2: Manual Start

**Terminal 1 - Start Backend:**
```powershell
cd d:\multiagent
.\venv\Scripts\Activate.ps1
python api\server.py
```

Wait until you see:
```
✅ API Server initialized successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Start Frontend:**
```powershell
cd d:\multiagent\frontend
npm run dev
```

Wait until you see:
```
  VITE v5.0.8  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  press h to show help
```

## ✅ Verification Checklist

### Backend Verification

1. **Open Backend URL**: http://localhost:8000
   - Should show: `{"status":"online","service":"Railway Intelligence Multi-Agent System"...}`

2. **Check API Documentation**: http://localhost:8000/docs
   - Should show Swagger UI with all endpoints

3. **Test Health Endpoint**: http://localhost:8000/api/health
   - Should show: `{"status":"healthy","orchestrator":true...}`

### Frontend Verification

1. **Open Frontend URL**: http://localhost:3000
   - Should show the dashboard

2. **Check Browser Console** (F12):
   - Should have no red errors
   - May show some info logs (that's OK)

3. **Verify Dashboard Elements**:
   - [ ] "Welcome to Railway Intelligence System" banner
   - [ ] System stats cards (Active Agents, System Status, RAG System)
   - [ ] Quick action cards (4 cards)
   - [ ] Agent status section

4. **Test Navigation**:
   - [ ] Click "Train Delay" - page loads
   - [ ] Click "Passenger Query" - page loads
   - [ ] Click "Crowd Prediction" - page loads
   - [ ] Click "Alerts" - page loads
   - [ ] Click "Agents" - page loads
   - [ ] Click "Dashboard" - returns to home

## 🧪 Testing Each Feature

### Test 1: Dashboard

**Expected Behavior**:
- Shows "System Active" with green dot
- Shows "5 / 5" active agents
- Shows "Healthy" system status
- All quick action cards clickable

### Test 2: Train Delay

**Steps**:
1. Click "Load Example" button
2. Form fills with sample data
3. Click "Process Delay"
4. Wait for processing (should take 5-15 seconds)
5. Check for AI response

**Expected Result**:
- Summary box with AI analysis
- Operations analysis section
- Alerts sent confirmation

### Test 3: Passenger Query

**Steps**:
1. Click example: "What is the refund policy for cancelled trains?"
2. Click "Get Answer"
3. Wait for response

**Expected Result**:
- Green box with AI response
- Response should mention refund policies from knowledge base

### Test 4: Crowd Prediction

**Steps**:
1. Click "Load Example"
2. Click "Predict Crowd"
3. Wait for analysis

**Expected Result**:
- Crowd prediction results
- Recommendations if applicable

### Test 5: Alerts

**Steps**:
1. Click "Load Example"
2. Verify channels are selected
3. Click "Send Alert"

**Expected Result**:
- Success message
- Delivery status shown

### Test 6: Agents Page

**Expected Behavior**:
- All 5 agents shown
- Each agent shows "active" status
- Agent capabilities listed
- Workflow diagram visible

## 🐛 Common Issues & Solutions

### Issue 1: "Cannot connect to backend"

**Symptoms**: Dashboard shows error toast

**Solutions**:
```powershell
# 1. Check if backend is running
# Open: http://localhost:8000
# Should show JSON response

# 2. Restart backend
cd d:\multiagent
.\venv\Scripts\Activate.ps1
python api\server.py

# 3. Check firewall settings
# Ensure ports 8000 and 3000 are not blocked
```

### Issue 2: "npm install" fails

**Symptoms**: Errors during npm install

**Solutions**:
```powershell
# 1. Clear npm cache
npm cache clean --force

# 2. Delete node_modules and reinstall
Remove-Item -Recurse -Force node_modules
npm install

# 3. Try with different registry
npm install --registry https://registry.npmjs.org
```

### Issue 3: Frontend shows blank page

**Symptoms**: White screen, no content

**Solutions**:
```powershell
# 1. Check browser console (F12)
# Look for red errors

# 2. Clear browser cache
# Ctrl+Shift+Delete

# 3. Restart dev server
# Ctrl+C in frontend terminal
npm run dev
```

### Issue 4: "Module not found" errors

**Symptoms**: Import errors in console

**Solutions**:
```powershell
# Reinstall dependencies
cd frontend
Remove-Item -Recurse -Force node_modules
npm install
```

### Issue 5: Port 3000 already in use

**Symptoms**: Error about port in use

**Solutions**:
```powershell
# Option 1: Kill process on port 3000
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process

# Option 2: Use different port
npm run dev -- --port 3001
```

### Issue 6: Backend crashes on startup

**Symptoms**: Python errors in terminal

**Solutions**:
```powershell
# 1. Check Python dependencies
pip install -r requirements.txt

# 2. Verify GEMINI_API_KEY
# Check .env file in project root

# 3. Check if ChromaDB is causing issues
# Delete data/vector_store folder and reinitialize
```

## 📊 Performance Benchmarks

**Expected Performance**:
- Dashboard load: < 1 second
- API health check: < 100ms
- Train delay processing: 5-15 seconds
- Passenger query: 3-10 seconds
- Page navigation: < 200ms

If you experience slower performance:
1. Check internet connection (Gemini API requires internet)
2. Verify system resources (CPU, RAM)
3. Check for background processes

## 🎉 Success Indicators

When everything works correctly:
- ✅ Backend shows "API Server initialized successfully!"
- ✅ Frontend shows dashboard without errors
- ✅ All navigation links work
- ✅ At least one test scenario completes successfully
- ✅ Agent status page shows 5 active agents
- ✅ No red errors in browser console
- ✅ System health shows "healthy"

## 📸 Expected Screenshots

### Dashboard
```
┌────────────────────────────────────────┐
│ 🚂 Welcome to Railway Intelligence    │
│    AI-powered multi-agent system...    │
└────────────────────────────────────────┘

Stats: [Active Agents: 5/5] [Status: Healthy] [RAG: Active]

Quick Actions: [Train Delay] [Passenger Query] [Crowd] [Alerts]

Agent Status: ✓ Planner ✓ Operations ✓ Passenger ✓ Crowd ✓ Alert
```

### Successful API Call
```
✅ Train delay processed successfully!

Summary:
Train 12627 delayed 45 minutes. Impact analysis complete.
Passengers notified. Alternative arrangements suggested.

Operations Analysis:
- Cascading delays identified
- Resource reallocation recommended
...
```

## 🔄 Stopping the System

### Graceful Shutdown

1. **Frontend**: Press `Ctrl+C` in frontend terminal, then `Y`
2. **Backend**: Press `Ctrl+C` in backend terminal

### Force Stop

```powershell
# Stop all Node.js processes
Get-Process node | Stop-Process -Force

# Stop Python processes
Get-Process python | Stop-Process -Force
```

## 📝 Next Steps

Once installation is verified:
1. Read [FRONTEND_GUIDE.md](FRONTEND_GUIDE.md) for detailed documentation
2. Explore each page and feature
3. Try different scenarios
4. Check API documentation at `/docs`
5. Customize the UI if desired

## 💡 Tips

1. **Keep terminals open**: Don't close the PowerShell windows while using the system
2. **Use browser DevTools**: F12 for debugging
3. **Check logs**: Both terminals show useful logs
4. **Test systematically**: Go through each feature one by one
5. **Save work**: Before stopping, ensure no processes are running

## 🆘 Getting Help

If issues persist:
1. Check all documentation files
2. Review error messages carefully
3. Verify all prerequisites are met
4. Try a clean reinstall
5. Check system requirements

## 🎓 Learning Path

Recommended order to explore:
1. Dashboard - Get overview
2. Agents - Understand the system
3. Train Delay - See orchestration in action
4. Passenger Query - Experience RAG
5. Crowd Prediction - See AI predictions
6. Alerts - Test notifications

---

**You're all set! Enjoy your Railway Intelligence Multi-Agent System!** 🚂✨
