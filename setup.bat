@echo off
setlocal EnableDelayedExpansion

echo Checking Python installation...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Python is not installed or not in PATH. Please:
    echo 1. Download Python 3.8 or higher from https://www.python.org/
    echo 2. Install Python (ensure "Add Python to PATH" is checked)
    echo 3. Run this script again
    pause
    exit /b 1
)

echo Checking for virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorLevel% neq 0 (
        echo Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate
if %errorLevel% neq 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Checking for Docker installation...
docker --version >nul 2>&1
if %errorLevel% neq 0 (
    echo Docker is not installed. Please:
    echo 1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
    echo 2. Install Docker Desktop
    echo 3. Start Docker Desktop
    echo 4. Run this script again
    pause
    exit /b 1
)

echo Checking if Docker is running...
docker info >nul 2>&1
if %errorLevel% neq 0 (
    echo Docker is not running. Please:
    echo 1. Start Docker Desktop
    echo 2. Wait for it to fully start
    echo 3. Run this script again
    pause
    exit /b 1
)

echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorLevel% neq 0 (
    echo Failed to install Python dependencies
    pause
    exit /b 1
)

echo Starting Docker containers...
docker-compose down >nul 2>&1
docker-compose up -d
if %errorLevel% neq 0 (
    echo Failed to start Docker containers
    pause
    exit /b 1
)

echo Waiting for Ollama to start...
timeout /t 10 /nobreak

echo Pulling DeepSeek model (this may take a while)...
docker exec ollama ollama pull deepseek-r1:8b
if %errorLevel% neq 0 (
    echo Failed to pull DeepSeek model. Check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo Setup complete! Before running the application:
echo 1. Ensure your microphone is connected and enabled
echo 2. Check Windows sound settings if needed
echo 3. Audio output should be configured in Windows
echo.
echo To start the application:
echo 1. Make sure Docker Desktop is running
echo 2. Run: python -m src.main
echo.
echo To stop the application:
echo 1. Press Ctrl+C to stop the Python application
echo 2. Run: docker-compose down
echo.
echo If you experience audio issues:
echo - Check Windows Sound settings
echo - Make sure no other application is using the microphone
echo - Try running the application with administrator privileges
echo - Check the device ID in config/audio_config.yaml
echo.
pause 