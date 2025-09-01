#!/usr/bin/env python3
"""
File Manager Application Entry Point
A Python web-based file manager with Flask interface
"""

import sys
import os
from web_server import app

def main():
    """Main entry point for the file manager web application"""
    try:
        print("Starting File Manager Web Server on port 5000...")
        # Run the Flask web application
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"Error starting file manager web server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
