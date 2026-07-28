# deploy.py
# Deployment Configuration for Nova

import os
import yaml
import json
from typing import Dict, List, Optional

class DeploymentConfig:
    """Deployment configuration for Nova applications"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load deployment configuration"""
        with open(self.config_path, 'r') as f:
            if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                return yaml.safe_load(f)
            return json.load(f)
    
    def get_environment_variables(self) -> Dict:
        """Get environment variables for deployment"""
        env = self.config.get('environment', {})
        
        # Add deployment-specific variables
        env.update({
            'NOVA_ENV': self.config.get('env', 'production'),
            'NOVA_VERSION': self.config.get('version', '1.0.0'),
            'NOVA_DEPLOYMENT_ID': os.environ.get('DEPLOYMENT_ID', 'unknown')
        })
        
        return env
    
    def get_replicas(self) -> int:
        """Get number of replicas"""
        return self.config.get('replicas', 1)
    
    def get_health_check(self) -> Dict:
        """Get health check configuration"""
        return self.config.get('health_check', {
            'path': '/health',
            'interval': 30,
            'timeout': 10,
            'healthy_threshold': 2,
            'unhealthy_threshold': 3
        })
    
    def get_resources(self) -> Dict:
        """Get resource limits"""
        return self.config.get('resources', {
            'cpu': {'request': '100m', 'limit': '500m'},
            'memory': {'request': '256Mi', 'limit': '1Gi'}
        })