import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, W, X, YES


class LogoutDialog:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.dialog = None
        self.logout_confirmed = False

    def show(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Confirm Logout")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        icon_frame = ttk.Frame(main_frame)
        icon_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(icon_frame, text="🚪", font=("Segoe UI", 48),
                  bootstyle="warning").pack(side=LEFT, padx=(0, 20))

        message_frame = ttk.Frame(icon_frame)
        message_frame.pack(side=LEFT, fill=X, expand=YES)

        ttk.Label(message_frame, text="Are you sure you want to logout?",
                  font=("Segoe UI", 16, "bold"), bootstyle="primary").pack(anchor=W)
        ttk.Label(message_frame, text="You will need to login again to access your account.",
                  font=("Segoe UI", 12), bootstyle="secondary").pack(anchor=W, pady=(5, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(20, 0))

        button_container = ttk.Frame(button_frame)
        button_container.pack(expand=True)

        ttk.Button(button_container, text="✅ Yes, Logout", command=self.confirm_logout,
                   bootstyle="danger", width=20, padding=(10, 5)).pack(side=LEFT, padx=(0, 10))
        ttk.Button(button_container, text="❌ No, Stay", command=self.cancel_logout,
                   bootstyle="secondary", width=20, padding=(10, 5)).pack(side=LEFT)

        self.dialog.update_idletasks()
        width = max(500, self.dialog.winfo_width())
        height = max(300, self.dialog.winfo_height())
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

        self.parent.wait_window(self.dialog)
        return self.logout_confirmed

    def confirm_logout(self):
        self.logout_confirmed = True
        self.dialog.destroy()

    def cancel_logout(self):
        self.logout_confirmed = False
        self.dialog.destroy()
