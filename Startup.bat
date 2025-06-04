import os
import subprocess
import sys

def create_environment():
    print("Setting up EcoEnergy Tracker environment...")
    
    # Create virtual environment in the package folder
    subprocess.call([sys.executable, "-m", "venv", "env"])
    
    # Path to the virtual environment's pip
    if os.name == 'nt':  # Windows
        pip_path = os.path.join("env", "Scripts", "pip")
    else:  # Linux/Mac
        pip_path = os.path.join("env", "bin", "pip")
    
    # Install required packages
    subprocess.call([pip_path, "install", "flask", "flask-cors"])
    
    print("Environment setup complete!")

if __name__ == "__main__":
    create_environment()