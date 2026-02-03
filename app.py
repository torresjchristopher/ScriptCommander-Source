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
VERSION = "3.0.0"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"
RECENT_FILES_PATH = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Recent')

console = Console()

class ShortcutTUI:
    def __init__(self):
        self.menu_options = ["Local Scripts", "Marketplace", "Recent Files", "Exit"]
        self.current_index = 0
        self.state = "MENU" # MENU, SCRIPTS, MARKET, RECENT
        self.items = []
        self.sub_index = 0
        self.running = True

    def get_local_scripts(self):
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)
        return [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".ps1") or f.endswith(".py")]

    def get_marketplace(self):
        try:
            response = requests.get(MARKETPLACE_URL, timeout=5)
            return response.json()
        except:
            return []

    def get_recent_files(self):
        if not os.path.exists(RECENT_FILES_PATH):
            return []
        # Get last 15 recent files (links)
        files = []
        try:
            items = os.listdir(RECENT_FILES_PATH)
            full_paths = [os.path.join(RECENT_FILES_PATH, i) for i in items if i.endswith(".lnk")]
            # Sort by modification time
            full_paths.sort(key=os.path.getmtime, reverse=True)
            for path in full_paths[:15]:
                name = os.path.basename(path).replace(".lnk", "")
                files.append({"name": name, "path": path})
        except:
            pass
        return files

    def draw_menu(self):
        table = Table(box=box.ROUNDED, show_header=False, expand=True, border_style="blue")
        for i, option in enumerate(self.menu_options):
            style = "bold white on blue" if i == self.current_index else "white"
            prefix = "> " if i == self.current_index else "  "
            table.add_row(Text(f"{prefix}{option}", style=style))
        
        return Panel(table, title=f"[bold cyan]{APP_NAME}[/bold cyan] v{VERSION}", subtitle="[dim]Arrows to navigate, Enter to select")

    def draw_list(self, title, items, index, is_market=False):
        table = Table(box=box.ROUNDED, expand=True, border_style="green")
        table.add_column("Selection", justify="center", width=4)
        table.add_column("Name", style="bold")
        if is_market:
            table.add_column("Description")

        for i, item in enumerate(items):
            style = "reverse" if i == index else ""
            prefix = ">>" if i == index else ""
            
            if is_market:
                table.add_row(prefix, item["name"], item.get("description", ""), style=style)
            elif isinstance(item, dict): # Recent files
                table.add_row(prefix, item["name"], "", style=style)
            else: # Local scripts
                table.add_row(prefix, item, "", style=style)

        return Panel(table, title=f"[bold green]{title}[/bold green]", subtitle="[dim]Enter to Execute/Download, 'q' to go back")

    def run_script(self, filename):
        script_path = os.path.join(SCRIPTS_DIR, filename)
        console.clear()
        console.print(Panel(f"Executing: [bold yellow]{filename}[/bold yellow]...", border_style="yellow"))
        
        if filename.endswith(".ps1"):
            ps_command = f"Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\" ' -Verb RunAs"
            command = ["powershell", "-Command", ps_command]
        else:
            command = [sys.executable, script_path]
        
        try:
            subprocess.run(command)
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            console.input("\nPress Enter to continue...")

    def download_script(self, item):
        console.clear()
        console.print(f"Downloading [bold cyan]{item['name']}[/bold cyan]...")
        target_path = os.path.join(SCRIPTS_DIR, f"{item['id']}.ps1")
        try:
            response = requests.get(item['url'], timeout=10)
            response.raise_for_status()
            with open(target_path, "wb") as f:
                f.write(response.content)
            console.print("[bold green]Successfully Installed![/bold green]")
        except Exception as e:
            console.print(f"[red]Failed: {e}[/red]")
        console.input("\nPress Enter to continue...")

    def open_recent(self, item):
        try:
            os.startfile(item['path'])
        except Exception as e:
            console.print(f"[red]Error opening file: {e}[/red]")
            console.input("\nPress Enter to continue...")

    def main_loop(self):
        with Live(refresh_per_second=10, screen=True) as live:
            while self.running:
                if self.state == "MENU":
                    live.update(self.draw_menu())
                elif self.state == "SCRIPTS":
                    live.update(self.draw_list("My Local Scripts", self.items, self.sub_index))
                elif self.state == "MARKET":
                    live.update(self.draw_list("Verified Marketplace", self.items, self.sub_index, True))
                elif self.state == "RECENT":
                    live.update(self.draw_list("Recently Used Files (Quick Open)", self.items, self.sub_index))

                if msvcrt.kbhit():
                    key = ord(msvcrt.getch())
                    if key == 224: # Arrow keys
                        key = ord(msvcrt.getch())
                        if key == 72: # Up
                            if self.state == "MENU":
                                self.current_index = (self.current_index - 1) % len(self.menu_options)
                            else:
                                self.sub_index = (self.sub_index - 1) % len(self.items) if self.items else 0
                        elif key == 80: # Down
                            if self.state == "MENU":
                                self.current_index = (self.current_index + 1) % len(self.menu_options)
                            else:
                                self.sub_index = (self.sub_index + 1) % len(self.items) if self.items else 0
                    
                    elif key == 13: # Enter
                        if self.state == "MENU":
                            choice = self.menu_options[self.current_index]
                            if choice == "Local Scripts":
                                self.items = self.get_local_scripts()
                                self.state = "SCRIPTS"
                                self.sub_index = 0
                            elif choice == "Marketplace":
                                self.state = "MARKET"
                                self.items = self.get_marketplace()
                                self.sub_index = 0
                            elif choice == "Recent Files":
                                self.items = self.get_recent_files()
                                self.state = "RECENT"
                                self.sub_index = 0
                            elif choice == "Exit":
                                self.running = False
                        
                        elif self.state == "SCRIPTS":
                            if self.items:
                                live.stop()
                                self.run_script(self.items[self.sub_index])
                                live.start()
                                self.items = self.get_local_scripts()
                        
                        elif self.state == "MARKET":
                            if self.items:
                                live.stop()
                                self.download_script(self.items[self.sub_index])
                                live.start()

                        elif self.state == "RECENT":
                            if self.items:
                                self.open_recent(self.items[self.sub_index])
                                self.running = False # Exit after opening to stay fast

                    elif key == ord('q') or key == 27: # 'q' or Esc
                        if self.state == "MENU":
                            self.running = False
                        else:
                            self.state = "MENU"

if __name__ == "__main__":
    tui = ShortcutTUI()
    tui.main_loop()
