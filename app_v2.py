import customtkinter as ctk
import os
import subprocess
import sys
import threading
import json
import requests
from PIL import Image
from tkinter import messagebox

# Configuration
APP_NAME = "Script Commander"
VERSION = "2.0.0"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
METADATA_FILE = os.path.join(SCRIPTS_DIR, "metadata.json")
# In production, this would be a URL to your hosted JSON (GitHub/Firebase)
MARKETPLACE_URL = "https://raw.githubusercontent.com/example/scripts/main/marketplace.json" 

# Colors & Style
ACCENT_COLOR = "#3B82F6"  # Modern Blue
SUCCESS_COLOR = "#10B981" # Emerald Green
BG_DARK = "#111827"       # Slate 900
CARD_BG = "#1F2937"       # Slate 800

class ScriptCommanderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("900x650")
        self.configure(fg_color=BG_DARK)

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#0F172A")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="COMMANDER", font=ctk.CTkFont(size=22, weight="bold"), text_color=ACCENT_COLOR)
        self.logo_label.pack(pady=30, padx=20)

        self.btn_local = self.create_sidebar_button("My Scripts", self.show_local_scripts)
        self.btn_market = self.create_sidebar_button("Marketplace", self.show_marketplace)
        self.btn_settings = self.create_sidebar_button("Settings", self.show_settings)

        # Main Content Area
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.view_title = ctk.CTkLabel(self.header, text="My Scripts", font=ctk.CTkFont(size=28, weight="bold"))
        self.view_title.pack(side="left")

        self.refresh_btn = ctk.CTkButton(self.header, text="Refresh", width=100, fg_color=ACCENT_COLOR, command=self.load_scripts)
        self.refresh_btn.pack(side="right")

        # Scrollable Area
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Status
        self.status_bar = ctk.CTkFrame(self, height=30, fg_color="#0F172A")
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.status_label = ctk.CTkLabel(self.status_bar, text="System Ready", font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.pack(side="left", padx=20)

        self.load_scripts()

    def create_sidebar_button(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, 
                            fg_color="transparent", text_color="white", 
                            hover_color=CARD_BG, anchor="w", height=40)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    def show_local_scripts(self):
        self.view_title.configure(text="My Scripts")
        self.load_scripts()

    def show_marketplace(self):
        self.view_title.configure(text="Marketplace")
        self.clear_view()
        
        # Load marketplace items (mocking a remote fetch)
        try:
            with open("marketplace_mock.json", "r") as f:
                items = json.load(f)
            
            for item in items:
                self.create_marketplace_card(item)
        except Exception as e:
            lbl = ctk.CTkLabel(self.scroll_frame, text=f"Error loading marketplace: {e}")
            lbl.pack(pady=50)

    def create_marketplace_card(self, item):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=8, padx=5)
        
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=20, pady=15, fill="both", expand=True)
        
        lbl_name = ctk.CTkLabel(info, text=item["name"], font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        lbl_name.pack(fill="x")
        
        lbl_desc = ctk.CTkLabel(info, text=item["description"], font=ctk.CTkFont(size=12), text_color="gray", anchor="w", wraplength=400)
        lbl_desc.pack(fill="x")

        # Install/Download Button
        is_installed = os.path.exists(os.path.join(SCRIPTS_DIR, f"{item['id']}.ps1"))
        btn_text = "Installed" if is_installed else "Download"
        btn_state = "disabled" if is_installed else "normal"
        btn_color = "gray" if is_installed else ACCENT_COLOR

        btn_action = ctk.CTkButton(card, text=btn_text, width=100, height=35,
                                  fg_color=btn_color, state=btn_state,
                                  command=lambda i=item: self.download_script(i))
        btn_action.pack(side="right", padx=20)

import requests
from tkinter import messagebox

# Configuration
APP_NAME = "Script Commander"
VERSION = "2.0.0"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")
# In production, this would be a URL to your hosted JSON (GitHub/Firebase)
MARKETPLACE_URL = "https://raw.githubusercontent.com/example/scripts/main/marketplace.json" 

# ... (keep existing color/style constants)

class ScriptCommanderApp(ctk.CTk):
    # ... (keep existing __init__ and sidebar logic)

    def download_script(self, item):
        # Security Confirmation
        confirm = messagebox.askyesno(
            "Security Warning", 
            f"You are about to download '{item['name']}' from a remote source.\n\n" +
            "Scripts can modify your system. Do you trust this author ({item['author']}) and want to proceed?"
        )
        
        if not confirm:
            return

        self.status_label.configure(text=f"Downloading {item['name']}...", text_color=ACCENT_COLOR)
        
        def do_download():
            target_path = os.path.join(SCRIPTS_DIR, f"{item['id']}.ps1")
            try:
                # Real download logic
                response = requests.get(item['url'], timeout=10)
                response.raise_for_status()
                
                with open(target_path, "wb") as f:
                    f.write(response.content)
                
                self.after(0, lambda: self.status_label.configure(text=f"Successfully Installed {item['name']}", text_color=SUCCESS_COLOR))
                self.after(0, self.show_marketplace)
            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text=f"Download Failed: {str(e)}", text_color="red"))

        threading.Thread(target=do_download, daemon=True).start()


    def show_settings(self):
        self.view_title.configure(text="Settings")
        self.clear_view()

    def clear_view(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def load_scripts(self):
        self.clear_view()
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)

        files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".ps1")]
        
        if not files:
            lbl = ctk.CTkLabel(self.scroll_frame, text="No scripts found. Visit the Marketplace to download some!", text_color="gray")
            lbl.pack(pady=50)
            return

        for script_file in files:
            self.create_script_card(script_file)

    def create_script_card(self, filename):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=8, padx=5)
        
        # Info Container
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=20, pady=15, fill="both", expand=True)
        
        name = filename.replace(".ps1", "").replace("-", " ")
        lbl_name = ctk.CTkLabel(info, text=name, font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        lbl_name.pack(fill="x")
        
        lbl_desc = ctk.CTkLabel(info, text="Local PowerShell Utility", font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        lbl_desc.pack(fill="x")

        # Action Button
        btn_run = ctk.CTkButton(card, text="Execute", width=100, height=35,
                               fg_color=SUCCESS_COLOR, hover_color="#059669",
                               command=lambda f=filename: self.run_script(f))
        btn_run.pack(side="right", padx=20)

    def run_script(self, filename):
        script_path = os.path.join(SCRIPTS_DIR, filename)
        self.status_label.configure(text=f"Executing {filename}...", text_color=ACCENT_COLOR)
        
        def execute():
            # Security: Basic validation before execution
            # In a real marketplace, we would check digital signatures or checksums here
            ps_command = f"Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\" ' -Verb RunAs"
            try:
                subprocess.run(["powershell", "-Command", ps_command], check=True)
                self.after(0, lambda: self.status_label.configure(text=f"Success: {filename}", text_color=SUCCESS_COLOR))
            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="red"))

        threading.Thread(target=execute, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = ScriptCommanderApp()
    app.mainloop()
