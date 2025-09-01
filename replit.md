# File Manager Application

## Overview

This is a Python desktop file manager application built with tkinter that provides a graphical interface for common file system operations. The application allows users to navigate directories, manage files and folders, and perform operations like copy, cut, paste, and delete through an intuitive GUI interface. It includes advanced features like search functionality and sorting capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure
The application follows a modular design with clear separation of concerns:

- **Main Application (`file_manager.py`)**: Contains the `FileManagerApp` class that handles the tkinter interface, user interactions, and overall application state management
- **File Operations (`file_operations.py`)**: Encapsulates all file system operations in the `FileOperations` class, providing methods for directory traversal, file manipulation, and system-specific operations
- **Utilities (`utils.py`)**: Provides helper functions through the `Utils` class for formatting, validation, and common operations like file size formatting and datetime handling
- **Entry Point (`main.py`)**: Simple application launcher that instantiates and runs the main application

### GUI Framework
The application uses tkinter as the primary GUI framework, which comes built-in with Python and provides excellent cross-platform compatibility. The interface includes:
- Menu system with File, Edit, View, and Help menus
- Toolbar with common navigation and operation buttons
- Search bar for finding files and directories
- Sortable column headers for organizing files by name, size, type, or date
- Context menus for right-click operations

### File System Integration
File operations are handled through Python's standard library (`pathlib`, `os`, `shutil`) with cross-platform compatibility considerations using the `platform` module. The application maintains state for:
- Current directory path
- Selected items
- Clipboard operations (copy/cut/paste)
- Search terms and filters
- Sorting preferences (column and order)

### Advanced Features
- **Search Functionality**: Real-time search that filters files and directories as you type
- **Sorting Capabilities**: Click any column header to sort by name, size, type, or modification date
- **Keyboard Shortcuts**: Full support for common operations (Ctrl+C, Ctrl+V, Ctrl+X, Delete, F5, Ctrl+F)
- **Context Menus**: Right-click support for quick access to file operations

### Error Handling
The application implements error handling for common file system operations, including permission errors and invalid operations, ensuring graceful degradation when operations fail.

### Security Features
- **Secure File Opening**: The `open_file` method includes validation to prevent command injection vulnerabilities when opening files with system applications
- **Path Validation**: File paths are resolved and validated before being passed to subprocess calls
- **Command Safety**: Subprocess calls use array syntax to prevent shell injection attacks

## Recent Changes

**September 01, 2025**: Applied security patch to fix command injection vulnerability in file opening functionality. Added path validation and safer subprocess handling.

## External Dependencies

- **tkinter**: Primary GUI framework (included with Python) for creating the desktop interface
- **Python Standard Library**: Core dependencies including `pathlib`, `os`, `shutil`, `platform`, `datetime`, `threading`, and `glob`
- **Operating System**: Cross-platform compatibility with Windows, macOS, and Linux through platform-specific adaptations

The application is designed to be lightweight with zero external dependencies, relying entirely on Python's built-in modules for both file system operations and the graphical user interface.