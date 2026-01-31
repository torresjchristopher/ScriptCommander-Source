#!/usr/bin/env python3
"""Quick microphone test to verify audio input."""

import speech_recognition as sr

print("🎤 Testing Microphone Setup...\n")

# Initialize recognizer
recognizer = sr.Recognizer()
print("✓ Speech recognizer initialized")

# List all available microphones
print("\n📱 Available Microphones:")
try:
    for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  [{i}] {mic_name}")
except Exception as e:
    print(f"  Error listing mics: {e}")

# Try default microphone
try:
    with sr.Microphone() as source:
        print("\n✓ Default microphone detected")
        print(f"  Sample rate: {source.SAMPLE_RATE} Hz")
        print(f"  Chunk size: {source.CHUNK} frames")
        
        print("\n🔊 Adjusting for ambient noise... (2 seconds)")
        recognizer.adjust_for_ambient_noise(source, duration=2)
        print(f"✓ Ambient noise level adjusted (threshold: {recognizer.energy_threshold})")
        
        print("\n🎙️  Recording audio for 5 seconds... SPEAK NOW!")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        print(f"✓ Audio captured ({len(audio.frame_data)} bytes)")
        
        print("\n🔄 Transcribing...")
        try:
            text = recognizer.recognize_google(audio)
            print(f"✅ SUCCESS - Recognized: '{text}'")
        except sr.UnknownValueError:
            print("❌ Could not understand audio (silence or too quiet)")
        except sr.RequestError as e:
            print(f"❌ API error: {e}")
        
except sr.UnknownValueError:
    print("✗ Could not understand audio")
except sr.RequestError as e:
    print(f"✗ Could not request results: {e}")
except Exception as e:
    print(f"✗ Microphone error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("If you saw 'SUCCESS' above, your mic works!")
print("If it timed out, your microphone isn't being detected.")

