import os
import sys
import subprocess
import requests
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Shared Configuration (Mirrors app.py)
APP_NAME = "Shortcut CLI"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"
RECENT_FILES_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')

console = Console()

@click.group()
def main():
    """Shortcut CLI: The high-speed companion to the Shortcut TUI."""
    pass

@main.command()
def list():
    """List all local scripts."""
    if not os.path.exists(SCRIPTS_DIR):
        console.print("[yellow]No scripts directory found.[/yellow]")
        return
    
    files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".ps1") or f.endswith(".py")]
    table = Table(title="Local Scripts", border_style="blue")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Filename", style="white")
    table.add_column("Type", style="green")

    for i, f in enumerate(files):
        ext = "PowerShell" if f.endswith(".ps1") else "Python"
        table.add_row(str(i+1), f, ext)
    
    console.print(table)

@main.command()
@click.argument('script_id', type=int)
def run(script_id):
    """Run a script by its ID from the list."""
    if not os.path.exists(SCRIPTS_DIR): return
    files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".ps1") or f.endswith(".py")]
    
    if 0 < script_id <= len(files):
        filename = files[script_id - 1]
        script_path = os.path.join(SCRIPTS_DIR, filename)
        console.print(Panel(f"Executing: [bold yellow]{filename}[/bold yellow]", border_style="yellow"))
        
        if filename.endswith(".ps1"):
            ps_command = f"Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\" ' -Verb RunAs"
            command = ["powershell", "-Command", ps_command]
        else:
            command = [sys.executable, script_path]
        
        subprocess.run(command)
    else:
        console.print("[red]Invalid Script ID.[/red]")

@main.command()
def market():
    """Show the verified marketplace."""
    console.print("[cyan]Fetching Marketplace...[/cyan]")
    try:
        response = requests.get(MARKETPLACE_URL, timeout=5)
        items = response.json()
        table = Table(title="Verified Marketplace", border_style="green")
        table.add_column("Name", style="bold cyan")
        table.add_column("Description", style="white")
        table.add_column("Author", style="dim")

        for item in items:
            table.add_row(item["name"], item.get("description", ""), item.get("author", "Unknown"))
        
        console.print(table)
    except:
        console.print("[red]Could not connect to marketplace.[/red]")

@main.command()
def recent():
    """List and open recently used files."""
    if not os.path.exists(RECENT_FILES_PATH): return
    
    items = os.listdir(RECENT_FILES_PATH)
    full_paths = [os.path.join(RECENT_FILES_PATH, i) for i in items if i.endswith(".lnk")]
    full_paths.sort(key=os.path.getmtime, reverse=True)
    
    table = Table(title="Recent Files", border_style="magenta")
    table.add_column("ID", justify="right", style="magenta")
    table.add_column("File Name", style="white")

    for i, path in enumerate(full_paths[:10]):
        name = os.path.basename(path).replace(".lnk", "")
        table.add_row(str(i+1), name)
    
    console.print(table)
    console.print("\n[dim]To open a file, use the TUI (app.py) for interactive selection.[/dim]")

if __name__ == "__main__":
    main()
