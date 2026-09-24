"""All SQL for the reports table."""
import json


class ReportRepository:
    def __init__(self, db):
        self.db = db

    def create(self, staff_id, report_type, description, report_data):
        """report_data may be a dict (stored as JSON) or a raw string."""
        payload = (
            json.dumps(report_data, default=str)
            if not isinstance(report_data, str)
            else report_data
        )
        return self.db.execute(
            """
            INSERT INTO reports (staff_id, report_type, description, report_data)
            VALUES (%s, %s, %s, %s)
            """,
            (staff_id, report_type, description, payload),
            fetch=False,
        )

    def list_all(self):
        return self.db.execute(
            """
            SELECT r.report_id, u.username AS staff_name, r.report_type,
                   r.generated_date, r.description
            FROM reports r
            JOIN users u ON r.staff_id = u.id
            ORDER BY r.generated_date DESC
            """
        )

    def get_data(self, report_id):
        rows = self.db.execute(
            "SELECT report_data FROM reports WHERE report_id = %s", (report_id,)
        )
        return rows[0]["report_data"] if rows else None
