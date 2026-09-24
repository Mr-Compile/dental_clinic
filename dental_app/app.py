import ttkbootstrap as ttk
from dental_app.database import DatabaseMixin
from dental_app.auth import AuthMixin
from dental_app.dashboard_router import DashboardRouterMixin
from dental_app.booking import BookingMixin

class DentalApp(ttk.Window, DatabaseMixin, AuthMixin, DashboardRouterMixin, BookingMixin):
    def __init__(self):
        super().__init__()
        self.title("Mirasol Dental Clinic Appointment System With SMS Notifications")
        self.geometry("1200x800")
        
        self.current_user = None
        self.current_frame = None

        if not self.setup_database():
            ttk.messagebox.showerror("Database Error", "Failed to connect to database. Application will exit.")
            self.quit()
            return

        self.create_login_frame()

    def run(self):
        self.mainloop()
