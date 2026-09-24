from admin_dashboard.main_dashboard import AdminDashboard
from staff_dashboard.main_dashboard import StaffDashboard
from client_dashboard.main_dashboard import ClientDashboard

class DashboardRouterMixin:
    def show_dashboard(self):
        if self.current_frame:
            self.current_frame.destroy()

        if self.current_user['role'] == 'admin':
            self.current_frame = AdminDashboard(self, self)
        elif self.current_user['role'] == 'staff':
            self.current_frame = StaffDashboard(self, self)
        else:
            self.current_frame = ClientDashboard(self, self)

        self.current_frame.pack(fill='both', expand=True)
