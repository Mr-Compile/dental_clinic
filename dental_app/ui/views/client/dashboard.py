from ttkbootstrap.constants import BOTH, YES

from dental_app.ui.views.base_dashboard import BaseDashboard
from dental_app.ui.views.client.appointments_view import ClientAppointmentsView
from dental_app.ui.views.client.booking_view import BookingView


class ClientDashboard(BaseDashboard):
    def build_tabs(self):
        booking_frame = self.add_tab("📅 Book Appointment")
        BookingView(booking_frame, self.app).pack(fill=BOTH, expand=YES)

        appointments_frame = self.add_tab("📋 My Appointments")
        ClientAppointmentsView(appointments_frame, self.app).pack(fill=BOTH, expand=YES)
