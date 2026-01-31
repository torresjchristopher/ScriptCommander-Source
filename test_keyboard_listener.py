#!/usr/bin/env python3
"""
Simple test: Use KeyboardHotkeyListener directly to test RIGHT SHIFT detection
"""

import sys
sys.path.insert(0, '/Users/serro/ScriptCommander/nemo-repo')

from nemo.systems.task_screen_simulator.keyboard_hotkeys import KeyboardHotkeyListener

print("🎤 Testing KeyboardHotkeyListener")
print("=" * 50)
print("Press RIGHT SHIFT...")
print("Press Ctrl+C to exit\n")

def on_tts_tap(event):
    print("\n✅ RIGHT SHIFT DETECTED!")
    print("🔊 Speech-to-Text activated")

def on_gemini_tap(event):
    print("\n✅ RIGHT ALT DETECTED!")
    print("🎤 Gemini Voice AI activated")

def on_rewind(event):
    print("\n⏮️  REWIND")

def on_forward(event):
    print("\n⏭️  FORWARD")

try:
    listener = KeyboardHotkeyListener()
    listener.register_callback('tts_tap', on_tts_tap)
    listener.register_callback('gemini_tap', on_gemini_tap)
    listener.register_callback('rewind', on_rewind)
    listener.register_callback('forward', on_forward)
    
    print("Starting listener...")
    listener.start()
    
    import time
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n\nShutting down...")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
