import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, W, X, YES

_ICON_BY_TYPE = {"warning": "⚠️", "info": "ℹ️", "danger": "❌", "success": "✅"}
_COLOR_BY_TYPE = {"warning": "warning", "info": "primary", "danger": "danger", "success": "success"}


class ModernConfirmationDialog:
    """Modal yes/no confirmation used by admin and staff dashboards."""

    def __init__(self, parent, title, message, action_type="info"):
        self.parent = parent
        self.confirmed = False

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        icon_frame = ttk.Frame(main_frame)
        icon_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            icon_frame,
            text=_ICON_BY_TYPE.get(action_type, "ℹ️"),
            font=("Segoe UI", 32),
            bootstyle=_COLOR_BY_TYPE.get(action_type, "primary"),
        ).pack(side=LEFT, padx=(0, 15))

        message_frame = ttk.Frame(icon_frame)
        message_frame.pack(side=LEFT, fill=X, expand=YES)

        ttk.Label(message_frame, text=title, font=("Segoe UI", 14, "bold"),
                  bootstyle="primary").pack(anchor=W)

        for line in message.split("\n"):
            if line.strip():
                ttk.Label(message_frame, text=line, font=("Segoe UI", 10),
                          bootstyle="secondary").pack(anchor=W, pady=(5, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(20, 0))

        ttk.Button(button_frame, text="Yes, Proceed", command=self.confirm,
                   bootstyle="success", width=15).pack(side=LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="No, Cancel", command=self.cancel,
                   bootstyle="secondary", width=15).pack(side=LEFT)

        self.dialog.update_idletasks()
        width = max(450, self.dialog.winfo_width())
        height = max(350, self.dialog.winfo_height())
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

        self.parent.wait_window(self.dialog)

    def confirm(self):
        self.confirmed = True
        self.dialog.destroy()

    def cancel(self):
        self.confirmed = False
        self.dialog.destroy()

    def show(self):
        return self.confirmed
