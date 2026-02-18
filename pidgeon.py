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
        self.ghost_map_path = os.path.join(self.pidgeon_dir, "ghost_identities.json")
        
        if not os.path.exists(self.pidgeon_dir):
            os.makedirs(self.pidgeon_dir)
        self._init_storage()

    def _init_storage(self):
        for path in [self.contacts_path, self.history_path, self.ghost_map_path]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump({}, f if "ghost" in path else [])

    def get_actual_id(self, ghost_name: str) -> str:
        """Resolves a masked Ghost Name to the real Spectre ID."""
        with open(self.ghost_map_path, 'r') as f:
            mapping = json.load(f)
            return mapping.get(ghost_name, ghost_name) # Fallback to input

    def generate_ghost_name(self, real_id: str) -> str:
        """
        Creates a unique, illusive name for a specific relationship.
        In production, this would be derived from a hardware-rooted hash.
        """
        ghosts = ["spectre-alpha", "phantom-node", "void-walker", "nebula-drift", "echo-point"]
        import random
        mask = f"{random.choice(ghosts)}-{random.randint(1000, 9999)}"
        
        # Save the relationship pointer
        with open(self.ghost_map_path, 'r+') as f:
            mapping = json.load(f)
            mapping[mask] = real_id
            f.seek(0)
            json.dump(mapping, f, indent=2)
            
        return mask

    def transfer_artifact(self, artifact_path: str, recipient_mask: str):
        """
        Simulate the peer-to-peer transfer using a Ghost Identity.
        """
        # Resolve identity internally
        real_id = self.get_actual_id(recipient_mask)
        filename = os.path.basename(artifact_path)
        
        console.print(f"[bold cyan]MESH[/bold cyan] :: Masked Route Established: [dim]{recipient_mask}[/dim]")
        console.print(f"[dim][SECURITY] Pidgeon resolving pointer to {real_id}...[/dim]")
        
        # Simulation: Copy to a 'shared' mesh folder
        mesh_dir = os.path.expanduser("~/.shortcut/mesh_inbox")
        if not os.path.exists(mesh_dir): os.makedirs(mesh_dir)
        
        import shutil
        shutil.copy(artifact_path, os.path.join(mesh_dir, filename))
        
        console.print(f"[green]✓ {filename} delivered to {recipient_mask}'s secure vault.[/green]")
        return True
