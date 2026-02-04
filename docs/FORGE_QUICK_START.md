# Forge Quick Start Guide

Get up and running with extreme container orchestration in under 2 minutes.

---

## 1. Installation

### Via Shortcut CLI (Recommended)
Forge is the primary engine for Shortcut CLI v4.0.
```bash
irm shortcut.cli.sh | iex
shortcut forge --version
```

### Standalone
```bash
git clone https://github.com/torresjchristopher/forge.git
cd forge
pip install -e .
```

---

## 2. Launch the Dashboard

The native TUI dashboard provides full visibility and control over your containers and workflows.
```bash
shortcut forge tui
```
**Controls:**
- `1-6`: Switch views (Overview, Workflows, Containers, Scheduler, Logs, Images)
- `Arrows`: Navigate lists
- `Enter`: Select/View details
- `d`: Delete container/image
- `t`: Trigger workflow
- `p`: Pause/Resume schedule

---

## 3. Sync Your First Repo

Use Omni-Sync to automatically scaffold workflows from a GitHub repository.
```bash
shortcut vault login <your-gh-token>
shortcut sync repo torresjchristopher/forge
```

---

## 4. Run a Container

Execute containers with &lt;25ms warmed startup latency.
```bash
shortcut forge container run python:3.11 python -c "print('Forge is fast')"
```

---

## 5. Benchmarking

Prove the speed on your own machine.
```bash
shortcut forge benchmark compare
```

**Built for speed. Optimized for developers. Made for the future.**