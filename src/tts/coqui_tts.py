"""
Coqui TTS implementation using RealtimeTTS's CoquiEngine.
"""
import logging
from typing import List, Dict, Optional
import yaml
from RealtimeTTS import TextToAudioStream, CoquiEngine
from .base_tts import BaseTTS

logger = logging.getLogger(__name__)

class CoquiTTS(BaseTTS):
    # Available voices with their friendly names
    AVAILABLE_VOICES = {
        "jenny": "tts_models/en/jenny/jenny",
        "glow": "tts_models/en/glow-tts/ljspeech",
        "tacotron": "tts_models/en/tacotron2-DDC/ljspeech",
        "vits": "tts_models/en/vits/ljspeech",
        "fast": "tts_models/en/fast_pitch/ljspeech",
        "multi": "tts_models/multilingual/multi-dataset/xtts_v1"
    }

    def __init__(self, config_path: str = None, device_name: str = None):
        """Initialize the Coqui TTS engine."""
        self._config = self._load_config(config_path) if config_path else {}
        self._device_name = device_name
        self._language = self._config.get('language', 'en')
        self._voice = self._config.get('voice', 'jenny')
        self._speed = float(self._config.get('speed', 1.0))
        self._volume = float(self._config.get('volume', 1.0))
        
        try:
            # Get voice model path
            voice_model = self.AVAILABLE_VOICES.get(self._voice.lower(), self._voice)
            
            # Initialize with settings from config
            self._engine = CoquiEngine(
                language=self._language,
                voice=voice_model,
                full_sentences=True  # Prevents mid-sentence stuttering
            )
            self._stream = TextToAudioStream(
                self._engine,
                log_characters=True,  # Log progress
                tokenizer="nltk"  # Use NLTK for faster tokenization
            )
            logger.info(f"Successfully initialized Coqui TTS with language: {self._language}, voice: {self._voice}")
        except Exception as e:
            logger.error(f"Error initializing Coqui TTS: {str(e)}")
            raise

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from yaml file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config from {config_path}: {str(e)}")
            return {}

    def speak(self, text: str) -> None:
        """Speak the given text."""
        try:
            self._stream.feed(text)
            self._stream.play()
        except Exception as e:
            logger.error(f"Error speaking text: {str(e)}")
            raise

    def save_to_file(self, text: str, output_path: str) -> None:
        """Convert text to speech and save it to a file."""
        try:
            # Set speed
            self._engine.rate = self._current_speed
            
            # Generate and save audio
            audio_stream = self._engine.generate(text)
            with open(output_path, 'wb') as f:
                f.write(audio_stream.audio_data)
            logger.info(f"Audio saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving text-to-speech to file: {str(e)}")
            raise

    def get_default_voice(self) -> str:
        """Get the default voice."""
        return "jenny"  # Default to Jenny model

    def list_voices(self) -> List[str]:
        """List available voices."""
        return list(self.AVAILABLE_VOICES.keys())

    def set_voice(self, voice_id: str) -> bool:
        """Set the voice for TTS."""
        try:
            # Check if voice_id is a friendly name or a model path
            voice_model = self.AVAILABLE_VOICES.get(voice_id.lower(), voice_id)
            
            if voice_model != self._voice:
                self._voice = voice_model
                # Reinitialize with updated settings
                self._engine = CoquiEngine(
                    language=self._language,
                    voice=voice_model,
                    full_sentences=True
                )
                self._stream = TextToAudioStream(
                    self._engine,
                    log_characters=True,
                    tokenizer="nltk"
                )
                logger.info(f"Successfully set voice to: {voice_id}")
                return True
        except Exception as e:
            logger.error(f"Error setting voice {voice_id}: {str(e)}")
            raise
        return False

    def __del__(self):
        """Cleanup when the object is destroyed."""
        try:
            if hasattr(self, '_engine'):
                del self._engine
        except:
            pass 