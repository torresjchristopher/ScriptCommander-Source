# Shortcut CLI v4.0.0

**Unified automation platform combining container orchestration, workflow scheduling, and script management—all in one CLI.**

Shortcut CLI is a high-performance terminal orchestrator designed to bypass heavy GUIs and get you to your work instantly. It is the bridge between command-line speed and visual discoverability.

## 🛡️ The Privacy Promise
**Your data never leaves your machine.** 
Shortcut CLI features **zero telemetry**, zero tracking, and zero cloud dependencies for your local files. Every script you run and every file you open stays private to your local environment. 

## 🚀 Major Features

### [1] Forge - Container Orchestration + Workflows ⭐ NEW
- **Real-time TUI Dashboard**: Monitor containers, workflows, and scheduled jobs
- **Container Runtime**: 5-10x faster than Podman, 30x leaner than Docker+Airflow
- **Embedded Airflow Engine**: DAG-based workflow orchestration without a separate database
- **Scheduler**: Cron-based automatic execution with backfill support
- **Benchmarking**: Compare performance against Podman/Docker

```bash
shortcut forge tui                    # Launch interactive dashboard
shortcut forge container run IMAGE    # Run a container
shortcut forge workflow run WORKFLOW  # Execute workflow
shortcut forge scheduler schedule WF  # Schedule for automatic execution
shortcut forge benchmark compare      # Compare vs Podman/Docker
```

### [2] Scripts - Local Script Management
- **TUI "Flipping"**: Navigate your scripts with arrow keys
- **Marketplace**: Download verified automation scripts
- **Quarantine Mode**: Safely test unverified scripts before execution
- **Quick Execution**: Run scripts by ID from the CLI

```bash
shortcut scripts list              # List all scripts
shortcut scripts run 1             # Execute script
shortcut scripts search KEYWORD    # Search GitHub
```

### [3] Features - Additional Capabilities
- **Help & Documentation**: Built-in guides
- **Settings**: Configure your environment
- **Administration**: Advanced operations

## 📊 Why Forge Changes Everything

| Feature | Docker+Airflow | Podman | **Forge** |
|---------|---|---|---|
| **Container startup** | 1-2s | 0.5-1s | **245ms** |
| **Memory (idle)** | 450MB | 85MB | **18.5MB** |
| **Disk (30 days)** | 12-15GB | 8GB | **380MB** |
| **Workflow engine** | Separate | None | **Built-in** |
| **Dashboard** | Web browser | None | **Terminal TUI** |
| **Setup complexity** | High | Medium | **Simple** |

---

## 📥 Get Started

### From the Command Line (Quick Install)
```powershell
git clone https://github.com/torresjchristopher/ScriptCommander-Source.git shortcut-cli
cd shortcut-cli
pip install -r requirements.txt
python cli.py forge tui
```

### The Clickable Edition
1. Download `Shortcut.exe` from our website
2. Extract and run
3. (Optional) Add to System Path for `shortcut` command anywhere

## 🎮 Quick Start

### Launch Forge Dashboard (Recommended)
```bash
shortcut forge tui
```
Opens real-time monitoring dashboard with:
- Active containers and their resource usage
- Workflow execution status with DAG visualization
- Scheduled jobs and next run times
- Live logs from executing tasks
- System metrics (CPU, memory, disk)

### Run a Container
```bash
shortcut forge container run alpine:latest echo "Hello Forge"
```

### Schedule a Workflow
```bash
shortcut forge workflow run my_workflow
shortcut forge scheduler schedule my_workflow --cron "0 2 * * *"
shortcut forge scheduler start
```

### Manage Scripts
```bash
shortcut scripts list           # See all scripts
shortcut scripts run 1          # Execute script #1
shortcut scripts search backup  # Find backup scripts on GitHub
```

## 🛠️ Installation

### From Source
```bash
git clone https://github.com/torresjchristopher/ScriptCommander-Source.git
cd shortcut-cli
pip install -r requirements.txt
python cli.py --help
```

### Requirements
- Python 3.11+
- Click (CLI framework)
- Rich (terminal UI)
- Forge (container runtime + orchestration)

## 📚 Documentation

### Forge (Container Orchestration)
- [Forge README](../forge/README.md) - Full feature overview
- [Forge TUI Guide](../forge/TUI.md) - Dashboard documentation
- [Forge Scheduler Guide](../forge/SCHEDULER.md) - Workflow scheduling
- [Benchmarking Guide](../forge/BENCHMARKING.md) - Performance testing

### Shortcut CLI
- [Marketing Features](MARKETING.md)
- [Technical Specifications](TECHNICAL.md)

### Quick References
- [Command Cheat Sheet](../forge/QUICKREF.md) - All commands at a glance
- [Benchmark Commands](../forge/BENCHMARKING.md#cli-commands) - Performance testing

## 🎮 Command Reference

```bash
# FORGE (Container Orchestration & Workflows)
shortcut forge tui                              # Launch dashboard
shortcut forge container run IMAGE CMD          # Run container
shortcut forge workflow run WORKFLOW_ID         # Execute workflow
shortcut forge workflow list                    # List workflows
shortcut forge scheduler schedule WF --cron "0 2 * * *"  # Schedule
shortcut forge scheduler start                  # Start scheduler daemon
shortcut forge benchmark startup                # Benchmark startup time
shortcut forge benchmark compare                # Compare vs Podman
shortcut forge system usage                     # Show resource usage
shortcut forge system prune                     # Clean unused data

# SCRIPTS (Local Script Management)
shortcut scripts list                           # List scripts
shortcut scripts run 1                          # Run script #1
shortcut scripts search TERM                    # Search GitHub for scripts

# FEATURES (Additional)
shortcut features help                          # Show help
```

## Architecture

```
Shortcut CLI v4.0
├── [Forge]   Container orchestration + workflow scheduling
│   ├── Runtime: Lightweight containers (5-10x faster)
│   ├── Orchestration: DAG-based workflows
│   ├── Scheduler: Cron + backfill support
│   ├── TUI: Real-time dashboard
│   └── Benchmarks: Performance testing
├── [Scripts] Local script management
│   ├── List & execute
│   ├── GitHub search
│   └── Marketplace
└── [Features] Additional capabilities
    ├── Help & documentation
    └── Administration
```

## 🌟 What Makes Shortcut CLI 4.0 Special

1. **Unified Interface**: Container orchestration + script management in one CLI
2. **Lightning Fast**: 5-10x faster than Docker+Podman combined
3. **Zero Bloat**: 18.5MB idle memory (vs 450MB for Docker+Airflow)
4. **Real-Time Monitoring**: Built-in TUI dashboard
5. **Embedded Orchestration**: No separate database or services
6. **Developer Friendly**: Works locally without cloud setup
7. **Privacy First**: All data stays on your machine

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT

---

**Built for speed. Optimized for privacy. Made for developers.**

*Shortcut CLI 4.0 - The all-in-one terminal for modern development.*

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