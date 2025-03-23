"""
Text-to-Speech module providing multiple TTS implementations.
"""
import logging
from typing import Optional
from .base_tts import BaseTTS
from .edge_tts import EdgeTTS
from .coqui_tts import CoquiTTS

logger = logging.getLogger(__name__)

class TTSFactory:
    """Factory class for creating TTS instances."""
    
    IMPLEMENTATIONS = {
        "coqui": CoquiTTS,
        "edge": EdgeTTS
    }
    
    @classmethod
    def create(cls, implementation: str = "coqui", config_path: str = "config/tts_config.yaml", device_name: str = None) -> BaseTTS:
        """
        Create a TTS instance.
        
        Args:
            implementation (str): The TTS implementation to use ("coqui" or "edge")
            config_path (str): Path to the configuration file
            device_name (str): Name of the audio device to use
            
        Returns:
            BaseTTS: A TTS instance
            
        Raises:
            ValueError: If the implementation is not supported
        """
        try:
            if implementation not in cls.IMPLEMENTATIONS:
                raise ValueError(f"Unsupported TTS implementation: {implementation}")
                
            tts_class = cls.IMPLEMENTATIONS[implementation]
            return tts_class(config_path=config_path, device_name=device_name)
            
        except Exception as e:
            logger.error(f"Error creating TTS instance: {str(e)}")
            raise

# For backward compatibility
def create_tts(implementation: str = "coqui", config_path: str = "config/tts_config.yaml", device_name: str = None) -> BaseTTS:
    """Convenience function to create a TTS instance."""
    return TTSFactory.create(implementation, config_path, device_name) 