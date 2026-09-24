import os
import webbrowser
from tkinter import messagebox
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class ReportGenerator:
    def __init__(self):
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def format_time(self, time_str):
        # Convert time string to datetime object
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        # Format to show only hour
        return time_obj.strftime('%I:00 %p')

    def generate_appointment_report(self, appointments_data):
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"appointments_report_{timestamp}.pdf")
        
        # Create the PDF document
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Title style
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        
        # Add title
        title = Paragraph("Dental Clinic Appointments Report", title_style)
        elements.append(title)
        
        # Add timestamp
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=20
        )
        date_text = Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y %I:%M %p')}", date_style)
        elements.append(date_text)
        elements.append(Spacer(1, 20))
        
        # Prepare table data
        headers = ['ID', 'Date', 'Time', 'Client', 'Service', 'Contact', 'Status']
        table_data = [headers]
        
        # Add appointment data
        for appt in appointments_data:
            row = [str(x) for x in appt]  # Convert all values to strings
            table_data.append(row)
        
        # Create table
        table = Table(table_data, colWidths=[0.5*inch, 1*inch, 1*inch, 1.5*inch, 2*inch, 1.25*inch, 1*inch])
        
        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        return filename

class ReportGenerationMixin:
    def generate_appointments_report(self):
        try:
            report_generator = ReportGenerator()

            date_filter = self.date_var.get()
            status_filter = self.status_var.get()
            client_search = self.appt_search_var.get()

            query = """
                SELECT a.id, DATE(a.appointment_date), DATE_FORMAT(a.appointment_time, '%H:%i:%s'),
                       u.username, a.service, u.phone_number, a.status
                FROM appointments a
                JOIN users u ON a.user_id = u.id
                WHERE 1=1
            """
            params = []

            if date_filter == "Today":
                query += " AND DATE(a.appointment_date) = CURDATE()"
            elif date_filter == "This Week":
                query += " AND YEARWEEK(a.appointment_date) = YEARWEEK(CURDATE())"
            elif date_filter == "This Month":
                query += " AND MONTH(a.appointment_date) = MONTH(CURDATE())"

            if status_filter != "All":
                query += " AND a.status = %s"
                params.append(status_filter)

            if client_search:
                query += " AND u.username LIKE %s"
                params.append(f"%{client_search}%")

            query += " ORDER BY a.appointment_date DESC, a.appointment_time DESC"

            result = self.app.execute_query(query, params)

            if not result:
                messagebox.showinfo("Report Generation", "No appointments found for the selected filters.")
                return

            formatted_result = []
            for row in result:
                appointment_data = {
                    'id': row[0],
                    'date': row[1],
                    'time': self.format_time(row[2]),
                    'service': row[3],
                    'patient': row[4],
                    'status': row[5]
                }
                formatted_result.append(appointment_data)

            filename = report_generator.generate_appointment_report(formatted_result)

            if messagebox.askyesno(
                "Report Generated",
                f"Report has been generated successfully!\nWould you like to open it now?"
            ):
                webbrowser.open(os.path.abspath(filename))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
