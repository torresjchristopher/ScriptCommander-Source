"""
Nemo Deployment Manager - Download & Install Nemo from GitHub

Handles:
- Downloading latest Nemo release from GitHub
- Verifying checksums
- Extracting and installing
- Update management
- Configuration
"""

import os
import sys
import json
import hashlib
import subprocess
import zipfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Tuple
from urllib.request import urlopen, Request
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DownloadManager:
    """
    Manages Nemo downloads, installation, and updates.
    
    Downloads from GitHub releases:
    https://github.com/YOUR_ORG/project-nemo/releases/
    """
    
    # GitHub configuration
    GITHUB_REPO = "username/project-nemo"  # Update this
    GITHUB_API = "https://api.github.com"
    RELEASE_DOWNLOAD_PATH = Path.home() / ".nemo" / "releases"
    NEMO_INSTALL_PATH = Path.home() / ".nemo" / "nemo"
    NEMO_CONFIG_FILE = Path.home() / ".nemo" / "nemo_manifest.json"
    
    def __init__(self):
        """Initialize download manager."""
        self.release_download_path = self.RELEASE_DOWNLOAD_PATH
        self.nemo_install_path = self.NEMO_INSTALL_PATH
        self.release_download_path.mkdir(parents=True, exist_ok=True)
        
    def get_latest_release(self) -> Optional[Dict]:
        """
        Get latest Nemo release info from GitHub.
        
        Returns:
            Release info dict or None if error
        """
        try:
            url = f"{self.GITHUB_API}/repos/{self.GITHUB_REPO}/releases/latest"
            req = Request(url, headers={'User-Agent': 'Nemo-Installer'})
            
            with urlopen(req, timeout=10) as response:
                release_data = json.loads(response.read().decode())
                
            return {
                'version': release_data.get('tag_name', 'unknown'),
                'name': release_data.get('name', 'Nemo Release'),
                'body': release_data.get('body', ''),
                'assets': release_data.get('assets', []),
                'published_at': release_data.get('published_at'),
                'download_url': self._get_download_url(release_data),
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch release info: {e}")
            return None
    
    def _get_download_url(self, release_data: Dict) -> Optional[str]:
        """Extract download URL from release assets."""
        for asset in release_data.get('assets', []):
            if 'nemo' in asset['name'].lower() and asset['name'].endswith('.zip'):
                return asset['browser_download_url']
        return None
    
    def download_release(self, version: Optional[str] = None, 
                        progress_callback=None) -> Tuple[bool, str]:
        """
        Download Nemo release.
        
        Args:
            version: Specific version to download (default: latest)
            progress_callback: Function to report progress
            
        Returns:
            (success, filepath_or_error)
        """
        # Get release info
        release = self.get_latest_release()
        if not release:
            return False, "Failed to fetch release info from GitHub"
        
        download_url = release.get('download_url')
        if not download_url:
            return False, "No downloadable asset found in latest release"
        
        version = release['version']
        filename = f"nemo-{version}.zip"
        filepath = self.release_download_path / filename
        
        try:
            logger.info(f"Downloading Nemo {version}...")
            
            # Download file
            req = Request(download_url, headers={'User-Agent': 'Nemo-Installer'})
            downloaded_size = 0
            chunk_size = 8192
            
            with urlopen(req, timeout=30) as response:
                total_size = int(response.headers.get('content-length', 0))
                
                with open(filepath, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            progress_callback(progress)
            
            logger.info(f"Downloaded to {filepath}")
            return True, str(filepath)
            
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return False, str(e)
    
    def verify_checksum(self, filepath: Path, expected_hash: str) -> bool:
        """Verify downloaded file integrity."""
        try:
            sha256_hash = hashlib.sha256()
            with open(filepath, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            
            computed_hash = sha256_hash.hexdigest()
            return computed_hash.lower() == expected_hash.lower()
            
        except Exception as e:
            logger.error(f"Checksum verification failed: {e}")
            return False
    
    def extract_release(self, filepath: Path) -> Tuple[bool, str]:
        """
        Extract Nemo release.
        
        Returns:
            (success, extracted_path_or_error)
        """
        try:
            extract_path = self.release_download_path / "extracted"
            extract_path.mkdir(exist_ok=True)
            
            logger.info(f"Extracting {filepath.name}...")
            
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            logger.info(f"Extracted to {extract_path}")
            return True, str(extract_path)
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return False, str(e)
    
    def install_release(self, extract_path: Path) -> Tuple[bool, str]:
        """
        Install extracted release.
        
        Returns:
            (success, message)
        """
        try:
            # Remove old installation
            if self.nemo_install_path.exists():
                logger.info("Removing old installation...")
                shutil.rmtree(self.nemo_install_path)
            
            # Copy to install location
            logger.info(f"Installing to {self.nemo_install_path}...")
            shutil.copytree(extract_path, self.nemo_install_path)
            
            # Install Python dependencies
            logger.info("Installing dependencies...")
            req_file = self.nemo_install_path / "requirements.txt"
            if req_file.exists():
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-r", str(req_file)]
                )
            
            # Create manifest
            manifest = {
                'installed_at': datetime.now().isoformat(),
                'version': self._get_version_from_path(self.nemo_install_path),
                'install_path': str(self.nemo_install_path),
            }
            
            with open(self.NEMO_CONFIG_FILE, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info("Installation complete!")
            return True, str(self.nemo_install_path)
            
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            return False, str(e)
    
    def _get_version_from_path(self, path: Path) -> str:
        """Extract version from installed Nemo."""
        try:
            version_file = path / "VERSION"
            if version_file.exists():
                return version_file.read_text().strip()
        except:
            pass
        return "unknown"
    
    def get_installed_version(self) -> Optional[str]:
        """Get currently installed Nemo version."""
        try:
            if self.NEMO_CONFIG_FILE.exists():
                with open(self.NEMO_CONFIG_FILE) as f:
                    manifest = json.load(f)
                return manifest.get('version')
        except Exception as e:
            logger.error(f"Failed to read manifest: {e}")
        return None
    
    def check_for_updates(self) -> Tuple[bool, Optional[str]]:
        """
        Check if updates are available.
        
        Returns:
            (update_available, new_version)
        """
        current = self.get_installed_version()
        latest = self.get_latest_release()
        
        if not latest:
            return False, None
        
        latest_version = latest['version']
        
        # Simple version comparison (assumes semantic versioning)
        if current and current != latest_version:
            return True, latest_version
        
        return False, None
    
    def cleanup(self):
        """Clean up old downloaded releases."""
        try:
            for file in self.release_download_path.glob("*.zip"):
                file.unlink()
                logger.info(f"Cleaned up {file.name}")
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")


class InstallationWizard:
    """Interactive installation wizard."""
    
    def __init__(self):
        self.manager = DownloadManager()
    
    def run(self):
        """Run installation wizard."""
        print("\n" + "="*70)
        print("NEMO INSTALLATION WIZARD")
        print("="*70)
        
        # Check for updates
        print("\n[*] Checking for latest Nemo release...")
        release = self.manager.get_latest_release()
        
        if not release:
            print("[!] Failed to fetch release info. Check your internet connection.")
            return False
        
        print(f"[✓] Found: {release['name']} ({release['version']})")
        
        # Download
        print("\n[*] Downloading Nemo...")
        success, result = self.manager.download_release(
            progress_callback=self._progress_callback
        )
        
        if not success:
            print(f"[!] Download failed: {result}")
            return False
        
        filepath = Path(result)
        print(f"[✓] Downloaded to {filepath}")
        
        # Extract
        print("\n[*] Extracting release...")
        success, extract_path = self.manager.extract_release(filepath)
        
        if not success:
            print(f"[!] Extraction failed: {extract_path}")
            return False
        
        print(f"[✓] Extracted")
        
        # Install
        print("\n[*] Installing Nemo...")
        success, install_path = self.manager.install_release(Path(extract_path))
        
        if not success:
            print(f"[!] Installation failed: {install_path}")
            return False
        
        print(f"[✓] Installed to {install_path}")
        
        # Cleanup
        print("\n[*] Cleaning up...")
        self.manager.cleanup()
        
        print("\n" + "="*70)
        print("[✓] INSTALLATION COMPLETE")
        print("="*70)
        print(f"\nNemo is ready! Run: nemo start")
        print(f"Configuration: ~/.nemo/")
        print(f"Setup wizard: nemo setup")
        
        return True
    
    def _progress_callback(self, progress: float):
        """Display download progress."""
        bar_length = 50
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f"\r[*] Downloading... [{bar}] {progress:.1f}%", end='', flush=True)


def main():
    """Run installation wizard."""
    wizard = InstallationWizard()
    success = wizard.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
