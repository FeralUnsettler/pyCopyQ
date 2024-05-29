import tkinter as tk
from tkinter import messagebox
import pyperclip
import threading
import time
import json
import os

class ClipboardHistoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard History")
        self.root.geometry("400x300")
        
        self.history_file = "clipboard_history.json"
        self.history = []
        self.max_history = 50
        
        self.load_history()
        
        self.listbox = tk.Listbox(root)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        
        self.paste_button = tk.Button(root, text="Paste", command=self.paste_from_history)
        self.paste_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_from_history)
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.clear_button = tk.Button(root, text="Clear All", command=self.clear_history)
        self.clear_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.listbox.bind("<Double-1>", lambda event: self.paste_from_history())
        
        self.check_clipboard_thread = threading.Thread(target=self.check_clipboard)
        self.check_clipboard_thread.daemon = True
        self.check_clipboard_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.update_listbox()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    self.history = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load history: {e}")
                self.history = []

    def save_history(self):
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.history, f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save history: {e}")

    def check_clipboard(self):
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
        self.listbox.delete(0, tk.END)
        for item in self.history:
            self.listbox.insert(tk.END, item)

    def paste_from_history(self):
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
        try:
            selected_item_index = self.listbox.curselection()[0]
            del self.history[selected_item_index]
            self.update_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "No item selected from the history.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete: {e}")

    def clear_history(self):
        self.history.clear()
        self.update_listbox()

    def on_closing(self):
        self.save_history()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardHistoryApp(root)
    root.mainloop()
