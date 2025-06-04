@echo off
:: filepath: c:\Users\User\Desktop\CAPSTONE\eco-energy-tracker\Start.bat
echo Starting EcoEnergy Tracker...

:: Check if virtual environment exists, if not create it
if not exist env (
    echo Setting up environment for first run...
    python setup.py
)

:: Activate virtual environment and start application
call env\Scripts\activate.bat
python main.py

:: Open browser to application
start http://127.0.0.1:5000

echo EcoEnergy Tracker is running!