# Shortcut CLI v3.0.0

Shortcut CLI is a high-performance terminal orchestrator designed to bypass heavy GUIs and get you to your work instantly. It is the bridge between command-line speed and visual discoverability.

## 🛡️ The Privacy Promise
**Your data never leaves your machine.** 
Shortcut CLI features **zero telemetry**, zero tracking, and zero cloud dependencies for your local files. Every script you run and every file you open stays private to your local environment. 

## 🚀 Modern Features
- **TUI "Flipping"**: Navigate your scripts with a high-speed, arrow-key driven interface. No more typing long paths.
- **Quick-Open Recent Files**: One-click access to your most recently used Word docs, PDFs, and projects. Bypasses the "Open" menus of heavy applications.
- **Verified Marketplace**: Audited, secure automation scripts ready to download and run instantly.
- **Dual-Mode Engine**: Use the interactive **TUI** for exploration or the **CLI** for direct execution.

## 📥 Get Started (Download & Install)

### From the Command Line (Quick Install)
Run this in PowerShell to clone and set up the dev environment instantly:
```powershell
git clone https://github.com/torresjchristopher/ScriptCommander-Source.git shortcut-cli; cd shortcut-cli; pip install -r requirements.txt
```

### The Clickable Edition
1. Download the `Shortcut-CLI.zip` from our website.
2. Extract `Shortcut.exe`.
3. (Optional) Add the folder to your **System Path** to launch it by just typing `shortcut` from anywhere.

## 🎮 How to Use
Shortcut CLI automatically detects how you want to work:

1. **Interactive Mode (TUI)**: 
   Simply run `shortcut` (or `python app.py`).
   *Arrows to navigate, Enter to select, 'q' to go back.*

2. **Direct Mode (CLI)**:
   Run `shortcut [command]`.
   - `shortcut list`: Show all scripts in a clean table.
   - `shortcut run [ID]`: Execute a specific script by its number.
   - `shortcut market`: View the verified marketplace.

---
*Built for speed. Optimized for privacy.*

## 🚀 Key Features

- **TUI "Flipping"**: Navigate through your scripts with arrow keys—no more searching through folders.
- **Recent Files (Quick Open)**: Instantly open your most recent Word docs, PDFs, or projects directly from the terminal. Bypasses the "Open File" menu of heavy applications.
- **Verified Marketplace**: Pull audited automation scripts directly into your local library.
- **Keyboard-First**: Optimized for speed. Keep your hands on the keys.

## 🛠️ Installation

### The Executable
Download `Shortcut.exe` from our website. Add it to your PATH to launch it from anywhere by just typing `shortcut`.

### From Source
```bash
pip install -r requirements.txt
python app.py
```

## 🎮 Navigation
- **Arrows**: Navigate menus and lists.
- **Enter**: Execute script or open file.
- **'q' or Esc**: Go back or exit.

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