#!/usr/bin/env python3
"""
Vercel entry point for File Manager Application
"""

import os
import sys

# Add the parent directory to Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_server import app

# Vercel requires the app to be named 'app' and be callable
if __name__ == "__main__":
    app.run()