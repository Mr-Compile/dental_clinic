import re
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def validate_phone(phone_number):
    """Validate Philippine phone number format: must start with 09 and have 11 digits."""
    pattern = r'^09\d{9}$'
    return re.match(pattern, phone_number) is not None

class ModernModal:
    def __init__(self, parent, title, width=450, height=350):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Prevent closing with X button
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        # Main container with padding
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Header section with icon and title
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))

        # Icon based on action type
        self.icon_label = ttk.Label(
            header_frame,
            font=("Segoe UI", 32),
            bootstyle="primary"
        )
        self.icon_label.pack(side=LEFT, padx=(0, 15))

        # Title label
        self.title_label = ttk.Label(
            header_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bootstyle="primary"
        )
        self.title_label.pack(side=LEFT, fill=X, expand=YES)

        # Content frame
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=BOTH, expand=YES)

        # Button frame
        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill=X, pady=(20, 0))

        # Calculate dialog size based on content
        self.dialog.update_idletasks()
        width = max(width, self.dialog.winfo_width())
        height = max(height, self.dialog.winfo_height())
        
        # Center the dialog
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')

    def set_icon(self, icon, style="primary"):
        self.icon_label.configure(text=icon, bootstyle=style)

    def add_content(self, widget, **kwargs):
        widget.pack(in_=self.content_frame, **kwargs)

    def add_button(self, text, command, style="primary", **kwargs):
        button = ttk.Button(
            self.button_frame,
            text=text,
            command=command,
            bootstyle=style,
            **kwargs
        )
        button.pack(side=LEFT, padx=5)
        return button

    def show(self):
        self.parent.wait_window(self.dialog)
        return self.result if hasattr(self, 'result') else None
