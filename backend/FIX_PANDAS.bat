@echo off
echo ========================================
echo Fixing Pandas Installation Issue
echo ========================================
echo.

echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing packages without building from source...
pip install Django==4.2.7 djangorestframework==3.14.0 django-cors-headers==4.3.1 reportlab==4.0.7

echo.
echo Installing pandas (latest version with Python 3.13 support)...
pip install pandas --upgrade

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo If pandas still fails, try:
echo   1. Use Python 3.11 or 3.12 instead
echo   2. Or install without pandas (CSV upload will use built-in csv module)
echo.
pause
