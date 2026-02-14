import os
import sys
import subprocess
import requests
import msvcrt
import shutil
try:
    from forge_integration import launch_forge_command
except ImportError:
    launch_forge_command = None
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
VERSION = "4.1.0"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
QUARANTINE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "quarantine")
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"
RECENT_FILES_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')

console = Console()

class ShortcutTUI:
    def __init__(self):
        # High-Caliber Menu Structure
        self.menu_options = [
            "Forge (Container Orchestration)", 
            "Pidgeon (CLI Email & Contacts)", 
            "Connect (Collaboration)", 
            "Local Scripts (Automation)", 
            "Additional Features (Utilities)", 
            "Exit"
        ]
        
        # Sub-menus
        self.forge_options = ["Launch Dashboard (TUI)", "System Status", "Sync GitHub Repo (Omni-Sync)", "Back"]
        self.pidgeon_options = ["Recent Contacts", "Send Pidgeon (Email)", "Message History", "Back"]
        self.connect_options = ["Discovery (Online Peers)", "Active Sessions", "Shared Workflows", "Back"]
        self.scripts_options = ["My Verified Scripts", "Marketplace", "GitHub Search", "Back"]
        self.features_options = ["Keycard Restores", "Workspaces (Morning Routine)", "Comms Hub", "Quick Explorer", "Manage Vault (VaultZero)", "Back"]

        self.current_index = 0
        self.state = "MENU" # MENU, FORGE_MENU, PIDGEON_MENU, CONNECT_MENU, SCRIPTS_MENU, FEATURES_MENU, ...
        self.items = []
        self.sub_index = 0
        self.current_path = os.path.expanduser("~") # For Explorer
        self.running = True

    def get_local_scripts(self):
        for d in [SCRIPTS_DIR, QUARANTINE_DIR]:
            if not os.path.exists(d): os.makedirs(d)
        scripts = []
        if os.path.exists(SCRIPTS_DIR):
            for f in os.listdir(SCRIPTS_DIR):
                if f.endswith(".ps1") or f.endswith(".py"):
                    scripts.append({"name": f, "path": os.path.join(SCRIPTS_DIR, f), "status": "Verified"})
        if os.path.exists(QUARANTINE_DIR):
            for f in os.listdir(QUARANTINE_DIR):
                if f.endswith(".ps1") or f.endswith(".py"):
                    scripts.append({"name": f, "path": os.path.join(QUARANTINE_DIR, f), "status": "QUARANTINE"})
        return scripts

    def get_pidgeon_contacts(self):
        from pidgeon import Pidgeon
        p = Pidgeon()
        return [{"name": c['name'], "email": c['email'], "status": "Contact"} for c in p.get_contacts()]

    def get_connect_peers(self):
        from connect import Connect
        c = Connect()
        return [{"name": p['username'], "status": p['status'], "ip": p['ip']} for p in c.get_online_peers()]

    def get_keycard_restores(self):
        try:
            from keycard_manager import KeycardManager
            mgr = KeycardManager()
            return mgr.get_all_restores()
        except: return []

    def get_marketplace(self):
        try: return requests.get(MARKETPLACE_URL, timeout=5).json()
        except: return []

    def search_github(self, query):
        url = f"https://api.github.com/search/code?q={query}+extension:ps1+extension:py"
        try:
            items = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json'}, timeout=10).json().get('items', [])
            results = []
            for item in items[:15]:
                repo = item['repository']['full_name']
                name = item['name']
                download_url = item['html_url'].replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
                results.append({"name": f"{name} ({repo})", "url": download_url, "id": name, "status": "Global"})
            return results
        except: return []

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

    def draw_menu(self, options, title_override=None):
        title = title_override if title_override else f"[bold cyan]{APP_NAME}[/bold cyan] v{VERSION}"
        table = Table(box=box.ROUNDED, show_header=False, expand=True, border_style="blue")
        for i, option in enumerate(options):
            style = "bold white on blue" if i == self.current_index else "white"
            prefix = "> " if i == self.current_index else "  "
            table.add_row(Text(f"{prefix}{option}", style=style))
        return Panel(table, title=title, subtitle="[dim]Arrows to navigate, Enter to select[/dim]")

    def draw_list(self, title, items, index, is_market=False, is_explorer=False):
        table = Table(box=box.ROUNDED, expand=True, border_style="green")
        table.add_column("Selection", justify="center", width=4)
        table.add_column("Name", style="bold")
        if is_market: table.add_column("Description")
        if not is_market and not is_explorer: table.add_column("Status")
        for i, item in enumerate(items):
            style = "bold white on green" if i == index else ""
            prefix = ">>" if i == index else "  "
            if is_market: table.add_row(prefix, item["name"], item.get("description", ""), style=style)
            elif is_explorer:
                icon = "📁" if item['type'] == 'dir' else "📄"
                table.add_row(prefix, f"{icon} {item['name']}", style=style)
            elif isinstance(item, dict):
                status = item.get("status", "") or item.get("id", "")
                s_style = "bold red" if status == "QUARANTINE" else "dim"
                table.add_row(prefix, item["name"], Text(status, style=s_style), style=style)
            else: table.add_row(prefix, str(item), "", style=style)
        sub = "[dim]Enter: Action | 'v': View Code | 'q': Back[/dim]"
        if is_explorer: sub = f"[bold cyan]{self.current_path}[/bold cyan] | {sub}"
        return Panel(table, title=f"[bold green]{title}[/bold green]", subtitle=sub)

    def view_code(self, item):
        path = item.get('path')
        content = ""
        if path and os.path.exists(path):
            try:
                with open(path, 'r', errors='ignore') as f: content = f.read()
            except: content = "Error reading file."
        elif item.get('url'):
            console.clear()
            console.print("[cyan]Fetching preview from GitHub...[/cyan]")
            try: content = requests.get(item['url'], timeout=5).text
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
        console.print(Panel(f"Executing: [bold yellow]{item['name']}[/bold yellow]", border_style="yellow"))
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path] if script_path.endswith(".ps1") else [sys.executable, script_path]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.stdout: console.print(f"\n[bold white]Output:[/bold white]\n{result.stdout}")
            if result.returncode != 0: console.print(f"\n[bold red]✕ Failed (Exit {result.returncode})[/bold red]")
            else: console.print("\n[bold green]✓ Execution Successful[/bold green]")
        except Exception as e: console.print(f"[red]Error: {e}[/red]")
        console.input("\n[dim]Press Enter to return...[/dim]")

    def download_script(self, item, is_global=False):
        console.clear()
        dest = QUARANTINE_DIR if is_global else SCRIPTS_DIR
        console.print(f"Downloading [bold cyan]{item['name']}[/bold cyan]...")
        try:
            res = requests.get(item['url'], timeout=10)
            with open(os.path.join(dest, item['name']), "wb") as f: f.write(res.content)
            console.print("[bold green]Success![/bold green]")
        except Exception as e: console.print(f"[red]Failed: {e}[/red]")
        console.input("\nPress Enter to continue...")

    def get_current_options(self):
        if self.state == "MENU": return self.menu_options
        if self.state == "FORGE_MENU": return self.forge_options
        if self.state == "PIDGEON_MENU": return self.pidgeon_options
        if self.state == "CONNECT_MENU": return self.connect_options
        if self.state == "SCRIPTS_MENU": return self.scripts_options
        if self.state == "FEATURES_MENU": return self.features_options
        return []

    def main_loop(self):
        with Live(refresh_per_second=10, screen=True) as live:
            while self.running:
                if self.state == "MENU": live.update(self.draw_menu(self.menu_options))
                elif self.state == "FORGE_MENU": live.update(self.draw_menu(self.forge_options, title_override="Forge Engine"))
                elif self.state == "PIDGEON_MENU": live.update(self.draw_menu(self.pidgeon_options, title_override="Pidgeon: CLI Email"))
                elif self.state == "CONNECT_MENU": live.update(self.draw_menu(self.connect_options, title_override="Connect: Collaboration"))
                elif self.state == "SCRIPTS_MENU": live.update(self.draw_menu(self.scripts_options, title_override="Local Scripts"))
                elif self.state == "FEATURES_MENU": live.update(self.draw_menu(self.features_options, title_override="Additional Features"))
                
                elif self.state == "KEYCARD_LIST": live.update(self.draw_list("Keycard: Restore Points", self.items, self.sub_index))
                elif self.state == "CONTACTS_LIST": live.update(self.draw_list("Pidgeon: Contacts", self.items, self.sub_index))
                elif self.state == "PEERS_LIST": live.update(self.draw_list("Connect: Online Peers", self.items, self.sub_index))
                elif self.state == "SCRIPTS_LIST": live.update(self.draw_list("My Scripts", self.items, self.sub_index))
                elif self.state == "MARKET": live.update(self.draw_list("Verified Marketplace", self.items, self.sub_index, True))
                elif self.state == "SEARCH": live.update(self.draw_list("GitHub Global Search", self.items, self.sub_index))
                elif self.state == "RECENT": live.update(self.draw_list("Quick Open Files", self.items, self.sub_index))
                elif self.state == "EXPLORER": live.update(self.draw_list("Quick Explorer", self.items, self.sub_index, is_explorer=True))

                if msvcrt.kbhit():
                    key = ord(msvcrt.getch())
                    if key == 224:
                        key = ord(msvcrt.getch())
                        if key == 72: # Up
                            if "MENU" in self.state: self.current_index = (self.current_index - 1) % len(self.get_current_options())
                            else: self.sub_index = (self.sub_index - 1) % len(self.items) if self.items else 0
                        elif key == 80: # Down
                            if "MENU" in self.state: self.current_index = (self.current_index + 1) % len(self.get_current_options())
                            else: self.sub_index = (self.sub_index + 1) % len(self.items) if self.items else 0
                    
                    elif key == 13: # Enter
                        if self.state == "MENU":
                            choice = self.menu_options[self.current_index]
                            if "Forge" in choice: self.state = "FORGE_MENU"; self.current_index = 0
                            elif "Pidgeon" in choice: self.state = "PIDGEON_MENU"; self.current_index = 0
                            elif "Connect" in choice: self.state = "CONNECT_MENU"; self.current_index = 0
                            elif "Local Scripts" in choice: self.state = "SCRIPTS_MENU"; self.current_index = 0
                            elif "Additional Features" in choice: self.state = "FEATURES_MENU"; self.current_index = 0
                            elif "Exit" in choice: self.running = False
                        
                        elif self.state == "FORGE_MENU":
                            c = self.forge_options[self.current_index]
                            if "Dashboard" in c: live.stop(); launch_forge_command(['tui']) if launch_forge_command else print("N/A"); live.start()
                            elif "System" in c: live.stop(); launch_forge_command(['system', 'usage']) if launch_forge_command else print("N/A"); console.input("\n..."); live.start()
                            elif "Sync GitHub" in c:
                                live.stop(); repo = console.input("[bold cyan]Repo: [/bold cyan]"); subprocess.run([sys.executable, "cli.py", "sync", "repo", repo]); console.input("\n..."); live.start()
                            elif "Back" in c: self.state = "MENU"; self.current_index = 0

                        elif self.state == "PIDGEON_MENU":
                            c = self.pidgeon_options[self.current_index]
                            if "Contacts" in c: self.state = "CONTACTS_LIST"; self.items = self.get_pidgeon_contacts(); self.sub_index = 0
                            elif "Send" in c:
                                live.stop(); to = console.input("To: "); sub = console.input("Subject: "); body = console.input("Body: ")
                                subprocess.run([sys.executable, "cli.py", "pidgeon", "send", to, "-s", sub, "-b", body]); console.input("\n..."); live.start()
                            elif "Back" in c: self.state = "MENU"; self.current_index = 0

                        elif self.state == "CONNECT_MENU":
                            c = self.connect_options[self.current_index]
                            if "Discovery" in c: self.state = "PEERS_LIST"; self.items = self.get_connect_peers(); self.sub_index = 0
                            elif "Back" in c: self.state = "MENU"; self.current_index = 0

                        elif self.state == "SCRIPTS_MENU":
                            c = self.scripts_options[self.current_index]
                            if "My Verified" in c: self.state = "SCRIPTS_LIST"; self.items = self.get_local_scripts(); self.sub_index = 0
                            elif "Marketplace" in c: self.state = "MARKET"; self.items = self.get_marketplace(); self.sub_index = 0
                            elif "GitHub Search" in c:
                                live.stop(); q = console.input("[bold cyan]Search: [/bold cyan]"); self.items = self.search_github(q); self.state = "SEARCH"; self.sub_index = 0; live.start()
                            elif "Back" in c: self.state = "MENU"; self.current_index = 0

                        elif self.state == "FEATURES_MENU":
                            c = self.features_options[self.current_index]
                            if "Keycard" in c: self.state = "KEYCARD_LIST"; self.items = self.get_keycard_restores(); self.sub_index = 0
                            elif "Workspaces" in c: live.stop(); subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "morning-routine.py")]); live.start()
                            elif "Comms Hub" in c: live.stop(); subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, "comms-hub.py")]); live.start()
                            elif "Quick Explorer" in c: self.state = "EXPLORER"; self.items = self.get_explorer_items(); self.sub_index = 0
                            elif "Recent Files" in c: self.state = "RECENT"; self.items = self.get_recent_files(); self.sub_index = 0
                            elif "Manage Vault" in c:
                                live.stop(); token = console.input("Token: "); subprocess.run([sys.executable, "cli.py", "vault", "login", token]); console.input("\n..."); live.start()
                            elif "Back" in c: self.state = "MENU"; self.current_index = 0

                        elif self.state == "SCRIPTS_LIST":
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
                        if self.state in ["SCRIPTS_LIST", "MARKET", "SEARCH"]:
                            if self.items: live.stop(); self.view_code(self.items[self.sub_index]); live.start()

                    elif key == ord('q') or key == 27:
                        if self.state == "MENU": self.running = False
                        elif "MENU" in self.state: self.state = "MENU"; self.current_index = 0
                        else:
                             if self.state in ["SCRIPTS_LIST", "MARKET", "SEARCH"]: self.state = "SCRIPTS_MENU"
                             elif self.state in ["EXPLORER", "RECENT"]: self.state = "FEATURES_MENU"
                             elif self.state in ["CONTACTS_LIST"]: self.state = "PIDGEON_MENU"
                             elif self.state in ["PEERS_LIST"]: self.state = "CONNECT_MENU"
                             else: self.state = "MENU"
                             self.current_index = 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try: from cli import main as cli_main; cli_main()
        except ImportError: print("[Error] cli.py not found.")
    else:
        tui = ShortcutTUI(); tui.main_loop()