Write-Host "Starting STEM ARENA Application with SQLite..." -ForegroundColor Green
Write-Host ""

Write-Host "Starting Backend Server (SQLite)..." -ForegroundColor Yellow
Set-Location "backend lessons"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "uvicorn main_sqlite:app --reload --host 0.0.0.0 --port 8000" -WindowStyle Normal

Write-Host ""
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Set-Location ".."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m http.server 5500" -WindowStyle Normal

Write-Host ""
Write-Host "Both servers are starting..." -ForegroundColor Cyan
Write-Host "Backend: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "Frontend: http://localhost:5500/pj.html" -ForegroundColor White
Write-Host ""
Write-Host "Opening frontend in browser..." -ForegroundColor Green
Start-Sleep -Seconds 3
Start-Process "http://localhost:5500/pj.html" 