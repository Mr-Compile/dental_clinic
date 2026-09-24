import logging
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk

from dental_app.utils.images import load_circular_image

log = logging.getLogger(__name__)

ENTRY_WIDTH = 30


class RegisterView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        main_frame = ttk.Frame(self, padding=20, bootstyle="light")
        main_frame.pack(expand=True, fill="both")

        left_frame = ttk.Frame(main_frame, bootstyle="light")
        left_frame.pack(side="left", expand=True, fill="both", padx=(0, 20))

        right_frame = ttk.Frame(main_frame, bootstyle="light")
        right_frame.pack(side="right", expand=True, fill="both")

        logo_frame = ttk.Frame(left_frame, bootstyle="light")
        logo_frame.pack(expand=True, fill="both")

        logo_photo = load_circular_image("dental.jpg", 320)
        if logo_photo:
            logo_label = ttk.Label(logo_frame, image=logo_photo, bootstyle="light")
            logo_label.image = logo_photo
        else:
            logo_label = ttk.Label(logo_frame, text="🦷", font=("Helvetica", 120),
                                   bootstyle="light")
        logo_label.pack(pady=(50, 20))

        ttk.Label(logo_frame, text="Welcome to Dental Clinic",
                  font=("Helvetica", 24, "bold"), bootstyle="primary").pack(pady=(0, 10))
        ttk.Label(logo_frame,
                  text="Create your account to manage your dental appointments",
                  font=("Helvetica", 12), bootstyle="secondary",
                  wraplength=300).pack(pady=(0, 20))

        form_frame = ttk.Frame(right_frame, padding=40, bootstyle="light")
        form_frame.pack(expand=True, fill="both")

        ttk.Label(form_frame, text="Create Your Account",
                  font=("Helvetica", 24, "bold"), bootstyle="primary").pack(pady=(0, 30))

        fields_container = ttk.Frame(form_frame, bootstyle="light")
        fields_container.pack(fill="x", expand=True)

        self.username_entry = self._field(fields_container, "👤", "Username")
        self.email_entry = self._field(fields_container, "📧", "Email")
        self.phone_entry = self._field(fields_container, "📱", "Phone")
        self.phone_entry.bind("<KeyPress>", self._validate_phone_input)
        self.phone_entry.bind("<KeyRelease>", self._format_phone_number)
        self.password_entry = self._field(fields_container, "🔒", "Password", show="•")
        self.confirm_password_entry = self._field(fields_container, "🔒",
                                                "Confirm Password", show="•")

        button_frame = ttk.Frame(form_frame, bootstyle="light")
        button_frame.pack(pady=30)

        ttk.Button(button_frame, text="📝 Create Account", command=self.register,
                   bootstyle="success", width=ENTRY_WIDTH, padding=(10, 5)).pack(pady=5)
        ttk.Button(button_frame, text="↩️ Back to Login",
                   command=self.app.show_login,
                   bootstyle="secondary", width=ENTRY_WIDTH, padding=(10, 5)).pack(pady=5)

        ttk.Label(form_frame,
                  text="ℹ️ By creating an account, you agree to our Terms of Service and Privacy Policy",
                  font=("Helvetica", 8), bootstyle="secondary").pack(pady=(20, 0))

    def _field(self, parent, icon, label, show=None):
        frame = ttk.Frame(parent, bootstyle="light")
        frame.pack(fill="x", pady=10)
        label_frame = ttk.Frame(frame, bootstyle="light")
        label_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(label_frame, text=icon, font=("Helvetica", 14)).pack(side="left", padx=(0, 5))
        ttk.Label(label_frame, text=label, bootstyle="secondary").pack(side="left")
        entry = ttk.Entry(frame, bootstyle="primary", width=ENTRY_WIDTH, show=show)
        entry.pack(fill="x", expand=True)
        return entry

    # ---------- phone input handling ----------

    def _validate_phone_input(self, event):
        if event.char.isdigit():
            if len(self.phone_entry.get()) >= 11:
                return "break"
        elif event.keysym not in ("BackSpace", "Delete", "Left", "Right"):
            return "break"

    def _format_phone_number(self, _event):
        current = self.phone_entry.get()
        cleaned = "".join(filter(str.isdigit, current))
        if len(cleaned) >= 2 and cleaned[:2] != "09":
            cleaned = "09" + cleaned[2:] if len(cleaned) > 2 else "09"
        cleaned = cleaned[:11]
        if cleaned != current:
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, cleaned)

    # ---------- submit ----------

    def register(self):
        try:
            ok, message = self.app.auth.register(
                username=self.username_entry.get().strip(),
                email=self.email_entry.get().strip(),
                password=self.password_entry.get(),
                confirm_password=self.confirm_password_entry.get(),
                phone=self.phone_entry.get().strip(),
            )
            if ok:
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                self.app.show_login()
            else:
                messagebox.showerror("Error", message)
        except Exception as err:
            log.error("Registration failed: %s", err)
            messagebox.showerror("Error", f"Registration failed: {err}")
