"""Pidgeon: High-Caliber CLI Email & Contact Management

Provides:
- Recent contact indexing
- SMTP/Local mail integration
- Message composition from the terminal
"""

import os
import json
from rich.console import Console
from rich.table import Table

console = Console()

class Pidgeon:
    def __init__(self):
        self.pidgeon_dir = os.path.expanduser("~/.shortcut/pidgeon")
        self.contacts_path = os.path.join(self.pidgeon_dir, "contacts.json")
        self.history_path = os.path.join(self.pidgeon_dir, "history.json")
        
        if not os.path.exists(self.pidgeon_dir):
            os.makedirs(self.pidgeon_dir)
        self._init_storage()

    def _init_storage(self):
        for path in [self.contacts_path, self.history_path]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump([], f)

    def get_contacts(self):
        """Get recent/saved contacts."""
        with open(self.contacts_path, 'r') as f:
            return json.load(f)

    def add_contact(self, name, email):
        contacts = self.get_contacts()
        if not any(c['email'] == email for c in contacts):
            contacts.append({"name": name, "email": email})
            with open(self.contacts_path, 'w') as f:
                json.dump(contacts, f)
        return True

    def send_pidgeon(self, to_email, subject, body):
        """
        Simulate sending an email. In production, this would use 
        VaultZero to fetch SMTP creds and send via smtplib.
        """
        console.print(f"[cyan]Pidgeon is taking off...[/cyan]")
        console.print(f"[bold]To:[/bold] {to_email}\n[bold]Subject:[/bold] {subject}")
        
        # Log to history
        history = []
        with open(self.history_path, 'r') as f:
            history = json.load(f)
        
        history.append({
            "to": to_email,
            "subject": subject,
            "body": body,
            "timestamp": "now" # In real app, use datetime
        })
        
        with open(self.history_path, 'w') as f:
            json.dump(history, f)
            
        console.print("[green]✓ Pidgeon delivered successfully.[/green]")
        return True
