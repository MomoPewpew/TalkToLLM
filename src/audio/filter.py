"""Audio filter module for applying effects to TTS output."""

import numpy as np
from scipy import signal
from typing import Optional, Tuple

class AudioFilter:
    """Applies various audio filters to make speech sound more AI-like."""
    
    def __init__(self, sample_rate: int = 22050):
        """Initialize the audio filter.
        
        Args:
            sample_rate: The sample rate of the audio in Hz
        """
        self.sample_rate = sample_rate
        
    def apply_filter(
        self,
        audio: np.ndarray,
        filter_type: str,
        intensity: float = 0.5,
        echo_delay: float = 0.1,
        echo_decay: float = 0.5
    ) -> np.ndarray:
        """Apply the specified filter to the audio.
        
        Args:
            audio: Input audio array
            filter_type: Type of filter to apply ("robot", "echo", or "none")
            intensity: Filter intensity (0.0 to 1.0)
            echo_delay: Echo delay in seconds (for echo filter)
            echo_decay: Echo decay factor (0.0 to 1.0)
            
        Returns:
            Filtered audio array
        """
        if filter_type == "none":
            return audio
            
        # Ensure audio is float32
        audio = audio.astype(np.float32)
        
        if filter_type == "robot":
            return self._apply_robot_filter(audio, intensity)
        elif filter_type == "echo":
            return self._apply_echo_filter(audio, echo_delay, echo_decay)
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")
            
    def _apply_robot_filter(self, audio: np.ndarray, intensity: float) -> np.ndarray:
        """Apply a robot-like filter using frequency modulation.
        
        Args:
            audio: Input audio array
            intensity: Filter intensity (0.0 to 1.0)
            
        Returns:
            Filtered audio array
        """
        # Create a modulating signal
        t = np.arange(len(audio)) / self.sample_rate
        modulator = np.sin(2 * np.pi * 10 * t) * intensity
        
        # Apply frequency modulation
        filtered = audio * (1 + modulator)
        
        # Normalize to prevent clipping
        filtered = filtered / np.max(np.abs(filtered))
        
        return filtered
        
    def _apply_echo_filter(
        self,
        audio: np.ndarray,
        delay: float,
        decay: float
    ) -> np.ndarray:
        """Apply an echo effect to the audio.
        
        Args:
            audio: Input audio array
            delay: Echo delay in seconds
            decay: Echo decay factor (0.0 to 1.0)
            
        Returns:
            Filtered audio array
        """
        # Calculate delay in samples
        delay_samples = int(delay * self.sample_rate)
        
        # Create echo buffer
        echo = np.zeros_like(audio)
        echo[delay_samples:] = audio[:-delay_samples] * decay
        
        # Combine original and echo
        filtered = audio + echo
        
        # Normalize to prevent clipping
        filtered = filtered / np.max(np.abs(filtered))
        
        return filtered 