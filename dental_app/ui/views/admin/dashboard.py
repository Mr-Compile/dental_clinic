from ttkbootstrap.constants import BOTH, YES

from dental_app.ui.views.admin.appointments_view import AdminAppointmentsView
from dental_app.ui.views.admin.overview_view import AdminOverviewView
from dental_app.ui.views.admin.reports_view import ReportsView
from dental_app.ui.views.admin.users_view import UsersView
from dental_app.ui.views.base_dashboard import BaseDashboard


class AdminDashboard(BaseDashboard):
    def build_tabs(self):
        overview_frame = self.add_tab("📊 Dashboard")
        self.overview = AdminOverviewView(overview_frame, self.app, self.notebook)
        self.overview.pack(fill=BOTH, expand=YES)

        users_frame = self.add_tab("👥 User Management")
        UsersView(users_frame, self.app).pack(fill=BOTH, expand=YES)

        appointments_frame = self.add_tab("📅 Appointment Management")
        AdminAppointmentsView(appointments_frame, self.app).pack(fill=BOTH, expand=YES)

        reports_frame = self.add_tab("📊 Reports")
        ReportsView(reports_frame, self.app).pack(fill=BOTH, expand=YES)
