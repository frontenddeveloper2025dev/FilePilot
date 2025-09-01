"""
Web server wrapper for the File Manager application.
Provides HTTP endpoints for file management operations compatible with Autoscale deployments.
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from file_operations import FileOperations
from utils import Utils

app = Flask(__name__)
file_ops = FileOperations()
utils = Utils()

# Global state to track current directory
current_directory = Path.home()

@app.route('/')
def index():
    """Main file manager interface"""
    global current_directory
    try:
        files = file_ops.list_directory(current_directory)
        current_path = str(current_directory)
        parent_path = str(current_directory.parent) if current_directory.parent != current_directory else None
        
        # Process files for web display
        file_list = []
        for file_path in files:
            file_info = {
                'name': file_path.name,
                'path': str(file_path),
                'is_dir': file_path.is_dir(),
                'size': utils.format_size(file_ops.get_file_size(file_path)) if not file_path.is_dir() else '',
                'modified': utils.format_datetime(file_ops.get_file_modified_time(file_path))
            }
            file_list.append(file_info)
        
        # Sort files by name, directories first
        file_list.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        
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
    if file.filename == '':
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
        file_ops.create_directory(new_folder)
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
        if path.is_file():
            file_ops.delete_file(path)
        elif path.is_dir():
            file_ops.delete_directory(path)
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
        file_ops.move_file(old, new)
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
        results = file_ops.search_files(current_directory, query)
        
        # Process results for web display
        file_list = []
        for file_path in results:
            file_info = {
                'name': file_path.name,
                'path': str(file_path),
                'is_dir': file_path.is_dir(),
                'size': utils.format_size(file_ops.get_file_size(file_path)) if not file_path.is_dir() else '',
                'modified': utils.format_datetime(file_ops.get_file_modified_time(file_path))
            }
            file_list.append(file_info)
        
        return render_template('search_results.html', 
                             files=file_list, 
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
    # Bind to 0.0.0.0:5000 for deployment compatibility
    app.run(host='0.0.0.0', port=5000, debug=False)