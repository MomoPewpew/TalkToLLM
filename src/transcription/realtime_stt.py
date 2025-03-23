"""
Real-time speech-to-text implementation using RealtimeSTT.
"""
import yaml
import logging
from RealtimeSTT import AudioToTextRecorder

logger = logging.getLogger(__name__)

class RealtimeTranscriber:
    def __init__(self, config_path: str = "config/audio_config.yaml"):
        """Initialize the transcriber."""
        # Load audio configuration
        try:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load audio config: {e}. Using defaults.")
            self.config = {
                "microphone": {
                    "device_id": 1,
                    "sample_rate": 16000,
                    "channels": 1,
                    "dtype": "float32"
                }
            }
        
        # Initialize the recorder with our config
        self.recorder = AudioToTextRecorder(
            device=self.config["microphone"]["device_id"],
            sample_rate=self.config["microphone"]["sample_rate"]
        )
        logger.info("Transcriber initialized. Wait until it says 'speak now'")

    def process_text(self, text: str) -> None:
        """
        Process the transcribed text.
        
        Args:
            text (str): The transcribed text
        """
        logger.info(f"Transcribed: {text}")

    def start(self) -> None:
        """Start the transcription process."""
        try:
            while True:
                self.recorder.text(self.process_text)
        except KeyboardInterrupt:
            logger.info("\nStopping transcription...")
            logger.info("Thank you for using TalkToLLM!")
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            raise


if __name__ == "__main__":
    transcriber = RealtimeTranscriber()
    transcriber.start() 