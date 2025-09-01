"""
File Manager GUI Application
Main application class handling the tkinter interface and user interactions
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import sys
from pathlib import Path
import threading
from datetime import datetime
import glob
from file_operations import FileOperations
from utils import Utils

class FileManagerApp:
    def __init__(self):
        """Initialize the File Manager application"""
        self.file_ops = FileOperations()
        self.utils = Utils()
        self.current_path = Path.home()
        self.view_mode = 'list'  # 'list' or 'grid'
        self.selected_items = []
        self.clipboard = {'action': None, 'items': []}
        self.sort_column = 'name'  # Default sort column
        self.sort_reverse = False  # Sort order
        self.search_term = ''  # Current search term
        
        # Initialize the main window
        self.root = tk.Tk()
        self.create_main_window()
    
    def create_main_window(self):
        """Create the main application window"""
        self.root.title('File Manager')
        self.root.geometry('1000x700')
        
        # Create menu
        self.create_menu()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create search bar
        self.create_search_bar()
        
        # Create address bar
        self.create_address_bar()
        
        # Create file list with treeview
        self.create_file_list()
        
        # Create status bar
        self.create_status_bar()
        
        # Bind keyboard shortcuts
        self.root.bind('<F5>', lambda e: self.refresh_file_list())
        self.root.bind('<Control-c>', lambda e: self.copy_items())
        self.root.bind('<Control-x>', lambda e: self.cut_items())
        self.root.bind('<Control-v>', lambda e: self.paste_items())
        self.root.bind('<Delete>', lambda e: self.delete_items())
        self.root.bind('<Control-f>', lambda e: self.focus_search())
        
        # Load initial directory
        self.refresh_file_list()
    
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Folder", command=self.create_new_folder)
        file_menu.add_command(label="New Text File", command=self.create_new_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Copy", command=self.copy_items)
        edit_menu.add_command(label="Cut", command=self.cut_items)
        edit_menu.add_command(label="Paste", command=self.paste_items)
        edit_menu.add_command(label="Delete", command=self.delete_items)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_file_list)
        
        # Sort menu
        sort_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Sort by", menu=sort_menu)
        sort_menu.add_command(label="Name", command=lambda: self.sort_files('name'))
        sort_menu.add_command(label="Size", command=lambda: self.sort_files('size'))
        sort_menu.add_command(label="Type", command=lambda: self.sort_files('type'))
        sort_menu.add_command(label="Date Modified", command=lambda: self.sort_files('modified'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.pack(fill='x', padx=5, pady=2)
        
        # Navigation buttons
        ttk.Button(toolbar_frame, text="Back", command=self.go_back).pack(side='left', padx=2)
        ttk.Button(toolbar_frame, text="Up", command=self.go_up).pack(side='left', padx=2)
        ttk.Button(toolbar_frame, text="Home", command=self.go_home).pack(side='left', padx=2)
        
        ttk.Separator(toolbar_frame, orient='vertical').pack(side='left', fill='y', padx=5)
        
        # File operation buttons
        ttk.Button(toolbar_frame, text="New Folder", command=self.create_new_folder).pack(side='left', padx=2)
        ttk.Button(toolbar_frame, text="Copy", command=self.copy_items).pack(side='left', padx=2)
        ttk.Button(toolbar_frame, text="Cut", command=self.cut_items).pack(side='left', padx=2)
        ttk.Button(toolbar_frame, text="Paste", command=self.paste_items).pack(side='left', padx=2)
        ttk.Button(toolbar_frame, text="Delete", command=self.delete_items).pack(side='left', padx=2)
        
        ttk.Separator(toolbar_frame, orient='vertical').pack(side='left', fill='y', padx=5)
        
        # View buttons
        ttk.Button(toolbar_frame, text="Refresh", command=self.refresh_file_list).pack(side='left', padx=2)
    
    def create_search_bar(self):
        """Create the search bar"""
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(search_frame, text="Search:").pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side='left', padx=2)
        self.search_var.trace('w', self.on_search_change)
        
        ttk.Button(search_frame, text="Search", command=self.perform_search).pack(side='left', padx=2)
        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side='left', padx=2)
    
    def create_address_bar(self):
        """Create the address bar"""
        address_frame = ttk.Frame(self.root)
        address_frame.pack(fill='x', padx=5, pady=2)
        
        ttk.Label(address_frame, text="Location:").pack(side='left', padx=(0, 5))
        
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(address_frame, textvariable=self.address_var, width=80)
        self.address_entry.pack(side='left', fill='x', expand=True, padx=2)
        self.address_entry.bind('<Return>', lambda e: self.navigate_to_path(self.address_var.get()))
        
        ttk.Button(address_frame, text="Go", command=lambda: self.navigate_to_path(self.address_var.get())).pack(side='left', padx=2)
    
    def create_file_list(self):
        """Create the file list with treeview"""
        # Frame for treeview and scrollbars
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill='both', expand=True, padx=5, pady=2)
        
        # Create treeview
        columns = ('name', 'size', 'type', 'modified')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        # Configure column headings
        self.tree.heading('name', text='Name', command=lambda: self.sort_files('name'))
        self.tree.heading('size', text='Size', command=lambda: self.sort_files('size'))
        self.tree.heading('type', text='Type', command=lambda: self.sort_files('type'))
        self.tree.heading('modified', text='Modified', command=lambda: self.sort_files('modified'))
        
        # Configure column widths
        self.tree.column('name', width=400)
        self.tree.column('size', width=100)
        self.tree.column('type', width=150)
        self.tree.column('modified', width=200)
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind events
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
        
        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Open", command=self.open_selected)
        self.context_menu.add_command(label="Copy", command=self.copy_items)
        self.context_menu.add_command(label="Cut", command=self.cut_items)
        self.context_menu.add_command(label="Delete", command=self.delete_items)
        self.context_menu.add_command(label="Rename", command=self.rename_item)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Properties", command=self.show_properties)
    
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill='x', side='bottom', padx=5, pady=2)
        
        self.status_var = tk.StringVar()
        self.status_var.set('Ready')
        ttk.Label(status_frame, textvariable=self.status_var).pack(side='left')
        
        self.file_count_var = tk.StringVar()
        ttk.Label(status_frame, textvariable=self.file_count_var).pack(side='right')
    
    def refresh_file_list(self):
        """Refresh the file list display"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Get directory contents
            items = self.file_ops.get_directory_contents(self.current_path)
            
            # Filter items based on search term
            if self.search_term:
                items = self.filter_items(items, self.search_term)
            
            # Sort items
            items = self.sort_items(items)
            
            # Add items to treeview
            for item in items:
                name = item['name']
                size = self.utils.format_size(item['size']) if item['size'] is not None else ''
                file_type = item['type']
                modified = self.utils.format_datetime(item['modified'])
                
                # Insert item into treeview
                self.tree.insert('', 'end', values=(name, size, file_type, modified))
            
            # Update address bar
            self.address_var.set(str(self.current_path))
            
            # Update status bar
            file_count = len([item for item in items if item['type'] != 'Folder'])
            folder_count = len([item for item in items if item['type'] == 'Folder'])
            status_text = f"{folder_count} folders, {file_count} files"
            self.file_count_var.set(status_text)
            self.status_var.set('Ready')
            
        except Exception as e:
            self.show_error(f"Error loading directory: {e}")
            self.status_var.set(f'Error: {e}')
    
    def navigate_to_path(self, path):
        """Navigate to a specific path"""
        try:
            new_path = Path(path).resolve()
            if new_path.exists() and new_path.is_dir():
                self.current_path = new_path
                self.clear_search()  # Clear search when navigating
                self.refresh_file_list()
                return True
            else:
                self.show_error(f"Path does not exist or is not a directory: {path}")
                return False
        except Exception as e:
            self.show_error(f"Error navigating to path: {e}")
            return False
    
    def get_selected_items(self):
        """Get currently selected items"""
        selected_items = []
        for item_id in self.tree.selection():
            item_values = self.tree.item(item_id, 'values')
            if item_values:
                item_name = item_values[0]  # Name is in first column
                item_path = self.current_path / item_name
                selected_items.append(item_path)
        return selected_items
    
    def on_double_click(self, event):
        """Handle double-click on file list item"""
        selected_items = self.get_selected_items()
        if len(selected_items) == 1:
            item_path = selected_items[0]
            if item_path.is_dir():
                self.navigate_to_path(item_path)
            else:
                # Try to open the file with default application
                try:
                    self.file_ops.open_file(item_path)
                except Exception as e:
                    self.show_error(f"Error opening file: {e}")
    
    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under cursor
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            self.context_menu.post(event.x_root, event.y_root)
    
    def create_new_folder(self):
        """Create a new folder"""
        folder_name = simpledialog.askstring('New Folder', 'Enter folder name:')
        if folder_name:
            try:
                new_folder_path = self.current_path / folder_name
                self.file_ops.create_folder(new_folder_path)
                self.refresh_file_list()
                self.status_var.set(f'Created folder: {folder_name}')
            except Exception as e:
                self.show_error(f"Error creating folder: {e}")
    
    def create_new_file(self):
        """Create a new text file"""
        file_name = simpledialog.askstring('New Text File', 'Enter file name:')
        if file_name:
            if not file_name.endswith('.txt'):
                file_name += '.txt'
            try:
                new_file_path = self.current_path / file_name
                self.file_ops.create_file(new_file_path)
                self.refresh_file_list()
                self.status_var.set(f'Created file: {file_name}')
            except Exception as e:
                self.show_error(f"Error creating file: {e}")
    
    def copy_items(self):
        """Copy selected items to clipboard"""
        selected_items = self.get_selected_items()
        if selected_items:
            self.clipboard = {'action': 'copy', 'items': selected_items}
            self.status_var.set(f'Copied {len(selected_items)} item(s)')
    
    def cut_items(self):
        """Cut selected items to clipboard"""
        selected_items = self.get_selected_items()
        if selected_items:
            self.clipboard = {'action': 'cut', 'items': selected_items}
            self.status_var.set(f'Cut {len(selected_items)} item(s)')
    
    def paste_items(self):
        """Paste items from clipboard"""
        if not self.clipboard['items']:
            messagebox.showinfo('Info', 'Nothing to paste')
            return
        
        try:
            action = self.clipboard['action']
            items = self.clipboard['items']
            
            for item_path in items:
                dest_path = self.current_path / item_path.name
                
                if action == 'copy':
                    self.file_ops.copy_item(item_path, dest_path)
                elif action == 'cut':
                    self.file_ops.move_item(item_path, dest_path)
            
            # Clear clipboard if cut operation
            if action == 'cut':
                self.clipboard = {'action': None, 'items': []}
            
            self.refresh_file_list()
            self.status_var.set(f'Pasted {len(items)} item(s)')
            
        except Exception as e:
            self.show_error(f"Error pasting items: {e}")
    
    def delete_items(self):
        """Delete selected items"""
        selected_items = self.get_selected_items()
        if not selected_items:
            return
        
        # Confirm deletion
        item_names = [item.name for item in selected_items]
        message = f"Are you sure you want to delete {len(selected_items)} item(s)?\n\n"
        message += "\n".join(item_names[:5])  # Show first 5 items
        if len(item_names) > 5:
            message += f"\n... and {len(item_names) - 5} more"
        
        if messagebox.askyesno('Confirm Delete', message):
            try:
                for item_path in selected_items:
                    self.file_ops.delete_item(item_path)
                
                self.refresh_file_list()
                self.status_var.set(f'Deleted {len(selected_items)} item(s)')
                
            except Exception as e:
                self.show_error(f"Error deleting items: {e}")
    
    def rename_item(self):
        """Rename selected item"""
        selected_items = self.get_selected_items()
        if len(selected_items) != 1:
            messagebox.showinfo('Info', 'Please select exactly one item to rename')
            return
        
        item_path = selected_items[0]
        current_name = item_path.name
        
        new_name = simpledialog.askstring('Rename', 'Enter new name:', initialvalue=current_name)
        if new_name and new_name != current_name:
            try:
                new_path = item_path.parent / new_name
                self.file_ops.rename_item(item_path, new_path)
                self.refresh_file_list()
                self.status_var.set(f'Renamed to: {new_name}')
            except Exception as e:
                self.show_error(f"Error renaming item: {e}")
    
    def show_properties(self):
        """Show properties of selected item"""
        selected_items = self.get_selected_items()
        if len(selected_items) != 1:
            messagebox.showinfo('Info', 'Please select exactly one item to view properties')
            return
        
        try:
            item_path = selected_items[0]
            properties = self.file_ops.get_item_properties(item_path)
            
            # Create properties dialog
            prop_window = tk.Toplevel(self.root)
            prop_window.title('Properties')
            prop_window.geometry('400x300')
            prop_window.resizable(False, False)
            
            # Make it modal
            prop_window.transient(self.root)
            prop_window.grab_set()
            
            ttk.Label(prop_window, text='Properties', font=('Arial', 12, 'bold')).pack(pady=10)
            
            info_frame = ttk.Frame(prop_window)
            info_frame.pack(fill='both', expand=True, padx=20)
            
            ttk.Label(info_frame, text=f"Name: {properties['name']}").pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Type: {properties['type']}").pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Size: {properties['size']}").pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Location: {properties['location']}").pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Created: {properties['created']}").pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Modified: {properties['modified']}").pack(anchor='w', pady=2)
            ttk.Label(info_frame, text=f"Accessed: {properties['accessed']}").pack(anchor='w', pady=2)
            
            ttk.Button(prop_window, text='OK', command=prop_window.destroy).pack(pady=20)
            
        except Exception as e:
            self.show_error(f"Error getting properties: {e}")
    
    def show_error(self, message):
        """Show error dialog"""
        messagebox.showerror('Error', message)
    
    def show_info(self, message):
        """Show info dialog"""
        messagebox.showinfo('Information', message)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """File Manager v1.0

A Python desktop file manager built with tkinter.

Features:
• Browse and navigate directories
• Create, copy, move, and delete files/folders
• Search and sort functionality
• File properties and operations
• Keyboard shortcuts support

Built with Python and tkinter."""
        
        messagebox.showinfo('About File Manager', about_text)
    
    def run(self):
        """Main event loop"""
        self.root.mainloop()
    
    # Navigation methods
    def go_back(self):
        """Go to parent directory"""
        parent = self.current_path.parent
        if parent != self.current_path:
            self.navigate_to_path(parent)
    
    def go_up(self):
        """Go to parent directory"""
        parent = self.current_path.parent
        if parent != self.current_path:
            self.navigate_to_path(parent)
    
    def go_home(self):
        """Go to home directory"""
        self.navigate_to_path(Path.home())
    
    def open_selected(self):
        """Open selected item"""
        selected_items = self.get_selected_items()
        if selected_items:
            item_path = selected_items[0]
            if item_path.is_dir():
                self.navigate_to_path(item_path)
            else:
                try:
                    self.file_ops.open_file(item_path)
                except Exception as e:
                    self.show_error(f"Error opening file: {e}")
    
    def select_all(self):
        """Select all items in the file list"""
        children = self.tree.get_children()
        self.tree.selection_set(children)
    
    # Search functionality
    def focus_search(self):
        """Focus on search entry"""
        self.search_entry.focus_set()
    
    def on_search_change(self, *args):
        """Handle search term change"""
        # Debounce search - only search after user stops typing
        if hasattr(self, 'search_timer'):
            self.root.after_cancel(self.search_timer)
        self.search_timer = self.root.after(300, self.perform_search)
    
    def perform_search(self):
        """Perform search with current search term"""
        self.search_term = self.search_var.get().strip().lower()
        self.refresh_file_list()
        
        if self.search_term:
            self.status_var.set(f'Searching for: {self.search_term}')
        else:
            self.status_var.set('Ready')
    
    def clear_search(self):
        """Clear search term and refresh"""
        self.search_var.set('')
        self.search_term = ''
        self.refresh_file_list()
    
    def filter_items(self, items, search_term):
        """Filter items based on search term"""
        if not search_term:
            return items
        
        filtered_items = []
        for item in items:
            # Search in filename
            if search_term in item['name'].lower():
                filtered_items.append(item)
            # Also search in file type for more comprehensive search
            elif search_term in item['type'].lower():
                filtered_items.append(item)
        
        return filtered_items
    
    # Sorting functionality
    def sort_files(self, column):
        """Sort files by specified column"""
        # Toggle sort order if clicking the same column
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        self.refresh_file_list()
        
        # Update status to show current sort
        order = "descending" if self.sort_reverse else "ascending"
        self.status_var.set(f'Sorted by {column} ({order})')
    
    def sort_items(self, items):
        """Sort items based on current sort settings"""
        if not items:
            return items
        
        # Define sort key functions
        def get_sort_key(item):
            if self.sort_column == 'name':
                # Sort folders first, then files, both alphabetically
                return (item['type'] != 'Folder', item['name'].lower())
            elif self.sort_column == 'size':
                # Handle None sizes (folders) by treating them as 0
                size = item['size'] if item['size'] is not None else 0
                return (item['type'] != 'Folder', size)
            elif self.sort_column == 'type':
                return (item['type'] != 'Folder', item['type'].lower())
            elif self.sort_column == 'modified':
                # Handle None dates
                date = item['modified'] if item['modified'] is not None else datetime.min
                return (item['type'] != 'Folder', date)
            else:
                return item['name'].lower()
        
        # Sort the items
        sorted_items = sorted(items, key=get_sort_key, reverse=self.sort_reverse)
        
        return sorted_items
