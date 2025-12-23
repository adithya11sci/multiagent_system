# Quick Start Script for Railway Intelligence System
# Run this after installing dependencies and configuring .env

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚂 Railway Intelligence Multi-Agent System                  ║" -ForegroundColor Cyan
Write-Host "║  Quick Start Setup                                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "🔍 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor Green

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host ""
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "   ✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "   ✅ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "   ✅ Dependencies installed" -ForegroundColor Green

# Check for .env file
Write-Host ""
Write-Host "⚙️  Checking configuration..." -ForegroundColor Yellow
if (-Not (Test-Path ".env")) {
    Write-Host "   ⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "   Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "   ⚠️  IMPORTANT: Edit .env and add your GEMINI_API_KEY" -ForegroundColor Red
    Write-Host "   Get your key from: https://makersuite.google.com/app/apikey" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "   Would you like to edit .env now? (y/n)"
    if ($response -eq "y") {
        notepad .env
    }
} else {
    Write-Host "   ✅ .env file found" -ForegroundColor Green
}

# Create necessary directories
Write-Host ""
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
$dirs = @("data\rag", "data\vector_store")
foreach ($dir in $dirs) {
    if (-Not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "   ✅ Directories created" -ForegroundColor Green

# Test imports
Write-Host ""
Write-Host "🧪 Testing imports..." -ForegroundColor Yellow
$testResult = python -c "import google.generativeai; import langchain; import chromadb; print('SUCCESS')" 2>&1
if ($testResult -match "SUCCESS") {
    Write-Host "   ✅ All imports successful" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Import test failed. Please check dependencies." -ForegroundColor Red
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ Setup Complete!                                          ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Cyan
Write-Host "   1. Make sure your GEMINI_API_KEY is set in .env" -ForegroundColor White
Write-Host "   2. Run the system: python main.py" -ForegroundColor White
Write-Host "   3. Choose a demo scenario or use interactive mode" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - README.md: Full documentation" -ForegroundColor White
Write-Host "   - SETUP.md: Detailed setup guide" -ForegroundColor White
Write-Host ""
Write-Host "Would you like to start the system now? (y/n): " -ForegroundColor Yellow -NoNewline
$start = Read-Host
if ($start -eq "y") {
    Write-Host ""
    python main.py
}
