"""
Web server wrapper for the File Manager application.
Provides HTTP endpoints for file management operations compatible with Autoscale deployments.
"""

import os
import json
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from file_operations import FileOperations
from utils import Utils

app = Flask(__name__)
file_ops = FileOperations()
utils = Utils()

# Add cache control headers to prevent caching issues
@app.after_request
def add_cache_control_headers(response):
    """Add cache control headers to prevent browser caching"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Global state to track current directory
current_directory = Path.home()

@app.route('/')
def index():
    """Main file manager interface"""
    global current_directory
    try:
        directory_contents = file_ops.get_directory_contents(current_directory)
        current_path = str(current_directory)
        parent_path = str(current_directory.parent) if current_directory.parent != current_directory else None
        
        # Process files for web display
        file_list = []
        for item in directory_contents:
            if item['name'] == '..':  # Skip parent directory entry
                continue
            file_info = {
                'name': item['name'],
                'path': str(item['path']),
                'is_dir': item['type'] == 'Folder',
                'size': utils.format_size(item['size']) if item['size'] is not None else '',
                'modified': utils.format_datetime(item['modified'])
            }
            file_list.append(file_info)
        
        return render_template('index.html', 
                             files=file_list, 
                             current_path=current_path,
                             parent_path=parent_path)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/navigate', methods=['POST'])
def navigate():
    """Navigate to a different directory"""
    global current_directory
    path = request.form.get('path')
    if path:
        try:
            new_path = Path(path).resolve()
            if new_path.exists() and new_path.is_dir():
                current_directory = new_path
        except Exception as e:
            pass  # Stay in current directory if navigation fails
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to the current directory"""
    global current_directory
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '' or file.filename is None:
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        filepath = current_directory / file.filename
        file.save(str(filepath))
        return jsonify({'success': 'File uploaded successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_folder', methods=['POST'])
def create_folder():
    """Create a new folder in the current directory"""
    global current_directory
    folder_name = request.form.get('name')
    if not folder_name:
        return jsonify({'error': 'Folder name is required'}), 400
    
    try:
        new_folder = current_directory / folder_name
        file_ops.create_folder(new_folder)
        return jsonify({'success': 'Folder created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete_item():
    """Delete a file or folder"""
    item_path = request.form.get('path')
    if not item_path:
        return jsonify({'error': 'Path is required'}), 400
    
    try:
        path = Path(item_path)
        file_ops.delete_item(path)
        return jsonify({'success': 'Item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/rename', methods=['POST'])
def rename_item():
    """Rename a file or folder"""
    old_path = request.form.get('old_path')
    new_name = request.form.get('new_name')
    
    if not old_path or not new_name:
        return jsonify({'error': 'Both old path and new name are required'}), 400
    
    try:
        old = Path(old_path)
        new = old.parent / new_name
        file_ops.rename_item(old, new)
        return jsonify({'success': 'Item renamed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download a file"""
    global current_directory
    try:
        filepath = current_directory / filename
        if filepath.exists() and filepath.is_file():
            return send_file(str(filepath), as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search')
def search():
    """Search for files and folders"""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))
    
    try:
        global current_directory
        # Implement search functionality
        results = []
        query_lower = query.lower()
        
        # Search in current directory and subdirectories
        for item in current_directory.rglob('*'):
            try:
                if query_lower in item.name.lower():
                    stat_info = item.stat()
                    file_info = {
                        'name': item.name,
                        'path': str(item),
                        'is_dir': item.is_dir(),
                        'size': utils.format_size(stat_info.st_size) if not item.is_dir() else '',
                        'modified': utils.format_datetime(datetime.fromtimestamp(stat_info.st_mtime))
                    }
                    results.append(file_info)
            except (OSError, PermissionError):
                # Skip files/directories we can't access
                continue
        
        # Sort results by name, directories first
        results.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
        return render_template('search_results.html', 
                             files=results, 
                             query=query,
                             current_path=str(current_directory))
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({'status': 'healthy', 'service': 'file-manager-web'}), 200

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'running',
        'current_directory': str(current_directory),
        'service': 'file-manager-web'
    })

if __name__ == '__main__':
    # For development and external deployments
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)