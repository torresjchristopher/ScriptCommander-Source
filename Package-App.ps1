# Package-App.ps1
# This script bundles Shortcut (by Script Commander) into a single EXE.

$ProjectDir = Get-Location
$DistDir = Join-Path $ProjectDir "dist"
$ZipFile = Join-Path $ProjectDir "Shortcut-v3.0.0.zip"

# 1. Install Dependencies
pip install rich requests msvcrt-type-safe # msvcrt is builtin but rich/requests are needed

# 2. Build the Executable
Write-Host "Building Shortcut CLI..." -ForegroundColor Cyan
# Removed --noconsole because TUIs need a console window
pyinstaller --onefile --name "Shortcut" --icon=favicon.ico --add-data "favicon.ico;." --add-data "marketplace.json;." app.py

# 3. Create the Zip
Write-Host "Creating Zip Package..." -ForegroundColor Cyan
if (Test-Path $ZipFile) { Remove-Item $ZipFile }
$FilesToZip = Get-ChildItem "$DistDir\Shortcut.exe"
Compress-Archive -Path $FilesToZip -DestinationPath $ZipFile

Write-Host "`nSuccessfully created: $ZipFile" -ForegroundColor Green
