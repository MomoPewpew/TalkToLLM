#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking Python installation..."
if ! command_exists python3; then
    echo
    echo "ERROR: Python is not installed or not in PATH."
    echo
    echo "Please follow these steps:"
    echo "1. Install Python 3.8 or higher using your package manager"
    echo "2. For Ubuntu/Debian: sudo apt install python3 python3-venv"
    echo "3. For macOS: brew install python"
    echo "4. Close and reopen your terminal"
    echo "5. Run this script again"
    echo
    echo "Current Python location:"
    which python3
    echo
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 -c 'import sys; print("".join(map(str, sys.version_info[:2])))')

# Check if version is 3.8 or higher
if [ "$PYTHON_VERSION" -lt 38 ]; then
    echo
    echo "ERROR: Python version must be 3.8 or higher."
    echo "Current version: $PYTHON_VERSION"
    echo
    echo "Please install a newer version using your package manager"
    exit 1
fi

echo "Found Python version $PYTHON_VERSION"
echo

echo "Checking for virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment"
        exit 1
    fi
fi

echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment"
    exit 1
fi

echo "Checking for Docker installation..."
if ! command_exists docker; then
    echo "Docker is not installed. Please:"
    echo "1. Install Docker using your package manager"
    echo "2. For Ubuntu/Debian: sudo apt install docker.io docker-compose"
    echo "3. For macOS: brew install docker docker-compose"
    echo "4. Start Docker service"
    echo "5. Run this script again"
    exit 1
fi

echo "Checking if Docker is running..."
if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running. Please:"
    echo "1. Start Docker service"
    echo "2. Wait for it to fully start"
    echo "3. Run this script again"
    exit 1
fi

echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip install wheel setuptools

echo "Installing remaining dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies"
    exit 1
fi

echo "Starting Docker containers..."
docker-compose down >/dev/null 2>&1
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "Failed to start Docker containers"
    exit 1
fi

echo "Waiting for Ollama to start..."
sleep 10

echo "Pulling DeepSeek model (this may take a while)..."
docker exec ollama ollama pull deepseek-r1:8b
if [ $? -ne 0 ]; then
    echo "Failed to pull DeepSeek model. Check your internet connection and try again."
    exit 1
fi

echo
echo "Setup complete! Before running the application:"
echo "1. Ensure your microphone is connected and enabled"
echo "2. Check your system's sound settings if needed"
echo "3. Audio output should be configured in your system"
echo
echo "To start the application:"
echo "1. Make sure Docker is running"
echo "2. Run: python3 -m src.main"
echo
echo "To stop the application:"
echo "1. Press Ctrl+C to stop the Python application"
echo "2. Run: docker-compose down"
echo
echo "If you experience audio issues:"
echo "- Check your system's Sound settings"
echo "- Make sure no other application is using the microphone"
echo "- Try running the application with sudo (Linux) or as administrator"
echo "- Check the device ID in config/audio_config.yaml"
echo 