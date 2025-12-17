# Quick Start Script
# Sets up the environment and runs basic tests

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Multi-Agent System - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -q
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "⚠ .env file not found!" -ForegroundColor Yellow
    Write-Host "Copying .env.example to .env..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Please edit .env with your API keys!" -ForegroundColor Red
    Write-Host "Required:" -ForegroundColor Yellow
    Write-Host "  - OPENAI_API_KEY" -ForegroundColor Yellow
    Write-Host "  - TWILIO_ACCOUNT_SID" -ForegroundColor Yellow
    Write-Host "  - TWILIO_AUTH_TOKEN" -ForegroundColor Yellow
    Write-Host "  - SECRET_KEY" -ForegroundColor Yellow
    Write-Host ""
    
    # Open .env in default editor
    Write-Host "Opening .env in editor..." -ForegroundColor Yellow
    Start-Process notepad.exe ".env"
    
    Write-Host ""
    Write-Host "Press any key after you've configured .env..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Running System Tests" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

python scripts\test_system.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Setup Gmail OAuth (optional):" -ForegroundColor White
Write-Host "   python scripts\setup_gmail_auth.py --user-id default --test" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the server:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Test with ngrok (for WhatsApp):" -ForegroundColor White
Write-Host "   ngrok http 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "See SETUP.md for detailed instructions." -ForegroundColor White
Write-Host ""
