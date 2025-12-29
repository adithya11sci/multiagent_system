# Railway Intelligence Multi-Agent System
# Startup Script - Start both backend and frontend

Write-Host "🚂 Starting Railway Intelligence Multi-Agent System..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path ".\venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Please run setup first." -ForegroundColor Red
    Write-Host "   Run: .\quickstart.ps1" -ForegroundColor Yellow
    exit 1
}

# Check if frontend dependencies are installed
if (-not (Test-Path ".\frontend\node_modules")) {
    Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    Set-Location ..
}

# Start backend server in a new window
Write-Host "🔧 Starting Backend API Server..." -ForegroundColor Green
$backendScript = @"
Set-Location '$PWD'
.\venv\Scripts\Activate.ps1
Write-Host '🚀 Backend API Server Starting on http://localhost:8000' -ForegroundColor Green
Write-Host '📚 API Documentation: http://localhost:8000/docs' -ForegroundColor Cyan
Write-Host ''
python api\server.py
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

# Wait for backend to initialize
Write-Host "⏳ Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

# Start frontend in a new window
Write-Host "🎨 Starting Frontend Dev Server..." -ForegroundColor Green
$frontendScript = @"
Set-Location '$PWD\frontend'
Write-Host '🚀 Frontend Dev Server Starting on http://localhost:3000' -ForegroundColor Green
Write-Host ''
npm run dev
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host ""
Write-Host "✅ System started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access Points:" -ForegroundColor Cyan
Write-Host "   Frontend UI:        http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API:        http://localhost:8000" -ForegroundColor White
Write-Host "   API Documentation:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "ℹ️  Two new PowerShell windows have been opened." -ForegroundColor Yellow
Write-Host "   Close them to stop the servers." -ForegroundColor Yellow
Write-Host ""
