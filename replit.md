# File Manager Application

## Overview

This is a Python-based file manager application that has evolved from a desktop tkinter application to a web-based file management system. The application provides a browser-based interface for common file system operations including navigation, file uploads, downloads, directory creation, and search functionality. It's designed for deployment on serverless platforms like Vercel and includes both local development capabilities and cloud deployment configurations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Web Framework Architecture
The application uses Flask as the primary web framework, providing a lightweight and flexible foundation for the file management interface. The web server (`web_server.py`) handles all HTTP routing and serves HTML templates through Jinja2 templating engine.

### Modular Design Pattern
The codebase follows a clear separation of concerns with three main modules:
- **FileOperations Module**: Encapsulates all file system operations including directory traversal, file type detection, and metadata extraction
- **Utils Module**: Provides utility functions for formatting file sizes, datetime handling, and filename validation
- **Web Server Module**: Manages HTTP requests, template rendering, and API endpoints

### Template-Based UI Architecture
The user interface is built using server-side rendering with Jinja2 templates:
- **Base Template**: Provides consistent layout, styling, and navigation structure
- **Index Template**: Main file browser interface with upload and folder creation capabilities
- **Search Template**: Dedicated search results page with filtering capabilities
- **Error Template**: Standardized error handling and user feedback

### File System Integration
File operations leverage Python's standard library (`pathlib`, `os`, `shutil`) for cross-platform compatibility. The application maintains session state through global variables tracking the current directory and implements secure file handling with path validation.

### Security Features
The application includes several security measures:
- Path validation to prevent directory traversal attacks
- Secure file handling with proper input sanitization
- Cache control headers to prevent browser caching of sensitive data
- Command injection prevention in file operations

### Deployment Architecture
The application supports multiple deployment scenarios:
- **Local Development**: Direct Flask development server execution
- **Vercel Serverless**: Configured with `vercel.json` for serverless deployment
- **Gunicorn Production**: WSGI server support for traditional hosting environments

### State Management
The application uses server-side state management with global variables to track:
- Current working directory
- User navigation history
- File operation context

### API Structure
RESTful endpoints handle file operations:
- GET `/` - Main file browser interface
- POST `/navigate` - Directory navigation
- GET `/search` - File search functionality
- POST `/upload` - File upload handling
- POST `/create_folder` - Directory creation
- GET `/download/<filename>` - File download

## External Dependencies

### Python Web Framework
- **Flask 3.1.2**: Core web framework providing routing, templating, and request handling
- **Jinja2 3.1.6**: Template engine for server-side HTML rendering
- **Werkzeug 3.1.3**: WSGI utility library underlying Flask

### Production Server
- **Gunicorn 23.0.0**: Python WSGI HTTP Server for production deployments

### Security and Utilities
- **MarkupSafe 3.0.2**: String handling and XSS prevention
- **Click 8.2.1**: Command-line interface utilities
- **ItsDangerous 2.2.0**: Cryptographic signing for secure data handling
- **Blinker 1.9.0**: Signal/event handling system

### Deployment Platform
- **Vercel**: Serverless deployment platform with automatic scaling and global CDN
- **Python 3.11.9**: Runtime environment specified in `runtime.txt`

### File System Operations
Built entirely on Python standard library modules for maximum compatibility and minimal external dependencies:
- `pathlib` for modern path handling
- `os` and `shutil` for file system operations
- `platform` for cross-platform compatibility detection