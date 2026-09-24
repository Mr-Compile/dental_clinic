"""Admin reports tab — list generated reports and open the PDF."""
import json
import logging
import os
import webbrowser
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, CENTER, END, LEFT, RIGHT, VERTICAL, X, Y, YES

log = logging.getLogger(__name__)

BUTTON_STYLE = {"width": 15, "padding": 10}


class ReportsView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        reports_container = ttk.Frame(self)
        reports_container.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        columns = ("report_id", "staff_name", "report_type", "generated_date", "description")
        column_configs = {"report_id": 80, "staff_name": 150, "report_type": 150,
                          "generated_date": 150, "description": 300}

        self.reports_tree = ttk.Treeview(reports_container, columns=columns,
                                         show="headings", bootstyle="primary")
        for col in columns:
            self.reports_tree.heading(col, text=col.replace("_", " ").title(), anchor=CENTER)
            self.reports_tree.column(col, width=column_configs[col], anchor=CENTER)

        scrollbar = ttk.Scrollbar(reports_container, orient=VERTICAL,
                                  command=self.reports_tree.yview)
        self.reports_tree.configure(yscrollcommand=scrollbar.set)
        self.reports_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        button_container = ttk.Frame(reports_container)
        button_container.pack(fill=X, pady=10)

        ttk.Button(button_container, text="📄 View Report",
                   command=self.view_selected_report, bootstyle="primary",
                   **BUTTON_STYLE).pack(side=LEFT, padx=5)
        ttk.Button(button_container, text="🔄 Refresh", command=self.load_reports,
                   bootstyle="info", **BUTTON_STYLE).pack(side=LEFT, padx=5)

        self.reports_tree.bind("<Double-1>", lambda e: self.view_selected_report())
        self.load_reports()

    def load_reports(self):
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)
        try:
            for report in self.app.reports.list_all():
                generated = report["generated_date"]
                if isinstance(generated, datetime):
                    generated = generated.strftime("%Y-%m-%d %H:%M:%S")
                self.reports_tree.insert("", END, values=(
                    report["report_id"], report["staff_name"], report["report_type"],
                    generated, report["description"],
                ))
        except Exception as err:
            messagebox.showerror("Database Error", f"Failed to load reports: {err}")

    def view_selected_report(self):
        selected = self.reports_tree.selection()
        if not selected:
            return

        try:
            report_id = self.reports_tree.item(selected[0])["values"][0]
            raw = self.app.reports.get_data(report_id)
            if not raw:
                messagebox.showerror("Error", "Report data not found in database.")
                return

            filename = json.loads(raw).get("filename")
            if filename and os.path.exists(filename):
                webbrowser.open(os.path.abspath(filename))
            else:
                messagebox.showerror(
                    "Error", "Report file not found. It may have been moved or deleted.")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to view report: {err}")
