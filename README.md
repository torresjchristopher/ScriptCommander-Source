# Nexus OS (formerly Shortcut CLI)

**The Sovereign Shell for Propagative Intelligence.**

Nexus OS is a command-line operating environment designed to replace "Installation" with "Detonation." It treats code, workflows, and contexts as ephemeral artifacts that are hydrated on-demand and pruned immediately after use.

## Core Pillars

1.  **Sovereign Artifacts (`.nxs`)**: Encrypted, compressed "Context Seeds" that contain everything needed to run a specific task or environment.
2.  **Forge Recursive Engine**: The underlying orchestration layer that hydrates these artifacts into RAM and shreds them upon completion.
3.  **Pidgeon Mesh**: The transport layer for sending Artifacts between users, creating a secure "Context-First" messaging system.

## Quick Start

### Installation

```bash
pip install shortcut-cli
```

### The "Context Messaging" Workflow

**1. Pack a Context**
Turn a local folder (code, scripts, dockerfiles) into a Sovereign Artifact.
```bash
nexus pack ./my-project --output project_v1.nxs
```

**2. Send to a Peer**
Transmit the artifact securely.
```bash
nexus send project_v1.nxs user@nexus.mesh
```

**3. Receive & Detonate**
The recipient "opens" the message, which automatically hydrates the environment locally.
```bash
nexus unpack project_v1.nxs --detonate
```

## Command Reference

### `nexus` (Core)
- `enter`: Enter the interactive Sovereign Shell.
- `pack`: Create a `.nxs` artifact.
- `unpack`: Extract and run a `.nxs` artifact.
- `send`: Transmit an artifact.

### `forge` (Engine)
- `tui`: Launch the real-time visualizer.
- `recursive run`: Execute a logic-seed directly.
- `container run`: Legacy Docker compatibility.

### `vault` (Security)
- `login`: Authenticate with hardware-rooted keys.

## Architecture

Nexus OS sits on top of the **Forge Engine**.

```
[User] -> [Nexus Shell] -> [Artifact (.nxs)] -> [Pidgeon Transport]
                                      ↓
                                [Receiver]
                                      ↓
                            [Forge Detonation]
                                      ↓
                            [Ephemeral Runtime]
```

## Legacy Compatibility

Nexus OS includes bridges for:
- **Docker:** Ingest images into seeds.
- **Airflow:** Run existing DAGs recursively.
- **Scripts:** Manage local `.py` and `.ps1` automations.

---

**License:** MIT
**Status:** Active Development (v4.0.0)
