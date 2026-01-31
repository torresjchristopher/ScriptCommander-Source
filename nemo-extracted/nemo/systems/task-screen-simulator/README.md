# Nemo Synthesis Engine - Phase 3.2+ (Four-Button + TTS)

**Pure Intelligence. No Storage. No Recording. Just Synthesis. Voice In. Voice Out.**

## The Four-Button Interface (NEW!)

### Button 1: RIGHT ALT = Internet AI (Voice Input)
Press to activate Gemini AI via voice. The AI butler responds with voice.

### Button 2: LEFT ALT (tap) = TTS Button (Voice Output) ⭐ NEW!
Tap to HEAR Nemo's synthesis. Your context. Your patterns. Spoken aloud.
**This is the human element. Voice replaces qwerty.**

### Button 3: LEFT ALT + LEFT ARROW = REWIND
Hold to infer what WAS on screen. Pure synthesis, not replay.

### Button 4: LEFT ALT + RIGHT ARROW = FORWARD  
Hold to predict what COMES NEXT. Based on your behavior patterns.

## The Vision: Replacing QWERTY

**Old way:** Type words into computer, read response.
**New way (Nemo):** Speak to computer, hear understanding.

TTS is the human element. Voice input (RIGHT ALT) + voice output (LEFT ALT) = natural interaction.

## Zero Audio Storage: Top-Line Security

### What NEVER Persists
```
❌ No voice recordings
❌ No audio files  
❌ No microphone cache
❌ No temp audio files
❌ No audio in logs
❌ No clipboard audio
❌ No audio in memory (cleared after playback)
```

### How Voice Works
```
User speaks (RIGHT ALT) → 
Audio captured (in-memory) → 
Sent to Google Speech-to-Text →
Audio buffer deleted immediately →
Text sent to Gemini →
Response text converted to speech (in-memory) →
Audio played through speakers/headphones →
Speech buffer deleted immediately →

RESULT: Zero audio storage. Pure text synthesis.
```

### Security Audit (NEW!)
```bash
nemo security verify          # Verify zero-storage guarantee
nemo security report          # Full audit report
nemo security report --verbose # Detailed findings
```

## Three-Button Interface (Original)
Hold to simulate what was on screen N seconds ago.
Uses keyboard signature + screen context to infer the past.

```
What the system knows:
  • You were typing in email app (screen analyzer)
  • Your pattern shows "composition" (keyboard synthesizer)
  • You're being deliberate, not rapid-firing

System infers:
  "5 seconds ago, you were still drafting the email body"
  Confidence: 85%
```

### 2. LEFT ALT + RIGHT ARROW = FORWARD
Hold to predict what comes next.
Uses intent + context to predict the future.

```
What the system knows:
  • Email form is complete (screen analyzer)
  • Keyboard pattern shows "ready to send" (synthesizer)
  • Next natural step in workflow

System predicts:
  "Your next action is likely clicking Send"
  Confidence: 80%
```

### 3. RIGHT ALT = VOICE (AI Butler)
Hold to talk to your Gemini AI assistant.
Responds with voice like a personal butler.

```
User presses RIGHT ALT and says:
  "What was I typing 3 minutes ago?"

System:
  1. Records voice input
  2. Converts to text
  3. Adds context: keyboard + screen state
  4. Sends to Gemini with synthesis context
  5. Gemini responds with AI answer
  6. Converts to speech
  7. Plays response
```

## Zero Storage Architecture

### What We DO NOT Do
❌ Store screenshots
❌ Record video
❌ Save action history
❌ Persist data
❌ Track user activity

### What We DO Do
✅ Analyze current screen state
✅ Learn keyboard patterns (real-time)
✅ Synthesize intent from keyboard + screen
✅ Infer past and future from synthesis
✅ Forget everything (ephemeral analysis)

## Four Core Components

### 1. Screen Analyzer (6.8K LOC)
Analyzes what's currently visible on screen.
No storage - just analysis of current state.

```python
from screen_analyzer import get_screen_analyzer

analyzer = get_screen_analyzer()
state = analyzer.analyze_current_screen()
```

Detects:
- Active window and application
- Visible UI elements
- Form fields and labels
- Content type (email, code, web, document)
- Language detection

### 2. Keyboard Synthesizer (9.4K LOC)
Learns your unique keystroke patterns in real-time.
Builds and updates your 35-D behavioral fingerprint.

```python
from keyboard_synthesizer import get_keyboard_synthesizer

synth = get_keyboard_synthesizer()
synth.record_keystroke(key="a", duration_ms=150)

# Continuously updated 35-D signature:
# - 12-D: timing (dwell, flight, intervals)
# - 8-D: pressure characteristics
# - 10-D: patterns (entropy, rhythm, bursts)
# - 5-D: intent (search, editing, coding, navigation, composition)
```

### 3. Temporal Inference Engine (11.2K LOC)
Infers what WAS (rewind) and what WILL BE (forward).
Uses keyboard signature + screen context.

```python
from temporal_inference import get_temporal_inference_engine

engine = get_temporal_inference_engine()

# What was 5 seconds ago?
past = engine.infer_rewind(seconds_back=5)

# What happens next?
future = engine.infer_forward(seconds_ahead=5)

# Returns: confidence score, likely actions, reasoning
```

### 4. Gemini Integration (10.1K LOC)
Live AI assistant with Google OAuth and credit management.
Supports Gemini, Claude, and Ollama (open source).

```python
from gemini_integration import get_gemini_integration

gemini = get_gemini_integration()

# Google OAuth login
gemini.set_credentials(oauth_code)

# Query with screen+keyboard context
response = gemini.query(
    text="What was I typing?",
    context={"active_app": "outlook", "intent": "composition"}
)

# Manage credits
balance = gemini.get_balance()
gemini.add_credit(amount_usd=10)
```

## CLI Commands

### Setup & First-Run
```bash
nemo setup                      # Interactive setup wizard
nemo buttons                    # Show button mapping
nemo help                       # Show all commands
```

### Account & Payments
```bash
nemo account link              # Google OAuth login
nemo account status            # Show linked accounts
nemo credits show              # View API credit balance
nemo credits refill            # Add credits ($5, $10, $25, custom)
nemo credits history           # Show usage history
```

### Agent Management
```bash
nemo agent list                # Show available agents
nemo agent status              # Check connection
nemo agent switch gemini       # Switch to Gemini
nemo agent switch claude       # Switch to Claude
nemo agent switch ollama       # Switch to Ollama (local)
```

### Analysis & Synthesis
```bash
nemo synthesis analyze         # Analyze current state
nemo rewind --seconds 5        # Infer what was 5 sec ago
nemo forward --seconds 5       # Predict next 5 seconds
```

### Voice Assistant
```bash
nemo voice start               # Start voice daemon
nemo voice status              # Show voice connection
nemo voice test                # Test voice hotkey
nemo voice configure           # Configure voice settings
```

## First-Run Experience

### Step 1: User Presses RIGHT ALT (First Time)
```
"Welcome to Nemo!"
"Open terminal and run: nemo setup"
```

### Step 2: User Runs `nemo setup`
Interactive wizard:
1. Welcome message
2. Select AI agent (Gemini recommended)
3. Link Google account (OAuth)
4. Add API credits
5. Test voice hotkey
6. Done!

### Step 3: All Set
```
Quick Start:
  • RIGHT ALT = Talk to AI
  • LEFT ALT + LEFT ARROW = Rewind
  • LEFT ALT + RIGHT ARROW = Forward
```

## Payment & Credits System

### Pricing
Pay-per-use model. You control costs.

```
Gemini Pricing Examples:
  • 1,000 queries ≈ $1
  • 10,000 queries ≈ $10
  • 100,000 queries ≈ $100
```

### Credit Management
```bash
nemo credits show
# Output:
# Balance: $2.50 (1.25M tokens)
# Usage This Month: $1.20
# Last Refill: Jan 30, 2026

nemo credits refill
# Choose: $5, $10, $25, or custom
# Payment via Stripe (built into CLI)
# Credits added immediately
```

## Multi-Agent Support

### Gemini (Default - Recommended)
- Latest AI models
- Multimodal (text, image, audio)
- Fast responses
- Pay-per-use ($0.0005 per 1K tokens)
- Requires Google account

### Claude (Anthropic)
- Long context window
- Thoughtful reasoning
- Pay-per-use
- Switch with: `nemo agent switch claude`

### Ollama (Open Source)
- Runs locally on your computer
- Completely free
- No internet required
- 100% private
- Slower but no costs
- Setup: Download Ollama, run `ollama pull llama2`

## Privacy First

✅ **No Cloud Storage**
- All analysis stays local
- Nothing sent to Nemo servers
- Nothing persists

✅ **Direct to Providers**
- Gemini API: Direct to Google
- Claude API: Direct to Anthropic
- Ollama: Runs on your machine

✅ **Encrypted Credentials**
- OAuth tokens stored locally
- API keys encrypted
- Never transmitted to Nemo

✅ **Voice is Optional**
- Voice data sent only to chosen provider
- User controls what's shared
- Can use text-only mode

✅ **Open Source Alternative**
- Ollama runs everything locally
- No internet needed
- Completely private

## Use Cases

### Email Composition
```
User: "Was my email professional?"
Nemo: Analyzes email + your typing pattern
Response: "Yes, it sounds professional and clear"
```

### Coding Session
```
User holds LEFT ALT + LEFT ARROW (rewind)
System: Infers you were debugging 5 minutes ago
Shows: "You were tracing through the authentication logic"
```

### Shopping Recovery
```
User: "Did I add the blue or red variant?"
Nemo: Checks screen + your selection pattern
Response: "You selected the blue variant, which is in your cart"
```

### Meeting Notes
```
User: "What did I write about budgets?"
Nemo: Synthesizes meeting notes + your typing rhythm
Response: "You noted Q4 budget approval needed by March 15"
```

## Architecture

```
USER PRESSES BUTTON
    ↓
┌───────────────────────────────────────┐
│  LEFT+LEFT  │  LEFT+RIGHT  │  RIGHT   │
│  (REWIND)   │  (FORWARD)   │  (VOICE) │
└───────────────────────────────────────┘
    ↓              ↓              ↓
┌──────────────────────────────────────────────┐
│ SCREEN ANALYZER: What's visible?            │
│ KEYBOARD SYNTHESIZER: Your pattern?         │
│ TEMPORAL INFERENCE: Past/Future?            │
│ GEMINI: What should I tell user?            │
└──────────────────────────────────────────────┘
    ↓
ANALYSIS (no storage)
    ↓
DISPLAY RESULT
```

## Technology

- **Python 3.9+** - Core language
- **click** - CLI framework
- **rich** - Terminal UI
- **numpy** - Numerical computing
- **google-generativeai** - Gemini API client
- **anthropic** - Claude API client
- **google-auth** - OAuth
- **pyaudio** - Voice I/O
- **SpeechRecognition** - Speech-to-text
- **google-cloud-texttospeech** - Text-to-speech

## Installation

```bash
# Clone repository
git clone <repo-url>
cd nemo

# Install dependencies
pip install -r requirements.txt

# Run setup
python cli.py setup
```

## Testing

```bash
# Test components
python -m pytest tests/

# Manual testing
python cli.py synthesis analyze
python cli.py voice test
python cli.py agent status
```

## Philosophy

**"Perfect Intelligence Without Perfect Storage"**

Traditional systems:
- Record everything
- Store everything
- Replay everything

Nemo:
- Understand everything
- Forget everything
- Remember nothing

We achieve perfect intelligence through **synthesis**, not storage.

---

**Based on: The Blanket Theory**

Just as God synthesizes all perspectives into omniscience,
Nemo synthesizes keyboard + screen into user omniscience.

Not storage. Not replay. **Synthesis.**

The future of AI isn't recording the past.
It's understanding the present.

🧠
