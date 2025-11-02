# Quick Start - Just run this!

Write-Host "🚀 Installing and starting bot..." -ForegroundColor Cyan

# Install dependencies if needed
if (-not (pip list 2>&1 | Select-String "python-telegram-bot")) {
    pip install -r requirements.txt
}

# Set dev environment
$env:ENVIRONMENT = "dev"

# Run bot
python src/main.py
