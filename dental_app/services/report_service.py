"""PDF report generation (reportlab)."""
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from dental_app.core.config import REPORTS_DIR


class ReportService:
    def __init__(self, reports_dir=None):
        self.reports_dir = str(reports_dir or REPORTS_DIR)
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_appointment_report(self, appointments_rows):
        """Rows: list of dicts with id, appointment_date, appointment_time,
        username, service, phone_number, status. Returns the PDF filename."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"appointments_report_{timestamp}.pdf")

        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        elements.append(Paragraph(
            "Dental Clinic Appointments Report",
            ParagraphStyle("CustomTitle", parent=styles["Heading1"], fontSize=24, spaceAfter=30),
        ))
        elements.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%B %d, %Y %I:%M %p')}",
            ParagraphStyle("DateStyle", parent=styles["Normal"], fontSize=12, spaceAfter=20),
        ))
        elements.append(Spacer(1, 20))

        table_data = [["ID", "Date", "Time", "Client", "Service", "Contact", "Status"]]
        for row in appointments_rows:
            table_data.append([
                str(row["id"]),
                str(row["appointment_date"]),
                str(row["appointment_time"]),
                str(row["username"]),
                str(row["service"]),
                str(row["phone_number"]),
                str(row["status"]),
            ])

        table = Table(
            table_data,
            colWidths=[0.5 * inch, 1 * inch, 1 * inch, 1.5 * inch, 2 * inch, 1.25 * inch, 1 * inch],
        )
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 14),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 1), (-1, -1), 12),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        doc.build(elements)
        return filename
