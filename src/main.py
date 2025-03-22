"""
Main entry point for the TalkToLLM application.
"""
from transcription.realtime_stt import RealtimeTranscriber
from llm.deepseek import DeepSeekLLM


def main():
    """Run the main application."""
    print("Starting TalkToLLM...")
    print("Initializing DeepSeek LLM...")
    llm = DeepSeekLLM()
    print("LLM initialized successfully!")
    
    print("\nInitializing speech recognition...")
    transcriber = RealtimeTranscriber()
    
    def process_text(text: str) -> None:
        """Process transcribed text and get LLM response."""
        print(f"\nYou said: {text}")
        try:
            response = llm.generate_response(text)
            print(f"\nDeepSeek: {response}")
        except Exception as e:
            print(f"\nError getting LLM response: {e}")
    
    transcriber.process_text = process_text
    transcriber.start()


if __name__ == "__main__":
    main() 