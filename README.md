# TalkToLLM

A self-hosted Python environment for voice interaction with Large Language Models.

## Features
- Real-time speech-to-text transcription using RealtimeSTT
- Integration with self-hosted DeepSeek LLM
- High-quality text-to-speech using Microsoft Edge TTS
- Multiple voice options with natural-sounding speech
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

3. Configure your settings:
   - Audio input: `config/audio_config.yaml`
   - Text-to-speech: `config/tts_config.yaml`
   - LLM settings: `config/llm_config.yaml`

## Voice Options
The system uses Microsoft Edge TTS for high-quality speech synthesis. Available voices include:
- Jenny (US Female) - Clear and professional
- Aria (US Female) - Natural and warm
- Guy (US Male) - Natural and friendly
- Emma (US Female) - Natural and engaging
- Brian (US Male) - Natural and professional
- Christopher (US Male) - Natural and authoritative
- Eric (US Male) - Natural and conversational
- British voices: Ryan (Male) and Sonia (Female)

You can configure your preferred voice in `config/tts_config.yaml`.

## Usage
[To be added]

## Development
[To be added] 