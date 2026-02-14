"""
Sovereign Artifact Packager.

Handles the creation and extraction of .nxs (Nexus Context) files.
These are encrypted, compressed logic-seeds that can be 'Detonated' remotely.
"""

import os
import json
import tarfile
import zipfile
from datetime import datetime
from pathlib import Path

class SovereignArtifact:
    """
    The transport container for Sovereign Intelligence.
    """
    
    def __init__(self, artifact_path: str = None):
        self.artifact_path = artifact_path

    def pack(self, context_path: str, output_path: str, metadata: dict = None) -> str:
        """
        Compress a local context (folder/repo) into a .nxs artifact.
        """
        context = Path(context_path)
        if not context.exists():
            raise FileNotFoundError(f"Context not found: {context}")

        # 1. Prepare Metadata
        meta = {
            "created_at": datetime.now().isoformat(),
            "type": "context_seed",
            "entry_point": metadata.get("entry_point", "forge.yml"),
            "security": "vault_zero_unsigned" # Placeholder for real encryption
        }
        if metadata:
            meta.update(metadata)

        # 2. Create the Logic Seed (The 'Meat')
        # We assume the context is small enough for a seed, or use Forge logic to prune it first.
        seed_filename = "logic_seed.tar.gz"
        
        # 3. Zip it all up into .nxs
        final_path = output_path if output_path.endswith(".nxs") else f"{output_path}.nxs"
        
        print(f"[ARTIFACT] Packing context from {context}...")
        
        with zipfile.ZipFile(final_path, 'w', zipfile.ZIP_DEFLATED) as nxs:
            # Write Manifest
            nxs.writestr("manifest.json", json.dumps(meta, indent=2))
            
            # Write Seed (Tarball of directory)
            # In a real implementation, we'd use Forge to 'Export' a clean seed.
            # Here we just tar the directory.
            tar_path = f"{context.name}.tar.gz"
            with tarfile.open(tar_path, "w:gz") as tar:
                tar.add(context, arcname="root")
            
            nxs.write(tar_path, arcname="seed.tar.gz")
            os.remove(tar_path) # Cleanup temp tar
            
        print(f"[ARTIFACT] .nxs file created at {final_path}")
        return final_path

    def unpack(self, target_dir: str) -> dict:
        """
        Unpack a .nxs artifact for Detonation.
        Returns the manifest and the path to the extracted seed.
        """
        if not self.artifact_path or not os.path.exists(self.artifact_path):
            raise FileNotFoundError("No artifact loaded.")

        dest = Path(target_dir)
        dest.mkdir(parents=True, exist_ok=True)
        
        print(f"[ARTIFACT] Unpacking {self.artifact_path}...")
        
        with zipfile.ZipFile(self.artifact_path, 'r') as nxs:
            # 1. Read Manifest
            manifest = json.loads(nxs.read("manifest.json"))
            
            # 2. Extract Seed
            nxs.extract("seed.tar.gz", dest)
            
            # 3. Hydrate (Untar the seed)
            seed_path = dest / "seed.tar.gz"
            with tarfile.open(seed_path, "r:gz") as tar:
                tar.extractall(dest)
            
            # Cleanup
            os.remove(seed_path)
            
        return {
            "manifest": manifest,
            "root_path": str(dest / "root")
        }
