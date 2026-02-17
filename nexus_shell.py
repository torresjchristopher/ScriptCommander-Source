"""
Nexus Shell - The Sovereign Interactive Interface.

Elevated with 'Workspace Dictionary' and 'Deep Autofill'.
Nexus is now directory-aware, mapping Bridge and Forge contexts automatically.
"""

import os
import sys
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Import local engines
from ephemeral_mind import EphemeralMind

console = Console()

class NexusShell:
    def __init__(self):
        self.prompt = "[bold cyan]nexus[/bold cyan][white]@sovereign[/white]:[bold blue]~$ [/bold blue]"
        self.running = True
        self.current_workspace = {} # The traversable dictionary
        
        # OS-Level Command Registry for Autofill
        self.registry = {
            "bridge": ["ship", "receive", "pull", "manifest", "sync", "follow"],
            "forge": ["detonate", "ingest", "recursive", "shred", "tui"],
            "pidgeon": ["send", "contacts", "mesh-inbox"],
            "nexus": ["enter", "vault", "workspace", "exit"]
        }

    def scan_workspace(self, path: str = "."):
        """
        Scans the current directory for Sovereign Artifacts and Bridge Logistics.
        Updates the traversable dictionary.
        """
        self.current_workspace = {
            "seeds": [],
            "logistics": None,
            "path": os.path.abspath(path)
        }
        
        try:
            files = os.listdir(path)
            for f in files:
                if f.endswith(".nxs"):
                    self.current_workspace["seeds"].append(f)
                if f == "forge.yml":
                    self.current_workspace["logistics"] = "forge_native"
                if f == "docker-compose.yml":
                    self.current_workspace["logistics"] = "bridge_legacy_compose"
        except Exception:
            pass
            
        return self.current_workspace

    def display_workspace_status(self):
        """Show a high-level summary of the discovered sovereign artifacts."""
        ws = self.current_workspace
        if not ws.get("seeds") and not ws.get("logistics"):
            return

        status = Text()
        if ws["logistics"]:
            status.append(f"[BRIDGE] Context: {ws['logistics']} ", style="bold purple")
        if ws["seeds"]:
            status.append(f"[FORGE] Seeds: {len(ws['seeds'])} available", style="bold blue")
        
        if status:
            console.print(status)

    def start(self):
        """Enter the Sovereign Shell loop with Workspace Awareness."""
        console.print(Panel("[bold cyan]NEXUS OS[/bold cyan] v4.2.0 | [bold green]WORKSPACE AWARENESS ACTIVE[/bold green]", border_style="cyan"))
        console.print("[dim]Nexus is monitoring local paths for Bridge Logistics & Forge Seeds.[/dim]\n")
        
        while self.running:
            try:
                # 1. Update Workspace Dictionary
                self.scan_workspace()
                self.display_workspace_status()
                
                cmd_input = console.input(self.prompt)
                
                if cmd_input.lower() in ['exit', 'quit', 'implode']:
                    self.running = False
                    continue
                
                if not cmd_input.strip():
                    continue

                if cmd_input.lower() == "workspace":
                    self.show_full_workspace()
                    continue

                self.process_command(cmd_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'implode' to exit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Shell Error: {e}[/red]")

    def show_full_workspace(self):
        """Display the traversable dictionary in a table."""
        ws = self.current_workspace
        table = Table(title=f"Workspace Dictionary: {os.path.basename(ws['path'])}", border_style="blue")
        table.add_column("Type", style="dim")
        table.add_column("Artifact / Config", style="white")
        
        if ws["logistics"]:
            table.add_row("Bridge Logistics", ws["logistics"])
        for seed in ws["seeds"]:
            table.add_row("Forge Seed", seed)
            
        if not ws["logistics"] and not ws["seeds"]:
            table.add_row("Status", "No Sovereign artifacts detected.")
            
        console.print(table)

    def process_command(self, cmd_input: str):
        """Logic for executing Nexus/Bridge commands."""
        with EphemeralMind() as mind:
            if cmd_input.startswith("bridge"):
                from bridge_engine import BridgeEngine
                engine = BridgeEngine()
                parts = cmd_input.split()
                if "ship" in parts:
                    engine.ship_workflow(".", "recipient_01")
                elif "pull" in parts:
                    engine.pull_and_inspect("artifact.nxs")
                return

            if cmd_input.lower().startswith("query") or cmd_input.lower().startswith("ask"):
                natural_query = cmd_input.split(" ", 1)[1] if " " in cmd_input else ""
                response = mind.think(natural_query)
                console.print(Panel(response, title="CCP Response", border_style="blue"))
                return

            self.execute_sovereign(cmd_input)

    def execute_sovereign(self, command):
        """Wrap execution in Forge Recursive Engine."""
        # Simple change directory handling for workspace awareness
        if command.startswith("cd "):
            path = command[3:].strip()
            try:
                os.chdir(path)
                return
            except Exception as e:
                console.print(f"[red]Path Error: {e}[/red]")
                return

        print(f"[FORGE] Detonating context for: {command}")
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    shell = NexusShell()
    shell.start()
