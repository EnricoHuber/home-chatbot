# Quick Local Test Script for PowerShell
# Run this to test the bot locally before deploying

Write-Host "🧪 Home Chatbot - Local Test" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ Error: .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Creating .env from example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: Edit .env and add your credentials:" -ForegroundColor Yellow
    Write-Host "   - GROQ_API_KEY" -ForegroundColor Yellow
    Write-Host "   - TELEGRAM_BOT_TOKEN" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Then run this script again." -ForegroundColor Yellow
    exit 1
}

# Check if Python is installed
Write-Host "🔍 Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Python not found!" -ForegroundColor Red
    Write-Host "Install Python 3.11 from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if dependencies are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Cyan
$pipList = pip list 2>&1
if ($pipList -notmatch "python-telegram-bot") {
    Write-Host "⚠️  Dependencies not installed" -ForegroundColor Yellow
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

# Load .env and check required variables
Write-Host "🔍 Checking environment variables..." -ForegroundColor Cyan
$envContent = Get-Content ".env" -Raw
if ($envContent -match "GROQ_API_KEY=gsk_\w+") {
    Write-Host "✅ GROQ_API_KEY found" -ForegroundColor Green
} else {
    Write-Host "❌ GROQ_API_KEY not set in .env" -ForegroundColor Red
    Write-Host "Get your key from: https://console.groq.com/keys" -ForegroundColor Yellow
    exit 1
}

if ($envContent -match "TELEGRAM_BOT_TOKEN=\d+:\w+") {
    Write-Host "✅ TELEGRAM_BOT_TOKEN found" -ForegroundColor Green
} else {
    Write-Host "❌ TELEGRAM_BOT_TOKEN not set in .env" -ForegroundColor Red
    Write-Host "Get your token from: https://t.me/BotFather" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting bot in DEV mode..." -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Test these commands in Telegram:" -ForegroundColor Yellow
Write-Host "   /start" -ForegroundColor White
Write-Host "   /help" -ForegroundColor White
Write-Host "   /info" -ForegroundColor White
Write-Host "   /addknowledge generale This is a test" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Set environment to dev for testing
$env:ENVIRONMENT = "dev"

# Run the bot
python src/main.py
