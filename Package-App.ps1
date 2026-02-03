# Package-App.ps1
# This script bundles Script Commander into a single EXE and Zips it for the website.

$ProjectDir = Get-Location
$DistDir = Join-Path $ProjectDir "dist"
$ZipFile = Join-Path $ProjectDir "ScriptCommander-v2.0.0.zip"

# 1. Install PyInstaller if missing
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Cyan
    pip install pyinstaller
}

# 2. Build the Executable
Write-Host "Building Executable..." -ForegroundColor Cyan
# --noconsole hides the CMD window when launching the GUI
# --onefile bundles everything into one EXE
pyinstaller --noconsole --onefile --name "ScriptCommander" --icon=favicon.ico --add-data "favicon.ico;." --add-data "marketplace.json;." app.py

# 3. Create the Zip for the website
Write-Host "Creating Zip Package..." -ForegroundColor Cyan
if (Test-Path $ZipFile) { Remove-Item $ZipFile }

# Include the EXE and README in the zip
$FilesToZip = Get-ChildItem "$DistDir\ScriptCommander.exe"
Compress-Archive -Path $FilesToZip -DestinationPath $ZipFile

Write-Host "`nSuccessfully created: $ZipFile" -ForegroundColor Green
Write-Host "You can now upload this zip to your website." -ForegroundColor Yellow
