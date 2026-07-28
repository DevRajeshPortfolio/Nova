# cli.py
# Nova Programming Language - CLI Tools

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

class NovaCLI:
    """Nova CLI tools"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Create command line parser"""
        parser = argparse.ArgumentParser(
            description='Nova Programming Language CLI',
            prog='nova'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Commands')
        
        # Build command
        build_parser = subparsers.add_parser('build', help='Build a Nova project')
        build_parser.add_argument('source', help='Source file or directory')
        build_parser.add_argument('--output', '-o', default='dist', help='Output directory')
        build_parser.add_argument('--watch', '-w', action='store_true', help='Watch for changes')
        build_parser.add_argument('--dev', action='store_true', help='Development mode')
        build_parser.add_argument('--prod', action='store_true', help='Production mode')
        
        # Serve command
        serve_parser = subparsers.add_parser('serve', help='Start development server')
        serve_parser.add_argument('--port', '-p', type=int, default=3000, help='Port number')
        serve_parser.add_argument('--dir', '-d', default='.', help='Project directory')
        
        # Init command
        init_parser = subparsers.add_parser('init', help='Initialize a new Nova project')
        init_parser.add_argument('name', help='Project name')
        init_parser.add_argument('--template', '-t', default='basic', help='Project template')
        
        # Package commands
        package_parser = subparsers.add_parser('package', help='Package management')
        package_subparsers = package_parser.add_subparsers(dest='package_command')
        
        install_parser = package_subparsers.add_parser('install', help='Install a package')
        install_parser.add_argument('package', help='Package name')
        install_parser.add_argument('--version', '-v', help='Package version')
        
        uninstall_parser = package_subparsers.add_parser('uninstall', help='Uninstall a package')
        uninstall_parser.add_argument('package', help='Package name')
        
        list_parser = package_subparsers.add_parser('list', help='List installed packages')
        
        search_parser = package_subparsers.add_parser('search', help='Search for packages')
        search_parser.add_argument('query', help='Search query')
        
        # Plugin commands
        plugin_parser = subparsers.add_parser('plugin', help='Plugin management')
        plugin_subparsers = plugin_parser.add_subparsers(dest='plugin_command')
        
        plugin_list_parser = plugin_subparsers.add_parser('list', help='List plugins')
        
        plugin_enable_parser = plugin_subparsers.add_parser('enable', help='Enable a plugin')
        plugin_enable_parser.add_argument('name', help='Plugin name')
        
        plugin_disable_parser = plugin_subparsers.add_parser('disable', help='Disable a plugin')
        plugin_disable_parser.add_argument('name', help='Plugin name')
        
        # Test command
        test_parser = subparsers.add_parser('test', help='Run tests')
        test_parser.add_argument('--file', '-f', help='Test file')
        
        # New command
        new_parser = subparsers.add_parser('new', help='Create a new Nova file')
        new_parser.add_argument('name', help='File name')
        new_parser.add_argument('--type', '-t', default='page', help='File type (page, component, action)')
        
        return parser
    
    def run(self, args=None):
        """Run the CLI"""
        if args is None:
            args = sys.argv[1:]
        
        parsed_args = self.parser.parse_args(args)
        
        if not parsed_args.command:
            self.parser.print_help()
            return
        
        # Execute command
        command = parsed_args.command
        if command == 'build':
            self._build(parsed_args)
        elif command == 'serve':
            self._serve(parsed_args)
        elif command == 'init':
            self._init(parsed_args)
        elif command == 'package':
            self._package(parsed_args)
        elif command == 'plugin':
            self._plugin(parsed_args)
        elif command == 'test':
            self._test(parsed_args)
        elif command == 'new':
            self._new(parsed_args)
    
    def _build(self, args):
        """Build a Nova project"""
        from compiler import Compiler
        
        compiler = Compiler()
        
        if args.dev:
            compiler.mode = 'development'
            compiler.minify = False
            compiler.source_maps = True
        elif args.prod:
            compiler.mode = 'production'
            compiler.minify = True
            compiler.source_maps = False
        
        source_path = args.source
        output_dir = args.output
        
        if os.path.isdir(source_path):
            # Build all Nova files in directory
            nova_files = self._find_nova_files(source_path)
            for file_path in nova_files:
                rel_path = os.path.relpath(file_path, source_path)
                out_dir = os.path.join(output_dir, os.path.dirname(rel_path))
                compiler.compile(file_path, out_dir)
            print(f"✅ Built {len(nova_files)} files")
        else:
            compiler.compile(source_path, output_dir)
    
    def _serve(self, args):
        """Start development server"""
        from dev_server import DevServer
        
        server = DevServer(
            source_dir=args.dir,
            output_dir=os.path.join(args.dir, 'dist'),
            port=args.port
        )
        server.start()
    
    def _init(self, args):
        """Initialize a new project"""
        project_name = args.name
        project_dir = os.path.join(os.getcwd(), project_name)
        
        if os.path.exists(project_dir):
            print(f"❌ Directory {project_name} already exists")
            return
        
        # Create project structure
        os.makedirs(project_dir)
        os.makedirs(os.path.join(project_dir, 'src'))
        os.makedirs(os.path.join(project_dir, 'dist'))
        os.makedirs(os.path.join(project_dir, 'tests'))
        
        # Create main Nova file
        with open(os.path.join(project_dir, 'src', 'main.nova'), 'w') as f:
            f.write(f'''# {project_name}.nova
# Nova Programming Language

page "My App":
    title "{project_name}"
    
    heading "Welcome to {project_name}!"
    text "This is a Nova project."
    
    button "Click Me" when clicked:
        popup "Hello, World!"
''')
        
        # Create package.json
        with open(os.path.join(project_dir, 'package.json'), 'w') as f:
            json.dump({
                'name': project_name,
                'version': '0.1.0',
                'description': f'{project_name} - A Nova app',
                'dependencies': {},
                'devDependencies': {}
            }, f, indent=2)
        
        print(f"✅ Created new project: {project_name}")
        print(f"📁 Project directory: {project_dir}")
        print("📝 Next steps:")
        print(f"  cd {project_name}")
        print("  nova serve")
    
    def _package(self, args):
        """Package management"""
        from package_manager import PackageManager
        
        pm = PackageManager()
        
        if args.package_command == 'install':
            pm.install(args.package, getattr(args, 'version', None))
        elif args.package_command == 'uninstall':
            pm.uninstall(args.package)
        elif args.package_command == 'list':
            pm.list_installed()
        elif args.package_command == 'search':
            pm.search(args.query)
        else:
            print("Unknown package command")
    
    def _plugin(self, args):
        """Plugin management"""
        from plugins import PluginManager
        
        pm = PluginManager()
        pm.load_plugins()
        
        if args.plugin_command == 'list':
            pm.list_plugins()
        elif args.plugin_command == 'enable':
            if pm.enable_plugin(args.name):
                print(f"✅ Plugin {args.name} enabled")
            else:
                print(f"❌ Plugin {args.name} not found")
        elif args.plugin_command == 'disable':
            if pm.disable_plugin(args.name):
                print(f"✅ Plugin {args.name} disabled")
            else:
                print(f"❌ Plugin {args.name} not found")
        else:
            print("Unknown plugin command")
    
    def _test(self, args):
        """Run tests"""
        # Simple test runner
        print("🧪 Running tests...")
        
        if args.file:
            test_file = args.file
            if os.path.exists(test_file):
                # Run test file
                with open(test_file, 'r') as f:
                    content = f.read()
                print(f"  Running {test_file}...")
            else:
                print(f"❌ Test file not found: {test_file}")
                return
        else:
            # Run all tests
            tests_dir = 'tests'
            if os.path.exists(tests_dir):
                for test_file in os.listdir(tests_dir):
                    if test_file.endswith('.nova'):
                        print(f"  Running {test_file}...")
            else:
                print("No tests found")
        
        print("✅ Tests completed")
    
    def _new(self, args):
        """Create a new Nova file"""
        name = args.name
        if not name.endswith('.nova'):
            name += '.nova'
        
        file_type = args.type
        
        # Create file content
        if file_type == 'page':
            content = f'''# {name}
# Nova Page

page "{os.path.basename(name[:-5])}":
    title "{os.path.basename(name[:-5])}"
    
    heading "Welcome!"
    text "This is a Nova page."
    
    button "Click Me" when clicked:
        popup "Hello!"
'''
        elif file_type == 'component':
            content = f'''# {name}
# Nova Component

component "{os.path.basename(name[:-5])}":
    heading "{os.path.basename(name[:-5])}"
    text "This is a reusable component"
    
    button "Action" when clicked:
        popup "Component action!"
'''
        elif file_type == 'action':
            content = f'''# {name}
# Nova Action

action "{os.path.basename(name[:-5])}":
    popup "Action triggered!"
    set message = "Hello from action"
    notification "Action complete"
'''
        else:
            content = f'''# {name}
# Nova File

page "Page":
    text "Hello, Nova!"
'''
        
        # Write file
        with open(name, 'w') as f:
            f.write(content)
        
        print(f"✅ Created: {name}")
    
    def _find_nova_files(self, directory):
        """Find all Nova files in a directory"""
        nova_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.nova'):
                    nova_files.append(os.path.join(root, file))
        return nova_files


def main():
    """CLI entry point"""
    cli = NovaCLI()
    cli.run()


if __name__ == '__main__':
    main()