# Quick Setup Script for Home Assistant Chatbot
# Run this to check your environment

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host "  Home Assistant Chatbot - Environment Check" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/6] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.1[1-9]") {
    Write-Host "  ✓ Python version OK: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python 3.11+ required. Found: $pythonVersion" -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
}
Write-Host ""

# Check if virtual environment exists
Write-Host "[2/6] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ✓ Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "  ! Virtual environment not found" -ForegroundColor Yellow
    Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Check .env file
Write-Host "[3/6] Checking environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✓ .env file found" -ForegroundColor Green
    
    # Check for required variables
    $envContent = Get-Content .env -Raw
    $hasGroq = $envContent -match "GROQ_API_KEY=.+"
    $hasTelegram = $envContent -match "TELEGRAM_BOT_TOKEN=.+"
    
    if ($hasGroq) {
        Write-Host "  ✓ GROQ_API_KEY is set" -ForegroundColor Green
    } else {
        Write-Host "  ✗ GROQ_API_KEY not set in .env" -ForegroundColor Red
        Write-Host "    Get your key: https://console.groq.com/keys" -ForegroundColor Yellow
    }
    
    if ($hasTelegram) {
        Write-Host "  ✓ TELEGRAM_BOT_TOKEN is set" -ForegroundColor Green
    } else {
        Write-Host "  ✗ TELEGRAM_BOT_TOKEN not set in .env" -ForegroundColor Red
        Write-Host "    Get your token from: https://t.me/BotFather" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ! .env file not found" -ForegroundColor Yellow
    Write-Host "  Copying from .env.example..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "  ✓ .env file created" -ForegroundColor Green
    Write-Host "  ! Please edit .env and add your API keys" -ForegroundColor Yellow
}
Write-Host ""

# Check dependencies
Write-Host "[4/6] Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>&1
if ($pipList -match "python-telegram-bot") {
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  ! Dependencies not installed" -ForegroundColor Yellow
    Write-Host "  Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
    Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
}
Write-Host ""

# Check directories
Write-Host "[5/6] Checking directories..." -ForegroundColor Yellow
$dirs = @("logs", "chroma_db")
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ Directory exists: $dir" -ForegroundColor Green
    } else {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "  ✓ Directory created: $dir" -ForegroundColor Green
    }
}
Write-Host ""

# Final status
Write-Host "[6/6] Final Status" -ForegroundColor Yellow
Write-Host ""

$ready = $true
if (-not (Test-Path ".env")) { $ready = $false }
if (-not ($envContent -match "GROQ_API_KEY=.+")) { $ready = $false }
if (-not ($envContent -match "TELEGRAM_BOT_TOKEN=.+")) { $ready = $false }

if ($ready) {
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 58) -ForegroundColor Green
    Write-Host "  ✓ Environment is ready!" -ForegroundColor Green
    Write-Host "=" -NoNewline -ForegroundColor Green
    Write-Host ("=" * 58) -ForegroundColor Green
    Write-Host ""
    Write-Host "To start the bot:" -ForegroundColor Cyan
    Write-Host "  1. Activate virtual environment: .\venv\Scripts\activate" -ForegroundColor White
    Write-Host "  2. Run the bot: python src/main.py" -ForegroundColor White
    Write-Host ""
    Write-Host "To deploy:" -ForegroundColor Cyan
    Write-Host "  - See DEPLOYMENT.md for free hosting options" -ForegroundColor White
    Write-Host "  - Railway.app recommended for demos" -ForegroundColor White
} else {
    Write-Host "=" -NoNewline -ForegroundColor Red
    Write-Host ("=" * 58) -ForegroundColor Red
    Write-Host "  ! Setup incomplete" -ForegroundColor Red
    Write-Host "=" -NoNewline -ForegroundColor Red
    Write-Host ("=" * 58) -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "  1. Edit .env file with your API keys" -ForegroundColor White
    Write-Host "  2. Get GROQ_API_KEY: https://console.groq.com/keys" -ForegroundColor White
    Write-Host "  3. Get TELEGRAM_BOT_TOKEN: https://t.me/BotFather" -ForegroundColor White
    Write-Host "  4. Run this script again" -ForegroundColor White
}

Write-Host ""
Write-Host "Documentation:" -ForegroundColor Cyan
Write-Host "  - README_NEW.md   : Full documentation" -ForegroundColor White
Write-Host "  - DEPLOYMENT.md   : Deployment guide" -ForegroundColor White
Write-Host "  - SUMMARY.md      : Quick summary" -ForegroundColor White
Write-Host ""
