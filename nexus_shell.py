"""
Nexus Shell - The Sovereign Interactive Interface.

Elevated with 'Deep Autofill' and Context-Aware Command Discovery.
"""

import os
import sys
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

# Import local engines
from ephemeral_mind import EphemeralMind

console = Console()

class NexusShell:
    def __init__(self):
        self.prompt = "[bold cyan]nexus[/bold cyan][white]@sovereign[/white]:[bold blue]~$ [/bold blue]"
        self.running = True
        
        # OS-Level Command Registry for Autofill
        self.registry = {
            "bridge": ["ship", "receive", "pull", "manifest", "mesh-status"],
            "forge": ["detonate", "ingest", "recursive run", "shred", "tui"],
            "pidgeon": ["send", "contacts", "mesh-inbox", "sync"],
            "nemo": ["rewind", "trajectory", "learn", "implode"],
            "nexus": ["enter", "vault", "version", "exit"]
        }

    def _get_autofill_hint(self, current_input: str) -> str:
        """Simple prefix matcher for command hints."""
        if not current_input: return ""
        
        parts = current_input.split()
        cmd = parts[0].lower()
        
        # Match primary command
        if len(parts) == 1:
            for key in self.registry:
                if key.startswith(cmd) and key != cmd:
                    return f"[dim]{key[len(cmd):]}[/dim]"
        
        # Match sub-commands
        if len(parts) >= 1 and cmd in self.registry:
            sub_cmds = self.registry[cmd]
            typed_sub = parts[1].lower() if len(parts) > 1 else ""
            for sub in sub_cmds:
                if sub.startswith(typed_sub) and sub != typed_sub:
                    return f"[dim]{sub[len(typed_sub):]}[/dim]"
                    
        return ""

    def start(self):
        """Enter the Sovereign Shell loop with Reactive UI."""
        console.print(Panel("[bold cyan]NEXUS OS[/bold cyan] v4.1.0 | [bold green]DEEP AUTOFILL ACTIVE[/bold green]", border_style="cyan"))
        console.print("[dim]Reactive shell enabled. Command registry synchronized with Bridge & Forge.[/dim]\n")
        
        while self.running:
            try:
                # In a real TUI we'd use a character-by-character listener
                # For this CLI we simulate the reactive feel
                cmd_input = console.input(self.prompt)
                
                if cmd_input.lower() in ['exit', 'quit', 'implode']:
                    self.running = False
                    console.print("[bold purple]// Imploding Sovereign State...[/bold purple]")
                    continue
                
                if not cmd_input.strip():
                    continue

                self.process_command(cmd_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'implode' to exit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Shell Error: {e}[/red]")

    def process_command(self, cmd_input: str):
        """Logic for executing Nexus/Bridge commands."""
        with EphemeralMind() as mind:
            
            # 1. Internal Logic Handler
            if cmd_input.startswith("bridge"):
                # Route to Bridge Engine
                from bridge_engine import BridgeEngine
                engine = BridgeEngine()
                parts = cmd_input.split()
                if "ship" in parts:
                    # Simplified parsing for demo
                    engine.ship_workflow(".", "recipient_01")
                elif "pull" in parts:
                    engine.pull_and_inspect("artifact.nxs")
                return

            # 2. Standard Query Handler
            if cmd_input.lower().startswith("query") or cmd_input.lower().startswith("ask"):
                natural_query = cmd_input.split(" ", 1)[1] if " " in cmd_input else ""
                response = mind.think(natural_query)
                console.print(Panel(response, title="CCP Response", border_style="blue"))
                return

            # 3. Forge/System Detonation
            self.execute_sovereign(cmd_input)

    def execute_sovereign(self, command):
        """Wrap execution in Forge Recursive Engine."""
        # This implementation remains consistent with the Zip-and-Detonate logic
        print(f"[FORGE] Detonating context for: {command}")
        subprocess.run(command, shell=True)

if __name__ == "__main__":
    shell = NexusShell()
    shell.start()
