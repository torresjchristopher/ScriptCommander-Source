"""
Keyboard Synthesizer - Learn user's 35-D keystroke fingerprint
Synthesizes keyboard patterns + screen context to understand user intent
No storage. Pure learning and inference.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from collections import deque
import time


@dataclass
class KeystrokeSignature:
    """User's current keystroke pattern (35-D vector)"""
    # Timing (12-D)
    dwell_time_mean: float = 0.0
    dwell_time_std: float = 0.0
    flight_time_mean: float = 0.0
    flight_time_std: float = 0.0
    latency: float = 0.0
    latency_variance: float = 0.0
    inter_key_delay_mean: float = 0.0
    inter_key_delay_std: float = 0.0
    key_repeat_interval: float = 0.0
    rapid_fire_count: int = 0
    pause_frequency: float = 0.0
    session_duration: float = 0.0
    
    # Pressure (8-D) - estimated from typing speed
    pressure_mean: float = 0.0
    pressure_std: float = 0.0
    pressure_skew: float = 0.0
    pressure_acceleration: float = 0.0
    max_pressure: float = 0.0
    min_pressure: float = 0.0
    pressure_consistency: float = 0.0
    pressure_pattern_hash: int = 0
    
    # Patterns (10-D)
    key_order_entropy: float = 0.0
    repetition_count: int = 0
    correction_freq: float = 0.0
    error_recovery_time: float = 0.0
    typing_rhythm_score: float = 0.0
    burst_count: int = 0
    burst_duration_mean: float = 0.0
    idle_duration_mean: float = 0.0
    digraph_freq: float = 0.0
    trigraph_freq: float = 0.0
    
    # Intent (5-D)
    search_pattern: float = 0.0
    editing_pattern: float = 0.0
    coding_pattern: float = 0.0
    navigation_pattern: float = 0.0
    composition_pattern: float = 0.0
    
    def to_vector(self) -> np.ndarray:
        """Convert to 35-D vector"""
        return np.array([
            # Timing (12)
            self.dwell_time_mean, self.dwell_time_std, self.flight_time_mean, self.flight_time_std,
            self.latency, self.latency_variance, self.inter_key_delay_mean, self.inter_key_delay_std,
            self.key_repeat_interval, self.rapid_fire_count, self.pause_frequency, self.session_duration,
            # Pressure (8)
            self.pressure_mean, self.pressure_std, self.pressure_skew, self.pressure_acceleration,
            self.max_pressure, self.min_pressure, self.pressure_consistency, self.pressure_pattern_hash,
            # Patterns (10)
            self.key_order_entropy, self.repetition_count, self.correction_freq, self.error_recovery_time,
            self.typing_rhythm_score, self.burst_count, self.burst_duration_mean, self.idle_duration_mean,
            self.digraph_freq, self.trigraph_freq,
            # Intent (5)
            self.search_pattern, self.editing_pattern, self.coding_pattern, self.navigation_pattern,
            self.composition_pattern
        ])


class KeyboardSynthesizer:
    """
    Learns user's unique keyboard pattern from raw keystroke data.
    Continuously updates 35-D signature.
    Infers user intent from pattern + screen context.
    """
    
    def __init__(self):
        self.current_signature = KeystrokeSignature()
        self.keystroke_history: deque = deque(maxlen=500)  # Last 500 keystrokes
        
        self.session_start = time.time()
        self.last_keystroke_time = time.time()
        
        # Pattern learning
        self.detected_patterns = {
            "search": 0.0,
            "editing": 0.0,
            "coding": 0.0,
            "navigation": 0.0,
            "composition": 0.0
        }
    
    def record_keystroke(self, key: str, duration_ms: float = 0) -> None:
        """
        Record a keystroke.
        
        Args:
            key: The key pressed
            duration_ms: How long key was held
        """
        current_time = time.time()
        inter_key_delay = (current_time - self.last_keystroke_time) * 1000
        
        keystroke_data = {
            "key": key,
            "timestamp": current_time,
            "dwell_time_ms": duration_ms,
            "inter_key_delay_ms": inter_key_delay
        }
        
        self.keystroke_history.append(keystroke_data)
        self.last_keystroke_time = current_time
        
        # Update signature
        self._update_signature()
    
    def _update_signature(self) -> None:
        """Update 35-D keystroke signature from history"""
        if not self.keystroke_history:
            return
        
        history = list(self.keystroke_history)
        
        # Calculate timing metrics
        dwell_times = [k["dwell_time_ms"] for k in history if k["dwell_time_ms"] > 0]
        if dwell_times:
            self.current_signature.dwell_time_mean = np.mean(dwell_times)
            self.current_signature.dwell_time_std = np.std(dwell_times)
        
        inter_key_delays = [k["inter_key_delay_ms"] for k in history]
        if inter_key_delays:
            self.current_signature.inter_key_delay_mean = np.mean(inter_key_delays)
            self.current_signature.inter_key_delay_std = np.std(inter_key_delays)
        
        # Detect rapid-fire typing
        rapid_fire = sum(1 for d in inter_key_delays if d < 50)
        self.current_signature.rapid_fire_count = rapid_fire
        
        # Session duration
        self.current_signature.session_duration = time.time() - self.session_start
        
        # Pattern detection
        self._detect_intent_patterns(history)
    
    def _detect_intent_patterns(self, history: List[Dict]) -> None:
        """Detect user intent patterns from keystroke sequence"""
        if not history:
            return
        
        keys = [k["key"] for k in history]
        keys_str = "".join(keys[-20:])  # Last 20 keys
        
        # Search pattern: typical search queries
        if any(q in keys_str.lower() for q in ["@", "gmail", "search", "google"]):
            self.detected_patterns["search"] += 0.1
        
        # Editing pattern: lots of backspace, arrow keys
        if keys_str.count("backspace") > 3:
            self.detected_patterns["editing"] += 0.1
        
        # Coding pattern: brackets, semicolons, special chars
        if any(c in keys_str for c in ["{", "}", "[", "]", ";", "def ", "class "]):
            self.detected_patterns["coding"] += 0.1
        
        # Navigation: arrow keys, page up/down
        if any(k in keys for k in ["up", "down", "left", "right", "pageup", "pagedown"]):
            self.detected_patterns["navigation"] += 0.1
        
        # Composition: long pauses between words, deliberate pacing
        if self.current_signature.inter_key_delay_mean > 200:
            self.detected_patterns["composition"] += 0.1
        
        # Normalize
        total = sum(self.detected_patterns.values())
        if total > 0:
            for k in self.detected_patterns:
                self.detected_patterns[k] /= total
        
        # Update signature
        self.current_signature.search_pattern = self.detected_patterns["search"]
        self.current_signature.editing_pattern = self.detected_patterns["editing"]
        self.current_signature.coding_pattern = self.detected_patterns["coding"]
        self.current_signature.navigation_pattern = self.detected_patterns["navigation"]
        self.current_signature.composition_pattern = self.detected_patterns["composition"]
    
    def get_current_signature(self) -> KeystrokeSignature:
        """Get current 35-D keystroke signature"""
        return self.current_signature
    
    def get_signature_vector(self) -> np.ndarray:
        """Get as 35-D numpy vector"""
        return self.current_signature.to_vector()
    
    def get_detected_intent(self) -> str:
        """What is user likely doing based on keyboard patterns?"""
        intents = self.detected_patterns
        if not intents:
            return "unknown"
        
        detected = max(intents.items(), key=lambda x: x[1])
        return detected[0] if detected[1] > 0.2 else "mixed"
    
    def get_typing_speed(self) -> float:
        """Words per minute estimate"""
        if self.current_signature.inter_key_delay_mean == 0:
            return 0
        
        # Rough estimate: 5 chars per word
        chars_per_sec = 1000 / self.current_signature.inter_key_delay_mean
        words_per_min = (chars_per_sec / 5) * 60
        
        return max(0, words_per_min)
    
    def get_user_style(self) -> Dict[str, str]:
        """Get detected user style markers"""
        return {
            "intent": self.get_detected_intent(),
            "typing_speed": f"{self.get_typing_speed():.0f} WPM",
            "consistency": "high" if self.current_signature.dwell_time_std < 50 else "low",
            "error_rate": "high" if self.current_signature.correction_freq > 0.1 else "low",
            "pattern": "rapid" if self.current_signature.rapid_fire_count > 10 else "deliberate"
        }


# Singleton
_synthesizer: Optional[KeyboardSynthesizer] = None


def get_keyboard_synthesizer() -> KeyboardSynthesizer:
    """Get singleton synthesizer"""
    global _synthesizer
    if _synthesizer is None:
        _synthesizer = KeyboardSynthesizer()
    return _synthesizer
