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
            "forge": ["detonate", "ingest", "recursive", "shred", "tui", "reclaim"],
            "pidgeon": ["send", "contacts", "mesh-inbox"],
            "nexus": ["enter", "vault", "workspace", "lens", "exit"]
        }

    def scan_workspace(self, path: str = "."):
        """
        Scans the current directory for Sovereign Artifacts and Bridge Logistics.
        Utilizes the NX- Protocol to decipher file functions.
        """
        self.current_workspace = {
            "seeds": [],
            "contexts": [],
            "logistics": [],
            "mesh": [],
            "inertia": [],
            "path": os.path.abspath(path)
        }
        
        try:
            items = os.listdir(path)
            for item in items:
                if item.startswith("NX-"):
                    # Decipher the code: NX-[TYPE]-[ATTR]-[NAME]
                    parts = item.split("-")
                    if len(parts) >= 4:
                        type_code = parts[1]
                        human_name = "-".join(parts[3:])
                        
                        if type_code == "SED": self.current_workspace["seeds"].append(human_name)
                        elif type_code == "CTX": self.current_workspace["contexts"].append(human_name)
                        elif type_code == "LGC": self.current_workspace["logistics"].append(human_name)
                        elif type_code == "MSH": self.current_workspace["mesh"].append(human_name)
                elif not item.startswith(".") and item not in ["venv", "__pycache__", "quarantine", "Setup-Yukora.ps1", "test_volatile_mind.py"]:
                    self.current_workspace["inertia"].append(item)
        except Exception:
            pass
            
        return self.current_workspace

    def display_workspace_status(self):
        """Show a high-level summary of the discovered sovereign artifacts."""
        ws = self.current_workspace
        
        status = Text()
        if ws["contexts"]: status.append(f"● [BRIDGE] {len(ws['contexts'])} Linked ", style="bold purple")
        if ws["seeds"]: status.append(f"● [FORGE] {len(ws['seeds'])} Seeds ", style="bold blue")
        if ws["inertia"]: status.append(f"● [INERTIA] {len(ws['inertia'])} Legacy ", style="bold red")
        
        if status:
            console.print(status)

    def show_full_workspace(self):
        """Display the deciphered dictionary in a table."""
        ws = self.current_workspace
        table = Table(title=f"Deciphered Workspace: {os.path.basename(ws['path'])}", border_style="blue")
        table.add_column("Sovereign Role", style="dim")
        table.add_column("Coded Identifier", style="white")
        table.add_column("Status", style="green")
        
        for ctx in ws["contexts"]: table.add_row("Bridge Context", ctx, "ACTIVE")
        for sed in ws["seeds"]: table.add_row("Forge Seed", sed, "PRIMED")
        for lgc in ws["logistics"]: table.add_row("Logistics Config", lgc, "MAPPED")
        for msh in ws["mesh"]: table.add_row("Mesh Inbox", msh, "UNREAD")
        
        for ine in ws["inertia"]:
            table.add_row("Legacy Inertia", ine, "RECLAIMABLE", style="red")
            
        console.print(table)

    def show_lens(self):
        """The 'Ghost Overlay' simulation - Spatial Context Map."""
        ws = self.current_workspace
        console.print(Panel(
            Text.assemble(
                ("NEXUS LENS :: ", "bold cyan"),
                (os.path.basename(ws['path']), "white italic"),
                ("\n\n"),
                ("SOVEREIGN MESH OVERLAY\n", "dim"),
                ("----------------------\n", "dim"),
                (f"Local Context: {len(ws['contexts'])} Active\n"),
                (f"Primed Seeds: {len(ws['seeds'])}\n"),
                (f"Mesh Visibility: {len(ws['mesh'])} Nodes\n"),
                (f"Legacy Inertia: {len(ws['inertia'])} objects detected", "red")
            ),
            title="Spatial HUD",
            border_style="cyan"
        ))

    def start(self):
        """Enter the Sovereign Shell loop with Workspace Awareness."""
        console.print(Panel("[bold cyan]NEXUS OS[/bold cyan] v4.2.0 | [bold green]WORKSPACE AWARENESS ACTIVE[/bold green]", border_style="cyan"))
        console.print("[dim]Nexus is deciphering NX- Protocol codes in real-time.[/dim]\n")
        
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

                if cmd_input.lower() == "lens":
                    self.show_lens()
                    continue

                self.process_command(cmd_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'implode' to exit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Shell Error: {e}[/red]")

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

            if cmd_input.startswith("forge reclaim"):
                from forge.recursive.reclaimer import InertiaReclaimer
                reclaimer = InertiaReclaimer(".")
                reclaimer.scan()
                reclaimer.report()
                return

            if cmd_input.lower().startswith("query") or cmd_input.lower().startswith("ask"):
                natural_query = cmd_input.split(" ", 1)[1] if " " in cmd_input else ""
                response = mind.think(natural_query)
                console.print(Panel(response, title="CCP Response", border_style="blue"))
                return

            self.execute_sovereign(cmd_input)

    def execute_sovereign(self, command):
        """Wrap execution in Forge Recursive Engine."""
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
