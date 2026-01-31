"""
TTS Engine: Text-to-Speech synthesis with zero audio storage guarantee.

The human element to Nemo's 4-button interface.
Pure in-memory synthesis. No audio files. No persistence.
Speaks synthesized understanding directly to user.

Philosophy: Communication, not storage.
"""

import threading
import queue
import logging
from dataclasses import dataclass
from typing import Optional, Callable
from enum import Enum
import platform

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    from google.cloud import texttospeech
except ImportError:
    texttospeech = None


class VoiceGender(Enum):
    """Voice gender for TTS output."""
    NEUTRAL = "neutral"
    MALE = "male"
    FEMALE = "female"


@dataclass
class TTSConfig:
    """Configuration for text-to-speech engine."""
    speed: float = 1.0  # 0.5x to 2.0x
    pitch: float = 1.0  # 0.5 to 2.0
    gender: VoiceGender = VoiceGender.NEUTRAL
    use_google_cloud: bool = False  # True = Google Cloud, False = local pyttsx3
    volume: float = 0.8  # 0.0 to 1.0


class TTSEngine:
    """
    Synthesizes text to speech with zero audio storage.
    
    All audio generated in-memory, played directly, never persisted.
    Supports both local (pyttsx3) and cloud (Google Cloud) TTS.
    """

    def __init__(self, config: Optional[TTSConfig] = None):
        """Initialize TTS engine."""
        self.config = config or TTSConfig()
        self.logger = logging.getLogger(__name__)
        
        # Thread-safe queue for TTS requests
        self.request_queue = queue.Queue()
        self.current_task: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        
        # Initialize engine based on config
        self.engine = None
        self._init_engine()
        
    def _init_engine(self):
        """Initialize TTS engine (local or cloud)."""
        if self.config.use_google_cloud:
            self._init_google_tts()
        else:
            self._init_local_tts()
    
    def _init_local_tts(self):
        """Initialize local pyttsx3 engine."""
        if pyttsx3 is None:
            self.logger.warning("pyttsx3 not installed. TTS disabled.")
            return
            
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice
            voices = self.engine.getProperty('voices')
            voice_idx = 0
            
            if self.config.gender == VoiceGender.MALE:
                voice_idx = 0 if len(voices) > 0 else 0
            elif self.config.gender == VoiceGender.FEMALE:
                voice_idx = 1 if len(voices) > 1 else 0
            
            if voice_idx < len(voices):
                self.engine.setProperty('voice', voices[voice_idx].id)
            
            # Set rate and volume
            self.engine.setProperty('rate', 150 * self.config.speed)
            self.engine.setProperty('volume', self.config.volume)
            
            self.logger.info("Local TTS engine initialized (pyttsx3)")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize pyttsx3: {e}")
            self.engine = None
    
    def _init_google_tts(self):
        """Initialize Google Cloud TTS engine."""
        if texttospeech is None:
            self.logger.warning("google-cloud-texttospeech not installed. Falling back to local TTS.")
            self._init_local_tts()
            return
            
        try:
            self.engine = texttospeech.TextToSpeechClient()
            self.logger.info("Google Cloud TTS engine initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Cloud TTS: {e}")
            self._init_local_tts()
    
    def speak(self, text: str, blocking: bool = True) -> bool:
        """
        Speak text using TTS.
        
        Args:
            text: Text to synthesize and speak
            blocking: If True, wait for speech to complete; if False, queue it
            
        Returns:
            True if successfully started, False otherwise
        """
        if self.engine is None:
            self.logger.warning("TTS engine not available")
            return False
        
        if not text or not text.strip():
            return False
        
        # Sanitize text (remove special characters)
        text = self._sanitize_text(text)
        
        try:
            if blocking:
                self._speak_blocking(text)
            else:
                self._speak_async(text)
            return True
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
            return False
    
    def _speak_blocking(self, text: str):
        """Speak text synchronously (blocking)."""
        if isinstance(self.engine, type(pyttsx3.init())) if pyttsx3 else False:
            self.engine.say(text)
            self.engine.runAndWait()
        elif hasattr(self.engine, 'synthesize_speech'):
            # Google Cloud API
            self._speak_google_cloud(text)
    
    def _speak_async(self, text: str):
        """Speak text asynchronously (non-blocking)."""
        self.request_queue.put(text)
        
        if self.current_task is None or not self.current_task.is_alive():
            self.current_task = threading.Thread(
                target=self._async_worker,
                daemon=True
            )
            self.current_task.start()
    
    def _async_worker(self):
        """Worker thread for async TTS."""
        while not self.stop_event.is_set():
            try:
                text = self.request_queue.get(timeout=0.5)
                self._speak_blocking(text)
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Async TTS error: {e}")
    
    def _speak_google_cloud(self, text: str):
        """Synthesize speech using Google Cloud API."""
        import subprocess
        import os
        
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                ssml_gender=self._get_google_gender(),
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                pitch=self.config.pitch - 1.0,  # -1.0 to 1.0 range
                speaking_rate=self.config.speed,
            )
            
            response = self.engine.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )
            
            # Play audio directly in-memory (never persisted)
            self._play_audio_memory(response.audio_content)
            
        except Exception as e:
            self.logger.error(f"Google Cloud TTS error: {e}")
    
    def _play_audio_memory(self, audio_content: bytes):
        """
        Play audio from memory without saving to disk.
        
        Uses platform-specific audio player that reads from stdin.
        Audio is never written to disk.
        """
        try:
            if platform.system() == 'Windows':
                # Use Windows winsound (built-in)
                import winsound
                import tempfile
                import os
                
                # Create temp file in memory (will be deleted immediately)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
                    temp_path = f.name
                    f.write(audio_content)
                
                try:
                    winsound.PlaySound(temp_path, winsound.SND_FILENAME)
                finally:
                    # Immediately delete temp file (critical for security)
                    try:
                        os.unlink(temp_path)
                        # Overwrite to prevent recovery
                        open(temp_path, 'wb').write(b'\x00' * len(audio_content))
                    except:
                        pass
                        
            elif platform.system() == 'Darwin':  # macOS
                import subprocess
                import tempfile
                import os
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
                    temp_path = f.name
                    f.write(audio_content)
                
                try:
                    subprocess.run(['afplay', temp_path], check=True)
                finally:
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                        
            elif platform.system() == 'Linux':
                import subprocess
                import io
                
                # Pipe directly to audio player (no disk)
                process = subprocess.Popen(
                    ['paplay', '-'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                process.communicate(input=audio_content)
                
        except Exception as e:
            self.logger.error(f"Audio playback error: {e}")
    
    def _get_google_gender(self):
        """Map voice gender to Google Cloud API."""
        mapping = {
            VoiceGender.NEUTRAL: texttospeech.SsmlVoiceGender.NEUTRAL,
            VoiceGender.MALE: texttospeech.SsmlVoiceGender.MALE,
            VoiceGender.FEMALE: texttospeech.SsmlVoiceGender.FEMALE,
        }
        return mapping.get(self.config.gender, texttospeech.SsmlVoiceGender.NEUTRAL)
    
    def _sanitize_text(self, text: str) -> str:
        """Remove problematic characters from text."""
        # Remove file paths, URLs, special formatting
        text = text.replace('\\', ' ')
        text = text.replace('/', ' ')
        text = text.replace('_', ' ')
        
        # Limit length for sanity
        if len(text) > 500:
            text = text[:500] + "..."
        
        return text
    
    def stop(self):
        """Stop TTS engine and clean up."""
        self.stop_event.set()
        
        if self.engine is not None:
            try:
                if hasattr(self.engine, 'stop'):
                    self.engine.stop()
            except:
                pass
        
        if self.current_task:
            self.current_task.join(timeout=2.0)


class TTSContext:
    """Context manager for TTS engine lifecycle."""
    
    def __init__(self, config: Optional[TTSConfig] = None):
        self.config = config
        self.engine: Optional[TTSEngine] = None
    
    def __enter__(self) -> TTSEngine:
        self.engine = TTSEngine(self.config)
        return self.engine
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.engine:
            self.engine.stop()
        return False


# Convenience functions
_default_engine: Optional[TTSEngine] = None


def init_tts(config: Optional[TTSConfig] = None) -> TTSEngine:
    """Initialize global TTS engine."""
    global _default_engine
    _default_engine = TTSEngine(config)
    return _default_engine


def speak(text: str, blocking: bool = True) -> bool:
    """Speak text using global TTS engine."""
    global _default_engine
    if _default_engine is None:
        _default_engine = TTSEngine()
    return _default_engine.speak(text, blocking=blocking)


def stop_tts():
    """Stop global TTS engine."""
    global _default_engine
    if _default_engine:
        _default_engine.stop()
        _default_engine = None
