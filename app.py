import os
import sys
import subprocess
import requests
import msvcrt
import shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich import box
from rich.text import Text
from datetime import datetime

# Configuration
APP_NAME = "Shortcut CLI"
VERSION = "3.1.0"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
QUARANTINE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "quarantine")
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"
RECENT_FILES_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')

console = Console()

class ShortcutTUI:
    def __init__(self):
        self.menu_options = ["Local Scripts", "Marketplace", "Quick Explorer", "Recent Files", "Exit"]
        self.current_index = 0
        self.state = "MENU" # MENU, SCRIPTS, MARKET, RECENT, EXPLORER
        self.items = []
        self.sub_index = 0
        self.current_path = os.path.expanduser("~") # For Explorer
        self.running = True

    def get_local_scripts(self):
        for d in [SCRIPTS_DIR, QUARANTINE_DIR]:
            if not os.path.exists(d): os.makedirs(d)
        
        scripts = []
        # Add Verified Scripts
        if os.path.exists(SCRIPTS_DIR):
            for f in os.listdir(SCRIPTS_DIR):
                if f.endswith(".ps1") or f.endswith(".py"):
                    scripts.append({"name": f, "path": os.path.join(SCRIPTS_DIR, f), "status": "Verified"})
        
        # Add Quarantined Scripts
        if os.path.exists(QUARANTINE_DIR):
            for f in os.listdir(QUARANTINE_DIR):
                if f.endswith(".ps1") or f.endswith(".py"):
                    scripts.append({"name": f, "path": os.path.join(QUARANTINE_DIR, f), "status": "QUARANTINE"})
        return scripts

    def get_marketplace(self):
        try:
            response = requests.get(MARKETPLACE_URL, timeout=5)
            return response.json()
        except:
            return []

    def get_recent_files(self):
        if not os.path.exists(RECENT_FILES_PATH):
            return []
        files = []
        try:
            items = os.listdir(RECENT_FILES_PATH)
            full_paths = [os.path.join(RECENT_FILES_PATH, i) for i in items if i.endswith(".lnk")]
            full_paths.sort(key=os.path.getmtime, reverse=True)
            for path in full_paths[:15]:
                name = os.path.basename(path).replace(".lnk", "")
                files.append({"name": name, "path": path})
        except:
            pass
        return files

    def get_explorer_items(self):
        try:
            items = []
            # Add ".." to go back
            items.append({"name": ".. [Go Back]", "path": os.path.dirname(self.current_path), "type": "dir"})
            with os.scandir(self.current_path) as it:
                for entry in it:
                    if not entry.name.startswith('.'):
                        t = "dir" if entry.is_dir() else "file"
                        items.append({"name": entry.name, "path": entry.path, "type": t})
            return sorted(items, key=lambda x: (x['type'] != 'dir', x['name'].lower()))
        except:
            return [{"name": "Permission Denied", "path": self.current_path, "type": "error"}]

    def draw_menu(self):
        table = Table(box=box.ROUNDED, show_header=False, expand=True, border_style="blue")
        for i, option in enumerate(self.menu_options):
            style = "bold white on blue" if i == self.current_index else "white"
            prefix = "> " if i == self.current_index else "  "
            table.add_row(Text(f"{prefix}{option}", style=style))
        
        return Panel(table, title=f"[bold cyan]{APP_NAME}[/bold cyan] v{VERSION}", subtitle="[dim]Arrows to navigate, Enter to select[/dim]")

    def draw_list(self, title, items, index, is_market=False, is_explorer=False):
        table = Table(box=box.ROUNDED, expand=True, border_style="green")
        table.add_column("Selection", justify="center", width=4)
        table.add_column("Name", style="bold")
        
        if is_market: table.add_column("Description")
        if not is_market and not is_explorer: table.add_column("Status")

        for i, item in enumerate(items):
            style = "bold white on green" if i == index else ""
            prefix = ">>" if i == index else "  "
            
            if is_market:
                table.add_row(prefix, item["name"], item.get("description", ""), style=style)
            elif is_explorer:
                icon = "📁" if item['type'] == 'dir' else "📄"
                table.add_row(prefix, f"{icon} {item['name']}", style=style)
            elif isinstance(item, dict): # Recent or Local
                status = item.get("status", "")
                s_style = "bold red" if status == "QUARANTINE" else "dim"
                table.add_row(prefix, item["name"], Text(status, style=s_style), style=style)
            else:
                table.add_row(prefix, str(item), "", style=style)

        sub = "[dim]Enter: Action | 'q': Back | Arrows: Flip[/dim]"
        if is_explorer: sub = f"[bold cyan]{self.current_path}[/bold cyan] | {sub}"
        return Panel(table, title=f"[bold green]{title}[/bold green]", subtitle=sub)

    def run_script(self, item):
        script_path = item['path']
        is_quarantine = item.get('status') == "QUARANTINE"
        
        console.clear()
        if is_quarantine:
            console.print(Panel("[bold red]SECURITY WARNING[/bold red]\nThis script is in QUARANTINE. It has not been verified.", border_style="red"))
            console.print("[yellow]Potentially dangerous commands check...[/yellow]")
            dangerous = ["rm ", "format ", "net user", "del ", "Invoke-WebRequest", "wget"]
            found = []
            try:
                with open(script_path, 'r', errors='ignore') as f:
                    content = f.read().lower()
                    for d in dangerous:
                        if d in content: found.append(d)
            except: pass
            
            if found:
                console.print(f"[bold red]DANGER:[/bold red] Found potential risk keywords: {', '.join(found)}")
            
            if not console.input("\nType 'run' to proceed anyway: ").lower() == 'run':
                return

        console.print(Panel(f"Executing: [bold yellow]{item['name']}[/bold yellow]\n[dim]Capturing output...[/dim]", border_style="yellow"))
        
        if script_path.endswith(".ps1"):
            command = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
        else:
            command = [sys.executable, script_path]
        
        try:
            # Run and capture output
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.stdout:
                console.print("\n[bold white]Output:[/bold white]")
                console.print(result.stdout)
            
            if result.returncode == 0:
                console.print("\n[bold green]✓ Execution Successful[/bold green]")
            else:
                console.print(f"\n[bold red]✕ Failed (Exit Code: {result.returncode})[/bold red]")
                if result.stderr:
                    console.print(f"[red]{result.stderr}[/red]")
        except Exception as e:
            console.print(f"[red]Execution Error: {e}[/red]")
        
        console.input("\n[dim]Press Enter to return to Shortcut...[/dim]")

    def download_script(self, item, is_global=False):
        console.clear()
        dest = QUARANTINE_DIR if is_global else SCRIPTS_DIR
        console.print(f"Downloading [bold cyan]{item['name']}[/bold cyan] to {os.path.basename(dest)}...")
        target_path = os.path.join(dest, f"{item['id']}.ps1" if not item['name'].endswith(('.ps1', '.py')) else item['name'])
        try:
            response = requests.get(item['url'], timeout=10)
            response.raise_for_status()
            with open(target_path, "wb") as f:
                f.write(response.content)
            console.print("[bold green]Successfully Downloaded![/bold green]")
        except Exception as e:
            console.print(f"[red]Failed: {e}[/red]")
        console.input("\nPress Enter to continue...")

    def main_loop(self):
        with Live(refresh_per_second=10, screen=True) as live:
            while self.running:
                if self.state == "MENU":
                    live.update(self.draw_menu())
                elif self.state == "SCRIPTS":
                    live.update(self.draw_list("My Scripts", self.items, self.sub_index))
                elif self.state == "MARKET":
                    live.update(self.draw_list("Verified Marketplace", self.items, self.sub_index, True))
                elif self.state == "RECENT":
                    live.update(self.draw_list("Quick Open Files", self.items, self.sub_index))
                elif self.state == "EXPLORER":
                    live.update(self.draw_list("Quick Explorer", self.items, self.sub_index, is_explorer=True))

                if msvcrt.kbhit():
                    key = ord(msvcrt.getch())
                    if key == 224: # Arrow keys
                        key = ord(msvcrt.getch())
                        if key == 72: # Up
                            if self.state == "MENU": self.current_index = (self.current_index - 1) % len(self.menu_options)
                            else: self.sub_index = (self.sub_index - 1) % len(self.items) if self.items else 0
                        elif key == 80: # Down
                            if self.state == "MENU": self.current_index = (self.current_index + 1) % len(self.menu_options)
                            else: self.sub_index = (self.sub_index + 1) % len(self.items) if self.items else 0
                    
                    elif key == 13: # Enter
                        if self.state == "MENU":
                            choice = self.menu_options[self.current_index]
                            if choice == "Local Scripts":
                                self.state = "SCRIPTS"; self.items = self.get_local_scripts(); self.sub_index = 0
                            elif choice == "Quick Explorer":
                                self.state = "EXPLORER"; self.items = self.get_explorer_items(); self.sub_index = 0
                            elif choice == "Marketplace":
                                self.state = "MARKET"; self.items = self.get_marketplace(); self.sub_index = 0
                            elif choice == "Recent Files":
                                self.state = "RECENT"; self.items = self.get_recent_files(); self.sub_index = 0
                            elif choice == "Exit": self.running = False
                        
                        elif self.state == "SCRIPTS":
                            if self.items:
                                live.stop(); self.run_script(self.items[self.sub_index]); live.start()
                                self.items = self.get_local_scripts()
                        
                        elif self.state == "EXPLORER":
                            if self.items:
                                item = self.items[self.sub_index]
                                if item['type'] == 'dir':
                                    self.current_path = item['path']
                                    self.items = self.get_explorer_items()
                                    self.sub_index = 0
                                else:
                                    os.startfile(item['path'])
                                    self.running = False # Fast exit after opening file

                        elif self.state == "MARKET":
                            if self.items:
                                live.stop(); self.download_script(self.items[self.sub_index]); live.start()

                        elif self.state == "RECENT":
                            if self.items:
                                os.startfile(self.items[self.sub_index]['path'])
                                self.running = False

                    elif key == ord('q') or key == 27: # Back
                        if self.state == "MENU": self.running = False
                        else: self.state = "MENU"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI Mode
        try:
            from cli import main as cli_main
            cli_main()
        except ImportError:
            print("[Error] cli.py not found.")
    else:
        # TUI Mode
        tui = ShortcutTUI()
        tui.main_loop()