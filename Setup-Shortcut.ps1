# Setup-Shortcut.ps1
# Automated Installation Script for Shortcut CLI

$InstallDir = "C:\ShortcutCLI"
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir | Out-Null
}

Set-Location $InstallDir

Write-Host "--- Downloading Shortcut CLI ---" -ForegroundColor Cyan
git clone https://github.com/torresjchristopher/ScriptCommander-Source.git .

Write-Host "--- Installing Dependencies ---" -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "--- Finalizing Setup ---" -ForegroundColor Cyan
.\Setup-DesktopShortcut.ps1

Write-Host "`n[SUCCESS] Shortcut CLI is now installed in $InstallDir" -ForegroundColor Green
Write-Host "Launch it from your desktop or by typing 'python app.py' in the folder." -ForegroundColor Yellow
