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
        Performs smart ingestion: Sanitizes heavy dirs and detects runtime.
        """
        context = Path(context_path)
        if not context.exists():
            raise FileNotFoundError(f"Context not found: {context}")

        # 1. Analyze and Sanitize
        project_info = self._analyze_context(context)
        
        # 2. Prepare Metadata
        meta = {
            "created_at": datetime.now().isoformat(),
            "type": "context_seed",
            "runtime_detected": project_info['runtime'],
            "entry_point": metadata.get("entry_point", project_info['entry_point']),
            "security": "vault_zero_unsigned"
        }
        if metadata:
            meta.update(metadata)

        # 3. Zip it all up into .nxs (NX- Protocol)
        import hashlib
        checksum = hashlib.md5(context_path.encode()).hexdigest()[:3].upper()
        
        type_code = "SED"
        if project_info['runtime'] == "forge_native": type_code = "CTX"
        if project_info['runtime'] == "docker_compose": type_code = "LGC"
        
        coded_name = f"NX-{type_code}-{checksum}-{os.path.basename(context_path)}.nxs"
        final_path = os.path.join(os.path.dirname(output_path), coded_name)
        
        print(f"[ARTIFACT] Packing context from {context}...")
        print(f"[NX-CODE] Generated: {coded_name}")
        print(f"[INGEST] Detected {project_info['runtime']}. Pruning heavy artifacts...")
        
        with zipfile.ZipFile(final_path, 'w', zipfile.ZIP_DEFLATED) as nxs:
            # Write Manifest
            nxs.writestr("manifest.json", json.dumps(meta, indent=2))
            
            # Auto-scaffold forge.yml if missing
            if project_info['runtime'] != "forge_native":
                scaffold = self._generate_forge_scaffold(project_info)
                nxs.writestr("root/forge.yml", scaffold)
                print(f"[INGEST] Auto-generated forge.yml for {project_info['runtime']}")

            # Write Seed (Tarball of filtered directory)
            tar_path = f"{context.name}.tar.gz"
            
            # Smart Filter
            def filter_heavy(tarinfo):
                name = tarinfo.name
                if any(x in name for x in ['node_modules', 'venv', '.git', '__pycache__', '.env', 'dist', 'build']):
                    return None # Exclude
                return tarinfo

            with tarfile.open(tar_path, "w:gz") as tar:
                tar.add(context, arcname="root", filter=filter_heavy)
            
            nxs.write(tar_path, arcname="seed.tar.gz")
            os.remove(tar_path) # Cleanup temp tar
            
        print(f"[ARTIFACT] .nxs file created at {final_path}")
        return final_path

    def _analyze_context(self, path: Path) -> dict:
        """
        Heuristic scan to determine project type and entry point.
        """
        info = {"runtime": "unknown", "entry_point": "forge.yml"}
        
        # Check for Forge Config first
        if (path / "forge.yml").exists():
            info["runtime"] = "forge_native"
            return info

        # Check for Docker
        if (path / "docker-compose.yml").exists():
            info["runtime"] = "docker_compose"
            info["entry_point"] = "docker-compose.yml"
        elif (path / "Dockerfile").exists():
            info["runtime"] = "docker"
            info["entry_point"] = "Dockerfile"
            
        # Check for Language Runtimes
        elif (path / "package.json").exists():
            info["runtime"] = "node"
            info["entry_point"] = "npm start"
        elif (path / "requirements.txt").exists() or (path / "pyproject.toml").exists():
            info["runtime"] = "python"
            info["entry_point"] = "python main.py" # Guess
            
        return info

    def _generate_forge_scaffold(self, info: dict) -> str:
        """Create a default forge.yml for ingested projects."""
        runtime = info['runtime']
        entry = info['entry_point']
        
        template = {
            "name": "ingested_context",
            "version": "1.0.0",
            "recursive": True,
            "tasks": [
                {
                    "name": "setup",
                    "image": f"{runtime}:latest" if runtime in ['python', 'node'] else "alpine",
                    "command": "pip install -r requirements.txt" if runtime == 'python' else "npm install" if runtime == 'node' else "echo setup"
                },
                {
                    "name": "execute",
                    "depends_on": ["setup"],
                    "image": f"{runtime}:latest" if runtime in ['python', 'node'] else "alpine",
                    "command": entry
                }
            ]
        }
        import yaml
        return yaml.dump(template)

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
