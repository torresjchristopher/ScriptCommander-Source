"""VaultZero Keycard Manager: Content-Addressable State Restoration

This module handles the 'Keycard' logic:
- Deciphering context codes (strings/URLs)
- Unpacking snapshot zips
- Restoring Forge and Script contexts with zero-knowledge/zero-password logic
"""

import os
import json
import zipfile
import base64
from pathlib import Path
from rich.console import Console

console = Console()

class KeycardManager:
    def __init__(self):
        self.keycards_dir = os.path.expanduser("~/.shortcut/keycards")
        self.registry_path = os.path.join(self.keycards_dir, "registry.json")
        if not os.path.exists(self.keycards_dir):
            os.makedirs(self.keycards_dir)
        self._init_registry()

    def _init_registry(self):
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, 'w') as f:
                json.dump([], f)

    def get_all_restores(self):
        """Amass all known restore points."""
        with open(self.registry_path, 'r') as f:
            return json.load(f)

    def register_code(self, code_str):
        """Decipher a string code and add to registry."""
        try:
            # Simple Base64 logic for now to 'decipher' context
            # In a real implementation, this would handle FGR:// style URLs
            decoded = base64.b64decode(code_str).decode('utf-8')
            context = json.loads(decoded)
            
            restores = self.get_all_restores()
            context['id'] = f"RESTORE_{len(restores) + 1}"
            context['type'] = context.get('type', 'Unknown')
            restores.append(context)
            
            with open(self.registry_path, 'w') as f:
                json.dump(restores, f)
            return True
        except Exception as e:
            console.print(f"[red]Failed to decipher keycard code: {e}[/red]")
            return False

    def unpack_zip(self, zip_path):
        """Restore from a ZIP keycard."""
        if not os.path.exists(zip_path):
            return False
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as z:
                # Expecting a manifest.json inside the zip
                manifest_data = z.read('manifest.json')
                manifest = json.loads(manifest_data)
                
                # Logic to restore files to ~/.forge/ or ~/.shortcut/
                # z.extractall(path=...)
                
                self.register_code(base64.b64encode(manifest_data).decode('utf-8'))
                return True
        except Exception as e:
            console.print(f"[red]Failed to unpack zip keycard: {e}[/red]")
            return False

    def restore_context(self, restore_id):
        """Execute the logic to move the CLI into the saved context."""
        restores = self.get_all_restores()
        target = next((r for r in restores if r.get('id') == restore_id), None)
        if not target:
            return False
            
        console.print(f"[green]Restoring {target['type']} context: {target.get('name', 'Unnamed')}[/green]")
        # Implementation would trigger Forge or Script execution based on target data
        return True
