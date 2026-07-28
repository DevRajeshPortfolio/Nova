# debug.py
# Nova Programming Language - Debugging Support

import sys
import traceback
import time
from datetime import datetime

class Debugger:
    """Interactive debugger for Nova"""
    
    def __init__(self):
        self.breakpoints = {}
        self.watch_variables = []
        self.call_stack = []
        self.step_mode = 'none'
        self._stopped = False
        self._variables = {}
        self._current_line = None
        self._current_file = None
    
    def set_breakpoint(self, filename, line):
        """Set a breakpoint"""
        if filename not in self.breakpoints:
            self.breakpoints[filename] = []
        if line not in self.breakpoints[filename]:
            self.breakpoints[filename].append(line)
    
    def remove_breakpoint(self, filename, line):
        """Remove a breakpoint"""
        if filename in self.breakpoints:
            if line in self.breakpoints[filename]:
                self.breakpoints[filename].remove(line)
    
    def should_stop(self, filename, line):
        """Check if execution should stop"""
        if filename in self.breakpoints:
            return line in self.breakpoints[filename]
        return False
    
    def stop(self, filename, line, variables):
        """Stop execution at breakpoint"""
        self._stopped = True
        self._current_file = filename
        self._current_line = line
        self._variables = variables
        
        print(f"\n🔴 Breakpoint at {filename}:{line}")
        print("Variables:")
        for name, value in variables.items():
            print(f"  {name} = {value}")
        
        self._interactive_loop()
    
    def _interactive_loop(self):
        """Interactive debugging loop"""
        commands = {
            'c': self._continue,
            'n': self._next,
            's': self._step,
            'p': self._print_var,
            'w': self._watch,
            'b': self._set_breakpoint,
            'r': self._remove_breakpoint,
            'l': self._list_breakpoints,
            'q': self._quit
        }
        
        while self._stopped:
            try:
                cmd = input("(nova-debug) ").strip()
                if not cmd:
                    continue
                
                parts = cmd.split()
                command = parts[0].lower()
                
                if command in commands:
                    commands[command](*parts[1:])
                else:
                    print(f"Unknown command: {command}")
                    print("Available commands: c(continue), n(next), s(step), p(var), w(var), b(line), r(line), l(list), q(quit)")
            except KeyboardInterrupt:
                print()
                continue
            except Exception as e:
                print(f"Error: {e}")
    
    def _continue(self, *args):
        """Continue execution"""
        self._stopped = False
        print("▶️ Continuing...")
    
    def _next(self, *args):
        """Step to next line"""
        self.step_mode = 'step_over'
        self._stopped = False
        print("⏭️ Stepping over...")
    
    def _step(self, *args):
        """Step into function"""
        self.step_mode = 'step_into'
        self._stopped = False
        print("⏬ Stepping into...")
    
    def _print_var(self, *args):
        """Print variable value"""
        if args:
            name = args[0]
            if name in self._variables:
                print(f"{name} = {self._variables[name]}")
            else:
                print(f"Variable '{name}' not found")
        else:
            print("Usage: p <variable>")
    
    def _watch(self, *args):
        """Add variable to watch list"""
        if args:
            name = args[0]
            if name not in self.watch_variables:
                self.watch_variables.append(name)
                print(f"Watching '{name}'")
            else:
                print(f"Already watching '{name}'")
        else:
            print("Usage: w <variable>")
    
    def _set_breakpoint(self, *args):
        """Set breakpoint"""
        if args:
            try:
                line = int(args[0])
                self.set_breakpoint(self._current_file, line)
                print(f"Breakpoint set at line {line}")
            except ValueError:
                print("Usage: b <line>")
        else:
            print("Usage: b <line>")
    
    def _remove_breakpoint(self, *args):
        """Remove breakpoint"""
        if args:
            try:
                line = int(args[0])
                self.remove_breakpoint(self._current_file, line)
                print(f"Breakpoint removed at line {line}")
            except ValueError:
                print("Usage: r <line>")
        else:
            print("Usage: r <line>")
    
    def _list_breakpoints(self, *args):
        """List breakpoints"""
        if self.breakpoints:
            print("Breakpoints:")
            for filename, lines in self.breakpoints.items():
                print(f"  {filename}: {', '.join(map(str, lines))}")
        else:
            print("No breakpoints set")
    
    def _quit(self, *args):
        """Quit debugger"""
        print("👋 Exiting debugger...")
        sys.exit(0)


class ErrorHandler:
    """Error handler with detailed reporting"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.error_handlers = {}
    
    def register_handler(self, error_type, handler):
        """Register a custom error handler"""
        self.error_handlers[error_type] = handler
    
    def handle_error(self, error):
        """Handle an error"""
        error_type = type(error).__name__
        if error_type in self.error_handlers:
            return self.error_handlers[error_type](error)
        else:
            return self.default_handler(error)
    
    def default_handler(self, error):
        """Default error handling"""
        error_info = {
            'type': type(error).__name__,
            'message': str(error),
            'timestamp': datetime.now().isoformat()
        }
        
        if hasattr(error, '__traceback__'):
            error_info['traceback'] = ''.join(
                traceback.format_exception(type(error), error, error.__traceback__)
            )
        
        self.errors.append(error_info)
        return error_info
    
    def report_error(self, error):
        """Report an error to the user"""
        error_info = self.handle_error(error)
        
        print(f"\n❌ Error: {error_info['message']}")
        if 'traceback' in error_info:
            print("\nTraceback:")
            print(error_info['traceback'])
        
        return error_info


class Logger:
    """Logging system"""
    
    def __init__(self, log_level='info'):
        self.log_level = log_level
        self.logs = []
        self._levels = {
            'debug': 0,
            'info': 1,
            'warning': 2,
            'error': 3
        }
    
    def log(self, message, level='info', category=None):
        """Log a message"""
        if self._levels.get(level, 1) >= self._levels.get(self.log_level, 1):
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'level': level,
                'message': message,
                'category': category
            }
            self.logs.append(log_entry)
            
            # Print to console
            prefix = {
                'debug': '🔍',
                'info': 'ℹ️',
                'warning': '⚠️',
                'error': '❌'
            }.get(level, '📝')
            
            print(f"{prefix} {message}")
    
    def debug(self, message, category=None):
        self.log(message, 'debug', category)
    
    def info(self, message, category=None):
        self.log(message, 'info', category)
    
    def warning(self, message, category=None):
        self.log(message, 'warning', category)
    
    def error(self, message, category=None):
        self.log(message, 'error', category)
    
    def get_logs(self, level=None, category=None):
        """Get filtered logs"""
        result = []
        for log in self.logs:
            if level and log['level'] != level:
                continue
            if category and log['category'] != category:
                continue
            result.append(log)
        return result
    
    def clear(self):
        """Clear logs"""
        self.logs = []
    
    def to_json(self):
        """Export logs to JSON"""
        import json
        return json.dumps(self.logs, indent=2)