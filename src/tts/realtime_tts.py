"""
Text-to-Speech integration using RealtimeTTS.
"""
import yaml
from typing import Dict, Any, List
import logging
import edge_tts
import asyncio
import pyaudio
import tempfile
import os
import wave
import sounddevice as sd
import soundfile as sf

logger = logging.getLogger(__name__)

class RealtimeTTS:
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
        """
        Initialize the TTS client.
        
        Args:
            config_path (str): Path to the configuration file
            device_name (str): Name of the audio device to use (partial match)
        """
        self.config = self._load_config(config_path)
        
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
        
        # Initialize settings
        self._current_voice = None
        voice = self.config.get("voice", "jenny")  # Default to friendly name
        self.set_voice(voice)  # This will handle conversion to full name
            
        self._current_speed = self.config.get("speed", 1.0)
        self._current_volume = self.config.get("volume", 1.0)
        
        # Initialize audio
        self._audio = pyaudio.PyAudio()
        self._device_name = device_name
        
        # Print audio device information
        #self._print_audio_info()
        
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

    def _print_audio_info(self):
        """Print information about audio devices for debugging."""
        try:
            print("\nAudio Device Information:")
            print("-" * 50)
            
            # Get default output device info
            default_output = self._audio.get_default_output_device_info()
            print(f"Default Output Device:")
            print(f"  Name: {default_output['name']}")
            print(f"  Sample Rate: {int(default_output['defaultSampleRate'])} Hz")
            print(f"  Channels: {default_output['maxOutputChannels']}")
            print(f"  Device Index: {default_output['index']}")
            
            # List all available output devices
            print("\nAvailable Output Devices:")
            for i in range(self._audio.get_device_count()):
                try:
                    info = self._audio.get_device_info_by_index(i)
                    if info['maxOutputChannels'] > 0:  # Only show output devices
                        print(f"\nDevice {i}:")
                        print(f"  Name: {info['name']}")
                        print(f"  Sample Rate: {int(info['defaultSampleRate'])} Hz")
                        print(f"  Channels: {info['maxOutputChannels']}")
                except Exception as e:
                    logger.error(f"Error getting info for device {i}: {str(e)}")
            print("-" * 50)
        except Exception as e:
            logger.error(f"Error getting audio information: {str(e)}")

    def _get_device_by_name(self, name: str = None) -> dict:
        """Get audio device info by name (partial match)."""
        if not name:
            return self._audio.get_default_output_device_info()
            
        # Try to find a device matching the name
        for i in range(self._audio.get_device_count()):
            try:
                info = self._audio.get_device_info_by_index(i)
                if (info['maxOutputChannels'] > 0 and  # Only output devices
                    name.lower() in info['name'].lower()):  # Case-insensitive partial match
                    return info
            except:
                continue
                
        # Fall back to default device
        logger.warning(f"Could not find audio device matching '{name}', using default")
        return self._audio.get_default_output_device_info()

    async def _speak_async(self, text: str) -> None:
        """
        Internal async method to handle TTS.
        """
        try:
            if not self._current_voice:
                raise Exception("No voice selected")
                
            # Create communicator with voice with specific format
            communicate = edge_tts.Communicate(
                text,
                self._current_voice,
                rate=f"{int((self._current_speed - 1.0) * 100):+d}%",
                volume=f"{int(self._current_volume * 100) - 100:+d}%"
            )
            
            # Save to a temporary file first
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_path = temp_file.name
                
            # Save the audio data to the temp file
            await communicate.save(temp_path)
            
            # Read the audio file
            try:
                data, samplerate = sf.read(temp_path)
                sd.play(data, samplerate)
                sd.wait()  # Wait until audio is finished playing
            except Exception as e:
                logger.error(f"Error playing audio: {str(e)}")
                raise
            finally:
                # Clean up the temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                    
        except Exception as e:
            raise Exception(f"TTS error: {str(e)}")

    def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.
        
        Args:
            text (str): The text to convert to speech
        """
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
        """
        Internal async method to handle saving TTS to file.
        """
        try:
            if not self._current_voice:
                raise Exception("No voice selected")
                
            communicate = edge_tts.Communicate(text, self._current_voice)
            await communicate.save(output_path)
        except Exception as e:
            raise Exception(f"TTS save error: {str(e)}")

    def save_to_file(self, text: str, output_path: str) -> None:
        """
        Convert text to speech and save it to a file.
        
        Args:
            text (str): The text to convert to speech
            output_path (str): Path to save the audio file
        """
        try:
            self._loop.run_until_complete(self._save_async(text, output_path))
            logger.info(f"Audio saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving text-to-speech to file: {str(e)}")

    def set_voice(self, voice: str) -> None:
        """
        Set the voice to use for text-to-speech.
        
        Args:
            voice (str): The voice to use (can be friendly name or full voice name)
        """
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
            volume (float): The volume to use (0.0 to 1.0, where 0.5 is normal)
        """
        try:
            if 0.0 <= volume <= 1.0:
                self._current_volume = volume
                logger.info(f"Volume set to {volume}")
            else:
                raise ValueError("Volume must be between 0.0 and 1.0")
        except Exception as e:
            logger.error(f"Error setting volume: {str(e)}")

    def list_voices(self) -> List[str]:
        """
        Get a list of available friendly voice names.
        
        Returns:
            List[str]: List of available voice names
        """
        return list(self.AVAILABLE_VOICES.keys())

    def __del__(self):
        """Cleanup when the object is destroyed."""
        try:
            if hasattr(self, '_audio'):
                self._audio.terminate()
            if hasattr(self, '_loop') and self._loop and not self._loop.is_closed():
                self._loop.close()
        except:
            pass


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Simple test
    try:
        print("\nInitializing Text-to-Speech System...")
        tts = RealtimeTTS()
        
        print("\nVoice Information:")
        print("- Available voices:", ", ".join(tts.list_voices()))
        print("- Current voice:", tts._current_voice)
        
        print("\nStarting voice tests...")
        
        # Test with different voices
        print("\n1. Basic TTS Test")
        tts.speak("Hello! This is a test of the text to speech system.")
        
        # Test speed changes
        print("\n2. Testing Speed Changes")
        tts.set_speed(1.5)
        tts.speak("Now I'm speaking 50% faster!")
        
        tts.set_speed(0.8)
        tts.speak("And now I'm speaking a bit slower.")
        
        # Test voice changes
        print("\n3. Testing Different Voices")
        tts.set_voice("guy")
        tts.speak("Now I'm Guy, a different voice.")
        
        tts.set_voice("aria")
        tts.speak("And now I'm Aria. Notice how each voice sounds unique!")
        
        print("\nAll tests completed successfully!")
        
    except Exception as e:
        print(f"\nError during test: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Check your internet connection")
        print("2. Verify your audio output device is working")
        print("3. Try running with administrator privileges if needed")
        print("4. Check the logs for more detailed error information")
        print("\nIf the issue persists, please report the following error:")
        import traceback
        print(traceback.format_exc()) 