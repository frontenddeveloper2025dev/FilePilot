#!/usr/bin/env python3
"""
File Manager Application Entry Point
A Python desktop file manager with PySimpleGUI interface
"""

import sys
import os
from file_manager import FileManagerApp

def main():
    """Main entry point for the file manager application"""
    try:
        # Create and run the file manager application
        app = FileManagerApp()
        app.run()
    except Exception as e:
        print(f"Error starting file manager: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
