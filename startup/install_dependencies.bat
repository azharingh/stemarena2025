@echo off
echo Installing STEM ARENA Dependencies...
echo.

echo Installing Python dependencies...
cd "backend lessons"
pip install -r requirements_flask.txt

echo.
echo Dependencies installed successfully!
echo You can now run start.bat or start.ps1 to start the application.
echo.
pause 