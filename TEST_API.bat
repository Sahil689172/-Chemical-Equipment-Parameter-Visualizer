@echo off
echo ========================================
echo Testing Backend API
echo ========================================
echo.

echo Testing connection to http://localhost:8000/api/datasets/...
echo.

curl -s http://localhost:8000/api/datasets/

echo.
echo.
echo ========================================
if %ERRORLEVEL% EQU 0 (
    echo Status: Backend is running! ✓
) else (
    echo Status: Backend is NOT running! ✗
    echo.
    echo Make sure you've started the Django server:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   python manage.py runserver
)
echo ========================================
echo.
pause
