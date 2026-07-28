# package_manager.py
# Nova Programming Language - Package Manager

import os
import json
import shutil
import requests
import tempfile
import zipfile
from pathlib import Path
import urllib.request

class Package:
    """Package definition"""
    
    def __init__(self, name, version='latest', source=None):
        self.name = name
        self.version = version
        self.source = source or f"https://registry.nova-lang.com/packages/{name}"
        self.metadata = None
        self.files = []
        self.dependencies = []
    
    def load_metadata(self):
        """Load package metadata"""
        try:
            response = requests.get(f"{self.source}/metadata.json")
            if response.status_code == 200:
                self.metadata = response.json()
                self.version = self.metadata.get('version', '0.1.0')
                self.dependencies = self.metadata.get('dependencies', [])
                return True
            return False
        except:
            return False


class PackageManager:
    """Package manager for Nova"""
    
    def __init__(self, project_dir='.'):
        self.project_dir = os.path.abspath(project_dir)
        self.packages_dir = os.path.join(self.project_dir, 'nova_modules')
        self.registry_url = "https://registry.nova-lang.com"
        self.installed_packages = {}
        self._load_package_json()
    
    def _load_package_json(self):
        """Load package.json if exists"""
        package_json_path = os.path.join(self.project_dir, 'package.json')
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                data = json.load(f)
                self.installed_packages = data.get('dependencies', {})
    
    def _save_package_json(self):
        """Save package.json"""
        package_json_path = os.path.join(self.project_dir, 'package.json')
        data = {
            'name': os.path.basename(self.project_dir),
            'version': '0.1.0',
            'description': 'Nova project',
            'dependencies': self.installed_packages
        }
        with open(package_json_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def install(self, package_name, version=None):
        """Install a package"""
        print(f"📦 Installing {package_name}...")
        
        # Create packages directory
        os.makedirs(self.packages_dir, exist_ok=True)
        
        # Create package
        pkg = Package(package_name, version)
        
        # Load metadata
        if not pkg.load_metadata():
            print(f"❌ Failed to load metadata for {package_name}")
            return False
        
        # Download package
        package_path = self._download_package(pkg)
        if not package_path:
            print(f"❌ Failed to download {package_name}")
            return False
        
        # Extract package
        if self._extract_package(package_path, pkg):
            self.installed_packages[package_name] = pkg.version
            self._save_package_json()
            print(f"✅ Installed {package_name} version {pkg.version}")
            return True
        
        return False
    
    def _download_package(self, pkg):
        """Download a package"""
        url = f"{self.registry_url}/packages/{pkg.name}/download/{pkg.version}"
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                temp_file.close()
                return temp_file.name
            return None
        except Exception as e:
            print(f"Download error: {e}")
            return None
    
    def _extract_package(self, zip_path, pkg):
        """Extract a package"""
        try:
            target_dir = os.path.join(self.packages_dir, pkg.name)
            os.makedirs(target_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            
            # Clean up zip file
            os.unlink(zip_path)
            return True
        except Exception as e:
            print(f"Extract error: {e}")
            return False
    
    def uninstall(self, package_name):
        """Uninstall a package"""
        if package_name in self.installed_packages:
            # Remove files
            package_dir = os.path.join(self.packages_dir, package_name)
            if os.path.exists(package_dir):
                shutil.rmtree(package_dir)
            
            # Remove from dependencies
            del self.installed_packages[package_name]
            self._save_package_json()
            print(f"🗑️ Uninstalled {package_name}")
            return True
        else:
            print(f"⚠️ Package {package_name} not installed")
            return False
    
    def list_installed(self):
        """List installed packages"""
        if self.installed_packages:
            print("📦 Installed packages:")
            for name, version in self.installed_packages.items():
                print(f"  - {name}@{version}")
        else:
            print("No packages installed")
    
    def search(self, query):
        """Search for packages"""
        try:
            response = requests.get(f"{self.registry_url}/search?q={query}")
            if response.status_code == 200:
                results = response.json()
                if results:
                    print(f"🔍 Search results for '{query}':")
                    for pkg in results:
                        print(f"  - {pkg['name']} v{pkg['version']} - {pkg.get('description', '')}")
                else:
                    print(f"No packages found for '{query}'")
            else:
                print("Failed to search packages")
        except Exception as e:
            print(f"Search error: {e}")
    
    def get_package_info(self, package_name):
        """Get package information"""
        if package_name in self.installed_packages:
            package_dir = os.path.join(self.packages_dir, package_name)
            metadata_path = os.path.join(package_dir, 'metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    return json.load(f)
        return None
    
    def import_module(self, module_name):
        """Import a module"""
        # Check if installed
        if module_name in self.installed_packages:
            module_path = os.path.join(self.packages_dir, module_name, 'index.nova')
            if os.path.exists(module_path):
                return self._load_module(module_path)
            else:
                # Try other entry points
                for ext in ['.nova', '.js', '.py']:
                    alt_path = os.path.join(self.packages_dir, module_name, f'index{ext}')
                    if os.path.exists(alt_path):
                        return self._load_module(alt_path)
        
        # Check local
        local_path = os.path.join(self.project_dir, f'{module_name}.nova')
        if os.path.exists(local_path):
            return self._load_module(local_path)
        
        return None
    
    def _load_module(self, path):
        """Load a module from path"""
        # This would load and execute the module
        # For now, just return the path
        return path


def create_package(name, version='0.1.0', description=''):
    """Create a new package"""
    # Create package structure
    package_dir = f"{name}-{version}"
    os.makedirs(package_dir, exist_ok=True)
    os.makedirs(os.path.join(package_dir, 'src'), exist_ok=True)
    
    # Create metadata.json
    metadata = {
        'name': name,
        'version': version,
        'description': description,
        'main': 'src/index.nova',
        'dependencies': [],
        'author': '',
        'license': 'MIT'
    }
    
    with open(os.path.join(package_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Create index file
    with open(os.path.join(package_dir, 'src', 'index.nova'), 'w') as f:
        f.write(f"""
# {name} - Nova Package
# Version {version}

# Export your package functionality here
export "Hello from {name}!"
""")
    
    print(f"✅ Created package: {package_dir}")
    return package_dir


def publish_package(package_dir, registry_url=None):
    """Publish a package to registry"""
    if registry_url is None:
        registry_url = "https://registry.nova-lang.com"
    
    # Validate package
    metadata_path = os.path.join(package_dir, 'metadata.json')
    if not os.path.exists(metadata_path):
        print("❌ metadata.json not found")
        return False
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Create zip
    zip_path = tempfile.NamedTemporaryFile(delete=False, suffix='.zip').name
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
    
    # Upload
    try:
        with open(zip_path, 'rb') as f:
            files = {'package': f}
            response = requests.post(
                f"{registry_url}/publish",
                data={'metadata': json.dumps(metadata)},
                files=files
            )
        
        os.unlink(zip_path)
        
        if response.status_code == 200:
            print(f"✅ Published {metadata['name']} v{metadata['version']}")
            return True
        else:
            print(f"❌ Failed to publish: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Publish error: {e}")
        return False