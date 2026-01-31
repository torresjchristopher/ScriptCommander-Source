"""
Voice Assistant CLI - Live AI Butler
RIGHT ALT hotkey for voice chat with AI assistant
Internet-enabled. Voice input/output. Like a butler.
"""

from dataclasses import dataclass
from typing import Optional, Dict
from enum import Enum
import threading


class VoiceAssistantMode(Enum):
    """Voice assistant operating modes"""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    RESPONDING = "responding"


@dataclass
class VoiceQuery:
    """Voice query to AI"""
    text: str
    timestamp: float = 0.0
    context: Dict = None
    
    def __post_init__(self):
        import time
        if self.timestamp == 0:
            self.timestamp = time.time()
        if self.context is None:
            self.context = {}


@dataclass
class VoiceResponse:
    """Response from AI"""
    text: str
    audio_path: Optional[str] = None
    confidence: float = 0.0
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class VoiceAssistant:
    """
    Live AI voice assistant.
    Accessible via RIGHT ALT hotkey.
    Responds with voice (butler-like).
    Has internet connectivity for real-time AI.
    """
    
    def __init__(self):
        self.mode = VoiceAssistantMode.IDLE
        self.current_query: Optional[VoiceQuery] = None
        self.last_response: Optional[VoiceResponse] = None
        
        # AI backends (configurable)
        self.ai_backend = "openai"  # or "claude", "gemini"
        self.voice_model = "elevenlabs"  # Voice synthesis
        
        # Session context
        self.conversation_history = []
        self.max_history = 10
    
    def activate_hotkey(self) -> None:
        """RIGHT ALT pressed - start listening"""
        self.mode = VoiceAssistantMode.LISTENING
        print("[🎤] Listening... (speak now)")
    
    def deactivate_hotkey(self) -> None:
        """RIGHT ALT released - stop listening"""
        if self.mode == VoiceAssistantMode.LISTENING:
            self.mode = VoiceAssistantMode.PROCESSING
            self._process_query()
    
    def process_voice_input(self, audio_text: str) -> VoiceResponse:
        """
        Process voice input (transcribed to text).
        Send to AI backend.
        Get response.
        Convert to voice.
        """
        self.mode = VoiceAssistantMode.PROCESSING
        
        query = VoiceQuery(text=audio_text)
        self.current_query = query
        
        # Add to history
        self.conversation_history.append({"role": "user", "content": audio_text})
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
        
        # Get AI response
        response_text = self._call_ai_backend(audio_text)
        
        # Create response object
        response = VoiceResponse(
            text=response_text,
            confidence=0.95,  # Confidence that response is relevant
            metadata={
                "backend": self.ai_backend,
                "context": query.context
            }
        )
        
        self.last_response = response
        
        # Convert to speech
        self._synthesize_voice(response_text)
        
        self.mode = VoiceAssistantMode.RESPONDING
        
        return response
    
    def _process_query(self) -> None:
        """Process current query (stub)"""
        if self.current_query:
            self.process_voice_input(self.current_query.text)
    
    def _call_ai_backend(self, query: str) -> str:
        """
        Call AI backend to get response.
        In production: OpenAI, Anthropic, Google APIs
        """
        # Stub responses for now
        if "what" in query.lower():
            return "I can help you with that. What would you like to know?"
        elif "how" in query.lower():
            return "Here's how to do that..."
        elif "why" in query.lower():
            return "Great question. The reason is..."
        else:
            return f"You asked: {query}. I'm processing that now."
    
    def _synthesize_voice(self, text: str) -> None:
        """
        Convert text to voice.
        In production: ElevenLabs, Google TTS, or similar
        """
        print(f"🎵 [Voice Response]: {text}")
    
    def get_status(self) -> Dict:
        """Get current status"""
        return {
            "mode": self.mode.value,
            "backend": self.ai_backend,
            "last_query": self.current_query.text if self.current_query else None,
            "last_response": self.last_response.text if self.last_response else None,
            "conversation_history_length": len(self.conversation_history)
        }
    
    def set_ai_backend(self, backend: str) -> None:
        """Change AI backend"""
        valid_backends = ["openai", "claude", "gemini"]
        if backend in valid_backends:
            self.ai_backend = backend
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        self.current_query = None
        self.last_response = None


class VoiceAssistantCLI:
    """CLI interface for voice assistant"""
    
    def __init__(self):
        self.assistant = VoiceAssistant()
        self.running = False
    
    def start(self) -> None:
        """Start the voice assistant daemon"""
        self.running = True
        print("[✓] Voice Assistant started")
        print("[ℹ️] Press RIGHT ALT to activate microphone")
        print("[ℹ️] Hold and speak your question")
        print("[ℹ️] Release to send")
    
    def stop(self) -> None:
        """Stop the voice assistant"""
        self.running = False
        print("[✓] Voice Assistant stopped")
    
    def handle_hotkey_press(self) -> None:
        """Called when RIGHT ALT is pressed"""
        if self.running:
            self.assistant.activate_hotkey()
    
    def handle_hotkey_release(self) -> None:
        """Called when RIGHT ALT is released"""
        if self.running:
            self.assistant.deactivate_hotkey()
    
    def display_status(self) -> None:
        """Show current status"""
        status = self.assistant.get_status()
        
        print("\n[🎤 Voice Assistant Status]")
        print(f"  Mode: {status['mode']}")
        print(f"  Backend: {status['backend']}")
        print(f"  Last query: {status['last_query'] or 'None'}")
        print(f"  Last response: {status['last_response'] or 'None'}")
        print(f"  History: {status['conversation_history_length']} messages")
    
    def configure(self) -> None:
        """Configure voice assistant"""
        print("\n[⚙️ Voice Assistant Configuration]")
        print("1. OpenAI (GPT-4)")
        print("2. Claude (Anthropic)")
        print("3. Gemini (Google)")
        
        choice = input("Select AI backend (1-3): ")
        
        backends = {"1": "openai", "2": "claude", "3": "gemini"}
        if choice in backends:
            self.assistant.set_ai_backend(backends[choice])
            print(f"[✓] Backend set to {self.assistant.ai_backend}")


# Singleton
_assistant_cli: Optional[VoiceAssistantCLI] = None


def get_voice_assistant_cli() -> VoiceAssistantCLI:
    """Get singleton CLI"""
    global _assistant_cli
    if _assistant_cli is None:
        _assistant_cli = VoiceAssistantCLI()
    return _assistant_cli


if __name__ == "__main__":
    # Test
    cli = get_voice_assistant_cli()
    cli.start()
    cli.display_status()
    
    # Simulate query
    print("\nSimulating voice query...")
    response = cli.assistant.process_voice_input("What is machine learning?")
    print(f"\nResponse: {response.text}")
    
    cli.stop()
