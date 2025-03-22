# TalkToLLM

A self-hosted Python environment for voice interaction with Large Language Models.

## Features
- Real-time speech-to-text transcription
- Integration with self-hosted DeepSeek LLM
- Text-to-speech response playback
- Configurable microphone input

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

## Setup
1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your microphone settings in `config/audio_config.yaml`

## Usage
[To be added]

## Development
[To be added] 