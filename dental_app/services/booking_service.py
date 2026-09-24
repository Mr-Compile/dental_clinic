"""Booking business logic — availability checks, book/cancel/reschedule."""
import logging

from dental_app.core.database import DatabaseError

log = logging.getLogger(__name__)

ER_DUP_ENTRY = 1062


class BookingService:
    def __init__(self, appointment_repo, user_repo):
        self.appointments = appointment_repo
        self.users = user_repo

    def slot_status(self, date, time, user_id):
        return self.appointments.slot_status(date, time, user_id)

    def book(self, user_id, service, date, time):
        """Returns (ok, message)."""
        if not self.users.booking_allowed(user_id):
            return False, "You do not have permission to book appointments"

        if self.appointments.slot_taken(date, time):
            return False, "This time slot is no longer available. Please select a different time."

        try:
            self.appointments.create(user_id, service, date, time)
        except DatabaseError as err:
            if err.errno == ER_DUP_ENTRY:
                return False, "This time slot was just taken. Please select a different time."
            log.error("Booking failed: %s", err)
            return False, f"Booking failed: {err}"

        return True, "Appointment booked successfully"

    def cancel(self, user_id, appointment_id):
        try:
            ok = self.appointments.cancel(appointment_id, user_id)
        except DatabaseError as err:
            log.error("Cancel failed: %s", err)
            return False, f"Failed to cancel appointment: {err}"
        return (True, "Appointment cancelled successfully!") if ok else (
            False, "Appointment not found or not yours")

    def reschedule(self, user_id, appointment_id, date, time):
        """Returns (ok, message)."""
        if self.appointments.slot_taken(date, time, exclude_id=appointment_id):
            return False, "This time slot is no longer available. Please select a different time."

        try:
            ok = self.appointments.reschedule(appointment_id, user_id, date, time)
        except DatabaseError as err:
            if err.errno == ER_DUP_ENTRY:
                return False, "This time slot was just taken. Please select a different time."
            log.error("Reschedule failed: %s", err)
            return False, f"Failed to reschedule appointment: {err}"

        return (True, "Appointment rescheduled successfully!") if ok else (
            False, "Appointment not found or not yours")
