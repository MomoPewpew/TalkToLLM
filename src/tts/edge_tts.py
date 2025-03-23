"""
Edge TTS implementation using Microsoft Edge's online TTS service.
"""
import logging
import asyncio
import edge_tts
from typing import List
from .base_tts import BaseTTS

logger = logging.getLogger(__name__)

class EdgeTTS(BaseTTS):
    # Some good voice options from Edge TTS:
    DEFAULT_VOICE = "en-US-JennyNeural"  # Clear female voice
    AVAILABLE_VOICES = {
        "jenny": "en-US-JennyNeural",      # Clear female voice
        "aria": "en-US-AriaNeural",        # Natural female voice
        "guy": "en-US-GuyNeural",          # Natural male voice
        "emma": "en-US-EmmaNeural",        # Natural female voice
        "brian": "en-US-BrianNeural",      # Natural male voice
        "christopher": "en-US-ChristopherNeural",  # Natural male voice
        "eric": "en-US-EricNeural",        # Natural male voice
        "british_ryan": "en-GB-RyanNeural",  # British male voice
        "british_sonia": "en-GB-SoniaNeural",  # British female voice
    }

    def __init__(self, config_path: str = "config/tts_config.yaml", device_name: str = None):
        """Initialize Edge TTS."""
        super().__init__(config_path, device_name)
        
        # Create event loop for async operations
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
        except Exception as e:
            logger.error(f"Error setting up event loop: {str(e)}")
            raise
        
        # Get available voices
        try:
            self._voices = self._loop.run_until_complete(edge_tts.list_voices())
            logger.info(f"Found {len(self._voices)} voices")
            
            # Log available voices for debugging
            logger.debug("Available voices:")
            for v in self._voices:
                if v["Locale"].startswith("en-"):
                    logger.debug(f"- {v['ShortName']} ({v['Locale']})")
            
        except Exception as e:
            logger.error(f"Error getting voices: {str(e)}")
            self._voices = []

    async def _speak_async(self, text: str) -> None:
        """Internal async method to handle TTS."""
        try:
            if not self._current_voice:
                raise Exception("No voice selected")
                
            # Create communicator with voice
            communicate = edge_tts.Communicate(
                text,
                self._current_voice,
                rate=f"{int((self._current_speed - 1.0) * 100):+d}%",
                volume=f"{int(self._current_volume * 100) - 100:+d}%"
            )
            
            # Get audio stream
            audio_stream = await communicate.stream()
            audio_data = b""
            async for chunk in audio_stream:
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            
            # Play the audio
            self.audio_player.play_with_temp_file(audio_data)
                    
        except Exception as e:
            raise Exception(f"TTS error: {str(e)}")

    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        if not text.strip():
            logger.warning("Empty text provided, skipping TTS")
            return
            
        try:
            self._loop.run_until_complete(self._speak_async(text))
            logger.info("Speech completed successfully")
        except Exception as e:
            logger.error(f"Error during text-to-speech: {str(e)}")
            raise

    async def _save_async(self, text: str, output_path: str) -> None:
        """Internal async method to handle saving TTS to file."""
        try:
            if not self._current_voice:
                raise Exception("No voice selected")
                
            communicate = edge_tts.Communicate(text, self._current_voice)
            await communicate.save(output_path)
        except Exception as e:
            raise Exception(f"TTS save error: {str(e)}")

    def save_to_file(self, text: str, output_path: str) -> None:
        """Convert text to speech and save it to a file."""
        try:
            self._loop.run_until_complete(self._save_async(text, output_path))
            logger.info(f"Audio saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving text-to-speech to file: {str(e)}")

    def set_voice(self, voice: str) -> None:
        """Set the voice to use for text-to-speech."""
        try:
            # Convert friendly name to full voice name if needed
            voice_id = self.AVAILABLE_VOICES.get(voice.lower(), voice)
            
            # Find the voice in available voices
            matching_voices = [v for v in self._voices if v["ShortName"] == voice_id]
            if matching_voices:
                self._current_voice = voice_id
                logger.info(f"Voice set to {voice_id}")
            else:
                # If voice not found, try to find it in the list of voices
                english_voices = [v for v in self._voices if v["Locale"].startswith("en-")]
                if english_voices:
                    # Try to find a voice that matches our preferred voices first
                    preferred_voices = set(self.AVAILABLE_VOICES.values())
                    preferred_matches = [v for v in english_voices if v["ShortName"] in preferred_voices]
                    
                    if preferred_matches:
                        self._current_voice = preferred_matches[0]["ShortName"]
                        logger.info(f"Using preferred voice: {self._current_voice}")
                    else:
                        self._current_voice = english_voices[0]["ShortName"]
                        logger.info(f"Using English voice: {self._current_voice}")
                else:
                    # Last resort: use the first available voice
                    self._current_voice = self._voices[0]["ShortName"]
                    logger.warning(f"No English voices found, using fallback voice: {self._current_voice}")
        except Exception as e:
            logger.error(f"Error setting voice: {str(e)}")
            if not self._current_voice and self._voices:
                self._current_voice = self._voices[0]["ShortName"]
                logger.warning(f"Using fallback voice: {self._current_voice}")

    def get_default_voice(self) -> str:
        """Get the default voice name."""
        return "jenny"  # Default to Jenny

    def list_voices(self) -> List[str]:
        """Get a list of available friendly voice names."""
        return list(self.AVAILABLE_VOICES.keys())

    def __del__(self):
        """Cleanup when the object is destroyed."""
        try:
            if hasattr(self, '_loop') and self._loop and not self._loop.is_closed():
                self._loop.close()
        except:
            pass 