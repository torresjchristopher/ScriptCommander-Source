"""
Nexus Shell - The Sovereign Interactive Interface.

Wraps every command in a Forge Recursive Detonation.
Utilizes the Ephemeral Mind for on-demand intelligence.
"""

import os
import sys
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

# Try to find Forge for the core wrapper
FORGE_PATH = "C:/Users/serro/Yukora/forge"
if os.path.exists(FORGE_PATH):
    sys.path.append(FORGE_PATH)

try:
    from forge.recursive.engine import RecursiveEngine
    FORGE_CORE_AVAILABLE = True
except ImportError:
    FORGE_CORE_AVAILABLE = False

from ephemeral_mind import EphemeralMind

console = Console()

class NexusShell:
    """
    An interactive shell that enforces Zero-Inertia for every command.
    """
    
    def __init__(self):
        self.prompt = "[bold cyan]nexus[/bold cyan][white]@sovereign[/white]:[bold blue]~$ [/bold blue]"
        self.running = True

    def start(self):
        """Enter the Sovereign Shell loop."""
        console.print(Panel("[bold cyan]NEXUS OS[/bold cyan] v4.0.0 | [bold green]SOVEREIGN STATE ACTIVE[/bold green]", border_style="cyan"))
        
        status = []
        if FORGE_CORE_AVAILABLE: status.append("[green]Forge Engine: ONLINE[/green]")
        else: status.append("[red]Forge Engine: OFFLINE[/red]")
        status.append("[green]Volatile Mind: READY[/green]")
        
        console.print(" | ".join(status))
        console.print("[dim]The AI is currently DORMANT. Every command triggers a momentary wake-event.[/dim]\n")
        
        while self.running:
            try:
                cmd_input = console.input(self.prompt)
                
                if cmd_input.lower() in ['exit', 'quit', 'implode']:
                    self.running = False
                    console.print("[bold purple]// Imploding Sovereign State...[/bold purple]")
                    continue
                
                if not cmd_input.strip():
                    continue

                # Handle the interaction through the Ephemeral Mind
                with EphemeralMind() as mind:
                    
                    if cmd_input.lower() == 'rewind':
                        console.print("[bold yellow]⚠ Initiating Temporal Scrub...[/bold yellow]")
                        mind.nemo.scrub()
                        continue

                    # Compounded Context Protocol Handler
                    if cmd_input.lower().startswith("query") or cmd_input.lower().startswith("ask"):
                        natural_query = cmd_input.split(" ", 1)[1] if " " in cmd_input else ""
                        response = mind.think(natural_query)
                        console.print(Panel(response, title="Compounded Context Protocol", border_style="blue"))
                        continue

                    # Standard Command Execution
                    mind.observe(cmd_input) # Record the action
                    self.execute_sovereign(cmd_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'implode' to exit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Shell Error: {e}[/red]")

    def execute_sovereign(self, command):
        """Execute a command within a recursive detonation context."""
        if FORGE_CORE_AVAILABLE:
            with RecursiveEngine() as engine:
                console.print(f"[dim][DETONATE] Command: {command}[/dim]")
                parts = command.split()
                try:
                    subprocess.run(parts, shell=True)
                except Exception as e:
                    console.print(f"[red]Execution Error: {e}[/red]")
        else:
            subprocess.run(command, shell=True)
