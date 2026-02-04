import os
import sys
import subprocess
import requests
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from artifact_sync import ArtifactSync, get_auth_token, save_auth_token
from keycard_manager import KeycardManager
from pidgeon import Pidgeon
from connect import Connect

# Shared Configuration
APP_NAME = "Shortcut CLI"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
QUARANTINE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "quarantine")
REPOS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "repos")
KEYCARDS_DIR = os.path.expanduser("~/.shortcut/keycards")
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"
RECENT_FILES_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')

console = Console()

@click.group()
def main():
    """Shortcut CLI: Container orchestration + Script management + Automation."""
    for d in [SCRIPTS_DIR, QUARANTINE_DIR, REPOS_DIR, KEYCARDS_DIR]:
        if not os.path.exists(d): os.makedirs(d)


# ─────────────────────────────────────────────────────────────
# PIDGEON GROUP (Email & Contacts)
# ─────────────────────────────────────────────────────────────

@main.group(name='pidgeon')
def pidgeon():
    """Email and contact management from the command line."""
    pass

@pidgeon.command(name='send')
@click.argument('to')
@click.option('--subject', '-s', required=True)
@click.option('--body', '-b', required=True)
def pidgeon_send(to, subject, body):
    """Send a Pidgeon (email)."""
    p = Pidgeon()
    p.send_pidgeon(to, subject, body)

@pidgeon.command(name='contacts')
def pidgeon_contacts():
    """List recent contacts."""
    p = Pidgeon()
    contacts = p.get_contacts()
    table = Table(title="Recent Contacts")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="green")
    for c in contacts:
        table.add_row(c['name'], c['email'])
    console.print(table)


# ─────────────────────────────────────────────────────────────
# CONNECT GROUP (Collaboration & Messaging)
# ─────────────────────────────────────────────────────────────

@main.group(name='connect')
def connect():
    """Collaborate with other Nexus users."""
    pass

@connect.command(name='peers')
def connect_peers():
    """Discover online peers."""
    c = Connect()
    peers = c.get_online_peers()
    table = Table(title="Online Nexus Users")
    table.add_column("User", style="bold cyan")
    table.add_column("Status", style="yellow")
    table.add_column("IP", style="dim")
    for p in peers:
        table.add_row(p['username'], p['status'], p['ip'])
    console.print(table)

@connect.command(name='msg')
@click.argument('user')
@click.argument('text')
def connect_msg(user, text):
    """Send a direct message."""
    c = Connect()
    c.send_message(user, text)


# ─────────────────────────────────────────────────────────────
# FORGE INTEGRATION (Container Orchestration + Workflows)
# ─────────────────────────────────────────────────────────────

try:
    from forge_integration import attach_forge_commands
    attach_forge_commands(main)
except ImportError:
    console.print("[yellow]Note: Forge integration not available[/yellow]")


# ─────────────────────────────────────────────────────────────
# VAULT GROUP (VaultZero Secret Management)
# ─────────────────────────────────────────────────────────────

@main.group(name='vault')
def vault():
    """Secure secret management (VaultZero)."""
    pass

@vault.command(name='login')
@click.argument('token')
def vault_login(token):
    """Save GitHub token to VaultZero."""
    save_auth_token(token)


# ─────────────────────────────────────────────────────────────
# SYNC GROUP (Omni-Sync Repository Orchestration)
# ─────────────────────────────────────────────────────────────

@main.group(name='sync')
def sync():
    """Sync repositories and auto-scaffold Forge workflows."""
    pass

@sync.command(name='repo')
@click.argument('repo_name')
def sync_repo(repo_name):
    """Clone/Update a repo and auto-generate Forge config."""
    token = get_auth_token()
    syncer = ArtifactSync(token=token)
    success = syncer.clone_and_sync(repo_name, REPOS_DIR)
    if success:
        console.print(f"[bold green]✓ Successfully synced {repo_name}[/bold green]")


# ─────────────────────────────────────────────────────────────
# SCRIPTS GROUP (Local Script Management)
# ─────────────────────────────────────────────────────────────

@main.group(name='scripts')
def scripts():
    """Manage local scripts and automations."""
    pass


@scripts.command(name='list')
def scripts_list():
    """List all local and quarantined scripts."""
    scripts_list_items = []
    if os.path.exists(SCRIPTS_DIR):
        for f in os.listdir(SCRIPTS_DIR):
            if f.endswith((".ps1", ".py")): scripts_list_items.append((f, "Verified"))
    if os.path.exists(QUARANTINE_DIR):
        for f in os.listdir(QUARANTINE_DIR):
            if f.endswith((".ps1", ".py")): scripts_list_items.append((f, "QUARANTINE"))
    
    table = Table(title="Local Scripts", border_style="blue")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Filename", style="white")
    table.add_column("Status", style="green")

    for i, (f, status) in enumerate(scripts_list_items):
        style = "bold red" if status == "QUARANTINE" else "dim"
        table.add_row(str(i+1), f, status, style=style)
    
    console.print(table)


@scripts.command(name='search')
@click.argument('query')
def scripts_search(query):
    """Search GitHub for automation scripts (QUARANTINE MODE)."""
    console.print(f"[cyan]Searching GitHub for: {query}...[/cyan]")
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
            console.print(f"[bold green]Saved to Quarantine.[/bold green] Use 'shortcut scripts run' to execute.")
            
    except Exception as e:
        console.print(f"[red]GitHub Search Error: {e}[/red]")


@scripts.command(name='run')
@click.argument('script_id', type=int)
def scripts_run(script_id):
    """Run a script by its ID from the list."""
    scripts_list_items = []
    for d in [SCRIPTS_DIR, QUARANTINE_DIR]:
        if os.path.exists(d):
            for f in os.listdir(d):
                if f.endswith((".ps1", ".py")): scripts_list_items.append(os.path.join(d, f))
    
    if 0 < script_id <= len(scripts_list_items):
        script_path = scripts_list_items[script_id - 1]
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


# ─────────────────────────────────────────────────────────────
# FEATURES GROUP (Additional Features & Administration)
# ─────────────────────────────────────────────────────────────

@main.group(name='features')
def features():
    """Additional features and administration."""
    pass


@features.command(name='help')
def features_help():
    """Show help and documentation."""
    console.print(Panel("""[bold cyan]Shortcut CLI - Help[/bold cyan]

[bold]Usage:[/bold]
  shortcut [COMMAND] [OPTIONS]

[bold]Command Groups:[/bold]
  forge              Container orchestration + workflows
  scripts            Local script management  
  features           Additional features & administration

[bold]Examples:[/bold]
  shortcut forge tui                    # Launch Forge dashboard
  shortcut forge container run IMAGE    # Run a container
  shortcut forge workflow run WF         # Execute workflow
  
  shortcut scripts list                 # List scripts
  shortcut scripts run 1                # Run script #1
  shortcut scripts search KEYWORD       # Search GitHub

[bold]For more info:[/bold]
  shortcut [GROUP] --help
""", border_style="cyan"))


if __name__ == "__main__":
    main()