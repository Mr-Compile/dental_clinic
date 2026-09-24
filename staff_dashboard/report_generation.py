import os
import webbrowser
import json
from tkinter import messagebox
from shared.report_generator import ReportGenerator
from datetime import datetime
import mysql.connector

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

            # Execute query using MySQL connector
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dental"
            )
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()

            if not result:
                messagebox.showinfo("Report Generation", "No appointments found for the selected filters.")
                return

            filename = report_generator.generate_appointment_report(result)

            # Convert result to list of dictionaries with serializable values
            serializable_result = []
            for row in result:
                serializable_result.append({
                    'id': row[0],
                    'appointment_date': str(row[1]),  # Convert date to string
                    'appointment_time': str(row[2]),  # Convert time to string
                    'username': row[3],
                    'service': row[4],
                    'phone_number': row[5],
                    'status': row[6]
                })

            # Save report to database
            report_data = {
                'filename': filename,
                'filters': {
                    'date_filter': date_filter,
                    'status_filter': status_filter,
                    'client_search': client_search
                },
                'appointments': serializable_result,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            save_query = """
                INSERT INTO reports (staff_id, report_type, description, report_data)
                VALUES (%s, %s, %s, %s)
            """
            save_params = (
                self.app.current_user['id'],
                'Appointments Report',
                f"Appointment Report Successfully",
                json.dumps(report_data, default=str)
            )
            
            cursor.execute(save_query, save_params)
            conn.commit()

            if messagebox.askyesno(
                "Report Generated",
                f"Report has been generated successfully!\nWould you like to open it now?"
            ):
                webbrowser.open(os.path.abspath(filename))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
