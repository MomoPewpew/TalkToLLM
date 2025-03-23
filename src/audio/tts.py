"""Text-to-speech module for handling speech synthesis."""

import asyncio
import edge_tts
import numpy as np
import sounddevice as sd
import soundfile as sf
from typing import Optional
from .filter import AudioFilter
from ..config import Config

class TTS:
    """Text-to-speech handler using Edge TTS."""

    def __init__(self, config: Config):
        """Initialize TTS with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.tts_config = config.tts_config
        self.audio_filter = AudioFilter(sample_rate=22050)  # Edge TTS sample rate
        
    async def speak(self, text: str) -> None:
        """Convert text to speech and play it.
        
        Args:
            text: Text to convert to speech
        """
        # Get voice from config
        voice = self.tts_config.get("voice", "en-US-JennyNeural")
        
        # Generate speech using Edge TTS
        communicate = edge_tts.Communicate(text, voice)
        audio_data = await communicate.get_audio()
        
        # Convert to numpy array
        audio = np.frombuffer(audio_data, dtype=np.float32)
        
        # Apply filter if enabled
        if self.tts_config.get("filter", {}).get("enabled", False):
            filter_config = self.tts_config["filter"]
            audio = self.audio_filter.apply_filter(
                audio,
                filter_type=filter_config.get("type", "robot"),
                intensity=filter_config.get("intensity", 0.5),
                echo_delay=filter_config.get("echo_delay", 0.1),
                echo_decay=filter_config.get("echo_decay", 0.5)
            )
        
        # Apply volume adjustment
        volume = self.tts_config.get("volume", 1.0)
        audio = audio * volume
        
        # Play the audio
        sd.play(audio, samplerate=22050)
        sd.wait()  # Wait until audio is finished playing 