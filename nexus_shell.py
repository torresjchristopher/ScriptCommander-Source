"""
Nexus Shell - The Sovereign Interactive Interface.

Wraps every command in a Forge Recursive Detonation.
"""

import os
import sys
import subprocess
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

# Try to find Forge
FORGE_PATH = "C:/Users/serro/Yukora/forge"
if os.path.exists(FORGE_PATH):
    sys.path.append(FORGE_PATH)

# Try to find Nemo
NEMO_PATH = "C:/Users/serro/Yukora/nemo"
if os.path.exists(NEMO_PATH):
    sys.path.append(NEMO_PATH)

try:
    from forge.recursive.engine import RecursiveEngine
    FORGE_CORE_AVAILABLE = True
except ImportError:
    FORGE_CORE_AVAILABLE = False

try:
    from nemo.core.nemo_code import NemoCodeStack
    NEMO_AVAILABLE = True
except ImportError:
    NEMO_AVAILABLE = False

console = Console()

class NexusShell:
    """
    An interactive shell that enforces Zero-Inertia for every command.
    """
    
    def __init__(self):
        self.prompt = "[bold cyan]nexus[/bold cyan][white]@sovereign[/white]:[bold blue]~$ [/bold blue]"
        self.running = True
        self.nemo = NemoCodeStack() if NEMO_AVAILABLE else None

    def start(self):
        """Enter the Sovereign Shell loop."""
        console.print(Panel("[bold cyan]NEXUS OS[/bold cyan] v4.0.0 | [bold green]SOVEREIGN STATE ACTIVE[/bold green]", border_style="cyan"))
        
        status = []
        if FORGE_CORE_AVAILABLE: status.append("[green]Forge Engine: ONLINE[/green]")
        else: status.append("[red]Forge Engine: OFFLINE[/red]")
        
        if NEMO_AVAILABLE: status.append("[green]Nemo Telemetry: ACTIVE[/green]")
        else: status.append("[red]Nemo Telemetry: OFFLINE[/red]")
        
        console.print(" | ".join(status))
        console.print("[dim]Every command is wrapped in a Forge Detonation loop.[/dim]\n")
        
        while self.running:
            try:
                cmd_input = console.input(self.prompt)
                
                if cmd_input.lower() in ['exit', 'quit', 'implode']:
                    self.running = False
                    console.print("[bold purple]// Imploding Sovereign State...[/bold purple]")
                    continue
                
                if cmd_input.lower() == 'rewind':
                    if self.nemo:
                        console.print("[bold yellow]⚠ Initiating Temporal Scrub...[/bold yellow]")
                        self.nemo.scrub()
                    else:
                        console.print("[red]Nemo module not found.[/red]")
                    continue

                if not cmd_input.strip():
                    continue
                
                self.execute_sovereign(cmd_input)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'implode' to exit.[/yellow]")
            except Exception as e:
                console.print(f"[red]Shell Error: {e}[/red]")

    def execute_sovereign(self, command):
        """Execute a command within a recursive detonation context."""
        
        # 1. Record to Nemo Stack (if active)
        if self.nemo:
            # We treat every shell command as a 'detonate' action in the context of Nexus
            self.nemo.push("detonate", command)

        # 2. Execute via Forge
        if FORGE_CORE_AVAILABLE:
            # Wrap the command in a RecursiveEngine detonation
            with RecursiveEngine() as engine:
                console.print(f"[dim][DETONATE] Command: {command}[/dim]")
                
                # Split command for subprocess
                parts = command.split()
                try:
                    # Run the command logic
                    subprocess.run(parts, shell=True)
                except Exception as e:
                    console.print(f"[red]Execution Error: {e}[/red]")
                
                # Engine automatically implodes here
        else:
            # Fallback to standard execution if Forge not found
            subprocess.run(command, shell=True)
