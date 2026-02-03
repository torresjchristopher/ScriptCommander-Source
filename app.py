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
from rich.syntax import Syntax
from datetime import datetime

# Configuration
APP_NAME = "Shortcut CLI"
VERSION = "3.2.0"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
QUARANTINE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "quarantine")
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"
RECENT_FILES_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')

console = Console()

class ShortcutTUI:
    def __init__(self):
        # PROMOTED MENU: Putting the magic front and center
        self.menu_options = [
            "🚀 Workspaces (Morning Routine)", 
            "📧 Comms Hub (Email/Slack)", 
            "📂 Local Scripts", 
            "🌐 Marketplace", 
            "🔍 GitHub Search", 
            "📁 Quick Explorer", 
            "🕒 Recent Files", 
            "Exit"
        ]
        self.current_index = 0
        self.state = "MENU" # MENU, SCRIPTS, MARKET, RECENT, EXPLORER, SEARCH
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

    def search_github(self, query):
        url = f"https://api.github.com/search/code?q={query}+extension:ps1+extension:py"
        try:
            headers = {'Accept': 'application/vnd.github.v3+json'}
            response = requests.get(url, headers=headers, timeout=10)
            items = response.json().get('items', [])
            results = []
            for item in items[:15]:
                repo = item['repository']['full_name']
                name = item['name']
                download_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                results.append({"name": f"{name} ({repo})", "url": download_url, "id": name, "status": "Global"})
            return results
        except:
            return []

    def get_recent_files(self):
        if not os.path.exists(RECENT_FILES_PATH): return []
        files = []
        try:
            items = os.listdir(RECENT_FILES_PATH)
            full_paths = [os.path.join(RECENT_FILES_PATH, i) for i in items if i.endswith(".lnk")]
            full_paths.sort(key=os.path.getmtime, reverse=True)
            for path in full_paths[:15]:
                name = os.path.basename(path).replace(".lnk", "")
                files.append({"name": name, "path": path})
        except: pass
        return files

    def get_explorer_items(self):
        try:
            items = []
            items.append({"name": ".. [Go Back]", "path": os.path.dirname(self.current_path), "type": "dir"})
            with os.scandir(self.current_path) as it:
                for entry in it:
                    if not entry.name.startswith('.'):
                        t = "dir" if entry.is_dir() else "file"
                        items.append({"name": entry.name, "path": entry.path, "type": t})
            return sorted(items, key=lambda x: (x['type'] != 'dir', x['name'].lower()))
        except: return [{"name": "Permission Denied", "path": self.current_path, "type": "error"}]

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
            elif isinstance(item, dict):
                status = item.get("status", "")
                s_style = "bold red" if status == "QUARANTINE" else "dim"
                table.add_row(prefix, item["name"], Text(status, style=s_style), style=style)
            else:
                table.add_row(prefix, str(item), "", style=style)

        sub = "[dim]Enter: Action | 'v': View Code | 'q': Back[/dim]"
        if is_explorer: sub = f"[bold cyan]{self.current_path}[/bold cyan] | {sub}"
        return Panel(table, title=f"[bold green]{title}[/bold green]", subtitle=sub)

    def view_code(self, item):
        path = item.get('path')
        content = ""
        if path and os.path.exists(path):
            try:
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
            except: content = "Error reading file."
        elif item.get('url'):
            console.clear()
            console.print("[cyan]Fetching preview from GitHub...[/cyan]")
            try:
                content = requests.get(item['url'], timeout=5).text
            except: content = "Could not fetch preview."

        console.clear()
        syntax = Syntax(content, "python" if item['name'].endswith(".py") else "powershell", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title=f"[bold]Preview: {item['name']}[/bold]", border_style="blue"))
        console.input("\n[dim]Press Enter to return...[/dim]")

    def run_script(self, item):
        script_path = item['path']
        is_quarantine = item.get('status') == "QUARANTINE"
        
        console.clear()
        if is_quarantine:
            console.print(Panel("[bold red]SECURITY WARNING[/bold red]\nThis script is unverified.", border_style="red"))
            if not console.input("Type 'run' to proceed: ").lower() == 'run': return

        console.print(Panel(f"Executing: [bold yellow]{item['name']}[/bold yellow]\n[dim]Capturing output...[/dim]", border_style="yellow"))
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path] if script_path.endswith(".ps1") else [sys.executable, script_path]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout: console.print(f"\n[bold white]Output:[/bold white]\n{result.stdout}")
            if result.returncode != 0:
                console.print(f"\n[bold red]✕ Failed (Exit {result.returncode})[/bold red]")
                if result.stderr: console.print(f"[red]{result.stderr}[/red]")
            else:
                console.print("\n[bold green]✓ Execution Successful[/bold green]")
        except Exception as e: console.print(f"[red]Error: {e}[/red]")
        console.input("\n[dim]Press Enter to return...[/dim]")

    def download_script(self, item, is_global=False):
        console.clear()
        dest = QUARANTINE_DIR if is_global else SCRIPTS_DIR
        console.print(f"Downloading [bold cyan]{item['name']}[/bold cyan]...")
        target_path = os.path.join(dest, item['name'])
        try:
            response = requests.get(item['url'], timeout=10)
            with open(target_path, "wb") as f:
                f.write(response.content)
            console.print("[bold green]Success![/bold green]")
        except Exception as e: console.print(f"[red]Failed: {e}[/red]")
        console.input("\nPress Enter to continue...")

    def main_loop(self):
        with Live(refresh_per_second=10, screen=True) as live:
            while self.running:
                if self.state == "MENU": live.update(self.draw_menu())
                elif self.state == "SCRIPTS": live.update(self.draw_list("My Scripts", self.items, self.sub_index))
                elif self.state == "MARKET": live.update(self.draw_list("Verified Marketplace", self.items, self.sub_index, True))
                elif self.state == "SEARCH": live.update(self.draw_list("GitHub Global Search", self.items, self.sub_index))
                elif self.state == "RECENT": live.update(self.draw_list("Quick Open Files", self.items, self.sub_index))
                elif self.state == "EXPLORER": live.update(self.draw_list("Quick Explorer", self.items, self.sub_index, is_explorer=True))

                if msvcrt.kbhit():
                    key = ord(msvcrt.getch())
                    if key == 224:
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
                            if "Workspaces" in choice:
                                live.stop(); subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "morning-routine.py")]); live.start()
                            elif "Comms Hub" in choice:
                                live.stop(); subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "comms-hub.py")]); live.start()
                            elif "Local Scripts" in choice: self.state = "SCRIPTS"; self.items = self.get_local_scripts(); self.sub_index = 0
                            elif "Quick Explorer" in choice: self.state = "EXPLORER"; self.items = self.get_explorer_items(); self.sub_index = 0
                            elif "GitHub Search" in choice:
                                live.stop()
                                q = console.input("[bold cyan]GitHub Search Query: [/bold cyan]")
                                self.items = self.search_github(q); self.state = "SEARCH"; self.sub_index = 0
                                live.start()
                            elif "Marketplace" in choice: self.state = "MARKET"; self.items = self.get_marketplace(); self.sub_index = 0
                            elif "Recent Files" in choice: self.state = "RECENT"; self.items = self.get_recent_files(); self.sub_index = 0
                            elif "Exit" in choice: self.running = False
                        elif self.state == "SCRIPTS":
                            if self.items: live.stop(); self.run_script(self.items[self.sub_index]); live.start()
                        elif self.state == "EXPLORER":
                            if self.items:
                                item = self.items[self.sub_index]
                                if item['type'] == 'dir': self.current_path = item['path']; self.items = self.get_explorer_items(); self.sub_index = 0
                                else: os.startfile(item['path']); self.running = False
                        elif self.state == "MARKET":
                            if self.items: live.stop(); self.download_script(self.items[self.sub_index]); live.start()
                        elif self.state == "SEARCH":
                            if self.items: live.stop(); self.download_script(self.items[self.sub_index], is_global=True); live.start()
                        elif self.state == "RECENT":
                            if self.items: os.startfile(self.items[self.sub_index]['path']); self.running = False

                    elif key == ord('v'): # View Code
                        if self.state in ["SCRIPTS", "MARKET", "SEARCH"]:
                            if self.items: live.stop(); self.view_code(self.items[self.sub_index]); live.start()

                    elif key == ord('q') or key == 27:
                        if self.state == "MENU": self.running = False
                        else: self.state = "MENU"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try: from cli import main as cli_main; cli_main()
        except ImportError: print("[Error] cli.py not found.")
    else:
        tui = ShortcutTUI()
        tui.main_loop()