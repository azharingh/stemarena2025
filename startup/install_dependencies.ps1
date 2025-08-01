Write-Host "Installing STEM ARENA Dependencies..." -ForegroundColor Green
Write-Host ""

Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
Set-Location "backend lessons"
pip install -r requirements_flask.txt

Write-Host ""
Write-Host "Dependencies installed successfully!" -ForegroundColor Green
Write-Host "You can now run start.bat or start.ps1 to start the application." -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue" 