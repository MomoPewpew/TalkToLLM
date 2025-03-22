"""
Main entry point for the TalkToLLM application.
"""
from transcription.realtime_stt import RealtimeTranscriber


def main():
    """Run the main application."""
    print("Starting TalkToLLM...")
    transcriber = RealtimeTranscriber()
    transcriber.start()


if __name__ == "__main__":
    main() 