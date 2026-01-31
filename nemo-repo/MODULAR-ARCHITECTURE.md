# Nemo Modular Architecture

## Overview

Nemo is organized as a modular system where each keyboard hotkey has its own isolated folder. This allows independent development, testing, and deployment of features.

## Directory Structure

```
nemo/
├── core/                           # Core orchestrator & keyboard listener
│   ├── __init__.py
│   ├── main.py                    # Main entry point
│   └── keyboard_listener.py       # Hotkey detection engine
│
├── cli/                            # Command-line interface
│   ├── __init__.py
│   ├── buttons_start.py           # CLI entry point
│   └── config.py                  # Global configuration
│
├── keys/                           # Individual key implementations
│   │
│   ├── right_shift_stt/           # RIGHT SHIFT - Speech-to-Text
│   │   ├── __init__.py
│   │   ├── voice_input.py         # STT engine
│   │   └── config.py              # STT config
│   │
│   ├── right_alt_gemini/          # RIGHT ALT - Gemini Voice AI
│   │   ├── __init__.py
│   │   ├── gemini_handler.py      # Gemini integration
│   │   └── config.py              # Gemini config
│   │
│   ├── right_alt_left_rewind/     # RIGHT ALT + LEFT - Rewind (PROPRIETARY)
│   │   ├── __init__.py
│   │   ├── nemo_rewind.py         # Rewind engine with NEMO CODE
│   │   └── config.py              # Rewind config
│   │
│   ├── right_alt_right_forward/   # RIGHT ALT + RIGHT - Forward (PROPRIETARY)
│   │   ├── __init__.py
│   │   ├── nemo_forward.py        # Forward prediction engine
│   │   └── config.py              # Forward config
│   │
│   └── right_alt_up_agent/        # RIGHT ALT + UP - Agent Synthesis (PROPRIETARY)
│       ├── __init__.py
│       ├── agentic_synthesis.py   # File extraction & context wrapping
│       └── config.py              # Agent config
│
└── systems/                        # Shared utilities
    └── shared_utils.py            # TTS, logging, etc.
```

## Key Isolation

Each key folder is completely independent:

- **Own configuration** - Each key has `config.py`
- **Own implementation** - Each key has its engine/handler
- **Own dependencies** - Can be imported/excluded independently
- **Easy to update** - Change one key without affecting others
- **Easy to add new keys** - Just create a new folder

## Proprietary Keys

The following keys are **proprietary** (NEMO CODE) and excluded from public git:

- `right_alt_left_rewind/` - Temporal reversal using keystroke inversion
- `right_alt_right_forward/` - Temporal prediction engine
- `right_alt_up_agent/` - Agentic synthesis with file extraction

These folders are listed in `.gitignore` and distributed as compiled bytecode.

## Public Keys

The following keys are **open-source** and visible in the repository:

- `right_shift_stt/` - Speech-to-text with fallback engines
- `right_alt_gemini/` - Gemini integration with screenshots

These can be audited, forked, and extended by the community.

## Adding a New Key

To add a new hotkey feature:

1. Create a new folder in `nemo/keys/`: `right_alt_FEATURE/`
2. Add `__init__.py`, implementation file, and `config.py`
3. Register in `nemo/core/keyboard_listener.py`
4. Add callback in `nemo/cli/buttons_start.py`
5. Update `.gitignore` if proprietary

Example:
```
nemo/keys/right_ctrl_custom/
├── __init__.py
├── custom_engine.py
└── config.py
```

## Execution Flow

```
User presses RIGHT SHIFT
  ↓
keyboard_listener.py detects hotkey
  ↓
Triggers callback in buttons_start.py
  ↓
Imports nemo/keys/right_shift_stt/
  ↓
Executes STT engine
  ↓
Returns result to user
```

## Dependencies

- **Core dependencies** shared across all keys:
  - `keyboard` library for hotkey detection
  - `rich` for console output
  - Python 3.8+

- **Per-key dependencies**:
  - STT: `speech_recognition`, `pyaudio`
  - Gemini: `google-generativeai`
  - Rewind: (built-in, proprietary)
  - Forward: (built-in, proprietary)
  - Agent: (built-in, proprietary)

## Data Ownership

Each key respects data invisibility:
- No persistent storage of user data
- All processing in-memory
- No logs, no profiles, no tracking

Proprietary keys achieve this through NEMO CODE:
- Keystroke → NEMO CODE → execution
- No intermediate data structures
- No state reconstruction

## Future Evolution

As Nemo evolves, the modular architecture enables:

✅ **Quick feature addition** - Add new keys without refactoring
✅ **Independent versioning** - Update individual keys
✅ **Community contributions** - Fork and extend public keys
✅ **Selective privatization** - Protect only proprietary logic
✅ **Performance optimization** - Profile and optimize per-key

---

**Nemo: Keyboard orchestration through modular, composable key engines.**
