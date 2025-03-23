"""
FastAPI server for Coqui TTS.
"""
import os
import io
import logging
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Coqui TTS Server")

# Define request model
class TTSRequest(BaseModel):
    text: str
    speaker_id: Optional[str] = None
    language_id: Optional[str] = None

# Get model info from environment
MODEL_NAME = os.getenv("MODEL_NAME", "tts_models/en/ljspeech/tacotron2-DDC")
VOCODER_NAME = os.getenv("VOCODER_NAME", "vocoder_models/en/ljspeech/hifigan_v2")
USE_CPU = os.getenv("USE_CPU", "true").lower() == "true"

# Initialize TTS
try:
    logger.info(f"Initializing TTS with model {MODEL_NAME}")
    manager = ModelManager()
    
    # List available models for debugging
    logger.info("Available models:")
    for model_type in manager.models_dict:
        for lang in manager.models_dict[model_type]:
            for dataset in manager.models_dict[model_type][lang]:
                for model in manager.models_dict[model_type][lang][dataset]:
                    logger.info(f"- {model_type}/{lang}/{dataset}/{model}")
    
    # Download and initialize models
    logger.info(f"Downloading TTS model: {MODEL_NAME}")
    model_path, config_path, model_item = manager.download_model(MODEL_NAME)
    logger.info(f"TTS model downloaded successfully: {model_path}")
    
    # Initialize synthesizer
    logger.info("Initializing synthesizer...")
    synthesizer = Synthesizer(
        model_path,
        config_path,
        use_cuda=not USE_CPU
    )
    logger.info("TTS initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize TTS: {str(e)}")
    logger.error("Full error details:", exc_info=True)
    raise

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "use_cpu": USE_CPU
    }

@app.post("/api/tts")
def text_to_speech(request: TTSRequest):
    """Convert text to speech."""
    try:
        logger.info(f"Generating speech for text: {request.text}")
        wav = synthesizer.tts(request.text, speaker_name=request.speaker_id, language_name=request.language_id)
        
        # Convert to bytes
        wav_bytes = io.BytesIO()
        synthesizer.save_wav(wav, wav_bytes)
        wav_bytes.seek(0)
        
        return StreamingResponse(wav_bytes, media_type="audio/wav")
    except Exception as e:
        logger.error(f"TTS failed: {str(e)}")
        logger.error("Full error details:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/speakers")
def list_speakers():
    """List available speakers."""
    try:
        speakers = synthesizer.speakers if hasattr(synthesizer, "speakers") else []
        return speakers
    except Exception as e:
        logger.error(f"Failed to list speakers: {str(e)}")
        logger.error("Full error details:", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e)) 