# asset_pipeline.py
# Asset Pipeline for CDN Integration

import hashlib
import os
import json
from pathlib import Path

class AssetPipeline:
    """Asset pipeline for CDN deployment"""
    
    def __init__(self, public_dir: str = 'public'):
        self.public_dir = public_dir
        self.manifest = {}
        self.cdn_url = None
    
    def set_cdn_url(self, url: str):
        """Set CDN URL for assets"""
        self.cdn_url = url
    
    def process_assets(self):
        """Process assets for CDN"""
        assets = {}
        
        for root, dirs, files in os.walk(self.public_dir):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.public_dir)
                
                # Generate hash
                with open(file_path, 'rb') as f:
                    content = f.read()
                    file_hash = hashlib.md5(content).hexdigest()[:8]
                
                # Versioned filename
                name, ext = os.path.splitext(file)
                versioned = f"{name}-{file_hash}{ext}"
                
                # Add to manifest
                assets[rel_path] = {
                    'path': rel_path,
                    'versioned': versioned,
                    'hash': file_hash,
                    'cdn_url': f"{self.cdn_url}/{versioned}" if self.cdn_url else None
                }
        
        self.manifest = assets
        return assets
    
    def get_asset_url(self, asset_path: str) -> str:
        """Get CDN URL for an asset"""
        if asset_path in self.manifest:
            asset = self.manifest[asset_path]
            return asset.get('cdn_url') or asset['versioned']
        return asset_path
    
    def save_manifest(self, path: str = 'manifest.json'):
        """Save manifest to file"""
        with open(path, 'w') as f:
            json.dump(self.manifest, f, indent=2)