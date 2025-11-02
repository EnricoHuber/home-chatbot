# Simple Docker Compose Runner

# Ensure .env exists
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  Created .env file - please edit it with your credentials!" -ForegroundColor Yellow
    notepad .env
    exit
}

# Run with docker-compose
Write-Host "🐳 Starting bot with Docker Compose..." -ForegroundColor Cyan
docker-compose up --build
