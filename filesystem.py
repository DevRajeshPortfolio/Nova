# filesystem.py
# Nova Programming Language - File System Operations

import os
import shutil
import json
import tempfile
from datetime import datetime
import mimetypes

class FileSystem:
    """File system operations"""
    
    def __init__(self, base_path='./storage'):
        self.base_path = base_path
        self._ensure_directory(base_path)
    
    def _ensure_directory(self, path):
        """Ensure directory exists"""
        os.makedirs(path, exist_ok=True)
    
    def _safe_path(self, path):
        """Get safe full path"""
        full_path = os.path.join(self.base_path, path)
        # Prevent directory traversal
        if not os.path.abspath(full_path).startswith(os.path.abspath(self.base_path)):
            raise ValueError("Access denied")
        return full_path
    
    def read_file(self, path):
        """Read a file"""
        try:
            full_path = self._safe_path(path)
            with open(full_path, 'r', encoding='utf-8') as f:
                return {
                    'success': True,
                    'content': f.read(),
                    'path': path
                }
        except FileNotFoundError:
            return {'success': False, 'error': 'File not found'}
        except PermissionError:
            return {'success': False, 'error': 'Permission denied'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def read_binary(self, path):
        """Read a binary file"""
        try:
            full_path = self._safe_path(path)
            with open(full_path, 'rb') as f:
                return {
                    'success': True,
                    'content': f.read(),
                    'path': path
                }
        except FileNotFoundError:
            return {'success': False, 'error': 'File not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def write_file(self, path, content, encoding='utf-8'):
        """Write a file"""
        try:
            full_path = self._safe_path(path)
            # Ensure directory exists
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding=encoding) as f:
                f.write(content)
            return {'success': True, 'path': path}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def write_binary(self, path, content):
        """Write a binary file"""
        try:
            full_path = self._safe_path(path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'wb') as f:
                f.write(content)
            return {'success': True, 'path': path}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_file(self, path):
        """Delete a file"""
        try:
            full_path = self._safe_path(path)
            os.remove(full_path)
            return {'success': True, 'path': path}
        except FileNotFoundError:
            return {'success': False, 'error': 'File not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_directory(self, path, recursive=True):
        """Delete a directory"""
        try:
            full_path = self._safe_path(path)
            if recursive:
                shutil.rmtree(full_path)
            else:
                os.rmdir(full_path)
            return {'success': True, 'path': path}
        except FileNotFoundError:
            return {'success': False, 'error': 'Directory not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def rename_file(self, old_path, new_path):
        """Rename a file or directory"""
        try:
            old_full = self._safe_path(old_path)
            new_full = self._safe_path(new_path)
            os.rename(old_full, new_full)
            return {'success': True, 'old': old_path, 'new': new_path}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def copy_file(self, source, destination):
        """Copy a file"""
        try:
            src_full = self._safe_path(source)
            dst_full = self._safe_path(destination)
            os.makedirs(os.path.dirname(dst_full), exist_ok=True)
            shutil.copy2(src_full, dst_full)
            return {'success': True, 'source': source, 'destination': destination}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_directory(self, path='', include_hidden=False):
        """List directory contents"""
        try:
            full_path = self._safe_path(path)
            items = []
            
            for item in os.listdir(full_path):
                if not include_hidden and item.startswith('.'):
                    continue
                
                item_path = os.path.join(full_path, item)
                is_dir = os.path.isdir(item_path)
                size = os.path.getsize(item_path) if not is_dir else 0
                modified = datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                
                items.append({
                    'name': item,
                    'path': os.path.join(path, item).replace('\\', '/'),
                    'is_directory': is_dir,
                    'size': size,
                    'modified': modified,
                    'extension': os.path.splitext(item)[1].lower()
                })
            
            # Sort: directories first, then files
            items.sort(key=lambda x: (0 if x['is_directory'] else 1, x['name'].lower()))
            
            return {'success': True, 'items': items, 'path': path}
        except FileNotFoundError:
            return {'success': False, 'error': 'Directory not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_file_info(self, path):
        """Get file information"""
        try:
            full_path = self._safe_path(path)
            stat = os.stat(full_path)
            
            info = {
                'path': path,
                'name': os.path.basename(path),
                'is_directory': os.path.isdir(full_path),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat()
            }
            
            if not info['is_directory']:
                # Get MIME type
                mime_type, _ = mimetypes.guess_type(path)
                info['mime_type'] = mime_type or 'application/octet-stream'
                
                # Get extension
                info['extension'] = os.path.splitext(path)[1].lower()
            
            return {'success': True, 'info': info}
        except FileNotFoundError:
            return {'success': False, 'error': 'File not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_directory(self, path):
        """Create a directory"""
        try:
            full_path = self._safe_path(path)
            os.makedirs(full_path, exist_ok=True)
            return {'success': True, 'path': path}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def exists(self, path):
        """Check if path exists"""
        try:
            full_path = self._safe_path(path)
            return os.path.exists(full_path)
        except:
            return False
    
    def is_file(self, path):
        """Check if path is a file"""
        try:
            full_path = self._safe_path(path)
            return os.path.isfile(full_path)
        except:
            return False
    
    def is_directory(self, path):
        """Check if path is a directory"""
        try:
            full_path = self._safe_path(path)
            return os.path.isdir(full_path)
        except:
            return False
    
    def get_size(self, path):
        """Get file size in bytes"""
        try:
            full_path = self._safe_path(path)
            if os.path.isdir(full_path):
                total = 0
                for root, dirs, files in os.walk(full_path):
                    for f in files:
                        total += os.path.getsize(os.path.join(root, f))
                return total
            return os.path.getsize(full_path)
        except:
            return 0
    
    def find_files(self, pattern, path='', recursive=True):
        """Find files matching pattern"""
        results = []
        try:
            full_path = self._safe_path(path)
            
            if recursive:
                for root, dirs, files in os.walk(full_path):
                    for file in files:
                        if self._matches_pattern(file, pattern):
                            rel_path = os.path.join(root, file)
                            rel_path = os.path.relpath(rel_path, self.base_path)
                            results.append(rel_path)
            else:
                for item in os.listdir(full_path):
                    if self._matches_pattern(item, pattern):
                        results.append(os.path.join(path, item).replace('\\', '/'))
            
            return {'success': True, 'files': results}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _matches_pattern(self, filename, pattern):
        """Check if filename matches pattern"""
        import fnmatch
        return fnmatch.fnmatch(filename, pattern)
    
    def upload_file(self, file_data, filename, path=''):
        """Upload a file"""
        try:
            file_path = os.path.join(path, filename).replace('\\', '/')
            full_path = self._safe_path(file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Handle file_data (could be bytes or file-like object)
            if hasattr(file_data, 'read'):
                content = file_data.read()
            else:
                content = file_data
            
            with open(full_path, 'wb') as f:
                f.write(content)
            
            return {'success': True, 'path': file_path}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class TemporaryFileManager:
    """Temporary file management"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='nova_temp_')
        self.files = {}
    
    def create_temp_file(self, content=None, suffix='.tmp'):
        """Create a temporary file"""
        import uuid
        filename = f"{uuid.uuid4().hex}{suffix}"
        filepath = os.path.join(self.temp_dir, filename)
        
        with open(filepath, 'wb') as f:
            if content:
                f.write(content if isinstance(content, bytes) else content.encode())
        
        self.files[filename] = filepath
        return filename, filepath
    
    def get_temp_file(self, filename):
        """Get temporary file path"""
        return self.files.get(filename)
    
    def delete_temp_file(self, filename):
        """Delete a temporary file"""
        if filename in self.files:
            try:
                os.remove(self.files[filename])
                del self.files[filename]
                return True
            except:
                return False
        return False
    
    def cleanup(self):
        """Clean up all temporary files"""
        for filename, filepath in self.files.items():
            try:
                os.remove(filepath)
            except:
                pass
        self.files.clear()
        
        try:
            os.rmdir(self.temp_dir)
        except:
            pass