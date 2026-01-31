"""
Temporal Inference Engine - Simulate past/future without storage
Given current keyboard + screen state, infer what WAS (rewind) or WILL BE (forward).
No recording. Pure inference.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List
from enum import Enum


class InferenceMode(Enum):
    """Direction of inference"""
    REWIND = "rewind"      # Simulate what was
    FORWARD = "forward"    # Predict what will be


@dataclass
class InferredState:
    """Inferred screen/keyboard state"""
    mode: InferenceMode
    confidence: float  # 0-1, how confident is this inference?
    
    # Inferred content
    likely_text: str = ""
    likely_actions: List[str] = None
    likely_window: str = ""
    
    # Reasoning
    reasoning: str = ""
    
    def __post_init__(self):
        if self.likely_actions is None:
            self.likely_actions = []


class TemporalInferenceEngine:
    """
    Infers what was (rewind) or what will be (forward).
    Uses keyboard signature + screen context.
    No storage. Pure mathematical inference.
    """
    
    def __init__(self, keyboard_synthesizer=None, screen_analyzer=None):
        self.keyboard = keyboard_synthesizer
        self.screen = screen_analyzer
        
        # Inference cache (recent inferences only, no history)
        self.last_inference: Optional[InferredState] = None
    
    def infer_rewind(self, seconds_back: int = 5) -> InferredState:
        """
        Infer what was on screen N seconds ago.
        Uses keyboard patterns + screen context.
        """
        confidence = 0.0
        reasoning_parts = []
        
        # Factor 1: Keyboard pattern suggests what user was doing
        if self.keyboard:
            style = self.keyboard.get_user_style()
            intent = style["intent"]
            
            if intent == "editing":
                confidence += 0.3
                reasoning_parts.append("Keyboard pattern shows editing (backspace, corrections)")
            elif intent == "searching":
                confidence += 0.2
                reasoning_parts.append("Keyboard pattern shows search behavior")
            elif intent == "coding":
                confidence += 0.3
                reasoning_parts.append("Keyboard pattern shows coding activity")
        
        # Factor 2: Screen context shows where user likely was
        if self.screen:
            state = self.screen.get_current_state()
            if state:
                if state.content_type == "email":
                    confidence += 0.2
                    reasoning_parts.append("Current email context suggests previous email editing")
                elif state.content_type == "web":
                    confidence += 0.2
                    reasoning_parts.append("Web context suggests browsing history")
                elif state.content_type == "code":
                    confidence += 0.25
                    reasoning_parts.append("Code context suggests previous edit location")
        
        # Inference: what was user likely doing?
        likely_text = self._infer_previous_content(seconds_back)
        likely_actions = self._infer_previous_actions(seconds_back)
        
        inference = InferredState(
            mode=InferenceMode.REWIND,
            confidence=min(confidence, 1.0),
            likely_text=likely_text,
            likely_actions=likely_actions,
            likely_window=self._infer_previous_window(),
            reasoning="; ".join(reasoning_parts)
        )
        
        self.last_inference = inference
        return inference
    
    def infer_forward(self, seconds_ahead: int = 5) -> InferredState:
        """
        Predict what user will likely do next N seconds.
        Uses keyboard patterns + screen context + intent.
        """
        confidence = 0.0
        reasoning_parts = []
        
        # Factor 1: What's the user's next likely action based on intent?
        if self.keyboard:
            intent = self.keyboard.get_detected_intent()
            
            if intent == "editing":
                confidence += 0.25
                reasoning_parts.append("User in editing mode - likely to continue editing or save")
            elif intent == "search":
                confidence += 0.2
                reasoning_parts.append("Search pattern detected - likely to click/navigate")
            elif intent == "coding":
                confidence += 0.3
                reasoning_parts.append("Coding activity - likely to test/debug/commit")
            elif intent == "composition":
                confidence += 0.2
                reasoning_parts.append("Composition mode - likely to review/send")
        
        # Factor 2: What's the natural next step based on current screen?
        if self.screen:
            state = self.screen.get_current_state()
            if state:
                # If in email, next is likely send/save
                if state.content_type == "email" and state.buttons:
                    confidence += 0.2
                    reasoning_parts.append("Email form likely progresses to send")
                
                # If viewing results, next is likely click
                if state.content_type == "web":
                    confidence += 0.15
                    reasoning_parts.append("Web context suggests navigation click likely")
        
        # Predict next actions
        likely_actions = self._predict_next_actions()
        likely_text = self._predict_next_input()
        
        inference = InferredState(
            mode=InferenceMode.FORWARD,
            confidence=min(confidence, 1.0),
            likely_text=likely_text,
            likely_actions=likely_actions,
            likely_window=self._predict_next_window(),
            reasoning="; ".join(reasoning_parts)
        )
        
        self.last_inference = inference
        return inference
    
    def _infer_previous_content(self, seconds_back: int) -> str:
        """What text was user likely editing/viewing?"""
        # In production: ML model trained on user's past patterns
        # For now: reasonable inference based on context
        
        if self.keyboard:
            intent = self.keyboard.get_detected_intent()
            
            if intent == "coding":
                return "[previous code implementation]"
            elif intent == "composition":
                return "[draft text being composed]"
            elif intent == "editing":
                return "[edited document content]"
        
        return "[previous screen content]"
    
    def _infer_previous_actions(self, seconds_back: int) -> List[str]:
        """What actions led to current state?"""
        actions = []
        
        if self.keyboard:
            typing_speed = self.keyboard.get_typing_speed()
            correction_freq = self.keyboard.current_signature.correction_freq
            
            if correction_freq > 0.1:
                actions.append("corrected_text")
            if typing_speed > 60:
                actions.append("rapid_typing")
            else:
                actions.append("deliberate_editing")
        
        return actions
    
    def _infer_previous_window(self) -> str:
        """What window was user in?"""
        if self.screen:
            state = self.screen.get_current_state()
            if state:
                return state.active_window
        return "[previous window]"
    
    def _predict_next_actions(self) -> List[str]:
        """What actions likely come next?"""
        actions = []
        
        if self.keyboard:
            intent = self.keyboard.get_detected_intent()
            
            if intent == "editing":
                actions.extend(["save", "review"])
            elif intent == "coding":
                actions.extend(["test", "debug", "commit"])
            elif intent == "composition":
                actions.extend(["review", "send"])
            elif intent == "search":
                actions.extend(["click", "navigate"])
            else:
                actions.append("continue_typing")
        
        return actions
    
    def _predict_next_input(self) -> str:
        """What will user likely input next?"""
        if self.keyboard:
            intent = self.keyboard.get_detected_intent()
            
            if intent == "email":
                return "[likely to type email body or subject]"
            elif intent == "code":
                return "[likely to type code logic]"
            elif intent == "search":
                return "[likely to type search query]"
        
        return "[next likely input]"
    
    def _predict_next_window(self) -> str:
        """What application/window next?"""
        if self.keyboard:
            intent = self.keyboard.get_detected_intent()
            
            if intent == "coding":
                return "[ IDE or terminal]"
            elif intent == "email":
                return "[mail client]"
            elif intent == "search":
                return "[browser]"
        
        if self.screen:
            state = self.screen.get_current_state()
            if state:
                return state.active_window
        
        return "[next likely window]"
    
    def get_confidence_score(self) -> float:
        """How confident is current inference?"""
        if self.last_inference:
            return self.last_inference.confidence
        return 0.0
    
    def get_last_inference(self) -> Optional[InferredState]:
        """Get most recent inference"""
        return self.last_inference
    
    def as_human_readable(self, inference: InferredState) -> str:
        """Convert inference to human-readable description"""
        direction = "Before (rewind)" if inference.mode == InferenceMode.REWIND else "Next (forward)"
        
        return f"""
{direction}:
  Confidence: {inference.confidence*100:.0f}%
  Likely window: {inference.likely_window}
  Likely content: {inference.likely_text}
  Likely next steps: {', '.join(inference.likely_actions)}
  Reasoning: {inference.reasoning}
        """


# Singleton
_engine: Optional[TemporalInferenceEngine] = None


def get_temporal_inference_engine(keyboard=None, screen=None) -> TemporalInferenceEngine:
    """Get singleton engine"""
    global _engine
    if _engine is None:
        # Try to import and get singletons
        try:
            if keyboard is None:
                from keyboard_synthesizer import get_keyboard_synthesizer
                keyboard = get_keyboard_synthesizer()
        except:
            pass
        
        try:
            if screen is None:
                from screen_analyzer import get_screen_analyzer
                screen = get_screen_analyzer()
        except:
            pass
        
        _engine = TemporalInferenceEngine(keyboard, screen)
    
    return _engine
