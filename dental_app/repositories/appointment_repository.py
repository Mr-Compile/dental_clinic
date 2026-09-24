"""All SQL for the appointments table."""

_ACTIVE_STATUSES = ("pending", "confirmed")

_DATE_FILTER_SQL = {
    "Today": " AND DATE(a.appointment_date) = CURDATE()",
    "This Week": " AND YEARWEEK(a.appointment_date) = YEARWEEK(CURDATE())",
    "This Month": " AND MONTH(a.appointment_date) = MONTH(CURDATE())",
}

_SELECT_WITH_USER = """
    SELECT a.id, u.username, a.service, a.appointment_date,
           a.appointment_time, u.phone_number, a.status
    FROM appointments a
    JOIN users u ON a.user_id = u.id
"""


class AppointmentRepository:
    def __init__(self, db):
        self.db = db

    # ---------- reads ----------

    def list_filtered(self, date_filter="All", status="All", search=""):
        query = _SELECT_WITH_USER + " WHERE 1=1"
        params = []

        query += _DATE_FILTER_SQL.get(date_filter, "")

        if status != "All":
            query += " AND a.status = %s"
            params.append(status)

        if search:
            query += " AND (u.username LIKE %s OR a.service LIKE %s OR a.status LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])

        query += " ORDER BY a.appointment_date DESC, a.appointment_time DESC"
        return self.db.execute(query, params)

    def list_for_report(self, date_filter="All", status="All", search=""):
        query = """
            SELECT a.id, DATE(a.appointment_date) AS appointment_date,
                   DATE_FORMAT(a.appointment_time, '%H:%i:%s') AS appointment_time,
                   u.username, a.service, u.phone_number, a.status
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            WHERE 1=1
        """
        params = []

        query += _DATE_FILTER_SQL.get(date_filter, "")

        if status != "All":
            query += " AND a.status = %s"
            params.append(status)

        if search:
            query += " AND u.username LIKE %s"
            params.append(f"%{search}%")

        query += " ORDER BY a.appointment_date DESC, a.appointment_time DESC"
        return self.db.execute(query, params)

    def list_by_user(self, user_id, status="All", search=""):
        query = """
            SELECT id, service, appointment_date, appointment_time, status
            FROM appointments
            WHERE user_id = %s
        """
        params = [user_id]

        if status != "All":
            query += " AND status = %s"
            params.append(status)

        if search:
            query += " AND (service LIKE %s OR appointment_date LIKE %s OR appointment_time LIKE %s)"
            like = f"%{search}%"
            params.extend([like, like, like])

        query += " ORDER BY appointment_date DESC, appointment_time DESC"
        return self.db.execute(query, params)

    def list_recent(self, limit=10):
        return self.db.execute(
            """
            SELECT
                DATE_FORMAT(a.appointment_date, '%Y-%m-%d') AS formatted_date,
                TIME_FORMAT(a.appointment_time, '%H:%i') AS formatted_time,
                u.username,
                a.service,
                a.status
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
            LIMIT %s
            """,
            (limit,),
        )

    def get_with_user(self, appointment_id):
        rows = self.db.execute(
            """
            SELECT a.*, u.phone_number, u.username
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            WHERE a.id = %s
            """,
            (appointment_id,),
        )
        return rows[0] if rows else None

    def slot_status(self, date, time, user_id):
        """One query per slot: 'mine' | 'taken' | 'available'."""
        rows = self.db.execute(
            """
            SELECT user_id FROM appointments
            WHERE appointment_date = %s AND appointment_time = %s
              AND status IN ('pending', 'confirmed')
            """,
            (date, time),
        )
        for row in rows:
            if row["user_id"] == user_id:
                return "mine"
        return "taken" if rows else "available"

    def slot_taken(self, date, time, exclude_id=None):
        query = """
            SELECT COUNT(*) AS count FROM appointments
            WHERE appointment_date = %s AND appointment_time = %s
              AND status IN ('pending', 'confirmed')
        """
        params = [date, time]
        if exclude_id is not None:
            query += " AND id != %s"
            params.append(exclude_id)
        rows = self.db.execute(query, params)
        return rows[0]["count"] > 0

    def count_all(self):
        return self.db.execute("SELECT COUNT(*) AS count FROM appointments")[0]["count"]

    def count_today(self):
        return self.db.execute(
            "SELECT COUNT(*) AS count FROM appointments WHERE DATE(appointment_date) = CURDATE()"
        )[0]["count"]

    def count_by_status(self, status):
        return self.db.execute(
            "SELECT COUNT(*) AS count FROM appointments WHERE status = %s", (status,)
        )[0]["count"]

    # ---------- writes ----------

    def create(self, user_id, service, date, time):
        return self.db.execute(
            """
            INSERT INTO appointments (user_id, service, appointment_date, appointment_time, status)
            VALUES (%s, %s, %s, %s, 'pending')
            """,
            (user_id, service, date, time),
            fetch=False,
        )

    def update(self, appointment_id, service, date, time, status):
        return self.db.execute(
            """
            UPDATE appointments
            SET service = %s, appointment_date = %s, appointment_time = %s, status = %s
            WHERE id = %s
            """,
            (service, date, time, status, appointment_id),
            fetch=False,
        )

    def update_status(self, appointment_id, status):
        return self.db.execute(
            "UPDATE appointments SET status = %s WHERE id = %s",
            (status, appointment_id),
            fetch=False,
        )

    def cancel(self, appointment_id, user_id):
        return self.db.execute(
            "UPDATE appointments SET status = 'cancelled' WHERE id = %s AND user_id = %s",
            (appointment_id, user_id),
            fetch=False,
        )

    def reschedule(self, appointment_id, user_id, date, time):
        return self.db.execute(
            """
            UPDATE appointments
            SET appointment_date = %s, appointment_time = %s, status = 'pending'
            WHERE id = %s AND user_id = %s
            """,
            (date, time, appointment_id, user_id),
            fetch=False,
        )

    def delete(self, appointment_id):
        return self.db.execute(
            "DELETE FROM appointments WHERE id = %s", (appointment_id,), fetch=False
        )

    def delete_by_user(self, user_id):
        return self.db.execute(
            "DELETE FROM appointments WHERE user_id = %s", (user_id,), fetch=False
        )
