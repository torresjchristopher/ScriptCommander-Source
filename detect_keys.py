#!/usr/bin/env python3
"""
Detect what key names the keyboard library uses.
Run this and press keys to see their names.
"""

import keyboard

print("Press any keys - I'll show you their names")
print("Press ESC to exit\n")

try:
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            print(f"Pressed: '{event.name}'")
            if event.name == 'esc':
                break
        
except KeyboardInterrupt:
    print("\nDone")
