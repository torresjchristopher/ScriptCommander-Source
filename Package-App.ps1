# Package-App.ps1
# This script bundles Shortcut CLI into a single high-performance EXE.

$ProjectDir = Get-Location
$DistDir = Join-Path $ProjectDir "dist"
$ZipFile = Join-Path $ProjectDir "Shortcut-CLI-v3.0.0.zip"

# 1. Ensure Dependencies are met
Write-Host "Installing/Updating build dependencies..." -ForegroundColor Cyan
pip install rich requests click pyinstaller

# 2. Build the Unified Executable
# This bundles app.py (TUI) and cli.py (CLI) into one Shortcut.exe
Write-Host "Building Unified Shortcut CLI Executable..." -ForegroundColor Cyan
pyinstaller --onefile --name "Shortcut" --icon=favicon.ico --add-data "favicon.ico;." --add-data "marketplace.json;." app.py

# 3. Create the Release Zip
Write-Host "Creating Release Package..." -ForegroundColor Cyan
if (Test-Path $ZipFile) { Remove-Item $ZipFile }

# We include the EXE and the README for the user
$FilesToZip = Get-ChildItem "$DistDir\Shortcut.exe"
Compress-Archive -Path $FilesToZip -DestinationPath $ZipFile

Write-Host "`n[SUCCESS] Shortcut CLI v3.0.0 is ready for deployment!" -ForegroundColor Green
Write-Host "Release Zip: $ZipFile" -ForegroundColor Yellow