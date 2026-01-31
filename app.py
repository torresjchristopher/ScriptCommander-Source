import customtkinter as ctk
import os
import subprocess
import sys

# Configuration
APP_NAME = "Script Commander"
SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "scripts")

class ScriptCommanderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title(APP_NAME)
        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Scrollable frame expands

        # Header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_label = ctk.CTkLabel(self.header_frame, text=APP_NAME, font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.pack(pady=10)
        self.refresh_btn = ctk.CTkButton(self.header_frame, text="Refresh List", width=100, command=self.load_scripts)
        self.refresh_btn.pack(pady=(0, 10))

        # Scrollable Script List
        self.scroll_frame = ctk.CTkScrollableFrame(self, label_text="Available Scripts")
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Status Bar
        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="w")

        self.load_scripts()

    def load_scripts(self):
        # Clear existing buttons
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Check directory
        if not os.path.exists(SCRIPTS_DIR):
            os.makedirs(SCRIPTS_DIR)
            self.status_label.configure(text=f"Created directory: {SCRIPTS_DIR}")

        # Find .ps1 files
        files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".ps1")]
        
        if not files:
            lbl = ctk.CTkLabel(self.scroll_frame, text=".ps1 scripts not found in /scripts folder.")
            lbl.pack(pady=20)
            return

        for script_file in files:
            script_path = os.path.join(SCRIPTS_DIR, script_file)
            self.create_script_button(script_file, script_path)

        self.status_label.configure(text=f"Loaded {len(files)} scripts.")

    def create_script_button(self, name, path):
        # Container for the row
        row = ctk.CTkFrame(self.scroll_frame)
        row.pack(fill="x", pady=5, padx=5)
        
        # Script Name Label
        lbl = ctk.CTkLabel(row, text=name, anchor="w")
        lbl.pack(side="left", padx=10, pady=10, fill="x", expand=True)

        # Run Button
        btn = ctk.CTkButton(row, text="Run (Admin)", fg_color="#2CC985", hover_color="#229966", 
                            width=100, command=lambda p=path: self.run_script(p))
        btn.pack(side="right", padx=10, pady=10)

    def run_script(self, script_path):
        self.status_label.configure(text=f"Launching: {os.path.basename(script_path)}...")
        
        # Command to run PowerShell as Admin, keeping the window open (-NoExit would keep it open, but we use Read-Host in script)
        # We use Start-Process -Verb RunAs to trigger UAC prompt
        ps_command = f"Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"{script_path}\"' -Verb RunAs"
        
        try:
            subprocess.run(["powershell", "-Command", ps_command], check=True)
        except subprocess.CalledProcessError as e:
            self.status_label.configure(text=f"Error launching script: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = ScriptCommanderApp()
    app.mainloop()
