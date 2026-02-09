@echo off
echo Stopping all Django servers on port 8000...
taskkill /F /PID 21724 2>nul
taskkill /F /PID 28036 2>nul
taskkill /F /PID 31392 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *manage.py*" 2>nul
echo.
echo Waiting 2 seconds...
timeout /t 2 /nobreak >nul
echo.
echo Starting fresh Django server...
cd backend
call venv\Scripts\activate
python manage.py runserver
pause
