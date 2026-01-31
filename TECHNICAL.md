# Technical Specifications: Script Commander

## Core Architecture
- **Language**: Python 3.11+
- **UI Framework**: CustomTkinter (Modernized Tkinter wrapper)
- **Script Engine**: PowerShell 5.1 / Core (via Subprocess)
- **Threading**: Native Python `threading` for non-blocking UI operations.

## Security Model
- **UAC Integration**: Automatic Windows User Account Control elevation for admin-level scripts.
- **Execution Policy**: Dynamic `Bypass` context (Scoped specifically to the child process).
- **Network**: HTTPS-only marketplace downloads via `requests`.

## Dependencies
- `customtkinter`: Modern UI components.
- `requests`: Secure marketplace connectivity.
- `pillow`: Advanced image and icon rendering.
- `markdown-pdf`: High-fidelity document conversion.

## GitHub Repositories
- **Source Code**: [ScriptCommander-Source](https://github.com/torresjchristopher/ScriptCommander-Source)
- **Official Scripts**: [ScriptCommander-Marketplace](https://github.com/torresjchristopher/ScriptCommander-Scripts)
