import os
import sys
import subprocess
import requests
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Shared Configuration
APP_NAME = "Shortcut CLI"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
QUARANTINE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "quarantine")
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"
RECENT_FILES_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')

console = Console()

@click.group()
def main():
    """Shortcut CLI: The high-speed companion to the Shortcut TUI."""
    for d in [SCRIPTS_DIR, QUARANTINE_DIR]:
        if not os.path.exists(d): os.makedirs(d)

@main.command()
def list():
    """List all local and quarantined scripts."""
    scripts = []
    if os.path.exists(SCRIPTS_DIR):
        for f in os.listdir(SCRIPTS_DIR):
            if f.endswith((".ps1", ".py")): scripts.append((f, "Verified"))
    if os.path.exists(QUARANTINE_DIR):
        for f in os.listdir(QUARANTINE_DIR):
            if f.endswith((".ps1", ".py")): scripts.append((f, "QUARANTINE"))
    
    table = Table(title="Local Scripts", border_style="blue")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Filename", style="white")
    table.add_column("Status", style="green")

    for i, (f, status) in enumerate(scripts):
        style = "bold red" if status == "QUARANTINE" else "dim"
        table.add_row(str(i+1), f, status, style=style)
    
    console.print(table)

@main.command()
@click.argument('query')
def search(query):
    """Search GitHub for automation scripts (QUARANTINE MODE)."""
    console.print(f"[cyan]Searching GitHub for: {query}...[/cyan]")
    # Using GitHub search API for code/files
    # Note: We filter for .ps1 and .py
    url = f"https://api.github.com/search/code?q={query}+extension:ps1+extension:py"
    try:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        items = response.json().get('items', [])
        
        if not items:
            console.print("[yellow]No scripts found on GitHub.[/yellow]")
            return

        table = Table(title=f"Global Search Results: {query}", border_style="red")
        table.add_column("ID", justify="right")
        table.add_column("Script Name")
        table.add_column("Repository")

        results = []
        for i, item in enumerate(items[:10]):
            repo = item['repository']['full_name']
            name = item['name']
            download_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
            results.append({"name": name, "url": download_url})
            table.add_row(str(i+1), name, repo)
        
        console.print(table)
        console.print("\n[bold red]WARNING:[/bold red] These scripts are from unverified sources.")
        choice = console.input("Enter ID to download to QUARANTINE (or Enter to cancel): ")
        
        if choice.isdigit() and 0 < int(choice) <= len(results):
            selected = results[int(choice)-1]
            target = os.path.join(QUARANTINE_DIR, selected['name'])
            console.print(f"Downloading {selected['name']}...")
            res = requests.get(selected['url'])
            with open(target, 'wb') as f:
                f.write(res.content)
            console.print(f"[bold green]Saved to Quarantine.[/bold green] Use 'shortcut run' or the TUI to execute.")
            
    except Exception as e:
        console.print(f"[red]GitHub Search Error: {e}[/red]")

@main.command()
@click.argument('script_id', type=int)
def run(script_id):
    """Run a script by its ID from the list."""
    scripts = []
    for d in [SCRIPTS_DIR, QUARANTINE_DIR]:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.endswith((".ps1", ".py")): scripts.append(os.path.join(d, f))
    
    if 0 < script_id <= len(scripts):
        script_path = scripts[script_id - 1]
        filename = os.path.basename(script_path)
        
        if "quarantine" in script_path.lower():
            console.print(Panel("[bold red]QUARANTINE EXECUTION[/bold red]\nThis script is unverified.", border_style="red"))
            if not console.input("Type 'run' to proceed: ").lower() == 'run': return

        console.print(Panel(f"Executing: [bold yellow]{filename}[/bold yellow]", border_style="yellow"))
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path] if script_path.endswith(".ps1") else [sys.executable, script_path]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout: console.print(result.stdout)
        if result.returncode != 0: console.print(f"[bold red]Error (Exit {result.returncode}):[/bold red]\n{result.stderr}")
        else: console.print("[bold green]✓ Success[/bold green]")
    else:
        console.print("[red]Invalid Script ID.[/red]")

if __name__ == "__main__":
    main()