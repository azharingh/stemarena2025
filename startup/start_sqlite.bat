@echo off
echo Starting STEM ARENA Application with SQLite...
echo.

echo Starting Backend Server (SQLite)...
cd "backend lessons"
start "Backend Server" cmd /k "uvicorn main_sqlite:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting Frontend Server...
cd ..
start "Frontend Server" cmd /k "python -m http.server 5500"

echo.
echo Both servers are starting...
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:5500/pj.html
echo.
echo Press any key to open the frontend in your browser...
pause >nul
start http://localhost:5500/pj.html 