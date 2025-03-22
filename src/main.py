"""
Main entry point for the TalkToLLM application.
"""
import sys
from transcription.realtime_stt import RealtimeTranscriber
from llm.deepseek import DeepSeekLLM
from tts.realtime_tts import RealtimeTTS


def main():
    """Main entry point for the application."""
    print("Starting TalkToLLM...")
    
    try:
        # Initialize LLM
        print("Initializing DeepSeek LLM...")
        llm = DeepSeekLLM()
        print("DeepSeek LLM initialized successfully!")

        # Initialize STT
        print("Initializing Speech-to-Text...")
        transcriber = RealtimeTranscriber()
        print("Speech-to-Text initialized successfully!")

        # Initialize TTS
        print("Initializing Text-to-Speech...")
        tts = RealtimeTTS()
        print("Text-to-Speech initialized successfully!")

        # Main application loop
        print("\nTalkToLLM is ready! Press Ctrl+C to exit.")
        
        def process_text(text: str) -> None:
            if text:
                print(f"\nYou said: {text}")
                
                # Generate response
                response = llm.generate_response(text)
                print(f"\nAssistant: {response}")
                
                # Convert response to speech
                tts.speak(response)

        # Start the transcription loop
        while True:
            transcriber.recorder.text(process_text)

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Docker is running")
        print("2. Start Ollama with: docker-compose up -d")
        print("3. Check if all required services are running")
        print("4. Verify your configuration files")
        sys.exit(1)


if __name__ == "__main__":
    main() 