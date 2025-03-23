"""
Main entry point for the TalkToLLM application.
"""
import logging
import os
import sys
import re

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.transcription.realtime_stt import RealtimeTranscriber
from src.llm.deepseek import DeepSeekLLM
from src.tts import create_tts

def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences, handling multiple punctuation marks."""
    # Split on period, exclamation mark, or question mark followed by space or end of string
    sentences = re.split(r'(?<=[.!?])(?:\s+|\Z)', text)
    # Filter out empty strings and strip whitespace
    return [s.strip() for s in sentences if s.strip()]

def main():
    """Main function to run the voice interaction loop."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize components
        logger.info("Initializing components...")
        transcriber = RealtimeTranscriber()
        llm = DeepSeekLLM()
        tts = create_tts()  # Will use Coqui by default
        
        def process_voice_input(text: str) -> None:
            """Process transcribed text through LLM and TTS."""
            try:
                # Generate LLM response
                logger.info(f"User said: {text}")
                response = llm.generate_response(text)
                logger.info(f"LLM response: {response}")
                
                # Split response into sentences and speak each one
                sentences = split_into_sentences(response)
                for sentence in sentences:
                    if sentence:  # Skip empty sentences
                        try:
                            tts.speak(sentence)
                        except Exception as e:
                            logger.error(f"Error speaking sentence: {e}")
                            continue
            except Exception as e:
                logger.error(f"Error processing voice input: {e}")
        
        # Set up transcriber callback
        transcriber.process_text = process_voice_input
        
        # Start the voice interaction loop
        logger.info("Starting voice interaction loop. Speak into your microphone...")
        transcriber.start()
        
    except KeyboardInterrupt:
        logger.info("\nStopping TalkToLLM...")
        logger.info("Thank you for using TalkToLLM!")
    except Exception as e:
        logger.error(f"Error in main loop: {e}")
        raise

if __name__ == "__main__":
    main() 