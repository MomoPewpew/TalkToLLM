# TalkToLLM

A real-time voice chat application that uses speech-to-text, LLM, and text-to-speech to create a conversational AI assistant.

## Features

- Real-time speech recognition using RealtimeSTT
- Text-to-speech using Edge TTS
- LLM integration using Ollama
- Configurable audio settings
- AI voice effects (robot and echo filters)
- Cross-platform support (Windows, Linux, macOS)

## Project Structure

```
TalkToLLM/
├── config/
│   ├── audio_config.yaml    # Audio device and recording settings
│   ├── llm_config.yaml      # LLM model and API settings
│   └── tts_config.yaml      # TTS engine and voice settings
├── src/
│   ├── audio/
│   │   ├── __init__.py      # Audio package initialization
│   │   ├── filter.py        # Audio effects and filters
│   │   └── tts.py          # Text-to-speech implementation
│   ├── llm/
│   │   ├── __init__.py      # LLM package initialization
│   │   └── ollama.py        # Ollama API integration
│   ├── stt/
│   │   ├── __init__.py      # STT package initialization
│   │   └── realtime.py      # Real-time speech recognition
│   ├── __init__.py          # Main package initialization
│   └── main.py              # Application entry point
├── tests/                   # Test suite
├── .gitignore
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Docker build configuration
├── LICENSE                 # GNU General Public License v3
├── README.md
├── requirements.txt        # Python dependencies
├── setup.bat              # Windows setup script
└── setup.sh               # Unix-like systems setup script
```

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose
- Working microphone and speakers
- Windows 10/11, Linux, or macOS

## Installation

### Windows

1. Clone the repository:
   ```bash
   git clone https://github.com/MomoPewpew/TalkToLLM.git
   cd TalkToLLM
   ```

2. Run the setup script:
   ```bash
   setup.bat
   ```

### Linux/macOS

1. Clone the repository:
   ```bash
   git clone https://github.com/MomoPewpew/TalkToLLM.git
   cd TalkToLLM
   ```

2. Make the setup script executable and run it:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

## Usage

1. Start the application:
   ```bash
   python -m src.main
   ```

2. Speak into your microphone. The application will:
   - Convert your speech to text
   - Send it to the LLM for processing
   - Convert the response to speech
   - Play it through your speakers

3. Press Ctrl+C to stop the application

## Configuration

### Audio Settings

Edit `config/audio_config.yaml` to configure:
- Input device (microphone)
- Output device (speakers)
- Sample rate and channels
- Buffer size

### LLM Settings

Edit `config/llm_config.yaml` to configure:
- Model name and size
- API endpoint
- Temperature and other parameters

### TTS Settings

Edit `config/tts_config.yaml` to configure:
- Voice selection
- Speech rate and volume
- AI voice effects (robot/echo filters)

## Development

### Running Tests

```bash
pytest
```

### Code Style

The project uses:
- Black for code formatting
- Flake8 for linting
- isort for import sorting

Run the formatters:
```bash
black .
isort .
```

## Troubleshooting

### Audio Issues

1. Check your system's audio settings
2. Ensure no other application is using the microphone
3. Try running with administrator privileges
4. Verify device IDs in `config/audio_config.yaml`

### Docker Issues

1. Ensure Docker Desktop is running
2. Check Docker logs: `docker-compose logs`
3. Restart Docker services: `docker-compose down && docker-compose up -d`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the GNU General Public License v3 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [RealtimeSTT](https://github.com/KoljaB/RealtimeSTT) for speech recognition
- [Edge TTS](https://github.com/ganlvtech/edge-tts) for text-to-speech
- [Ollama](https://ollama.ai/) for LLM capabilities