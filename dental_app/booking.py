class BookingMixin:
    def book_appointment(self, appointment_data):
        if not self.current_user:
            return False, "Must be logged in to book appointments"
        
        result = self.execute_query(
            "SELECT booking_allowed FROM users WHERE id = %s",
            (self.current_user['id'],)
        )

        if not result or not result[0][0]:
            return False, "You do not have permission to book appointments"

        try:
            success = self.execute_query(
                """
                INSERT INTO appointments 
                (user_id, service, appointment_date, appointment_time, status)
                VALUES (%s, %s, %s, %s, 'pending')
                """,
                (self.current_user['id'], appointment_data['service'],
                 appointment_data['date'], appointment_data['time']),
                fetch=False
            )

            if success:
                return True, "Appointment booked successfully"
            return False, "Failed to book appointment"

        except Exception as e:
            return False, f"Booking failed: {str(e)}"
