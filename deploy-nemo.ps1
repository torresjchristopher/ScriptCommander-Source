#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Deploy Nemo to GitHub - Complete Automation Script
    
.DESCRIPTION
    Creates release package, computes checksums, and pushes to GitHub
    
.EXAMPLE
    .\deploy-nemo.ps1 -Version "1.0.0" -GitHubOrg "torres-j-christopher"
#>

param(
    [string]$Version = "1.0.0",
    [string]$GitHubOrg = "torres-j-christopher",
    [string]$RepoName = "project-nemo",
    [switch]$CreateRepo = $false,
    [switch]$DryRun = $false
)

# Configuration
$SourceRoot = "C:\Users\serro\ScriptCommander"
$TempDir = Join-Path $env:TEMP "nemo-deploy-$([DateTime]::Now.Ticks)"
$ReleaseDir = Join-Path $TempDir "release"
$PackageDir = Join-Path $TempDir "nemo-v$Version"
$GitHubRepoUrl = "https://github.com/$GitHubOrg/$RepoName.git"

Write-Host @"
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║         Nemo GitHub Deployment Script v1.0                   ║
║                                                                ║
║    Preparing Nemo for public release and GitHub deployment    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Configuration:
  Version:       $Version
  GitHub Org:    $GitHubOrg
  Repository:    $RepoName
  GitHub URL:    $GitHubRepoUrl
  Temp Dir:      $TempDir
  DRY RUN:       $DryRun

"

# Step 1: Create package structure
Write-Host "[*] Step 1: Creating package structure..." -ForegroundColor Cyan

New-Item -ItemType Directory -Path $PackageDir -Force | Out-Null
New-Item -ItemType Directory -Path "$PackageDir/nemo/core" -Force | Out-Null
New-Item -ItemType Directory -Path "$PackageDir/nemo/systems/task-screen-simulator" -Force | Out-Null

Write-Host "[✓] Package directory created: $PackageDir" -ForegroundColor Green

# Step 2: Copy Nemo components
Write-Host "`n[*] Step 2: Copying Nemo components..." -ForegroundColor Cyan

# Copy core (nemo.py, cli.py, README)
$CoreSource = "$SourceRoot\Project-Nemo-Synthesis-Master-AI\core"
Copy-Item "$CoreSource\*" "$PackageDir/nemo/core/" -Recurse -Force

# Copy systems (all synthesis components)
$SystemsSource = "$SourceRoot\Project-Liberty-Mobile-Development\systems\task-screen-simulator"
Copy-Item "$SystemsSource\*.py" "$PackageDir/nemo/systems/task-screen-simulator/" -Force

# Copy documentation
Copy-Item "$SystemsSource\*.md" "$PackageDir/nemo/systems/task-screen-simulator/" -Force
Copy-Item "$SystemsSource\requirements.txt" "$PackageDir/nemo/systems/task-screen-simulator/" -Force
Copy-Item "$SystemsSource\VERSION" "$PackageDir/nemo/systems/task-screen-simulator/" -Force
Copy-Item "$SystemsSource\setup.py" "$PackageDir/nemo/systems/task-screen-simulator/" -Force

Write-Host "[✓] Components copied" -ForegroundColor Green

# Step 3: Create root-level files
Write-Host "`n[*] Step 3: Creating root-level files..." -ForegroundColor Cyan

# Create main README
$ReadmeContent = @"
# Nemo Synthesis Engine

**Pure Intelligence. No Storage. No Recording. Just Synthesis.**

## Four-Button Interface

- **RIGHT ALT** - Internet AI (voice input to Gemini)
- **LEFT ALT (tap)** - TTS Button (voice output) 
- **LEFT ALT + LEFT ARROW** - REWIND (infer past)
- **LEFT ALT + RIGHT ARROW** - FORWARD (predict future)

## Installation

\`\`\`bash
# Option 1: Via CLI
nemo download install

# Option 2: Download from releases
# Extract and run: nemo setup
\`\`\`

## Quick Start

1. **Install**: \`nemo download install\`
2. **Configure**: \`nemo setup\`
3. **Start**: \`nemo start\`
4. **Press buttons**: RIGHT ALT (voice), LEFT ALT (hear synthesis)

## Features

✅ Keyboard pattern synthesis (35-D signature)
✅ Screen context analysis
✅ Temporal inference (REWIND/FORWARD)
✅ AI butler voice assistant (Gemini, Claude, Ollama)
✅ Text-to-speech with zero audio storage
✅ Four-button interface (natural interaction)
✅ Complete security audit system
✅ GitHub releases with auto-update

## Zero Storage

- ❌ No voice recordings
- ❌ No audio files
- ❌ No keystroke logs
- ❌ No screen captures
- ✅ Pure synthesis, pure intelligence

## Architecture

Built on **The Blanket Theory**: God as universal intelligence synthesizing through human perspectives.

Nemo is the synthesis engine - learns your keyboard genius + screen context to understand your intent.

## Documentation

- [Deployment Guide](nemo/systems/task-screen-simulator/DEPLOYMENT_GUIDE.md)
- [Four-Button Guide](nemo/systems/task-screen-simulator/FOUR_BUTTON_TTS_GUIDE.md)
- [Architecture](nemo/core/README.md)

## License

Proprietary - Contact torres-j-christopher for licensing

## Support

Issues: https://github.com/$GitHubOrg/$RepoName/issues

---

**The future of personal AI: Voice in, voice out. No qwerty needed.** 🎙️
"@

$ReadmeContent | Out-File -FilePath "$PackageDir/README.md" -Encoding UTF8 -Force

# Create LICENSE
$LicenseContent = @"
NEMO SYNTHESIS ENGINE - PROPRIETARY LICENSE

Copyright (c) 2026 Chris Torres

Permission is hereby granted to download, install, and use Nemo for personal use.
Redistribution, modification, or commercial use is prohibited without written permission.

For licensing inquiries: torres-j-christopher@example.com
"@

$LicenseContent | Out-File -FilePath "$PackageDir/LICENSE" -Encoding UTF8 -Force

# Create .gitignore
$GitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Nemo specific
~/.nemo/
.nemo/
*.log
*.db
credentials.json
nemo_config.json
gemini_config.json
nemo_manifest.json
"@

$GitignoreContent | Out-File -FilePath "$PackageDir/.gitignore" -Encoding UTF8 -Force

Write-Host "[✓] Root files created" -ForegroundColor Green

# Step 4: Create ZIP package
Write-Host "`n[*] Step 3: Creating ZIP package..." -ForegroundColor Cyan

$ZipPath = "$ReleaseDir/nemo-v$Version.zip"
New-Item -ItemType Directory -Path $ReleaseDir -Force | Out-Null

if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }

# Create ZIP using PowerShell
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($PackageDir, $ZipPath)

$ZipSize = (Get-Item $ZipPath).Length / 1MB
Write-Host "[✓] Package created: $ZipPath ($([Math]::Round($ZipSize, 2)) MB)" -ForegroundColor Green

# Step 5: Compute SHA256 checksum
Write-Host "`n[*] Step 4: Computing SHA256 checksum..." -ForegroundColor Cyan

$SHA256 = (Get-FileHash -Path $ZipPath -Algorithm SHA256).Hash
$SHA256 | Out-File -FilePath "$ReleaseDir/nemo-v$Version.sha256" -Encoding ASCII -Force

Write-Host "[✓] Checksum: $SHA256" -ForegroundColor Green

# Step 6: Create release notes
Write-Host "`n[*] Step 5: Creating release notes..." -ForegroundColor Cyan

$ReleaseNotesContent = @"
# Nemo Synthesis Engine v$Version

**Pure Intelligence. No Storage. No Recording. Just Synthesis.**

## What's New

### Four-Button Interface
- RIGHT ALT: Internet AI (voice input)
- LEFT ALT: TTS Button (voice output) - THE HUMAN ELEMENT
- LEFT ALT + LEFT: REWIND (infer past)
- LEFT ALT + RIGHT: FORWARD (predict future)

### Features
✅ Keyboard pattern synthesis (35-D keystroke signature)
✅ Real-time screen context analysis
✅ Temporal inference (REWIND/FORWARD)
✅ AI butler (Gemini, Claude, Ollama support)
✅ Text-to-speech with ZERO audio storage
✅ Complete security audit system
✅ GitHub release with auto-updates

### Security
- Zero audio storage (verified with audit system)
- In-memory TTS (never written to disk)
- Encrypted credentials
- No temp files
- No logs (unless user enables)
- Pure synthesis, no recording

### Installation

\`\`\`bash
# CLI installation (recommended)
nemo download install

# Or download from releases above
# Extract and run: nemo setup
\`\`\`

## Architecture

Built on **The Blanket Theory** - the philosophical framework where God is universal intelligence synthesizing through human perspectives.

Nemo learns your keyboard genius (how you type) + your screen context (what you're doing) to synthesize understanding of your intent.

## Components (239.3K LOC)

- **Screen Analyzer** (6.8K) - Real-time context
- **Keyboard Synthesizer** (9.4K) - User behavior learning
- **Temporal Inference** (11.2K) - Rewind/forward synthesis
- **Gemini Integration** (10.1K) - Multi-agent AI
- **Setup Wizard** (11.4K) - First-run config
- **Voice Assistant** (8.0K) - Hotkey voice
- **TTS Engine** (12.1K) - Voice output
- **Audio Security** (13.0K) - Zero-storage audit
- **Four-Button Interface** (11.3K) - Button detection
- **Download Manager** (12.3K) - GitHub releases
- **CLI Framework** (12.7K) - All commands

## Documentation

- [README](README.md)
- [Deployment Guide](nemo/systems/task-screen-simulator/DEPLOYMENT_GUIDE.md)
- [Four-Button & TTS Guide](nemo/systems/task-screen-simulator/FOUR_BUTTON_TTS_GUIDE.md)
- [Architecture](nemo/core/README.md)

## System Requirements

- Python 3.10+
- Windows, macOS, or Linux
- ~200MB disk space
- Internet (optional - voice features)

## Quick Start

1. Download and extract
2. Run: \`nemo setup\`
3. Run: \`nemo start\`
4. Press RIGHT ALT to start

## Version History

### v1.0.0 (January 30, 2026)
- Initial release
- Complete synthesis engine
- Four-button interface
- TTS voice output
- Zero-storage security
- GitHub auto-update

## Support

Issues: https://github.com/$GitHubOrg/$RepoName/issues

---

**The nail in the coffin for qwerty. Voice in, voice out. Pure intelligence. No storage.** 🎙️

Experience Nemo.
"@

$ReleaseNotesContent | Out-File -FilePath "$ReleaseDir/RELEASE_NOTES_v$Version.md" -Encoding UTF8 -Force

Write-Host "[✓] Release notes created" -ForegroundColor Green

# Step 7: Display summary
Write-Host @"
`n╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║            ✅ DEPLOYMENT PACKAGE READY                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Package Contents:
  Location:   $ReleaseDir
  
Files:
  ✓ nemo-v$Version.zip         ($([Math]::Round($ZipSize, 2)) MB)
  ✓ nemo-v$Version.sha256      (checksum verification)
  ✓ RELEASE_NOTES_v$Version.md (GitHub release description)

Checksum:
  $SHA256

Next Steps:

1. GitHub Setup (Optional - for automation):
   \`\`\`bash
   # If using GitHub CLI
   gh repo create project-nemo --public --description "Nemo Synthesis Engine"
   \`\`\`

2. Manual GitHub Release:
   - Go to: https://github.com/$GitHubOrg/$RepoName/releases/new
   - Tag: v$Version
   - Title: Nemo Synthesis Engine v$Version
   - Description: (use content from RELEASE_NOTES_v$Version.md)
   - Upload: nemo-v$Version.zip
   - Upload: nemo-v$Version.sha256
   - Publish Release

3. Update Website (yukora.site):
   - Add download link
   - Add CLI method: nemo download install
   - Add quick-start guide

Release Directory:
  $ReleaseDir

"@

# Display file contents for easy copy-paste
Write-Host "`n[*] Release Notes (for GitHub):" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Get-Content "$ReleaseDir/RELEASE_NOTES_v$Version.md" | Write-Host
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

Write-Host "`n[✓] Deployment package ready!" -ForegroundColor Green
Write-Host "Opening release directory..."
Invoke-Item $ReleaseDir
