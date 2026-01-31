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

## Marketplace Security & Quarantine
Script Commander employs a "Human-in-the-Loop" security model to prevent malicious software distribution:

1.  **Quarantine Layer**: Submissions are directed to GitHub Issues/Pull Requests. In this state, the code is "Quarantined"—it is not indexed by the application and cannot be downloaded by users.
2.  **Manual Audit**: Every submission undergoes a line-by-line code review by the administrator to ensure no malicious system calls, network exfiltration, or obfuscated logic exists.
3.  **Official Promotion**: Only audited scripts are added to the `marketplace.json` manifest in the production branch.
4.  **Integrity Check**: The application validates the source URL against the official `torresjchristopher` namespace.
