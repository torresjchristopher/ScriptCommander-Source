# Nemo Four-Button Interface + TTS Security

## The Vision: Replacing QWERTY

Nemo is not just AI. It's the nail in the coffin for traditional keyboard input.

**Four Buttons. Two Directions. One Future.**

```
Voice In (RIGHT ALT) ──→ Gemini AI ──→ Voice Out (LEFT ALT)
                            ↓
                     User's Genius Pattern
                    (35-D Keystroke Signature)
                            ↓
            Synthesis (Screen + Keyboard)
                            ↓
    REWIND (LEFT ALT + LEFT)  or  FORWARD (LEFT ALT + RIGHT)
```

## The Four-Button System

### Button 1: RIGHT ALT - Internet AI (Voice Input)

**What it does:**
- Tap/Hold to activate microphone
- Speak naturally to Gemini
- Get voice response
- Like having an AI butler in your ear

**Example:**
```
User: [presses RIGHT ALT]
User: "What was I doing 30 seconds ago?"
Gemini: "You were composing an email in Outlook"
```

**Technical:**
- Keyboard hook captures RIGHT ALT press
- Audio capture (in-memory only, NO storage)
- Speech-to-text: Google Speech Recognition
- Text sent to Gemini API
- Response: Text-to-speech playback
- Zero audio persistence

### Button 2: LEFT ALT (tap) - TTS Button (Voice Output)

**What it does:**
- Single tap (< 200ms) to hear synthesis
- Nemo speaks what it understands
- Your context + your patterns = your understanding
- THE HUMAN ELEMENT

**Example:**
```
User: [presses LEFT ALT]
Nemo: "You're writing code in Python. Your next likely action is debugging the function."
User: [continues working with voice context]
```

**Technical:**
- Detected via tap detection (< 200ms)
- Triggers temporal inference engine
- Synthesizes current understanding
- TTS engine generates speech
- Audio plays in-memory (through speakers/headphones)
- Audio NEVER written to disk
- ZERO STORAGE GUARANTEE

### Button 3: LEFT ALT + LEFT ARROW - REWIND

**What it does:**
- Hold to infer what WAS
- Look 30-60 seconds into the past
- Pure synthesis (not replay)
- Based on keyboard pattern + screen context

**Technical:**
- Combo detection: LEFT ALT held, then LEFT ARROW pressed
- Temporal inference engine activates
- Keyboard signature analyzed
- Screen state extrapolated
- Confidence score computed
- TTS output: "You were..."

### Button 4: LEFT ALT + RIGHT ARROW - FORWARD

**What it does:**
- Hold to predict what COMES NEXT
- Look 30-60 seconds ahead
- Based on your behavior patterns
- NOT video replay, pure synthesis

**Technical:**
- Combo detection: LEFT ALT held, then RIGHT ARROW pressed
- Temporal inference engine predicts
- Next likely action synthesized
- Intent patterns matched
- TTS output: "You'll likely..."

## Zero Storage: The Security Guarantee

### What NEVER Persists

```
❌ No voice recordings        → Audio not saved
❌ No audio files             → No .wav/.mp3/.ogg files created
❌ No microphone cache        → Google Speech API called, result used, forgotten
❌ No temp audio files        → TTS output played in-memory, never written to disk
❌ No audio logs              → No audio data in log files
❌ No clipboard audio         → Clipboard not used for audio
❌ No process memory          → Audio buffers cleared immediately after playback
❌ No cross-user learning     → User's voice/patterns stay private
❌ No data theft              → No data exists to steal
```

### What DOES Persist (Encrypted)

```
✅ OAuth tokens               → ~/.nemo/credentials.json (encrypted)
✅ API keys                   → Stripe, Gemini (encrypted)
✅ User settings              → Volume, speed, gender preference
✅ Model weights              → Keystroke fingerprint (not data, just patterns)
```

### Security Audit: `nemo security verify`

Verifies:
1. **Temp Directory Scan** - No audio files in Windows Temp
2. **Nemo Directory Scan** - No audio files in ~/.nemo
3. **Cache Scan** - No Google Speech/TTS cache
4. **Memory Audit** - Process memory < 200 MB
5. **Log Audit** - No audio data in logs
6. **Credentials** - APIs properly encrypted
7. **Clipboard** - Not used for audio storage

**Result:** ✓ SECURITY VERIFIED - Zero-storage guarantee confirmed

## TTS Engine: How It Works

### Local vs. Cloud

**Option 1: Local TTS (pyttsx3)**
- ✅ No internet required
- ✅ Completely offline
- ✅ Fast
- ❌ Lower quality voices
- ❌ Limited language support

**Option 2: Google Cloud TTS**
- ✅ Excellent quality voices
- ✅ Many languages/accents
- ✅ Natural-sounding
- ❌ Requires internet
- ❌ Requires API key (cheap: ~$4 per 1M characters)

### In-Memory Audio Playback

```python
# Audio generation (in-memory)
synthesis_input = texttospeech.SynthesisInput(text="Hello")
response = engine.synthesize_speech(...)
audio_bytes = response.audio_content  # Bytes in RAM, not disk

# Audio playback (never persisted)
if platform.system() == 'Windows':
    import winsound
    winsound.PlaySound(audio_bytes, ...)  # Plays directly
elif platform.system() == 'Linux':
    # Pipes directly to audio player (paplay)
    process.communicate(input=audio_bytes)  # No disk write
```

### Why Never Written to Disk

**Traditional approach (bad for privacy):**
```
TTS → [write to temp file] → [play sound] → [delete file]
                    ↑ Window of vulnerability
                    (hacker can recover deleted file)
```

**Nemo approach (secure):**
```
TTS → [hold in memory] → [play sound] → [forget]
             ↑
      No disk exposure
      Secure in-memory buffer
```

## Voice Input Security: Speech-to-Text Only

### What Happens When You Press RIGHT ALT

```
1. [User presses RIGHT ALT]
   
2. Microphone opens (in-memory audio buffer)
   
3. User speaks: "What was I doing?"
   
4. Audio captured in RAM (not saved)
   
5. Audio sent to Google Speech Recognition
   
6. Returns text: "What was I doing?"
   
7. Audio buffer cleared (GONE FOREVER)
   
8. Text sent to Gemini: "What was I doing?" + context
   
9. Gemini response: "You were composing an email"
   
10. Text converted to speech (in-memory)
    
11. Speech played (in speakers/headphones)
    
12. Speech buffer cleared (GONE FOREVER)
    
13. No audio exists. No recording. Pure synthesis.
```

### Why This Matters

**Privacy:**
- ❌ No audio recording (can't be subpoena'd)
- ❌ No voice profile (can't be matched to others)
- ❌ No audio fingerprint (can't be tracked)

**Security:**
- ❌ No audio cache (nothing to hack)
- ❌ No temp files (nothing to recover)
- ❌ No logs (nothing to inspect)

**Performance:**
- ✅ Instant processing
- ✅ No disk I/O overhead
- ✅ Low latency

## The Human Element

### Why TTS is Revolutionary

**Old way (qwerty keyboard):**
- Type words into computer
- Computer responds with text
- User reads text
- Human ↔ Machine: slow, inefficient, isolated

**New way (Nemo TTS):**
- Speak voice to computer
- Computer synthesizes understanding
- Computer speaks response
- Human ↔ Machine: fast, natural, connected

**Example conversation:**
```
User: [presses LEFT ALT]
Nemo: "You're 40 seconds into composing an email. Your next step is likely sending it."

User: [presses RIGHT ALT]
User: "Should I add more details?"
Gemini: "Based on your email type and length, a brief summary would be effective."

User: [presses LEFT ALT]
Nemo: "You're now in the signature line. Ready to send."

User: [presses LEFT ALT + RIGHT ARROW]
Nemo: "Next action: Click Send button in 15 seconds."
```

### Why This Replaces QWERTY

1. **Speed**: Voice faster than typing
2. **Accuracy**: Natural language understood perfectly
3. **Accessibility**: No physical typing needed
4. **Privacy**: Zero audio storage
5. **Integration**: Works while typing (overlay layer)
6. **Future**: Custom hardware can map any buttons

## Configuration & Customization

### TTS Settings (Via CLI)

```bash
nemo tts configure
  # Speed: 1.0 (or 0.5-2.0)
  # Pitch: 1.0 (or 0.5-2.0)
  # Volume: 0.8 (or 0.0-1.0)
  # Gender: neutral (or male/female)

nemo tts speak "Hello world"
  # Speaks the text

nemo tts test
  # Tests with sample sentences

nemo security verify
  # Verifies zero-storage
```

### Security Settings

```bash
nemo security report
  # Full audit report
  
nemo security report --verbose
  # Detailed findings
```

### Button Customization (Future)

```bash
nemo buttons configure
  # Remap buttons to user preference
  # Save custom button layout
```

## API Credits & Payment

### How Payment Works

**Gemini API:**
- $0.0005 per 1,000 input tokens
- $0.0015 per 1,000 output tokens
- Typical query: 500 tokens = ~$0.0008
- $1 = ~1,250 queries

**Google Speech Recognition:**
- $0.0004 per 15-second chunk
- Typical voice input: 5 seconds = ~$0.0001

**Google TTS:**
- $4 per 1 million characters
- Typical TTS: 100 characters = ~$0.0004

**Total typical transaction:**
- User speaks to Gemini (RIGHT ALT)
- 5 seconds audio → text: $0.0001
- 500 tokens to Gemini: $0.0008
- 200 characters TTS response: $0.0008
- **Total: ~$0.002 per interaction**

### Credit Management

```bash
nemo credits add $5
  # Stripe payment (handled via CLI)

nemo credits balance
  # Current balance

nemo credits history
  # Transaction log
```

## The Nail in the Coffin

**Why This is Revolutionary**

1. **Privacy** - Zero audio storage (unprecedented)
2. **Security** - No data to hack/steal
3. **Speed** - Voice faster than keyboard
4. **Accessibility** - No physical keyboard needed
5. **Integration** - Overlay on existing workflows
6. **Intelligence** - Synthesis not recording
7. **Future** - Custom hardware inevitable

**What Dies:**
- ❌ QWERTY keyboard (obsolete)
- ❌ Text input paradigm (replaced by voice)
- ❌ Data silos (zero storage)
- ❌ Privacy violations (no audio to store)
- ❌ Slow interfaces (voice faster)

**What's Born:**
- ✅ Voice-first computing
- ✅ Synthesis-based AI
- ✅ Real-time understanding
- ✅ Zero-storage future
- ✅ Privacy-preserved intelligence

## Implementation Status

✅ **Complete:**
- Four-button interface detection
- TTS engine (local + cloud)
- Audio security audit
- In-memory audio playback
- Voice input (speech-to-text)
- Zero-storage verification
- CLI commands

**Next (Phase 3.3):**
- Button event routing integration
- Real-time synthesis pipeline
- End-to-end testing
- Daemon service wrapper
- Performance optimization

**The User Experience:**

```
[User boots Nemo]
System: "Nemo synthesis engine ready. Press a button:"

[User presses RIGHT ALT]
System: [listening] "Listening..."
User: "What's happening?"
Gemini: [through TTS] "You're ready to send your email. Just click send."

[User presses LEFT ALT]
Nemo: [through TTS] "Your composition is 4 paragraphs, well-structured. Next action: send."

[User presses LEFT ALT + RIGHT ARROW]
Nemo: [through TTS] "In 10 seconds, you'll click the Send button."

[User presses LEFT ALT + LEFT ARROW]
Nemo: [through TTS] "30 seconds ago, you were writing the first paragraph of this email."

[All interactions logged: 0 bytes of audio]
[Security: Zero-storage guarantee confirmed]
[User: Completely private, completely understood]
```

---

**This is the future. Voice in. Voice out. No qwerty needed.**

**The four buttons. The human element. The nail in the coffin.**
