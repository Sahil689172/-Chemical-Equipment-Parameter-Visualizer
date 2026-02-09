@echo off
echo ========================================
echo Restarting Django Server with Clean Cache
echo ========================================
echo.

echo Step 1: Stopping all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Clearing Python cache...
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d" 2>nul
del /s /q *.pyc 2>nul
echo Cache cleared.

echo Step 3: Starting fresh server...
echo.
call venv\Scripts\activate
python manage.py runserver
pause
