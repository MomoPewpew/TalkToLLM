"""
Audio input/output handling module.
"""
import logging
import os
import tempfile
import sounddevice as sd
import soundfile as sf
import pyaudio

logger = logging.getLogger(__name__)

class AudioPlayer:
    def __init__(self, device_name: str = None):
        """
        Initialize audio playback system.
        
        Args:
            device_name (str): Name of the audio device to use (partial match)
        """
        self._audio = pyaudio.PyAudio()
        self._device_name = device_name
        self._print_audio_info()
        
    def _print_audio_info(self):
        """Print information about audio devices for debugging."""
        try:
            logger.info("\nAudio Device Information:")
            logger.info("-" * 50)
            
            # Get default output device info
            default_output = self._audio.get_default_output_device_info()
            logger.info(f"Default Output Device:")
            logger.info(f"  Name: {default_output['name']}")
            logger.info(f"  Sample Rate: {int(default_output['defaultSampleRate'])} Hz")
            logger.info(f"  Channels: {default_output['maxOutputChannels']}")
            logger.info(f"  Device Index: {default_output['index']}")
            
            # List all available output devices
            logger.info("\nAvailable Output Devices:")
            for i in range(self._audio.get_device_count()):
                try:
                    info = self._audio.get_device_info_by_index(i)
                    if info['maxOutputChannels'] > 0:  # Only show output devices
                        logger.info(f"\nDevice {i}:")
                        logger.info(f"  Name: {info['name']}")
                        logger.info(f"  Sample Rate: {int(info['defaultSampleRate'])} Hz")
                        logger.info(f"  Channels: {info['maxOutputChannels']}")
                except Exception as e:
                    logger.error(f"Error getting info for device {i}: {str(e)}")
            logger.info("-" * 50)
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

    def play_audio(self, audio_data: bytes = None, file_path: str = None, sample_rate: int = None):
        """
        Play audio from either bytes data or a file.
        
        Args:
            audio_data (bytes): Raw audio data to play
            file_path (str): Path to audio file to play
            sample_rate (int): Sample rate for raw audio data
        """
        try:
            if audio_data and sample_rate:
                # Play from memory
                sd.play(audio_data, sample_rate)
                sd.wait()
            elif file_path:
                # Play from file
                data, samplerate = sf.read(file_path)
                sd.play(data, samplerate)
                sd.wait()
            else:
                raise ValueError("Either audio_data with sample_rate or file_path must be provided")
                
        except Exception as e:
            logger.error(f"Error playing audio: {str(e)}")
            raise

    def play_with_temp_file(self, audio_data: bytes, suffix: str = '.wav'):
        """
        Play audio data by first saving to a temporary file.
        Useful for formats that need to be written to disk first.
        
        Args:
            audio_data (bytes): The audio data to play
            suffix (str): File extension for the temp file
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = temp_file.name
            try:
                # Write data to temp file
                temp_file.write(audio_data)
                temp_file.flush()
                
                # Play the file
                self.play_audio(file_path=temp_path)
                
            finally:
                # Clean up
                try:
                    os.unlink(temp_path)
                except:
                    pass

    def __del__(self):
        """Cleanup when the object is destroyed."""
        try:
            if hasattr(self, '_audio'):
                self._audio.terminate()
        except:
            pass 