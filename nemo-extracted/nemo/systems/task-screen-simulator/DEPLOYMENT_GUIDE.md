# Nemo Deployment Guide - GitHub Release & CLI Installation

**Version**: 1.0  
**Date**: January 30, 2026  
**Status**: Ready for Production Release

---

## Deployment Architecture

### Three-Tier Distribution

```
GitHub Repository
    ├─ Source Code (for developers)
    │  └─ Full Nemo codebase + components
    │
    ├─ GitHub Releases (for end-users)
    │  └─ Packaged .zip file (all-in-one)
    │
    └─ Website (yukora.site)
       ├─ Download button → GitHub Release
       └─ Setup instructions

CLI Download System
    ├─ nemo download latest    → Fetch release info
    ├─ nemo download install   → Full installation
    ├─ nemo download update    → Update to latest
    └─ nemo download status    → Check installation
```

---

## GitHub Release Structure

### Release Package Contents

```
nemo-v1.0.0.zip
├── nemo/
│   ├── core/
│   │   ├── nemo.py
│   │   ├── cli.py
│   │   └── README.md
│   ├── systems/
│   │   └── task-screen-simulator/
│   │       ├── screen_analyzer.py
│   │       ├── keyboard_synthesizer.py
│   │       ├── temporal_inference.py
│   │       ├── gemini_integration.py
│   │       ├── setup_wizard.py
│   │       ├── voice_assistant.py
│   │       ├── tts_engine.py
│   │       ├── audio_security.py
│   │       ├── four_button_interface.py
│   │       ├── download_manager.py
│   │       ├── cli.py
│   │       └── requirements.txt
│   ├── requirements.txt
│   ├── VERSION
│   └── INSTALL.md
└── README.md
```

### GitHub Release Metadata

```
Tag: v1.0.0
Name: Nemo Synthesis Engine v1.0.0
Body: 
  Release notes with features, fixes, and improvements
  
Assets:
  - nemo-v1.0.0.zip (All-in-one package)
  - nemo-v1.0.0.sha256 (Checksum)
```

---

## CLI Download System

### Command Reference

#### Check Latest Release
```bash
nemo download latest
# Output:
# Version: v1.0.0
# Name: Nemo Synthesis Engine v1.0.0
# Released: 2026-01-30
# Current Installed: v0.9.5
# Update Available: YES
```

#### Install Nemo
```bash
nemo download install
# Runs interactive wizard:
# 1. Fetch release info
# 2. Download .zip
# 3. Verify checksum
# 4. Extract to ~/.nemo/nemo
# 5. Install Python dependencies
# 6. Create manifest
```

#### Update to Latest
```bash
nemo download update
# Checks for updates
# If available, runs install wizard
```

#### Check Installation Status
```bash
nemo download status
# Shows:
# - Installed version
# - Latest available
# - Update status
# - Install path
```

---

## Installation Process (Detailed)

### Step 1: User Initiates Download

```bash
nemo download install
```

### Step 2: Check Release

```python
DownloadManager.get_latest_release()
# Calls: GET /repos/YOUR_ORG/project-nemo/releases/latest
# Returns: {
#   'version': 'v1.0.0',
#   'name': 'Nemo Synthesis Engine v1.0.0',
#   'assets': [
#     {'name': 'nemo-v1.0.0.zip', 'browser_download_url': '...'}
#   ],
#   'published_at': '2026-01-30T...'
# }
```

### Step 3: Download Package

```python
DownloadManager.download_release()
# Downloads: nemo-v1.0.0.zip
# Location: ~/.nemo/releases/nemo-v1.0.0.zip
# Shows progress bar
```

### Step 4: Verify Integrity

```python
DownloadManager.verify_checksum(filepath, expected_hash)
# Computes SHA256 of downloaded file
# Compares with published checksum
# Confirms: Not corrupted, not tampered
```

### Step 5: Extract Package

```python
DownloadManager.extract_release(filepath)
# Unzips to: ~/.nemo/releases/extracted/
# Preserves directory structure
```

### Step 6: Install

```python
DownloadManager.install_release(extract_path)
# Removes: old ~/.nemo/nemo/
# Copies: extracted → ~/.nemo/nemo/
# Installs: Python dependencies (pip install -r requirements.txt)
# Creates: manifest.json with version info
```

### Step 7: Complete

```
✓ Installation complete
✓ Ready to use: nemo start
✓ Setup: nemo setup
```

---

## File Locations

### Installation Directories

```
~/.nemo/
├── nemo/                     (Installed Nemo)
│   ├── core/
│   ├── systems/
│   ├── requirements.txt
│   └── VERSION
├── releases/                 (Downloaded packages)
│   ├── nemo-v1.0.0.zip
│   ├── nemo-v1.0.1.zip
│   └── extracted/
├── credentials.json          (Encrypted OAuth tokens)
├── nemo_config.json          (User settings)
├── gemini_config.json        (Gemini settings)
├── nemo_manifest.json        (Installation metadata)
└── nemo.log                  (Application logs)
```

### Manifest File: `~/.nemo/nemo_manifest.json`

```json
{
  "installed_at": "2026-01-30T02:35:37.326Z",
  "version": "v1.0.0",
  "install_path": "C:\\Users\\username\\.nemo\\nemo",
  "python_version": "3.10.0",
  "dependencies_installed": true
}
```

---

## Website Integration

### Download Button on yukora.site

```html
<!-- Download Button -->
<a href="https://github.com/YOUR_ORG/project-nemo/releases/download/v1.0.0/nemo-v1.0.0.zip"
   class="btn btn-primary">
  Download Nemo
</a>

<!-- Or: CLI Download -->
<code>nemo download install</code>
```

### Quick Start on Website

```
┌─────────────────────────────────────┐
│ Install Nemo in 3 Commands          │
├─────────────────────────────────────┤
│                                     │
│ 1. Download:                        │
│    nemo download install            │
│                                     │
│ 2. Configure:                       │
│    nemo setup                       │
│                                     │
│ 3. Start:                           │
│    nemo start                       │
│                                     │
└─────────────────────────────────────┘
```

### Website Links

- **Download**: GitHub Release (direct .zip link)
- **CLI Method**: Show `nemo download install` command
- **Docs**: Link to GitHub repository
- **Support**: Issue tracker on GitHub

---

## Update Mechanism

### Automatic Check

```bash
nemo download update
# 1. Get current version from manifest
# 2. Fetch latest from GitHub
# 3. Compare versions
# 4. If newer: Run install wizard
```

### User Flow

```
User runs: nemo start
           ↓
System checks: nemo download update (background)
           ↓
If update available:
  "Update available (v1.0.1). Run: nemo download update"
           ↓
User runs: nemo download update
           ↓
Installation wizard runs, replaces old version
```

---

## Security Considerations

### Checksum Verification

- Download includes SHA256 checksum
- DownloadManager verifies integrity
- Prevents: Corruption, tampering, MITM attacks

### Directory Permissions

```bash
# ~/.nemo/ is user-owned
# ~/.nemo/nemo is writable by user
# Credentials encrypted at rest
```

### Dependency Security

```bash
# requirements.txt specifies exact versions
# Pip install verified from PyPI
# No arbitrary code execution
```

---

## CLI Commands (Complete Reference)

### Download Group

```bash
nemo download latest           # Check latest release
nemo download install          # Install from latest
nemo download update           # Update to latest
nemo download status           # Show installation status
```

### Other Groups (Already Implemented)

```bash
nemo setup                      # First-run setup
nemo start                      # Start Nemo daemon
nemo synthesis analyze          # Show synthesis analysis
nemo rewind                     # Infer past (demo)
nemo forward                    # Predict future (demo)
nemo voice start                # Start voice assistant
nemo tts speak "text"           # Text-to-speech
nemo security verify            # Security audit
nemo buttons show               # Show button mapping
```

---

## Deployment Checklist

### Before First Release

- [ ] Update GitHub repository URL in download_manager.py
- [ ] Create VERSION file with v1.0.0
- [ ] Package all components into .zip
- [ ] Compute SHA256 checksum
- [ ] Create GitHub release with tag v1.0.0
- [ ] Upload .zip to release assets
- [ ] Upload .sha256 to release assets
- [ ] Write comprehensive release notes
- [ ] Test `nemo download install` on clean machine
- [ ] Test `nemo download update` from v0.9.5 → v1.0.0
- [ ] Verify zero-storage audit passes
- [ ] Update website (yukora.site) with download link

### Ongoing Maintenance

- [ ] Monitor GitHub releases
- [ ] Update version in VERSION file
- [ ] Create new release for each version
- [ ] Test all CLI download commands
- [ ] Monitor user feedback/issues
- [ ] Release patches as needed
- [ ] Document breaking changes

---

## Example: User Downloads & Installs Nemo

### Scenario: First-Time User

```bash
$ nemo download install

════════════════════════════════════════════════════════════════
NEMO INSTALLATION WIZARD
════════════════════════════════════════════════════════════════

[*] Checking for latest Nemo release...
[✓] Found: Nemo Synthesis Engine v1.0.0 (v1.0.0)

[*] Downloading Nemo...
[*] Downloading... [██████████████████████░░░░░░░░░] 75.0%
[✓] Downloaded to ~/.nemo/releases/nemo-v1.0.0.zip

[*] Verifying checksum...
[✓] Checksum verified

[*] Extracting release...
[✓] Extracted

[*] Installing Nemo...
Collecting click==8.1.7
  Downloading click-8.1.7-py3-none-any.whl (97 kB)
Installing collected packages: click, rich, pyttsx3, ...
Successfully installed click-8.1.7 rich-13.7.0 ...

[✓] Installed to ~/.nemo/nemo

[*] Cleaning up...
[✓] Cleaned up nemo-v1.0.0.zip

════════════════════════════════════════════════════════════════
[✓] INSTALLATION COMPLETE
════════════════════════════════════════════════════════════════

Nemo is ready! Run: nemo start
Configuration: ~/.nemo/
Setup wizard: nemo setup
```

### Next: User Configures

```bash
$ nemo setup

╔════════════════════════════════════════════════════════════════╗
║        🧠 Nemo First-Run Setup                               ║
║     Screen + Keyboard Intelligence Synthesis                  ║
╚════════════════════════════════════════════════════════════════╝

[*] Welcome to Nemo! Let's get you set up.

[?] Which AI agent would you like to use?
  1) Gemini (Google, requires API key)
  2) Claude (Anthropic, requires API key)
  3) Ollama (Local, free, no internet required)
  [Select: 3]

[*] Ollama selected (Local mode)

[?] Enter your name: John

[?] Do you want to enable voice assistant? (Y/n): y

[✓] Setup complete!
[✓] Ready to start: nemo start
```

### Finally: User Starts Nemo

```bash
$ nemo start

╔════════════════════════════════════════════════════════════════╗
║        🧠 Nemo Synthesis Engine v1.0.0                      ║
║     Screen + Keyboard Intelligence Synthesis                  ║
╚════════════════════════════════════════════════════════════════╝

[✓] Nemo daemon started
[✓] Listening for button presses:
  • RIGHT ALT      → Internet AI
  • LEFT ALT       → TTS Button
  • LEFT ALT + ←  → REWIND
  • LEFT ALT + →  → FORWARD

[✓] Press your buttons. Nemo is ready.
```

---

## Troubleshooting

### Installation Fails

```bash
# Check internet connection
nemo download latest

# Check GitHub access
# (Ensure your network allows api.github.com)

# Try again
nemo download install
```

### Update Not Available

```bash
# Check current version
nemo download status

# Force re-check
nemo download latest

# If version is same, you're up to date
```

### Dependencies Not Installed

```bash
# Reinstall dependencies
pip install -r ~/.nemo/nemo/requirements.txt

# Or: Fresh install
nemo download install
```

---

## Summary

### What Users Get

✅ One-command installation: `nemo download install`
✅ Automatic updates: `nemo download update`
✅ Website download link (direct .zip)
✅ Secure: Checksum verification
✅ Fast: Progress tracking, parallel downloads
✅ Complete: All components included

### What Developers Get

✅ Version control on GitHub
✅ Release management system
✅ Source code accessible
✅ Fork/contribute capability
✅ Issue tracking
✅ Documentation

### What Company Gets

✅ Distributed through official channels
✅ User statistics (download counts)
✅ Feedback mechanism (issues)
✅ Support infrastructure
✅ Future monetization ready

---

**Deployment Ready. Ready for v1.0.0 Release.** 🚀
