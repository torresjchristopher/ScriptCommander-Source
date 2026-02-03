# Script Commander v2.0.0

Script Commander is a modern, open-source automation dashboard that allows you to manage and execute PowerShell and Python scripts with a single click. It features a curated marketplace for community-built tools and a focus on security and privacy.

## Features

- 🚀 **One-Click Execution**: Launch complex tools instantly.
- 💻 **Headless CLI**: Full script management from the terminal.
- 🌎 **Global Marketplace**: Download verified scripts from the official repository.
- 🛡️ **Security First**: Dynamic execution policies and UAC integration.
- 🎨 **Modern UI**: Dark-mode interface built with CustomTkinter.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Windows 10/11 (PowerShell 5.1+)

### Running the Application

1. **Option A: The Executable (Recommended)**
   Download the latest `.zip` from our website, extract it, and run `ScriptCommander.exe`.

2. **Option B: From Source**
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

## CLI Usage

Script Commander features a robust CLI for power users:

- **List Local Scripts**: `python app.py --list`
- **Browse Marketplace**: `python app.py --market`
- **Pagination**: `python app.py --market --page 2`

*If using the executable, replace `python app.py` with `ScriptCommander.exe`.*

## Usage

- **My Scripts**: Manage your local collection of `.ps1` and `.py` scripts located in the `/scripts` directory.
- **Marketplace**: Browse and download new tools directly into your library.
- **Settings**: Configure your environment and update the application.

## Documentation

- [Marketing Features](MARKETING.md)
- [Technical Specifications](TECHNICAL.md)
- [Official Website](https://scriptcommander.store)

## Contributing

Contributions are welcome! Please check out the [Technical Specifications](TECHNICAL.md) for architecture details before submitting a pull request.

## License

This project is licensed under the MIT License.