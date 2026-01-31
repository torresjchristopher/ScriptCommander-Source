"""
Screen Analyzer - Real-time screen content analysis
Reads what's currently visible without storing anything.
Pure analysis. Pure inference. No persistence.
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum


class UIElementType(Enum):
    """Types of UI elements"""
    INPUT_FIELD = "input"
    BUTTON = "button"
    TEXT = "text"
    IMAGE = "image"
    LINK = "link"
    WINDOW = "window"
    MENU = "menu"
    FORM = "form"


@dataclass
class UIElement:
    """Single UI element on screen"""
    element_type: UIElementType
    text: str
    position: tuple = (0, 0)  # x, y
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ScreenState:
    """Current state of screen (real-time analysis, no storage)"""
    active_window: str = ""
    active_app: str = ""
    window_title: str = ""
    
    # Visible UI elements
    input_fields: List[UIElement] = None
    buttons: List[UIElement] = None
    text_content: List[UIElement] = None
    visible_urls: List[str] = None
    form_labels: List[str] = None
    
    # Context
    page_title: str = ""
    page_url: str = ""
    detected_language: str = "en"
    content_type: str = ""  # email, document, web, code, etc.
    
    # Derived
    context_hash: int = 0  # For quick comparison
    
    def __post_init__(self):
        if self.input_fields is None:
            self.input_fields = []
        if self.buttons is None:
            self.buttons = []
        if self.text_content is None:
            self.text_content = []
        if self.visible_urls is None:
            self.visible_urls = []
        if self.form_labels is None:
            self.form_labels = []


class ScreenAnalyzer:
    """
    Analyzes current screen state.
    Uses accessibility APIs to read what's visible.
    No recording. No storage. Pure analysis.
    """
    
    def __init__(self):
        self.current_state: Optional[ScreenState] = None
        self.last_state: Optional[ScreenState] = None
        
        # Content patterns for detection
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.url_pattern = re.compile(r'https?://[^\s]+')
        self.code_pattern = re.compile(r'(def |class |function |const |let |var |\{|\})')
    
    def analyze_current_screen(self) -> ScreenState:
        """
        Analyze current screen state.
        In production: use accessibility APIs (UIA on Windows, JAWS on screen readers, etc.)
        For now: simulation mode
        """
        state = ScreenState()
        
        # In real implementation:
        # - Use pyautogui to get screen size
        # - Use accessibility APIs to read UI structure
        # - Use OCR (pytesseract) to read visible text
        # - Parse DOM if web app (using accessibility tree)
        
        # Simulate for now
        state.active_app = "outlook.exe"
        state.active_window = "Outlook"
        state.window_title = "Meeting Notes - Outlook"
        state.content_type = "email"
        state.detected_language = "en"
        
        # Simulate UI elements
        state.form_labels = ["To:", "Subject:", "Body:"]
        state.input_fields = [
            UIElement(UIElementType.INPUT_FIELD, "", (100, 100), {"label": "To"}),
            UIElement(UIElementType.INPUT_FIELD, "", (100, 140), {"label": "Subject"}),
            UIElement(UIElementType.INPUT_FIELD, "", (100, 200), {"label": "Body"}),
        ]
        state.buttons = [
            UIElement(UIElementType.BUTTON, "Send", (200, 400)),
            UIElement(UIElementType.BUTTON, "Cancel", (300, 400)),
        ]
        
        # Calculate context hash (for change detection)
        state.context_hash = hash((
            state.active_app,
            state.content_type,
            tuple(state.form_labels)
        ))
        
        # Update state tracking
        self.last_state = self.current_state
        self.current_state = state
        
        return state
    
    def detect_content_type(self, content: str) -> str:
        """Detect what type of content user is interacting with"""
        if self.email_pattern.search(content):
            return "email"
        elif self.url_pattern.search(content):
            return "web"
        elif self.code_pattern.search(content):
            return "code"
        elif len(content) > 500:
            return "document"
        else:
            return "text"
    
    def extract_visible_text(self) -> str:
        """Extract all visible text from current screen"""
        if not self.current_state:
            return ""
        
        texts = []
        texts.extend([t.text for t in self.current_state.text_content])
        texts.extend(self.current_state.form_labels)
        texts.extend([b.text for b in self.current_state.buttons])
        
        return " ".join(texts)
    
    def get_state_change(self) -> Dict:
        """What changed since last analysis?"""
        if not self.last_state or not self.current_state:
            return {"new_state": True}
        
        changes = {}
        
        if self.last_state.active_window != self.current_state.active_window:
            changes["window_changed"] = True
        
        if self.last_state.content_type != self.current_state.content_type:
            changes["content_type_changed"] = True
        
        if self.last_state.context_hash != self.current_state.context_hash:
            changes["context_changed"] = True
        
        return changes
    
    def get_current_state(self) -> Optional[ScreenState]:
        """Get current screen state"""
        return self.current_state
    
    def get_context_summary(self) -> Dict[str, str]:
        """Summarize current screen context for AI/inference"""
        if not self.current_state:
            return {}
        
        return {
            "app": self.current_state.active_app,
            "window": self.current_state.window_title,
            "content_type": self.current_state.content_type,
            "visible_labels": ", ".join(self.current_state.form_labels),
            "buttons": ", ".join([b.text for b in self.current_state.buttons]),
            "language": self.current_state.detected_language
        }


# Singleton
_analyzer: Optional[ScreenAnalyzer] = None


def get_screen_analyzer() -> ScreenAnalyzer:
    """Get singleton analyzer"""
    global _analyzer
    if _analyzer is None:
        _analyzer = ScreenAnalyzer()
    return _analyzer
