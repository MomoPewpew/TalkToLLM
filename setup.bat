@echo off
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

echo Starting Ollama container...
docker-compose up -d

echo Waiting for Ollama to start...
timeout /t 5

echo Pulling DeepSeek model (this may take a while)...
docker exec ollama ollama pull deepseek-r1:8b

echo Installing Python dependencies...
.\venv\Scripts\python.exe -m pip install -r requirements.txt

echo.
echo Setup complete! To run the application:
echo 1. Make sure Docker Desktop is running
echo 2. Run: python src/main.py
echo.
echo To stop the application:
echo 1. Press Ctrl+C to stop the Python application
echo 2. Run: docker-compose down
pause 