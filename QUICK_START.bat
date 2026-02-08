@echo off
echo ========================================
echo Chemical Equipment Parameter Visualizer
echo Quick Start Script
echo ========================================
echo.

echo Step 1: Setting up Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Running migrations...
python manage.py migrate --noinput
echo Loading sample data...
python manage.py load_equipment
echo.
echo Backend setup complete!
echo.
echo Starting Django server...
echo Backend will run at http://localhost:8000
echo Press CTRL+C to stop the server
echo.
start cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"
timeout /t 3 /nobreak >nul

echo.
echo Step 2: Setting up Frontend...
cd ..\frontend-web
if not exist node_modules (
    echo Installing npm packages...
    call npm install
)
echo.
echo Starting React development server...
echo Frontend will run at http://localhost:3000
echo Press CTRL+C to stop the server
echo.
start cmd /k "cd frontend-web && npm start"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Both servers are starting in separate windows.
echo Wait a few seconds for them to fully start.
echo.
echo Then open http://localhost:3000 in your browser!
echo.
pause
