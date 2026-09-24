import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, X, YES


class ModernModal:
    def __init__(self, parent, title, width=450, height=350):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=X, pady=(0, 20))

        self.icon_label = ttk.Label(header_frame, font=("Segoe UI", 32), bootstyle="primary")
        self.icon_label.pack(side=LEFT, padx=(0, 15))

        self.title_label = ttk.Label(
            header_frame, text=title, font=("Segoe UI", 14, "bold"), bootstyle="primary"
        )
        self.title_label.pack(side=LEFT, fill=X, expand=YES)

        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill=BOTH, expand=YES)

        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill=X, pady=(20, 0))

        self.dialog.update_idletasks()
        width = max(width, self.dialog.winfo_width())
        height = max(height, self.dialog.winfo_height())
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

    def set_icon(self, icon, style="primary"):
        self.icon_label.configure(text=icon, bootstyle=style)

    def add_content(self, widget, **kwargs):
        widget.pack(in_=self.content_frame, **kwargs)

    def add_button(self, text, command, style="primary", **kwargs):
        button = ttk.Button(self.button_frame, text=text, command=command,
                            bootstyle=style, **kwargs)
        button.pack(side=LEFT, padx=5)
        return button
