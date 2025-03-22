"""
Real-time speech-to-text implementation using RealtimeSTT.
"""
from RealtimeSTT import AudioToTextRecorder


class RealtimeTranscriber:
    def __init__(self):
        """Initialize the transcriber."""
        self.recorder = AudioToTextRecorder()
        print("Transcriber initialized. Wait until it says 'speak now'")

    def process_text(self, text: str) -> None:
        """
        Process the transcribed text.
        
        Args:
            text (str): The transcribed text
        """
        print(f"Transcribed: {text}")

    def start(self) -> None:
        """Start the transcription process."""
        try:
            while True:
                self.recorder.text(self.process_text)
        except KeyboardInterrupt:
            print("\nStopping transcription...")
            print("Thank you for using TalkToLLM!")


if __name__ == "__main__":
    transcriber = RealtimeTranscriber()
    transcriber.start() 