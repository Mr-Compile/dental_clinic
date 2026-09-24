"""Application entry point — window, service wiring, screen routing."""
import logging
from tkinter import messagebox

import ttkbootstrap as ttk

from dental_app.core.config import APP_GEOMETRY, APP_TITLE
from dental_app.core.database import Database
from dental_app.repositories.appointment_repository import AppointmentRepository
from dental_app.repositories.report_repository import ReportRepository
from dental_app.repositories.user_repository import UserRepository
from dental_app.services.auth_service import AuthService
from dental_app.services.booking_service import BookingService
from dental_app.services.report_service import ReportService
from dental_app.services.sms_service import SMSService
from dental_app.ui.views.landing_view import LandingView
from dental_app.ui.views.login_view import LoginView
from dental_app.ui.views.register_view import RegisterView

log = logging.getLogger(__name__)


class DentalApp(ttk.Window):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        self.current_user = None
        self.current_frame = None
        self._ready = False

        # Infrastructure + services (single shared DB connection)
        self.db = Database()
        self.users = UserRepository(self.db)
        self.appointments = AppointmentRepository(self.db)
        self.reports = ReportRepository(self.db)
        self.auth = AuthService(self.users)
        self.booking = BookingService(self.appointments, self.users)
        self.sms = SMSService()
        self.report_service = ReportService()

        if not self.db.setup():
            messagebox.showerror(
                "Database Error",
                "Failed to connect to database. Application will exit.")
            self.destroy()
            return

        self.show_login()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._ready = True

    # ---------- screen routing ----------

    def _swap(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(expand=True, fill="both")

    def show_login(self):
        self._swap(LoginView(self, self))

    def show_register(self):
        self._swap(RegisterView(self, self))

    def show_landing(self):
        self._swap(LandingView(self, self))

    def show_dashboard(self):
        from dental_app.ui.views.admin.dashboard import AdminDashboard
        from dental_app.ui.views.client.dashboard import ClientDashboard
        from dental_app.ui.views.staff.dashboard import StaffDashboard

        role = self.current_user["role"]
        view_cls = {"admin": AdminDashboard, "staff": StaffDashboard}.get(
            role, ClientDashboard)
        self._swap(view_cls(self, self))

    # ---------- auth ----------

    def login(self, email, password):
        """Returns (ok, message)."""
        user = self.auth.login(email, password)
        if not user:
            return False, "Invalid email or password"
        self.current_user = user
        self.show_dashboard()
        return True, ""

    def logout(self):
        self.current_user = None
        self.show_login()

    # ---------- lifecycle ----------

    def _on_close(self):
        self.db.close()
        self.destroy()

    def run(self):
        if self._ready:
            self.mainloop()
