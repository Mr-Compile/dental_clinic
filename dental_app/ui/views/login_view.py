import logging
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, RIGHT

from dental_app.utils.images import load_circular_image, load_image_cover

log = logging.getLogger(__name__)


class LoginView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        left_frame = ttk.Frame(self, width=self.winfo_screenwidth() // 2)
        left_frame.pack(side=LEFT, expand=True, fill="both")

        right_frame = ttk.Frame(self, width=self.winfo_screenwidth() // 2, bootstyle="light")
        right_frame.pack(side=RIGHT, expand=True, fill="both")

        bg_photo = load_image_cover(
            "www.jpg", self.winfo_screenwidth() // 2, self.winfo_screenheight()
        )
        if bg_photo:
            bg_label = ttk.Label(left_frame, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(relx=0, rely=0.5, anchor="w")

        form_container = ttk.Frame(right_frame, bootstyle="light")
        form_container.place(relx=0.5, rely=0.5, anchor="center", width=500)

        logo_frame = ttk.Frame(form_container, bootstyle="light")
        logo_frame.pack(expand=True, fill="both", pady=(0, 20))

        logo_photo = load_circular_image("dental.jpg", 120)
        if logo_photo:
            logo_label = ttk.Label(logo_frame, image=logo_photo, bootstyle="light")
            logo_label.image = logo_photo
        else:
            logo_label = ttk.Label(logo_frame, text="🦷", font=("Helvetica", 50),
                                   bootstyle="light")
        logo_label.pack(pady=(0, 20))

        ttk.Label(logo_frame, text="Mirasol Dental Center",
                  font=("Helvetica", 18, "bold"), bootstyle="primary").pack(pady=(0, 10))
        ttk.Label(logo_frame, text="Sign in to manage your dental appointments",
                  font=("Helvetica", 10), bootstyle="secondary",
                  wraplength=400).pack(pady=(0, 20))

        form_frame = ttk.Frame(form_container, padding=30, bootstyle="light")
        form_frame.pack(expand=True, fill="both")

        ttk.Label(form_frame, text="Sign In", font=("Helvetica", 20, "bold"),
                  bootstyle="primary").pack(pady=(0, 20))

        fields_container = ttk.Frame(form_frame, bootstyle="light")
        fields_container.pack(expand=True)

        email_frame = ttk.Frame(fields_container, bootstyle="light")
        email_frame.pack(fill="x", pady=10)
        email_label_frame = ttk.Frame(email_frame, bootstyle="light")
        email_label_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(email_label_frame, text="📧", font=("Helvetica", 12)).pack(side="left", padx=(0, 5))
        ttk.Label(email_label_frame, text="Email", bootstyle="secondary").pack(side="left")
        self.email_entry = ttk.Entry(email_frame, bootstyle="primary", width=35)
        self.email_entry.pack(fill="x", pady=5)

        password_frame = ttk.Frame(fields_container, bootstyle="light")
        password_frame.pack(fill="x", pady=10)
        password_label_frame = ttk.Frame(password_frame, bootstyle="light")
        password_label_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(password_label_frame, text="🔒", font=("Helvetica", 12)).pack(side="left", padx=(0, 5))
        ttk.Label(password_label_frame, text="Password", bootstyle="secondary").pack(side="left")
        self.password_entry = ttk.Entry(password_frame, show="•", bootstyle="primary", width=35)
        self.password_entry.pack(fill="x", pady=5)
        self.password_entry.bind("<Return>", lambda e: self.login())

        ttk.Button(form_frame, text="🔑 Sign In", command=self.login,
                   bootstyle="success", width=35, padding=(10, 5)).pack(pady=20)

        register_frame = ttk.Frame(form_frame, bootstyle="light")
        register_frame.pack(pady=10)

        ttk.Label(register_frame, text="👤 Don't have an account? ",
                  font=("Helvetica", 9), bootstyle="secondary").pack(side="left")
        register_link = ttk.Label(register_frame, text="📝 Create Account",
                                  font=("Helvetica", 9, "bold"), cursor="hand2",
                                  bootstyle="primary")
        register_link.pack(side="left")
        register_link.bind("<Button-1>", lambda e: self.app.show_register())

        landing_frame = ttk.Frame(form_frame, bootstyle="light")
        landing_frame.pack(pady=10)

        landing_link = ttk.Label(landing_frame, text="🏥 Visit Our Clinic Website",
                                 font=("Helvetica", 9, "bold"), cursor="hand2",
                                 bootstyle="primary")
        landing_link.pack()
        landing_link.bind("<Button-1>", lambda e: self.app.show_landing())

        ttk.Label(form_frame,
                  text="❓ Need help? Contact us at mirasoldentalcenter@gmail.com",
                  font=("Helvetica", 8), bootstyle="secondary",
                  wraplength=400).pack(pady=(20, 0))

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            ok, message = self.app.login(email, password)
            if not ok:
                messagebox.showerror("Error", message)
        except Exception as err:
            log.error("Login failed: %s", err)
            messagebox.showerror("Error", f"Login failed: {err}")
