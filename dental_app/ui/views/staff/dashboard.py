from ttkbootstrap.constants import BOTH, YES

from dental_app.ui.views.base_dashboard import BaseDashboard
from dental_app.ui.views.staff.appointments_view import StaffAppointmentsView
from dental_app.ui.views.staff.overview_view import StaffOverviewView


class StaffDashboard(BaseDashboard):
    def build_tabs(self):
        overview_frame = self.add_tab("📊 Dashboard")
        self.overview = StaffOverviewView(overview_frame, self.app, self.notebook)
        self.overview.pack(fill=BOTH, expand=YES)

        appointments_frame = self.add_tab("📅 Appointments")
        StaffAppointmentsView(appointments_frame, self.app).pack(fill=BOTH, expand=YES)

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def _on_tab_change(self, _event):
        if self.notebook.index(self.notebook.select()) == 0:
            self.overview.refresh()
