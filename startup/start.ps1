Write-Host "Starting STEM ARENA Application..." -ForegroundColor Green
Write-Host ""

Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Set-Location "backend lessons"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python main.py" -WindowStyle Normal

Write-Host ""
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Set-Location ".."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m http.server 5500" -WindowStyle Normal

Write-Host ""
Write-Host "Both servers are starting..." -ForegroundColor Green
Write-Host "Backend: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5500/pj.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to open the frontend in your browser..." -ForegroundColor Yellow
Read-Host
Start-Process "http://localhost:5500/pj.html" 