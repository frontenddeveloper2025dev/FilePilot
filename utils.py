"""
Utility Functions
Helper functions for formatting, validation, and common operations
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import re

class Utils:
    def __init__(self):
        """Initialize utilities"""
        pass
    
    def format_size(self, size_bytes):
        """Format file size in human-readable format"""
        if size_bytes is None:
            return ""
        
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB", "PB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        if i == 0:
            return f"{int(size)} {size_names[i]}"
        else:
            return f"{size:.1f} {size_names[i]}"
    
    def format_datetime(self, dt):
        """Format datetime in a user-friendly format"""
        if dt is None:
            return ""
        
        if isinstance(dt, datetime):
            return dt.strftime('%Y-%m-%d %H:%M')
        
        return str(dt)
    
    def is_valid_filename(self, filename):
        """Check if a filename is valid for the current OS"""
        if not filename or filename in ['.', '..']:
            return False
        
        # Check for invalid characters
        if os.name == 'nt':  # Windows
            invalid_chars = r'[<>:"/\\|?*]'
            reserved_names = [
                'CON', 'PRN', 'AUX', 'NUL',
                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
            ]
            
            if re.search(invalid_chars, filename):
                return False
            
            if filename.upper() in reserved_names:
                return False
            
            # Windows doesn't allow names ending with period or space
            if filename.endswith('.') or filename.endswith(' '):
                return False
        
        else:  # Unix-like systems
            # Only null character and forward slash are invalid
            if '\0' in filename or '/' in filename:
                return False
        
        return True
    
    def sanitize_filename(self, filename):
        """Sanitize a filename by removing/replacing invalid characters"""
        if not filename:
            return "unnamed"
        
        # Replace invalid characters with underscores
        if os.name == 'nt':  # Windows
            filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
            
            # Handle reserved names
            reserved_names = [
                'CON', 'PRN', 'AUX', 'NUL',
                'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
                'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
            ]
            
            if filename.upper() in reserved_names:
                filename = f"_{filename}"
            
            # Remove trailing periods and spaces
            filename = filename.rstrip('. ')
            
        else:  # Unix-like systems
            filename = filename.replace('\0', '').replace('/', '_')
        
        # Ensure filename is not empty after sanitization
        if not filename:
            filename = "unnamed"
        
        return filename
    
    def get_unique_name(self, base_path, name):
        """Generate a unique name by appending numbers if necessary"""
        path = Path(base_path) / name
        
        if not path.exists():
            return name
        
        # Extract base name and extension
        stem = path.stem
        suffix = path.suffix
        counter = 1
        
        while path.exists():
            if suffix:
                new_name = f"{stem} ({counter}){suffix}"
            else:
                new_name = f"{stem} ({counter})"
            
            path = Path(base_path) / new_name
            counter += 1
        
        return path.name
    
    def is_hidden_file(self, file_path):
        """Check if a file or directory is hidden"""
        file_path = Path(file_path)
        
        if os.name == 'nt':  # Windows
            try:
                import stat
                attrs = file_path.stat().st_file_attributes
                return bool(attrs & stat.FILE_ATTRIBUTE_HIDDEN)
            except (AttributeError, OSError):
                # Fallback to name-based check
                return file_path.name.startswith('.')
        else:  # Unix-like systems
            return file_path.name.startswith('.')
    
    def get_file_icon(self, file_path):
        """Get appropriate icon for file type (placeholder for future implementation)"""
        file_path = Path(file_path)
        
        if file_path.is_dir():
            return "📁"  # Folder icon
        
        # File type icons based on extension
        extension_icons = {
            '.txt': '📄',
            '.doc': '📝',
            '.docx': '📝',
            '.pdf': '📕',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.mp3': '🎵',
            '.wav': '🎵',
            '.mp4': '🎬',
            '.avi': '🎬',
            '.zip': '📦',
            '.rar': '📦',
            '.exe': '⚙️',
            '.py': '🐍',
            '.js': '📜',
            '.html': '🌐',
            '.css': '🎨'
        }
        
        return extension_icons.get(file_path.suffix.lower(), '📄')
    
    def calculate_selection_stats(self, selected_paths):
        """Calculate statistics for selected items"""
        if not selected_paths:
            return {'count': 0, 'size': 0, 'folders': 0, 'files': 0}
        
        total_size = 0
        folder_count = 0
        file_count = 0
        
        for path in selected_paths:
            path = Path(path)
            
            if path.is_dir():
                folder_count += 1
                # Calculate directory size
                try:
                    for sub_path in path.rglob('*'):
                        if sub_path.is_file():
                            try:
                                total_size += sub_path.stat().st_size
                            except (OSError, PermissionError):
                                continue
                except (OSError, PermissionError):
                    continue
            else:
                file_count += 1
                try:
                    total_size += path.stat().st_size
                except (OSError, PermissionError):
                    continue
        
        return {
            'count': len(selected_paths),
            'size': total_size,
            'folders': folder_count,
            'files': file_count
        }
    
    def get_common_file_extensions(self):
        """Get list of common file extensions for filtering"""
        return {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documents': ['.txt', '.doc', '.docx', '.pdf', '.rtf', '.odt'],
            'Audio': ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'],
            'Video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.php']
        }
    
    def escape_filename_for_display(self, filename):
        """Escape filename for safe display in GUI"""
        # Replace any potentially problematic characters for display
        return filename.replace('&', '&&')  # Escape ampersands for GUI frameworks
    
    def get_clipboard_format_info(self, items):
        """Get formatted information about clipboard contents"""
        if not items:
            return "Clipboard empty"
        
        stats = self.calculate_selection_stats(items)
        
        if stats['count'] == 1:
            item_name = Path(items[0]).name
            return f"1 item: {item_name}"
        else:
            parts = []
            if stats['folders'] > 0:
                parts.append(f"{stats['folders']} folder(s)")
            if stats['files'] > 0:
                parts.append(f"{stats['files']} file(s)")
            
            return f"{stats['count']} items: {', '.join(parts)}"
