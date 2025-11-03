# Quick Supabase + Docker Test

Write-Host "🐳 Testing Supabase with Docker" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "Creating from example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  Edit .env and add:" -ForegroundColor Yellow
    Write-Host "   - GROQ_API_KEY" -ForegroundColor White
    Write-Host "   - TELEGRAM_BOT_TOKEN" -ForegroundColor White
    Write-Host "   - SUPABASE_URL" -ForegroundColor White
    Write-Host "   - SUPABASE_KEY" -ForegroundColor White
    Write-Host "   - ENVIRONMENT=production" -ForegroundColor White
    Write-Host ""
    notepad .env
    exit 1
}

# Check if Docker is running
Write-Host "🔍 Checking Docker..." -ForegroundColor Cyan
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker Desktop is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Docker is running" -ForegroundColor Green

# Check for Supabase credentials
Write-Host "🔍 Checking Supabase credentials..." -ForegroundColor Cyan
$envContent = Get-Content ".env" -Raw

if ($envContent -match "SUPABASE_URL=https://\w+\.supabase\.co") {
    Write-Host "✅ SUPABASE_URL found" -ForegroundColor Green
} else {
    Write-Host "❌ SUPABASE_URL not set in .env" -ForegroundColor Red
    Write-Host "Follow SUPABASE_SETUP.md to get credentials" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Quick setup: https://supabase.com" -ForegroundColor Cyan
    exit 1
}

if ($envContent -match "SUPABASE_KEY=eyJ") {
    Write-Host "✅ SUPABASE_KEY found" -ForegroundColor Green
} else {
    Write-Host "❌ SUPABASE_KEY not set in .env" -ForegroundColor Red
    Write-Host "Follow SUPABASE_SETUP.md to get credentials" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting bot with Supabase storage..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Run docker-compose
docker-compose up --build

Write-Host ""
Write-Host "✅ Test complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Check Supabase dashboard for new data" -ForegroundColor White
Write-Host "   2. Test /addknowledge in Telegram" -ForegroundColor White
Write-Host "   3. Verify knowledge appears in Supabase" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop: docker-compose down" -ForegroundColor Yellow
