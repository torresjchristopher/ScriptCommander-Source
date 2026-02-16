"""
BRIDGE Logistics Engine - Refined Sovereign Sequence.

The sequence:
1. START: Nexus, Bridge
2. PRIME: Forge, Pidgeon (Native File Bridge)
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from artifact_packager import SovereignArtifact
from pidgeon import Pidgeon

console = Console()

class BridgeEngine:
    def __init__(self):
        # Nexus and Bridge are already 'Started' by the CLI entry point
        self.packager = SovereignArtifact()
        self.messenger = Pidgeon()

    def ship_workflow(self, source_path: str, recipient: str):
        """
        The 'Ship' command initiates the refined priming sequence.
        """
        console.print(Panel(f"[bold blue]BRIDGE SHIPMENT[/bold blue] :: Initiating Native Context Transfer", border_style="blue"))
        
        # 1. PRIME FORGE: Prepare the Compactor
        console.print("[dim][PRIME] Forge Engine: Initializing Ingestion Compactor...[/dim]")
        try:
            artifact_name = f"{os.path.basename(source_path)}.nxs"
            # Forge Ingests the path into a clean .nxs seed
            nxs_path = self.packager.pack(source_path, artifact_name)
            console.print(f"[green]✓ Forge: Context Ingested into {artifact_name}[/green]")
        except Exception as e:
            console.print(f"[bold red]Priming Error (Forge): {e}[/bold red]")
            return False

        # 2. PRIME PIDGEON: Open the Native Context Bridge
        console.print(f"[dim][PRIME] Pidgeon Mesh: Opening Native Bridge to {recipient}...[/dim]")
        try:
            # Pidgeon doesn't 'send an attachment' - it 'references' or 'copies' natively
            # This negates web-based transfers for local work
            success = self.messenger.transfer_artifact(nxs_path, recipient)
            
            if success:
                message = f"REFERENCE_PIDGEON_CONTEXT::{artifact_name}"
                self.messenger.send_pidgeon(recipient, "NATIVE_CONTEXT_PULL", message)
                console.print(f"[bold green]BRIDGE[/bold blue] :: Context is now NATIVELY AVAILABLE to {recipient}")
                console.print("[dim]Recipient can now pull, inspect, or detonate the reference.[/dim]")
        except Exception as e:
            console.print(f"[bold red]Priming Error (Pidgeon): {e}[/bold red]")
            return False

        return True

    def pull_and_inspect(self, artifact_ref: str):
        """
        Action on the receiving end: Pull the referenced context natively.
        """
        console.print(f"[bold blue]BRIDGE PULL[/bold blue] :: Fetching native reference: {artifact_ref}")
        
        # Simulation: Pidgeon 'pulls' the referenced file from the mesh inbox
        mesh_dir = os.path.expanduser("~/.shortcut/mesh_inbox")
        artifact_path = os.path.join(mesh_dir, artifact_ref)
        
        if os.path.exists(artifact_path):
            console.print(f"[green]✓ Context Pulled.[/green] Proceeding to Detonation...")
            # Detonate using Forge
            from forge_integration import launch_forge_command
            launch_forge_command(['recursive', 'run', '--seed', artifact_path])
        else:
            console.print(f"[red]Error: Native reference {artifact_ref} not found in mesh.[/red]")
