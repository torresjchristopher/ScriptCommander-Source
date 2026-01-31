#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Complete GitHub + downloadnemo.com Deployment Script
    
.DESCRIPTION
    Prepares Nemo for GitHub push and website deployment
    
.EXAMPLE
    .\deploy-github-complete.ps1
#>

param(
    [string]$Version = "1.0.0",
    [string]$GitHubUser = "torres-j-christopher",
    [string]$RepoName = "nemo",
    [string]$Domain = "downloadnemo.com"
)

$SourceRoot = "C:\Users\serro\ScriptCommander"
$TempDeployDir = Join-Path $env:TEMP "nemo-github-deploy-$([DateTime]::Now.Ticks)"

Write-Host "`n╔════════════════════════════════════════════════════════════════╗"
Write-Host "║                                                                ║"
Write-Host "║         Nemo GitHub & Website Deployment Script               ║"
Write-Host "║                                                                ║"
Write-Host "║    Deploying to GitHub + Setting up downloadnemo.com          ║"
Write-Host "║                                                                ║"
Write-Host "╚════════════════════════════════════════════════════════════════╝`n"

Write-Host "Configuration:"
Write-Host "  GitHub User:   $GitHubUser"
Write-Host "  Repository:    $RepoName"
Write-Host "  Domain:        $Domain"
Write-Host "  Version:       $Version"
Write-Host "  GitHub URL:    https://github.com/$GitHubUser/$RepoName`n"

# Step 1: Check if GitHub CLI is installed
Write-Host "[*] Checking GitHub CLI..." -ForegroundColor Cyan
$ghVersion = gh --version 2>$null
if ($null -eq $ghVersion) {
    Write-Host "[!] GitHub CLI not found. Please install from: https://cli.github.com" -ForegroundColor Yellow
    Write-Host "[*] Alternatively, use web interface to create repo at: https://github.com/new" -ForegroundColor Yellow
} else {
    Write-Host "[OK] GitHub CLI found: $($ghVersion[0])" -ForegroundColor Green
}

# Step 2: Create deployment structure
Write-Host "`n[*] Step 1: Preparing deployment structure..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path "$TempDeployDir/nemo" -Force | Out-Null
New-Item -ItemType Directory -Path "$TempDeployDir/nemo/nemo/core" -Force | Out-Null
New-Item -ItemType Directory -Path "$TempDeployDir/nemo/nemo/systems/task-screen-simulator" -Force | Out-Null

Write-Host "[OK] Deployment structure created" -ForegroundColor Green

# Step 3: Copy all files
Write-Host "`n[*] Step 2: Copying Nemo files..." -ForegroundColor Cyan

# Core files
Copy-Item "$SourceRoot\Project-Nemo-Synthesis-Master-AI\core\*" "$TempDeployDir\nemo\nemo\core\" -Recurse -Force

# System files
Copy-Item "$SourceRoot\Project-Liberty-Mobile-Development\systems\task-screen-simulator\*.py" `
    "$TempDeployDir\nemo\nemo\systems\task-screen-simulator\" -Force

# Documentation
Copy-Item "$SourceRoot\Project-Liberty-Mobile-Development\systems\task-screen-simulator\*.md" `
    "$TempDeployDir\nemo\nemo\systems\task-screen-simulator\" -Force

Copy-Item "$SourceRoot\Project-Liberty-Mobile-Development\systems\task-screen-simulator\requirements.txt" `
    "$TempDeployDir\nemo\nemo\systems\task-screen-simulator\" -Force

Copy-Item "$SourceRoot\Project-Liberty-Mobile-Development\systems\task-screen-simulator\VERSION" `
    "$TempDeployDir\nemo\nemo\systems\task-screen-simulator\" -Force

Copy-Item "$SourceRoot\Project-Liberty-Mobile-Development\systems\task-screen-simulator\setup.py" `
    "$TempDeployDir\nemo\nemo\systems\task-screen-simulator\" -Force

Write-Host "[OK] Files copied" -ForegroundColor Green

# Step 4: Create root files
Write-Host "`n[*] Step 3: Creating root-level files..." -ForegroundColor Cyan

# Create README.md
$readmeContent = @"
# Nemo Synthesis Engine

Pure Intelligence. No Storage. No Recording. Just Synthesis.

Visit: https://$Domain

## Four-Button Interface

- RIGHT ALT: Internet AI (voice input)
- LEFT ALT (tap): TTS Button (voice output) 
- LEFT ALT + LEFT ARROW: REWIND (infer past)
- LEFT ALT + RIGHT ARROW: FORWARD (predict future)

## Quick Installation

`nemo download install`

Or download from GitHub releases.

## Features

- Keyboard pattern synthesis (35-D signature)
- Screen context analysis
- Temporal inference (REWIND/FORWARD)
- AI butler (Gemini, Claude, Ollama)
- Text-to-speech with ZERO audio storage
- Four-button interface
- Complete security audit system

## Zero Storage

- No voice recordings
- No audio files  
- No keystroke logs
- No persistence
- Pure synthesis only

## Documentation

- Deployment Guide: nemo/systems/task-screen-simulator/DEPLOYMENT_GUIDE.md
- Four-Button & TTS: nemo/systems/task-screen-simulator/FOUR_BUTTON_TTS_GUIDE.md
- Architecture: nemo/core/README.md

## System Requirements

- Python 3.10+
- Windows, macOS, or Linux
- 200MB disk space

## Support

- Website: https://$Domain
- Issues: https://github.com/$GitHubUser/$RepoName/issues
- GitHub: https://github.com/$GitHubUser/$RepoName

The future of personal AI. Voice in, voice out. No qwerty needed.
"@

$readmeContent | Out-File -FilePath "$TempDeployDir\nemo\README.md" -Encoding UTF8 -Force

# Create LICENSE
$licenseContent = @"
NEMO SYNTHESIS ENGINE - PROPRIETARY LICENSE

Copyright (c) 2026 Chris Torres

Permission is hereby granted to download, install, and use Nemo for personal use.
Redistribution, modification, or commercial use is prohibited without written permission.

For licensing inquiries: contact torres-j-christopher
"@

$licenseContent | Out-File -FilePath "$TempDeployDir\nemo\LICENSE" -Encoding UTF8 -Force

# Create .gitignore
$gitignoreContent = @"
__pycache__/
*.py[cod]
*.so
.Python
build/
dist/
*.egg-info/
.installed.cfg
*.egg
venv/
ENV/
env/
.vscode/
.idea/
*.swp
*.swo
*~
~/.nemo/
.nemo/
*.log
*.db
credentials.json
nemo_config.json
gemini_config.json
nemo_manifest.json
"@

$gitignoreContent | Out-File -FilePath "$TempDeployDir\nemo\.gitignore" -Encoding UTF8 -Force

Write-Host "[OK] Root files created" -ForegroundColor Green

# Step 5: Initialize Git repo
Write-Host "`n[*] Step 4: Initializing Git repository..." -ForegroundColor Cyan

Set-Location "$TempDeployDir\nemo"

if (Test-Path ".git") {
    Write-Host "[*] Git repo already exists, skipping init" -ForegroundColor Yellow
} else {
    git init | Out-Null
    git config user.name "Chris Torres" | Out-Null
    git config user.email "torres-j-christopher@example.com" | Out-Null
}

Write-Host "[OK] Git initialized" -ForegroundColor Green

# Step 6: Commit files
Write-Host "`n[*] Step 5: Committing files..." -ForegroundColor Cyan

git add . | Out-Null
git commit -m "Nemo Synthesis Engine v$Version - Initial Release" --quiet | Out-Null

Write-Host "[OK] Files committed" -ForegroundColor Green

# Step 7: Create tag
Write-Host "`n[*] Step 6: Creating version tag..." -ForegroundColor Cyan

git tag -a "v$Version" -m "Nemo Synthesis Engine v$Version" --force | Out-Null

Write-Host "[OK] Tag v$Version created" -ForegroundColor Green

# Step 8: Display instructions
Write-Host @"
`n╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║            [OK] DEPLOYMENT READY                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

Repository Location:
  $TempDeployDir\nemo

Files Ready:
  [OK] All Nemo components
  [OK] Documentation
  [OK] README.md
  [OK] LICENSE
  [OK] .gitignore
  [OK] Git initialized
  [OK] Version tagged: v$Version

NEXT STEPS:

1. CREATE GITHUB REPOSITORY
   
   Using GitHub CLI:
   gh repo create $RepoName --public --description "Nemo Synthesis Engine"
   
   Then push:
   cd $TempDeployDir\nemo
   git remote add origin https://github.com/$GitHubUser/$RepoName.git
   git branch -M main
   git push -u origin main
   git push --tags

2. CREATE GITHUB RELEASE
   
   After push completes:
   - Go to: https://github.com/$GitHubUser/$RepoName/releases/new
   - Tag: v$Version
   - Title: Nemo Synthesis Engine v$Version
   - Publish release

3. SETUP WEBSITE
   
   Copy to downloadnemo.com:
   C:\Users\serro\.copilot\session-state\6222e9dc-d4d6-4d08-be1d-4a58870b75e1\files\downloadnemo-index.html
   
   Save as: index.html on your web server

4. CONFIGURE DNS
   
   Point downloadnemo.com to your hosting
   Enable HTTPS (SSL certificate)

Repository ready at:
  $TempDeployDir\nemo

"@

Write-Host "[*] Opening deployment directory..." -ForegroundColor Cyan
Invoke-Item "$TempDeployDir\nemo"

Write-Host "`n[OK] Deployment preparation complete!" -ForegroundColor Green
Write-Host "[*] Follow the steps above to complete GitHub and website setup`n" -ForegroundColor Cyan
