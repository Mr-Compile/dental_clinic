import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import mysql.connector
import json
import os
import webbrowser
from datetime import datetime
from tkinter import messagebox

class ReportViewMixin:
    def setup_reports_view(self):
        # Create main container
        reports_container = ttk.Frame(self.reports_frame)
        reports_container.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Create treeview for reports
        columns = ('report_id', 'staff_name', 'report_type', 'generated_date', 'description')
        self.reports_tree = ttk.Treeview(
            reports_container,
            columns=columns,
            show='headings',
            bootstyle="primary"
        )

        # Configure columns with specific widths and center alignment
        column_configs = {
            'report_id': 80,
            'staff_name': 150,
            'report_type': 150,
            'generated_date': 150,
            'description': 300
        }

        for col in columns:
            self.reports_tree.heading(col, text=col.replace('_', ' ').title(), anchor=CENTER)
            self.reports_tree.column(col, width=column_configs[col], anchor=CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            reports_container,
            orient=VERTICAL,
            command=self.reports_tree.yview
        )
        self.reports_tree.configure(yscrollcommand=scrollbar.set)

        # Pack treeview and scrollbar
        self.reports_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Button container
        button_container = ttk.Frame(reports_container)
        button_container.pack(fill=X, pady=10)

        # Style configuration for buttons
        button_style = {
            'width': 15,
            'padding': 10
        }

        # Add colored buttons
        ttk.Button(
            button_container,
            text="📄 View Report",
            command=self.view_selected_report,
            bootstyle="primary",
            **button_style
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            button_container,
            text="🔄 Refresh",
            command=self.load_reports,
            bootstyle="info",
            **button_style
        ).pack(side=LEFT, padx=5)

        # Bind double-click event
        self.reports_tree.bind("<Double-1>", lambda e: self.view_selected_report())

        # Load reports
        self.load_reports()

    def load_reports(self):
        # Clear existing items
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dental"
            )
            cursor = conn.cursor()
            
            # Join with users table to get staff names
            cursor.execute('''
                SELECT r.report_id, u.username, r.report_type, r.generated_date, r.description
                FROM reports r
                JOIN users u ON r.staff_id = u.id
                ORDER BY r.generated_date DESC
            ''')
            
            reports = cursor.fetchall()
            
            for report in reports:
                # Convert datetime to string if needed
                generated_date = report[3]
                if isinstance(generated_date, datetime):
                    generated_date = generated_date.strftime('%Y-%m-%d %H:%M:%S')
                
                # Insert with centered values
                self.reports_tree.insert('', END, values=(
                    report[0],  # report_id
                    report[1],  # username
                    report[2],  # report_type
                    generated_date,  # generated_date
                    report[4]   # description
                ))
                
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Failed to load reports: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def view_selected_report(self):
        selected_item = self.reports_tree.selection()
        if not selected_item:
            return

        try:
            report_id = self.reports_tree.item(selected_item[0])['values'][0]
            
            # Get report data from database
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dental"
            )
            cursor = conn.cursor()
            
            cursor.execute("SELECT report_data FROM reports WHERE report_id = %s", (report_id,))
            result = cursor.fetchone()
            
            if result:
                report_data = json.loads(result[0])
                filename = report_data['filename']
                
                if os.path.exists(filename):
                    webbrowser.open(os.path.abspath(filename))
                else:
                    messagebox.showerror("Error", "Report file not found. It may have been moved or deleted.")
            else:
                messagebox.showerror("Error", "Report data not found in database.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view report: {str(e)}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close() 