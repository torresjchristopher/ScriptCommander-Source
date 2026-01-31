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
MARKETPLACE_URL = "https://raw.githubusercontent.com/torresjchristopher/ScriptCommander-Scripts/main/marketplace.json"

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
        
        # Set App Icon
        if os.path.exists("favicon.ico"):
            try:
                self.after(200, lambda: self.iconbitmap("favicon.ico"))
            except:
                pass

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
        self.view_title.configure(text="Official Marketplace")
        self.clear_view()
        
        # Security Header
        sec_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#064e3b", corner_radius=8)
        sec_frame.pack(fill="x", pady=(0, 15), padx=5)
        sec_lbl = ctk.CTkLabel(sec_frame, text="🛡️ All scripts in this marketplace have been manually audited for security.", 
                               font=ctk.CTkFont(size=11, weight="bold"), text_color=SUCCESS_COLOR)
        sec_lbl.pack(pady=8)

        self.status_label.configure(text="Fetching verified scripts...", text_color=ACCENT_COLOR)
        
        def fetch_market():
            try:
                response = requests.get(MARKETPLACE_URL, timeout=10)
                response.raise_for_status()
                items = response.json()
                self.after(0, lambda: self.render_marketplace(items))
            except Exception as e:
                self.after(0, lambda: self.show_error(f"Marketplace Error: {e}"))

        threading.Thread(target=fetch_market, daemon=True).start()

    def render_marketplace(self, items):
        self.clear_view()
        for item in items:
            self.create_marketplace_card(item)
        self.status_label.configure(text="Marketplace loaded.", text_color="gray")

    def show_error(self, message):
        self.clear_view()
        lbl = ctk.CTkLabel(self.scroll_frame, text=message, text_color="red")
        lbl.pack(pady=50)
        self.status_label.configure(text="Error occurred.", text_color="red")

    def create_marketplace_card(self, item):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=8, padx=5)
        
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=20, pady=15, fill="both", expand=True)
        
        # Name + Verified Badge
        header_frame = ctk.CTkFrame(info, fg_color="transparent")
        header_frame.pack(fill="x")
        
        lbl_name = ctk.CTkLabel(header_frame, text=item["name"], font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        lbl_name.pack(side="left")
        
        if item.get("verified", False):
            badge = ctk.CTkLabel(header_frame, text="✓ VERIFIED", font=ctk.CTkFont(size=9, weight="bold"), 
                                 text_color=SUCCESS_COLOR, fg_color="#064e3b", corner_radius=4)
            badge.pack(side="left", padx=10)
        
        lbl_desc = ctk.CTkLabel(info, text=item["description"], font=ctk.CTkFont(size=12), text_color="gray", anchor="w", wraplength=400)
        lbl_desc.pack(fill="x")

        is_installed = os.path.exists(os.path.join(SCRIPTS_DIR, f"{item['id']}.ps1"))
        # ... (keep existing button logic)

        btn_text = "Installed" if is_installed else "Download"
        btn_state = "disabled" if is_installed else "normal"
        btn_color = "gray" if is_installed else ACCENT_COLOR

        btn_action = ctk.CTkButton(card, text=btn_text, width=100, height=35,
                                  fg_color=btn_color, state=btn_state,
                                  command=lambda i=item: self.download_script(i))
        btn_action.pack(side="right", padx=20)

    def download_script(self, item):
        confirm = messagebox.askyesno(
            "Security Warning", 
            f"You are about to download '{item['name']}' from a remote source.\n\n" +
            f"Scripts can modify your system. Do you trust this author ({item['author']}) and want to proceed?"
        )
        
        if not confirm:
            return

        self.status_label.configure(text=f"Downloading {item['name']}...", text_color=ACCENT_COLOR)
        
        def do_download():
            target_path = os.path.join(SCRIPTS_DIR, f"{item['id']}.ps1")
            try:
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
        
        container = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        container.pack(pady=20, padx=20, fill="both", expand=True)

        lbl = ctk.CTkLabel(container, text=f"{APP_NAME} v{VERSION}", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(pady=(0, 10), anchor="w")
        
        lbl_path = ctk.CTkLabel(container, text=f"Scripts Directory:\n{SCRIPTS_DIR}", justify="left", text_color="gray")
        lbl_path.pack(pady=10, anchor="w")

        # Marketplace Submission
        ctk.CTkLabel(container, text="Developer Portal", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 10), anchor="w")
        
        btn_submit = ctk.CTkButton(container, text="Submit Tool to Marketplace", fg_color=ACCENT_COLOR,
                                  command=lambda: subprocess.run(["explorer", "https://github.com/torresjchristopher/ScriptCommander-Scripts/issues/new"]))
        btn_submit.pack(pady=5, anchor="w")
        
        ctk.CTkLabel(container, text="All submissions undergo manual security review before appearing in the marketplace.", 
                     font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="w")

    def clear_view(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def load_scripts(self):
        self.clear_view()
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)

        files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".ps1") or f.endswith(".py")]
        
        if not files:
            lbl = ctk.CTkLabel(self.scroll_frame, text="No scripts found. Visit the Marketplace to download some!", text_color="gray")
            lbl.pack(pady=50)
            return

        for script_file in files:
            self.create_script_card(script_file)

    def create_script_card(self, filename):
        card = ctk.CTkFrame(self.scroll_frame, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x", pady=8, padx=5)
        
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=20, pady=15, fill="both", expand=True)
        
        name = filename.replace(".ps1", "").replace(".py", "").replace("-", " ")
        lbl_name = ctk.CTkLabel(info, text=name, font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
        lbl_name.pack(fill="x")
        
        script_type = "PowerShell" if filename.endswith(".ps1") else "Python"
        lbl_desc = ctk.CTkLabel(info, text=f"Local {script_type} Utility", font=ctk.CTkFont(size=12), text_color="gray", anchor="w")
        lbl_desc.pack(fill="x")

        btn_run = ctk.CTkButton(card, text="Execute", width=100, height=35,
                               fg_color=SUCCESS_COLOR, hover_color="#059669",
                               command=lambda f=filename: self.run_script(f))
        btn_run.pack(side="right", padx=20)

    def run_script(self, filename):
        script_path = os.path.join(SCRIPTS_DIR, filename)
        self.status_label.configure(text=f"Executing {filename}...", text_color=ACCENT_COLOR)
        
        def execute():
            if filename.endswith(".ps1"):
                ps_command = f"Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\" ' -Verb RunAs"
                command = ["powershell", "-Command", ps_command]
            else:
                command = [sys.executable, script_path]

            try:
                subprocess.run(command, check=True)
                self.after(0, lambda: self.status_label.configure(text=f"Success: {filename}", text_color=SUCCESS_COLOR))
            except Exception as e:
                self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}", text_color="red"))

        threading.Thread(target=execute, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    app = ScriptCommanderApp()
    app.mainloop()