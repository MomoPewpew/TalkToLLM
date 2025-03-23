# TalkToLLM

A self-hosted Python environment for voice interaction with Large Language Models.

## Features
- Real-time speech-to-text transcription using RealtimeSTT
- Integration with self-hosted DeepSeek LLM via Ollama
- High-quality text-to-speech using Coqui TTS
- Multiple voice options with natural-sounding speech
- Configurable microphone input
- Docker-based deployment for easy setup

## Project Structure
```
TalkToLLM/
├── src/
│   ├── audio/           # Audio input/output handling
│   ├── transcription/   # Speech-to-text functionality
│   ├── llm/            # LLM integration
│   └── tts/            # Text-to-speech functionality
├── config/             # Configuration files
├── tests/              # Test files
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Prerequisites
- Docker Desktop
- Python 3.8 or higher
- A working microphone
- Speakers or headphones

## Setup
1. Install Docker Desktop if not already installed:
   - Download from https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Wait for it to fully initialize

2. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Run the setup script:
   ```bash
   # On Windows
   setup.bat
   
   # On Linux/Mac
   ./setup.sh
   ```
   This will:
   - Start the required Docker containers
   - Pull the DeepSeek LLM model
   - Install Python dependencies
   - Configure audio settings

4. Configure your settings (optional):
   - Audio input: `config/audio_config.yaml`
   - Text-to-speech: `config/tts_config.yaml`
   - LLM settings: `config/llm_config.yaml`

## Usage
1. Ensure Docker Desktop is running
2. Activate your virtual environment:
   ```bash
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Linux/Mac
   ```
3. Start the application:
   ```bash
   python -m src.main
   ```
4. Wait for the "speak now" prompt
5. Start talking! The system will:
   - Transcribe your speech in real-time
   - Process it through the DeepSeek LLM
   - Respond using Coqui TTS

To stop the application:
1. Press Ctrl+C to stop the Python application
2. Run `docker-compose down` to stop the containers

## Troubleshooting
### Audio Issues
- Ensure your microphone is properly connected and enabled
- Check Windows Sound settings
- Verify no other application is using the microphone
- Try running with administrator privileges
- Check the device ID in `config/audio_config.yaml` matches your microphone

### Docker Issues
- Ensure Docker Desktop is running
- Check if containers are running: `docker ps`
- View container logs: `docker-compose logs`
- Restart containers: `docker-compose restart`

### Performance Issues
- The first speech synthesis may take longer (~10-15s)
- Subsequent responses will be faster
- Consider using a GPU for faster LLM responses

## Development
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
[To be added] 