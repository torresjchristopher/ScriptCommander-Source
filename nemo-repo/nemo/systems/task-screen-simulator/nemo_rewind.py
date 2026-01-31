"""
NEMO REWIND ENGINE - Ultimate Simplicity

NEMO CODE: Proprietary keystroke reversal library
- Simple mapping: keystroke → reverse instruction
- Zero state tracking
- Zero data storage
- Just: keystroke → NEMO CODE → store in deque

REWIND: While RIGHT ALT + LEFT held, pop stack and fire NEMO CODES
- That's literally it!
"""

from collections import deque
from typing import Tuple, Optional
import keyboard
import time

# NEMO CODE - Proprietary Reverse Instruction Library
# Keystroke → Reverse Keystroke
NEMO_CODE = {
    # Typing
    'a': 'backspace', 'b': 'backspace', 'c': 'backspace', 'd': 'backspace', 'e': 'backspace',
    'f': 'backspace', 'g': 'backspace', 'h': 'backspace', 'i': 'backspace', 'j': 'backspace',
    'k': 'backspace', 'l': 'backspace', 'm': 'backspace', 'n': 'backspace', 'o': 'backspace',
    'p': 'backspace', 'q': 'backspace', 'r': 'backspace', 's': 'backspace', 't': 'backspace',
    'u': 'backspace', 'v': 'backspace', 'w': 'backspace', 'x': 'backspace', 'y': 'backspace',
    'z': 'backspace',
    
    # Numbers
    '0': 'backspace', '1': 'backspace', '2': 'backspace', '3': 'backspace', '4': 'backspace',
    '5': 'backspace', '6': 'backspace', '7': 'backspace', '8': 'backspace', '9': 'backspace',
    
    # Symbols
    ' ': 'backspace', '!': 'backspace', '@': 'backspace', '#': 'backspace', '$': 'backspace',
    '%': 'backspace', '^': 'backspace', '&': 'backspace', '*': 'backspace', '(': 'backspace',
    ')': 'backspace', '-': 'backspace', '_': 'backspace', '=': 'backspace', '+': 'backspace',
    '[': 'backspace', ']': 'backspace', '{': 'backspace', '}': 'backspace', ';': 'backspace',
    ':': 'backspace', "'": 'backspace', '"': 'backspace', ',': 'backspace', '<': 'backspace',
    '.': 'backspace', '>': 'backspace', '/': 'backspace', '?': 'backspace', '\\': 'backspace',
    '|': 'backspace', '`': 'backspace', '~': 'backspace',
    
    # Navigation
    'right': 'left',
    'left': 'right',
    'up': 'down',
    'down': 'up',
    
    # Deletion
    'backspace': 'ctrl+z',
    'delete': 'ctrl+z',
    
    # Editing
    'enter': 'ctrl+z',
    'tab': 'backspace_spaces',
    
    # Undo/Redo
    'ctrl+z': 'ctrl+y',
    'ctrl+y': 'ctrl+z',
}


class NemoRewindEngine:
    """
    Ultra-simple rewind: keystroke → NEMO CODE → fire on command
    """
    
    MAX_HISTORY = 5000  # 5 minutes at 1000 WPM
    
    def __init__(self):
        # Stack of (keystroke, nemo_code) tuples
        self.stack = deque(maxlen=self.MAX_HISTORY)
        self.rewinding = False
    
    def track(self, key: str):
        """Track a keystroke with its NEMO CODE"""
        if key in ('right shift', 'right alt', 'escape', 'f1', 'f2', 'f3', 'f4', 'f5'):
            return
        
        nemo_code = NEMO_CODE.get(key)
        if nemo_code:
            self.stack.append((key, nemo_code))
    
    def rewind_tick(self):
        """
        Fire one reverse instruction while rewind is held.
        Called repeatedly while RIGHT ALT + LEFT is pressed.
        """
        if not self.rewinding:
            self.rewinding = True
        
        if not self.stack:
            return False
        
        # Pop one keystroke from the top
        key, nemo_code = self.stack.pop()
        
        # Execute NEMO CODE
        self._execute_nemo_code(nemo_code)
        
        return True
    
    def rewind_stop(self):
        """Stop rewinding"""
        self.rewinding = False
    
    def _execute_nemo_code(self, nemo_code: str):
        """Execute a NEMO CODE (fire reverse keystroke)"""
        try:
            if nemo_code == 'backspace':
                keyboard.press_and_release('backspace')
            elif nemo_code == 'left':
                keyboard.press_and_release('left')
            elif nemo_code == 'right':
                keyboard.press_and_release('right')
            elif nemo_code == 'up':
                keyboard.press_and_release('up')
            elif nemo_code == 'down':
                keyboard.press_and_release('down')
            elif nemo_code == 'backspace_spaces':
                for _ in range(4):
                    keyboard.press_and_release('backspace')
            elif nemo_code == 'ctrl+z':
                keyboard.hotkey('ctrl', 'z')
            elif nemo_code == 'ctrl+y':
                keyboard.hotkey('ctrl', 'y')
        except Exception as e:
            print(f"[NEMO ERROR] {nemo_code}: {e}")
    
    def get_stack_size(self) -> int:
        """Return stack size"""
        return len(self.stack)
    
    def clear(self):
        """Clear stack"""
        self.stack.clear()


# Global instance
_engine = NemoRewindEngine()


def get_nemo_rewind_engine() -> NemoRewindEngine:
    """Get global NEMO rewind engine"""
    return _engine
