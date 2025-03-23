"""
Base class for TTS implementations.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import yaml
import logging
from ..audio import AudioPlayer

logger = logging.getLogger(__name__)

class BaseTTS(ABC):
    def __init__(self, config_path: str = "config/tts_config.yaml", device_name: str = None):
        """
        Initialize the TTS system.
        
        Args:
            config_path (str): Path to the configuration file
            device_name (str): Name of the audio device to use
        """
        self.config = self._load_config(config_path)
        self.audio_player = AudioPlayer(device_name)
        
        # Initialize settings
        self._current_voice = None
        self._current_speed = self.config.get("speed", 1.0)
        self._current_volume = self.config.get("volume", 1.0)
        
        # Set initial voice
        voice = self.config.get("voice", self.get_default_voice())
        self.set_voice(voice)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            logger.info(f"Config file {config_path} not found. Using system defaults.")
            return {}
        except yaml.YAMLError as e:
            logger.warning(f"Error parsing config file: {e}. Using system defaults.")
            return {}

    @abstractmethod
    def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.
        
        Args:
            text (str): The text to convert to speech
        """
        pass

    @abstractmethod
    def save_to_file(self, text: str, output_path: str) -> None:
        """
        Convert text to speech and save it to a file.
        
        Args:
            text (str): The text to convert to speech
            output_path (str): Path to save the audio file
        """
        pass

    @abstractmethod
    def set_voice(self, voice: str) -> None:
        """
        Set the voice to use for text-to-speech.
        
        Args:
            voice (str): The voice to use
        """
        pass

    @abstractmethod
    def get_default_voice(self) -> str:
        """
        Get the default voice for this TTS implementation.
        
        Returns:
            str: The default voice identifier
        """
        pass

    @abstractmethod
    def list_voices(self) -> List[str]:
        """
        Get a list of available voice names.
        
        Returns:
            List[str]: List of available voice names
        """
        pass

    def set_speed(self, speed: float) -> None:
        """
        Set the speech speed.
        
        Args:
            speed (float): The speed multiplier (0.5 to 2.0, where 1.0 is normal)
        """
        try:
            if 0.5 <= speed <= 2.0:
                self._current_speed = speed
                logger.info(f"Speed set to {speed}")
            else:
                raise ValueError("Speed must be between 0.5 and 2.0")
        except Exception as e:
            logger.error(f"Error setting speed: {str(e)}")

    def set_volume(self, volume: float) -> None:
        """
        Set the speech volume.
        
        Args:
            volume (float): The volume to use (0.0 to 1.0, where 1.0 is full volume)
        """
        try:
            if 0.0 <= volume <= 1.0:
                self._current_volume = volume
                logger.info(f"Volume set to {volume}")
            else:
                raise ValueError("Volume must be between 0.0 and 1.0")
        except Exception as e:
            logger.error(f"Error setting volume: {str(e)}")

    def __del__(self):
        """Cleanup when the object is destroyed."""
        pass 