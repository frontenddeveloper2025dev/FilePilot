"""
File Operations Module
Handles all file system operations including copy, move, delete, create, etc.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
import subprocess
import platform

class FileOperations:
    def __init__(self):
        """Initialize file operations handler"""
        self.system = platform.system()
    
    def get_directory_contents(self, path):
        """Get contents of a directory with file information"""
        try:
            path = Path(path)
            items = []
            
            # Add parent directory entry if not at root
            if path.parent != path:
                items.append({
                    'name': '..',
                    'type': 'Folder',
                    'size': None,
                    'modified': None,
                    'path': path.parent
                })
            
            # Get all items in directory
            for item in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
                try:
                    stat = item.stat()
                    
                    item_info = {
                        'name': item.name,
                        'type': 'Folder' if item.is_dir() else self.get_file_type(item),
                        'size': stat.st_size if item.is_file() else None,
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'path': item
                    }
                    
                    items.append(item_info)
                    
                except (OSError, PermissionError):
                    # Skip items we can't access
                    continue
            
            return items
            
        except (OSError, PermissionError) as e:
            raise Exception(f"Cannot access directory: {e}")
    
    def get_file_type(self, file_path):
        """Determine file type based on extension"""
        if file_path.is_dir():
            return 'Folder'
        
        suffix = file_path.suffix.lower()
        
        # Define file type mappings
        type_map = {
            '.txt': 'Text File',
            '.doc': 'Word Document',
            '.docx': 'Word Document',
            '.pdf': 'PDF Document',
            '.jpg': 'JPEG Image',
            '.jpeg': 'JPEG Image',
            '.png': 'PNG Image',
            '.gif': 'GIF Image',
            '.bmp': 'Bitmap Image',
            '.mp3': 'MP3 Audio',
            '.wav': 'WAV Audio',
            '.mp4': 'MP4 Video',
            '.avi': 'AVI Video',
            '.zip': 'ZIP Archive',
            '.rar': 'RAR Archive',
            '.exe': 'Executable',
            '.py': 'Python File',
            '.js': 'JavaScript File',
            '.html': 'HTML Document',
            '.css': 'CSS File',
            '.xml': 'XML File',
            '.json': 'JSON File'
        }
        
        return type_map.get(suffix, 'File')
    
    def create_folder(self, folder_path):
        """Create a new folder"""
        try:
            folder_path = Path(folder_path)
            if folder_path.exists():
                raise Exception(f"Folder already exists: {folder_path.name}")
            
            folder_path.mkdir(parents=True, exist_ok=False)
            
        except OSError as e:
            raise Exception(f"Cannot create folder: {e}")
    
    def create_file(self, file_path):
        """Create a new empty file"""
        try:
            file_path = Path(file_path)
            if file_path.exists():
                raise Exception(f"File already exists: {file_path.name}")
            
            file_path.touch()
            
        except OSError as e:
            raise Exception(f"Cannot create file: {e}")
    
    def copy_item(self, source_path, dest_path):
        """Copy a file or directory"""
        try:
            source_path = Path(source_path)
            dest_path = Path(dest_path)
            
            # Handle name conflicts
            if dest_path.exists():
                base_name = dest_path.stem
                suffix = dest_path.suffix
                counter = 1
                
                while dest_path.exists():
                    if dest_path.is_dir():
                        dest_path = dest_path.parent / f"{base_name} ({counter})"
                    else:
                        dest_path = dest_path.parent / f"{base_name} ({counter}){suffix}"
                    counter += 1
            
            if source_path.is_dir():
                shutil.copytree(source_path, dest_path)
            else:
                shutil.copy2(source_path, dest_path)
                
        except (OSError, shutil.Error) as e:
            raise Exception(f"Cannot copy item: {e}")
    
    def move_item(self, source_path, dest_path):
        """Move a file or directory"""
        try:
            source_path = Path(source_path)
            dest_path = Path(dest_path)
            
            # Handle name conflicts
            if dest_path.exists():
                base_name = dest_path.stem
                suffix = dest_path.suffix
                counter = 1
                
                while dest_path.exists():
                    if dest_path.is_dir():
                        dest_path = dest_path.parent / f"{base_name} ({counter})"
                    else:
                        dest_path = dest_path.parent / f"{base_name} ({counter}){suffix}"
                    counter += 1
            
            shutil.move(str(source_path), str(dest_path))
            
        except (OSError, shutil.Error) as e:
            raise Exception(f"Cannot move item: {e}")
    
    def delete_item(self, item_path):
        """Delete a file or directory"""
        try:
            item_path = Path(item_path)
            
            if item_path.is_dir():
                shutil.rmtree(item_path)
            else:
                item_path.unlink()
                
        except (OSError, shutil.Error) as e:
            raise Exception(f"Cannot delete item: {e}")
    
    def rename_item(self, old_path, new_path):
        """Rename a file or directory"""
        try:
            old_path = Path(old_path)
            new_path = Path(new_path)
            
            if new_path.exists():
                raise Exception(f"An item with that name already exists")
            
            old_path.rename(new_path)
            
        except OSError as e:
            raise Exception(f"Cannot rename item: {e}")
    
    def get_item_properties(self, item_path):
        """Get detailed properties of a file or directory"""
        try:
            item_path = Path(item_path)
            stat = item_path.stat()
            
            # Calculate size for directories
            if item_path.is_dir():
                size = self.get_directory_size(item_path)
                size_str = self.format_size(size)
            else:
                size_str = self.format_size(stat.st_size)
            
            properties = {
                'name': item_path.name,
                'type': 'Folder' if item_path.is_dir() else self.get_file_type(item_path),
                'size': size_str,
                'location': str(item_path.parent),
                'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'accessed': datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return properties
            
        except OSError as e:
            raise Exception(f"Cannot get item properties: {e}")
    
    def get_directory_size(self, directory_path):
        """Calculate total size of a directory"""
        total_size = 0
        try:
            for path in directory_path.rglob('*'):
                if path.is_file():
                    try:
                        total_size += path.stat().st_size
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            pass
        
        return total_size
    
    def format_size(self, size_bytes):
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def open_file(self, file_path):
        """Open a file with the default system application"""
        try:
            file_path = Path(file_path).resolve()
            
            # Validate that the file exists and is a regular file or directory
            if not file_path.exists():
                raise Exception("File does not exist")
            
            if self.system == "Windows":
                # Use subprocess for better cross-platform compatibility
                subprocess.run(["cmd", "/c", "start", "", str(file_path)], shell=True, check=True)
            elif self.system == "Darwin":  # macOS
                subprocess.run(["open", str(file_path)], check=True)
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", str(file_path)], check=True)
                
        except Exception as e:
            raise Exception(f"Cannot open file: {e}")
    
    def get_drives(self):
        """Get available drives on the system"""
        drives = []
        
        if self.system == "Windows":
            # Get Windows drives
            import string
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append(Path(drive))
        else:
            # Unix-like systems
            drives = [Path("/")]
            
            # Add common mount points
            mount_points = ["/mnt", "/media", "/Volumes"]
            for mount_point in mount_points:
                if os.path.exists(mount_point):
                    try:
                        for item in os.listdir(mount_point):
                            full_path = Path(mount_point) / item
                            if full_path.is_dir():
                                drives.append(full_path)
                    except PermissionError:
                        continue
        
        return drives
