# plugins.py
# Nova Programming Language - Plugin System

import os
import sys
import json
import importlib
from pathlib import Path

class Plugin:
    """Base plugin class"""
    
    def __init__(self, name, version='0.1.0', author=''):
        self.name = name
        self.version = version
        self.author = author
        self.hooks = {}
        self.config = {}
        self._enabled = True
    
    def enable(self):
        """Enable the plugin"""
        self._enabled = True
        if hasattr(self, 'on_enable'):
            self.on_enable()
    
    def disable(self):
        """Disable the plugin"""
        self._enabled = False
        if hasattr(self, 'on_disable'):
            self.on_disable()
    
    def register_hook(self, hook_name, handler):
        """Register a hook handler"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(handler)
    
    def set_config(self, key, value):
        """Set plugin configuration"""
        self.config[key] = value
    
    def get_config(self, key, default=None):
        """Get plugin configuration"""
        return self.config.get(key, default)
    
    def load_config(self, config_path):
        """Load configuration from file"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config.update(json.load(f))
    
    def save_config(self, config_path):
        """Save configuration to file"""
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)


class PluginManager:
    """Plugin manager"""
    
    def __init__(self, plugins_dir='plugins'):
        self.plugins_dir = plugins_dir
        self.plugins = {}
        self.hooks = {}
        self._loaded = False
    
    def load_plugins(self):
        """Load all plugins from plugins directory"""
        if self._loaded:
            return
        
        os.makedirs(self.plugins_dir, exist_ok=True)
        
        # Load plugins from directory
        for item in os.listdir(self.plugins_dir):
            plugin_path = os.path.join(self.plugins_dir, item)
            
            if os.path.isdir(plugin_path):
                # Directory plugin
                self._load_directory_plugin(plugin_path)
            elif item.endswith('.py'):
                # Python plugin
                self._load_python_plugin(plugin_path)
            elif item.endswith('.json'):
                # JSON plugin configuration
                self._load_json_plugin(plugin_path)
        
        self._loaded = True
        print(f"🔌 Loaded {len(self.plugins)} plugins")
    
    def _load_directory_plugin(self, plugin_path):
        """Load a plugin from a directory"""
        # Check for plugin metadata
        metadata_path = os.path.join(plugin_path, 'plugin.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            name = metadata.get('name', os.path.basename(plugin_path))
            version = metadata.get('version', '0.1.0')
            author = metadata.get('author', 'Unknown')
            
            plugin = Plugin(name, version, author)
            plugin.config = metadata.get('config', {})
            
            # Load hooks from directory
            hooks_dir = os.path.join(plugin_path, 'hooks')
            if os.path.exists(hooks_dir):
                for hook_file in os.listdir(hooks_dir):
                    if hook_file.endswith('.py'):
                        hook_name = hook_file[:-3]
                        # Load hook handler
                        self._load_hook_from_file(
                            os.path.join(hooks_dir, hook_file),
                            hook_name,
                            plugin
                        )
            
            self.plugins[name] = plugin
            return plugin
        
        return None
    
    def _load_python_plugin(self, plugin_path):
        """Load a Python plugin"""
        try:
            spec = importlib.util.spec_from_file_location(
                os.path.basename(plugin_path)[:-3],
                plugin_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'create_plugin'):
                plugin = module.create_plugin()
                if isinstance(plugin, Plugin):
                    self.plugins[plugin.name] = plugin
                    return plugin
        except Exception as e:
            print(f"⚠️ Failed to load plugin {plugin_path}: {e}")
        
        return None
    
    def _load_json_plugin(self, plugin_path):
        """Load a JSON plugin configuration"""
        with open(plugin_path, 'r') as f:
            data = json.load(f)
        
        name = data.get('name', os.path.basename(plugin_path)[:-5])
        version = data.get('version', '0.1.0')
        author = data.get('author', 'Unknown')
        
        plugin = Plugin(name, version, author)
        plugin.config = data.get('config', {})
        
        self.plugins[name] = plugin
        return plugin
    
    def _load_hook_from_file(self, file_path, hook_name, plugin):
        """Load a hook handler from a file"""
        try:
            spec = importlib.util.spec_from_file_location(
                f"{plugin.name}.{hook_name}",
                file_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'handler'):
                plugin.register_hook(hook_name, module.handler)
        except Exception as e:
            print(f"⚠️ Failed to load hook {hook_name}: {e}")
    
    def get_plugin(self, name):
        """Get a plugin by name"""
        return self.plugins.get(name)
    
    def enable_plugin(self, name):
        """Enable a plugin"""
        plugin = self.plugins.get(name)
        if plugin:
            plugin.enable()
            return True
        return False
    
    def disable_plugin(self, name):
        """Disable a plugin"""
        plugin = self.plugins.get(name)
        if plugin:
            plugin.disable()
            return True
        return False
    
    def register_hook(self, hook_name, handler):
        """Register a hook handler"""
        if hook_name not in self.hooks:
            self.hooks[hook_name] = []
        self.hooks[hook_name].append(handler)
    
    def run_hook(self, hook_name, *args, **kwargs):
        """Run all hook handlers for an event"""
        results = []
        
        # Run plugin hooks
        for plugin in self.plugins.values():
            if plugin._enabled and hook_name in plugin.hooks:
                for handler in plugin.hooks[hook_name]:
                    try:
                        result = handler(*args, **kwargs)
                        results.append(result)
                    except Exception as e:
                        print(f"⚠️ Error in plugin {plugin.name} hook {hook_name}: {e}")
        
        # Run global hooks
        if hook_name in self.hooks:
            for handler in self.hooks[hook_name]:
                try:
                    result = handler(*args, **kwargs)
                    results.append(result)
                except Exception as e:
                    print(f"⚠️ Error in global hook {hook_name}: {e}")
        
        return results
    
    def list_plugins(self):
        """List all plugins"""
        if not self.plugins:
            print("No plugins loaded")
            return
        
        print("🔌 Plugins:")
        for name, plugin in self.plugins.items():
            status = "✅" if plugin._enabled else "❌"
            print(f"  {status} {name} v{plugin.version} by {plugin.author}")
    
    def reload_plugins(self):
        """Reload all plugins"""
        self._loaded = False
        self.plugins.clear()
        self.hooks.clear()
        self.load_plugins()


def create_plugin(name, version='0.1.0', author=''):
    """Create a new plugin"""
    plugin = Plugin(name, version, author)
    
    # Create plugin directory structure
    plugin_dir = os.path.join('plugins', name)
    os.makedirs(plugin_dir, exist_ok=True)
    os.makedirs(os.path.join(plugin_dir, 'hooks'), exist_ok=True)
    
    # Create plugin.json
    metadata = {
        'name': name,
        'version': version,
        'author': author,
        'description': f'{name} plugin for Nova',
        'config': {}
    }
    
    with open(os.path.join(plugin_dir, 'plugin.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Create example hook
    hook_content = '''
# Example hook handler
def handler(*args, **kwargs):
    print(f"Hook triggered with {args} and {kwargs}")
    return "Hook executed"
'''
    
    with open(os.path.join(plugin_dir, 'hooks', 'example_hook.py'), 'w') as f:
        f.write(hook_content)
    
    print(f"✅ Created plugin: {plugin_dir}")
    return plugin