"""
Coqui TTS implementation using Docker container.
"""
import logging
import requests
import tempfile
import os
from typing import List, Dict, Optional
import yaml
from .base_tts import BaseTTS

logger = logging.getLogger(__name__)

class CoquiTTS(BaseTTS):
    """TTS implementation using Coqui TTS Docker container."""
    
    def __init__(self, config_path: str = None, device_name: str = None):
        """Initialize the Coqui TTS engine."""
        super().__init__(config_path, device_name)
        self._config = self._load_config(config_path) if config_path else {}
        self._api_url = "http://localhost:5002"
        self._language = self._config.get('language', 'en')
        
        # Verify connection to TTS server
        try:
            response = requests.get(f"{self._api_url}/health")
            response.raise_for_status()
            server_info = response.json()
            logger.info(f"Successfully connected to Coqui TTS server using model: {server_info['model']}")
        except requests.exceptions.RequestException as e:
            raise Exception(
                "Could not connect to Coqui TTS server. Please ensure:\n"
                "1. Docker is running\n"
                "2. Coqui TTS container is started with: docker-compose up -d\n"
                "3. The service is accessible at http://localhost:5002"
            ) from e

    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        if not text.strip():
            logger.warning("Empty text provided, skipping TTS")
            return

        try:
            # Request speech synthesis
            response = requests.post(
                f"{self._api_url}/api/tts",
                json={
                    "text": text,
                    "speaker_id": None,  # Use default speaker
                    "language_id": self._language
                }
            )
            response.raise_for_status()
            
            # Get audio data
            audio_data = response.content
            
            # Play the audio
            self.audio_player.play_with_temp_file(audio_data)
            logger.info("Speech completed successfully")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error during text-to-speech request: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during speech playback: {e}")
            raise

    def save_to_file(self, text: str, output_path: str) -> None:
        """Convert text to speech and save it to a file."""
        try:
            response = requests.post(
                f"{self._api_url}/api/tts",
                json={
                    "text": text,
                    "speaker_id": None,
                    "language_id": self._language
                }
            )
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"Audio saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving text-to-speech to file: {e}")
            raise

    def get_default_voice(self) -> str:
        """Get the default voice."""
        return "default"  # The Tacotron2-DDC model doesn't have multiple voices

    def list_voices(self) -> List[str]:
        """List available voices."""
        try:
            response = requests.get(f"{self._api_url}/api/speakers")
            response.raise_for_status()
            speakers = response.json()
            if not speakers:
                return ["default"]  # Tacotron2-DDC doesn't have multiple voices
            return speakers
        except requests.exceptions.RequestException:
            logger.warning("Could not get speakers list from server, returning default")
            return ["default"]

    def set_voice(self, voice: str) -> None:
        """Set the voice to use for speech synthesis.
        
        Note: The Tacotron2-DDC model doesn't support multiple voices,
        so this method is implemented to satisfy the abstract base class
        contract but doesn't actually change the voice.
        """
        logger.info(f"Voice selection not supported by Tacotron2-DDC model. Ignoring voice: {voice}") 