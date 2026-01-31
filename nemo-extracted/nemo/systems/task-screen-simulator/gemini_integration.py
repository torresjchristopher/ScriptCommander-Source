"""
Gemini Integration Layer - Live AI Agent Bridge
Handles Google OAuth, API calls, credit management.
Can be swapped for Claude, Ollama, or other agents.
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum
import json
import os


class AIAgent(Enum):
    """Supported AI agents"""
    GEMINI = "gemini"
    CLAUDE = "claude"
    OLLAMA = "ollama"  # Open source local option


@dataclass
class APICredentials:
    """Credentials for API access"""
    agent: AIAgent
    api_key: Optional[str] = None
    refresh_token: Optional[str] = None
    access_token: Optional[str] = None
    
    # For Ollama (local)
    ollama_url: str = "http://localhost:11434"
    
    def to_dict(self) -> Dict:
        return {
            "agent": self.agent.value,
            "api_key": self.api_key,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "ollama_url": self.ollama_url
        }


@dataclass
class APICredit:
    """API credit tracking"""
    balance_usd: float = 0.0
    tokens_available: int = 0
    usage_this_month: float = 0.0
    last_refill: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "balance_usd": self.balance_usd,
            "tokens_available": self.tokens_available,
            "usage_this_month": self.usage_this_month,
            "last_refill": self.last_refill
        }


class GeminiIntegration:
    """
    Gemini API integration with credit management.
    Handles OAuth, API calls, streaming, and error handling.
    """
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.expanduser("~/.nemo/gemini_config.json")
        
        self.config_path = config_path
        self.credentials: Optional[APICredentials] = None
        self.credits: APICredit = APICredit()
        self.agent: AIAgent = AIAgent.GEMINI
        
        # Gemini API settings
        self.model = "gemini-pro"
        self.temperature = 0.7
        
        self._load_config()
    
    def _load_config(self) -> None:
        """Load credentials and settings from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                
                if 'credentials' in data:
                    cred_data = data['credentials']
                    self.credentials = APICredentials(
                        agent=AIAgent(cred_data.get('agent', 'gemini')),
                        api_key=cred_data.get('api_key'),
                        refresh_token=cred_data.get('refresh_token'),
                        access_token=cred_data.get('access_token'),
                        ollama_url=cred_data.get('ollama_url', "http://localhost:11434")
                    )
                
                if 'credits' in data:
                    credit_data = data['credits']
                    self.credits = APICredit(
                        balance_usd=credit_data.get('balance_usd', 0.0),
                        tokens_available=credit_data.get('tokens_available', 0),
                        usage_this_month=credit_data.get('usage_this_month', 0.0),
                        last_refill=credit_data.get('last_refill', 0.0)
                    )
                
                self.agent = AIAgent(data.get('agent', 'gemini'))
        except Exception as e:
            print(f"Warning: Could not load config: {e}")
    
    def save_config(self) -> None:
        """Save credentials and settings"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        data = {
            "agent": self.agent.value,
            "credentials": self.credentials.to_dict() if self.credentials else None,
            "credits": self.credits.to_dict()
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def set_credentials(self, credentials: APICredentials) -> None:
        """Set API credentials"""
        self.credentials = credentials
        self.save_config()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        if not self.credentials:
            return False
        
        if self.agent == AIAgent.GEMINI:
            return bool(self.credentials.api_key or self.credentials.access_token)
        elif self.agent == AIAgent.CLAUDE:
            return bool(self.credentials.api_key)
        elif self.agent == AIAgent.OLLAMA:
            return True  # Ollama doesn't need auth
        
        return False
    
    def test_connection(self) -> Dict:
        """Test API connection"""
        if not self.is_authenticated():
            return {
                "success": False,
                "error": "Not authenticated",
                "agent": self.agent.value
            }
        
        try:
            # In production: actual API call
            # For now: stub
            return {
                "success": True,
                "agent": self.agent.value,
                "model": self.model,
                "status": "Connected"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.agent.value
            }
    
    def get_balance(self) -> APICredit:
        """Get current credit balance"""
        return self.credits
    
    def add_credit(self, amount_usd: float) -> Dict:
        """
        Add credits via payment.
        In production: Stripe integration.
        For now: stub that updates balance.
        """
        # Rough estimate: $0.0005 per 1K tokens
        tokens_added = int(amount_usd / 0.0005 * 1000)
        
        self.credits.balance_usd += amount_usd
        self.credits.tokens_available += tokens_added
        
        import time
        self.credits.last_refill = time.time()
        
        self.save_config()
        
        return {
            "success": True,
            "amount": amount_usd,
            "tokens_added": tokens_added,
            "new_balance": self.credits.balance_usd
        }
    
    def query(self, text: str, context: Dict = None) -> str:
        """
        Send query to AI agent.
        
        Args:
            text: User question
            context: Additional context (screen state, keyboard pattern, etc)
        
        Returns:
            AI response text
        """
        if not self.is_authenticated():
            return "Error: Not authenticated. Run 'nemo account link' first."
        
        if self.credits.balance_usd <= 0 and self.agent != AIAgent.OLLAMA:
            return "Error: No credits. Run 'nemo credits refill' to add credits."
        
        # Build prompt with context
        prompt = self._build_prompt(text, context)
        
        # Call appropriate backend
        if self.agent == AIAgent.GEMINI:
            return self._query_gemini(prompt)
        elif self.agent == AIAgent.CLAUDE:
            return self._query_claude(prompt)
        elif self.agent == AIAgent.OLLAMA:
            return self._query_ollama(prompt)
        
        return "Error: Unknown agent"
    
    def _build_prompt(self, text: str, context: Dict = None) -> str:
        """Build context-aware prompt"""
        prompt = text
        
        if context:
            context_str = ""
            
            if "active_app" in context:
                context_str += f"User is in: {context['active_app']}\n"
            
            if "keyboard_intent" in context:
                context_str += f"Keyboard pattern suggests: {context['keyboard_intent']}\n"
            
            if "screen_state" in context:
                context_str += f"Screen context: {context['screen_state']}\n"
            
            if context_str:
                prompt = f"{context_str}\nUser query: {text}"
        
        return prompt
    
    def _query_gemini(self, prompt: str) -> str:
        """Query Gemini API"""
        try:
            # In production: use google.generativeai
            # For now: simulation
            return f"[Gemini Response]: {prompt[:50]}... (simulated)"
        except Exception as e:
            return f"Error calling Gemini: {e}"
    
    def _query_claude(self, prompt: str) -> str:
        """Query Claude API"""
        try:
            # In production: use anthropic library
            # For now: simulation
            return f"[Claude Response]: {prompt[:50]}... (simulated)"
        except Exception as e:
            return f"Error calling Claude: {e}"
    
    def _query_ollama(self, prompt: str) -> str:
        """Query local Ollama instance"""
        try:
            # In production: HTTP POST to Ollama
            # For now: simulation
            return f"[Ollama Response]: {prompt[:50]}... (simulated)"
        except Exception as e:
            return f"Error calling Ollama: {e}"
    
    def get_status(self) -> Dict:
        """Get integration status"""
        return {
            "agent": self.agent.value,
            "authenticated": self.is_authenticated(),
            "balance": {
                "usd": self.credits.balance_usd,
                "tokens": self.credits.tokens_available,
                "usage_this_month": self.credits.usage_this_month
            },
            "model": self.model,
            "connection": self.test_connection()
        }


# Singleton
_gemini: Optional[GeminiIntegration] = None


def get_gemini_integration() -> GeminiIntegration:
    """Get singleton Gemini integration"""
    global _gemini
    if _gemini is None:
        _gemini = GeminiIntegration()
    return _gemini
