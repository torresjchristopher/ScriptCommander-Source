"""
Nemo Four-Button Interface: The Human Element.

1. RIGHT ALT: Internet AI (voice input to Gemini)
2. LEFT ALT (tap): TTS Button (text-to-speech output)
3. LEFT ALT + LEFT ARROW: REWIND (inference backward)
4. LEFT ALT + RIGHT ARROW: FORWARD (inference forward)

This replaces the qwerty keyboard for natural human interaction.
Voice → TTS synthesis is the future.
"""

import logging
import threading
import time
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable, Dict
from collections import defaultdict

try:
    from pynput import keyboard
except ImportError:
    keyboard = None

try:
    import win32api
    import win32con
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


class ButtonState(Enum):
    """State of button press."""
    IDLE = "idle"
    PRESSED = "pressed"
    HELD = "held"
    RELEASED = "released"


@dataclass
class ButtonEvent:
    """A button event."""
    button: str  # "left_alt", "right_alt", "left_arrow", "right_arrow"
    state: ButtonState
    timestamp: float
    duration: Optional[float] = None  # For press duration
    combo: Optional[str] = None  # "left_alt+left_arrow", etc.


class FourButtonInterface:
    """
    Nemo's four-button interface for natural interaction.
    
    Buttons:
    - RIGHT ALT: Internet AI voice hotkey
    - LEFT ALT (tap): TTS button
    - LEFT ALT + LEFT ARROW: REWIND
    - LEFT ALT + RIGHT ARROW: FORWARD
    
    Behavior:
    - TAP (< 200ms): Triggers action
    - HOLD (>= 200ms): Enters mode (for streaming)
    """
    
    # Timing thresholds
    TAP_THRESHOLD_MS = 200
    HOLD_THRESHOLD_MS = 200
    
    def __init__(self):
        """Initialize four-button interface."""
        self.logger = logging.getLogger(__name__)
        
        # Button state tracking
        self.button_states: Dict[str, ButtonState] = {
            'left_alt': ButtonState.IDLE,
            'right_alt': ButtonState.IDLE,
            'left_arrow': ButtonState.IDLE,
            'right_arrow': ButtonState.IDLE,
        }
        
        # Press timing
        self.press_times: Dict[str, float] = {}
        
        # Callbacks
        self.callbacks: Dict[str, Callable[[ButtonEvent], None]] = {
            'right_alt_tap': None,      # Internet AI voice
            'right_alt_hold': None,
            'left_alt_tap': None,       # TTS button
            'left_alt_hold': None,
            'rewind': None,             # LEFT ALT + LEFT ARROW
            'forward': None,            # LEFT ALT + RIGHT ARROW
        }
        
        # Current key state
        self.keys_pressed = set()
        self.listener = None
        self.running = False
    
    def register_callback(self, action: str, callback: Callable[[ButtonEvent], None]):
        """Register callback for a button action."""
        if action in self.callbacks:
            self.callbacks[action] = callback
            self.logger.info(f"Registered callback for {action}")
        else:
            self.logger.warning(f"Unknown action: {action}")
    
    def start(self):
        """Start listening for button presses."""
        if self.running:
            return
        
        self.running = True
        
        try:
            if keyboard:
                # Use pynput listener
                self.listener = keyboard.Listener(
                    on_press=self._on_press,
                    on_release=self._on_release,
                )
                self.listener.start()
                self.logger.info("Four-button interface started (pynput)")
            else:
                self.logger.warning("pynput not available. Button interface disabled.")
        except Exception as e:
            self.logger.error(f"Failed to start button interface: {e}")
            self.running = False
    
    def stop(self):
        """Stop listening for button presses."""
        self.running = False
        
        if self.listener:
            self.listener.stop()
            self.listener.join()
    
    def _on_press(self, key):
        """Handle key press."""
        if not self.running:
            return
        
        try:
            button_name = self._map_key(key)
            if button_name is None:
                return
            
            # Track press time
            if button_name not in self.press_times:
                self.press_times[button_name] = time.time()
            
            # Update state
            self.button_states[button_name] = ButtonState.PRESSED
            self.keys_pressed.add(button_name)
            
            # Check for combos
            self._check_combo()
            
        except Exception as e:
            self.logger.error(f"Error in on_press: {e}")
    
    def _on_release(self, key):
        """Handle key release."""
        if not self.running:
            return
        
        try:
            button_name = self._map_key(key)
            if button_name is None:
                return
            
            # Calculate press duration
            press_time = self.press_times.get(button_name, time.time())
            duration_ms = (time.time() - press_time) * 1000
            
            # Update state
            self.button_states[button_name] = ButtonState.RELEASED
            
            if button_name in self.keys_pressed:
                self.keys_pressed.remove(button_name)
            
            # Determine if TAP or HOLD
            if duration_ms < self.TAP_THRESHOLD_MS:
                self._handle_tap(button_name)
            else:
                self._handle_hold_end(button_name, duration_ms)
            
            # Clean up
            if button_name in self.press_times:
                del self.press_times[button_name]
            
            self.button_states[button_name] = ButtonState.IDLE
            
        except Exception as e:
            self.logger.error(f"Error in on_release: {e}")
    
    def _map_key(self, key) -> Optional[str]:
        """Map pynput key to button name."""
        try:
            # Special keys
            if hasattr(key, 'name'):
                key_name = key.name.lower()
                
                if 'alt' in key_name:
                    if key_name == 'alt_l':
                        return 'left_alt'
                    elif key_name == 'alt_r':
                        return 'right_alt'
                
                elif key_name == 'left':
                    return 'left_arrow'
                elif key_name == 'right':
                    return 'right_arrow'
            
            # Character keys
            elif hasattr(key, 'char'):
                char = key.char.lower()
                if char in ['←', 'left']:
                    return 'left_arrow'
                elif char in ['→', 'right']:
                    return 'right_arrow'
            
        except Exception as e:
            self.logger.debug(f"Error mapping key {key}: {e}")
        
        return None
    
    def _check_combo(self):
        """Check if a combo is being pressed."""
        # Check for LEFT ALT + LEFT ARROW (REWIND)
        if ('left_alt' in self.keys_pressed and 'left_arrow' in self.keys_pressed):
            if self.button_states['left_arrow'] == ButtonState.PRESSED:
                self._trigger_action('rewind')
        
        # Check for LEFT ALT + RIGHT ARROW (FORWARD)
        if ('left_alt' in self.keys_pressed and 'right_arrow' in self.keys_pressed):
            if self.button_states['right_arrow'] == ButtonState.PRESSED:
                self._trigger_action('forward')
    
    def _handle_tap(self, button_name: str):
        """Handle a TAP (short press)."""
        if button_name == 'right_alt':
            self._trigger_action('right_alt_tap')
        elif button_name == 'left_alt':
            # Only trigger if not part of combo
            if 'left_arrow' not in self.keys_pressed and 'right_arrow' not in self.keys_pressed:
                self._trigger_action('left_alt_tap')
    
    def _handle_hold_end(self, button_name: str, duration_ms: float):
        """Handle end of HOLD (long press)."""
        if button_name == 'right_alt':
            self._trigger_action('right_alt_hold')
        elif button_name == 'left_alt':
            if 'left_arrow' not in self.keys_pressed and 'right_arrow' not in self.keys_pressed:
                self._trigger_action('left_alt_hold')
    
    def _trigger_action(self, action: str):
        """Trigger a registered action."""
        callback = self.callbacks.get(action)
        if callback is None:
            self.logger.debug(f"No callback registered for {action}")
            return
        
        try:
            event = ButtonEvent(
                button=action,
                state=ButtonState.PRESSED,
                timestamp=time.time(),
            )
            callback(event)
        except Exception as e:
            self.logger.error(f"Error executing callback for {action}: {e}")
    
    def get_status(self) -> Dict:
        """Get current button interface status."""
        return {
            'running': self.running,
            'button_states': {k: v.value for k, v in self.button_states.items()},
            'keys_pressed': list(self.keys_pressed),
        }


class FourButtonSimulator:
    """Simulates four-button interface for testing."""
    
    def __init__(self, interface: FourButtonInterface):
        self.interface = interface
    
    def simulate_right_alt_tap(self):
        """Simulate RIGHT ALT tap (Internet AI)."""
        event = ButtonEvent(
            button='right_alt',
            state=ButtonState.PRESSED,
            timestamp=time.time(),
        )
        callback = self.interface.callbacks.get('right_alt_tap')
        if callback:
            callback(event)
    
    def simulate_left_alt_tap(self):
        """Simulate LEFT ALT tap (TTS)."""
        event = ButtonEvent(
            button='left_alt',
            state=ButtonState.PRESSED,
            timestamp=time.time(),
        )
        callback = self.interface.callbacks.get('left_alt_tap')
        if callback:
            callback(event)
    
    def simulate_rewind(self):
        """Simulate LEFT ALT + LEFT ARROW (REWIND)."""
        event = ButtonEvent(
            button='left_alt+left_arrow',
            state=ButtonState.PRESSED,
            timestamp=time.time(),
            combo='rewind',
        )
        callback = self.interface.callbacks.get('rewind')
        if callback:
            callback(event)
    
    def simulate_forward(self):
        """Simulate LEFT ALT + RIGHT ARROW (FORWARD)."""
        event = ButtonEvent(
            button='left_alt+right_arrow',
            state=ButtonState.PRESSED,
            timestamp=time.time(),
            combo='forward',
        )
        callback = self.interface.callbacks.get('forward')
        if callback:
            callback(event)
