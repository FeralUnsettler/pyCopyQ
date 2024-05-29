import tkinter as tk
from tkinter import messagebox, simpledialog

try:
    # Check if Tkinter is available
    root = tk.Tk()
    root.withdraw()  # Hide the window
    root.destroy()   # Close the window
except ImportError:
    # Tkinter is not available, display error message
    messagebox.showerror("Tkinter Not Found", "Tkinter is required to run this application. Please install Tkinter and try again.")
    quit()

import pyperclip
import threading
import time
import json
import os

import tkinter as tk
from tkinter import messagebox, simpledialog
import pyperclip
import threading
import time
import json
import os

class ClipboardHistoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard History")
        self.root.geometry("600x400")
        
        # Set dark theme colors
        self.bg_color = "#2E2E2E"
        self.fg_color = "#FFFFFF"
        self.accent_color = "#FF6347"
        
        # Apply dark theme
        self.root.configure(bg=self.bg_color)
        
        # File to save clipboard history
        self.history_file = "clipboard_history.json"
        self.history = []
        self.max_history = 50
        
        self.load_history()
        
        # Listbox to display clipboard history
        self.listbox = tk.Listbox(root, bg=self.bg_color, fg=self.fg_color, selectbackground=self.accent_color)
        self.listbox.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        
        # Frame to hold buttons
        button_frame = tk.Frame(root, bg=self.bg_color)
        button_frame.pack(fill=tk.X)
        
        # Buttons with dark theme
        self.paste_button = tk.Button(button_frame, text="Paste", command=self.paste_from_history, bg=self.accent_color, fg=self.fg_color)
        self.paste_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self.delete_button = tk.Button(button_frame, text="Delete", command=self.delete_from_history, bg=self.accent_color, fg=self.fg_color)
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self.clear_button = tk.Button(button_frame, text="Clear All", command=self.clear_history, bg=self.accent_color, fg=self.fg_color)
        self.clear_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        self.listbox.bind("<Double-1>", lambda event: self.paste_from_history())
        
        # Start clipboard monitoring in a separate thread
        self.check_clipboard_thread = threading.Thread(target=self.check_clipboard)
        self.check_clipboard_thread.daemon = True
        self.check_clipboard_thread.start()
        
        # Handle window close event to save history
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.update_listbox()

    def load_history(self):
        """Load clipboard history from a file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load history: {e}")
                self.history = []

    def save_history(self):
        """Save clipboard history to a file"""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save history: {e}")

    def check_clipboard(self):
        """Monitor clipboard for new content and update history"""
        recent_value = ""
        while True:
            try:
                clipboard_content = pyperclip.paste()
                if clipboard_content != recent_value and clipboard_content not in self.history:
                    recent_value = clipboard_content
                    self.history.append(clipboard_content)
                    if len(self.history) > self.max_history:
                        self.history.pop(0)
                    self.update_listbox()
            except Exception as e:
                print(f"Error checking clipboard: {e}")
            time.sleep(1)

    def update_listbox(self):
        """Update the listbox with the current clipboard history"""
        self.listbox.delete(0, tk.END)
        for item in self.history:
            self.listbox.insert(tk.END, item)

    def paste_from_history(self):
        """Copy selected history item back to the clipboard"""
        try:
            selected_item_index = self.listbox.curselection()[0]
            selected_item = self.history[selected_item_index]
            pyperclip.copy(selected_item)
            messagebox.showinfo("Clipboard", f"'{selected_item}' copied to clipboard")
        except IndexError:
            messagebox.showwarning("Selection Error", "No item selected from the history.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste: {e}")

    def delete_from_history(self):
        """Delete selected history item"""
        try:
            selected_item_index = self.listbox.curselection()[0]
            del self.history[selected_item_index]
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "No item selected from the history.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {e}")

    def clear_history(self):
        """Clear the entire clipboard history"""
        self.history.clear()
        self.update_listbox()

    def on_closing(self):
        """Handle window close event, save history and exit"""
        self.save_history()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardHistoryApp(root)
    root.mainloop()
