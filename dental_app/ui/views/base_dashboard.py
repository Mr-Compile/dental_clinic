"""Shared dashboard scaffold — header, welcome bar, notebook, logout footer."""
import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, X, YES

from dental_app.core.config import APP_TITLE
from dental_app.ui.components.logout_dialog import LogoutDialog
from dental_app.ui.styles import configure_styles
from dental_app.utils.images import load_circular_image


class BaseDashboard(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        configure_styles()
        self._build()

    def _build(self):
        main_container = ttk.Frame(self, style="Modern.TFrame")
        main_container.pack(fill=BOTH, expand=YES)

        # Header
        header_frame = ttk.Frame(main_container, bootstyle="primary")
        header_frame.pack(fill=X, padx=0, pady=0)

        title_frame = ttk.Frame(header_frame, bootstyle="primary")
        title_frame.pack(fill=X, padx=20, pady=10)

        logo_photo = load_circular_image("dental.jpg", 60)
        if logo_photo:
            logo_label = ttk.Label(title_frame, image=logo_photo, bootstyle="inverse-primary")
            logo_label.image = logo_photo
        else:
            logo_label = ttk.Label(title_frame, text="🦷", font=("Helvetica", 32),
                                   bootstyle="inverse-primary")
        logo_label.pack(side=LEFT, padx=(0, 15))

        ttk.Label(title_frame, text=APP_TITLE, style="Title.TLabel",
                  bootstyle="inverse-primary").pack(side=LEFT)

        # Welcome bar
        welcome_frame = ttk.Frame(main_container, style="Card.TFrame")
        welcome_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(
            welcome_frame,
            text=f"Welcome, {self.app.current_user['username']}",
            style="Subtitle.TLabel",
        ).pack(side=LEFT, padx=20, pady=10)

        # Notebook
        content_frame = ttk.Frame(main_container, style="Modern.TFrame")
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        self.notebook = ttk.Notebook(content_frame, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES)

        self.build_tabs()

        # Footer
        footer_frame = ttk.Frame(main_container, style="Card.TFrame")
        footer_frame.pack(fill=X, padx=20, pady=10)

        ttk.Button(footer_frame, text="🚪 Logout", command=self.show_logout_dialog,
                   bootstyle="danger").pack(side=RIGHT, padx=20, pady=10)

    def add_tab(self, label):
        frame = ttk.Frame(self.notebook, style="Modern.TFrame")
        self.notebook.add(frame, text=label)
        return frame

    def build_tabs(self):
        """Subclasses add their tabs here via self.add_tab()."""
        raise NotImplementedError

    def show_logout_dialog(self):
        if LogoutDialog(self, self.app).show():
            self.app.logout()
