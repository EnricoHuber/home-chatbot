# Quick Docker Test Script
# Builds and runs your bot in Docker Desktop

Write-Host "🐳 Docker Local Test" -ForegroundColor Cyan
Write-Host "====================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "🔍 Checking Docker..." -ForegroundColor Cyan
try {
    docker --version | Out-Null
    Write-Host "✅ Docker is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker daemon is running
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker Desktop is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Docker Desktop is running" -ForegroundColor Green

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from example..." -ForegroundColor Cyan
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

Write-Host "✅ .env file found" -ForegroundColor Green
Write-Host ""

# Stop and remove existing container if exists
Write-Host "🧹 Cleaning up old containers..." -ForegroundColor Cyan
docker stop home-chatbot 2>$null | Out-Null
docker rm home-chatbot 2>$null | Out-Null
Write-Host "✅ Cleanup complete" -ForegroundColor Green
Write-Host ""

# Build image
Write-Host "🔨 Building Docker image (this may take 3-5 minutes)..." -ForegroundColor Cyan
docker build -t home-chatbot . --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Write-Host "Check the error messages above." -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Image built successfully" -ForegroundColor Green
Write-Host ""

# Run container
Write-Host "🚀 Starting container..." -ForegroundColor Cyan
docker run -d `
    --name home-chatbot `
    --env-file .env `
    -e ENVIRONMENT=dev `
    -p 10000:10000 `
    -v "${PWD}/chroma_db:/app/chroma_db" `
    -v "${PWD}/logs:/app/logs" `
    home-chatbot

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start container!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Container started!" -ForegroundColor Green
Write-Host ""

# Wait for bot to start
Write-Host "⏳ Waiting for bot to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# Show logs
Write-Host ""
Write-Host "📋 Container logs:" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan
docker logs home-chatbot

Write-Host ""
Write-Host "✅ Bot is running in Docker!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Useful commands:" -ForegroundColor Yellow
Write-Host "   docker logs -f home-chatbot      # Follow logs" -ForegroundColor White
Write-Host "   docker stop home-chatbot         # Stop bot" -ForegroundColor White
Write-Host "   docker start home-chatbot        # Start bot" -ForegroundColor White
Write-Host "   docker restart home-chatbot      # Restart bot" -ForegroundColor White
Write-Host "   docker exec -it home-chatbot /bin/bash  # Access shell" -ForegroundColor White
Write-Host ""
Write-Host "🧪 Test your bot in Telegram now!" -ForegroundColor Green
Write-Host "   /start" -ForegroundColor White
Write-Host "   /help" -ForegroundColor White
Write-Host "   /addknowledge generale Test from Docker" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Health check: http://localhost:10000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 View logs: docker logs -f home-chatbot" -ForegroundColor Yellow
Write-Host "🛑 Stop: docker stop home-chatbot" -ForegroundColor Yellow
