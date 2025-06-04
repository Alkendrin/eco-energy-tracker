@echo off
echo Setting up EcoEnergy Tracker dependencies...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH. Please install Python first.
    pause
    exit /b 1
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing required dependencies...
pip install flask
pip install werkzeug
pip install jinja2

:: Note: sqlite3 comes built-in with Python, so no need to install it separately

echo.
echo Setup complete! All dependencies have been installed.
echo You can now run Start.bat to launch the application.
pause