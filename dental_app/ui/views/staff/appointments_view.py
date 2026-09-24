"""Staff appointment tab — filter, search, status changes (SMS), PDF reports."""
import logging
import os
import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, CENTER, LEFT, RIGHT, VERTICAL, X, Y, YES

from dental_app.ui.components.confirm_dialog import ModernConfirmationDialog
from dental_app.utils.constants import (
    APPOINTMENT_STATUSES,
    DATE_FILTER_OPTIONS,
    STATUS_ICONS,
    STATUS_TAG_COLORS,
)
from dental_app.utils.formatting import format_time

log = logging.getLogger(__name__)

BUTTON_STYLE = {"width": 20, "padding": 12}

_STATUS_ACTION_TEXT = {
    "confirmed": ("Confirm Appointment", "confirm", "success"),
    "completed": ("Mark as Completed", "mark this appointment as completed", "info"),
    "cancelled": ("Cancel Appointment", "cancel this appointment", "danger"),
}


class StaffAppointmentsView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        filters_frame = ttk.Frame(self)
        filters_frame.pack(fill=X, padx=5, pady=5)

        search_frame = ttk.Frame(filters_frame)
        search_frame.pack(fill=X, pady=5)

        ttk.Label(search_frame, text="🔍 Search Appointment:", bootstyle="primary").pack(
            side=LEFT, padx=(5, 0))
        self.appt_search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.appt_search_var,
                  width=30).pack(side=LEFT, padx=5)
        ttk.Button(search_frame, text="🔎 Search", bootstyle="primary",
                   command=self.search_appointments).pack(side=LEFT, padx=5)
        ttk.Button(search_frame, text="🔄 Clear", bootstyle="info",
                   command=self.clear_search).pack(side=LEFT, padx=5)

        filter_options_frame = ttk.Frame(filters_frame)
        filter_options_frame.pack(fill=X, pady=5)

        ttk.Label(filter_options_frame, text="📅 Date:", bootstyle="primary").pack(
            side=LEFT, padx=5)
        self.date_var = tk.StringVar(value="All")
        ttk.Combobox(filter_options_frame, textvariable=self.date_var,
                     values=DATE_FILTER_OPTIONS, state="readonly",
                     width=15).pack(side=LEFT, padx=5)

        ttk.Label(filter_options_frame, text="📊 Status:", bootstyle="primary").pack(
            side=LEFT, padx=5)
        self.status_var = tk.StringVar(value="All")
        ttk.Combobox(filter_options_frame, textvariable=self.status_var,
                     values=["All"] + APPOINTMENT_STATUSES, state="readonly",
                     width=15).pack(side=LEFT, padx=5)

        ttk.Button(filter_options_frame, text="✅ Apply Filters",
                   bootstyle="primary-outline",
                   command=self.load_appointments).pack(side=LEFT, padx=5)

        horizontal_frame = ttk.Frame(self)
        horizontal_frame.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        left_frame = ttk.Frame(horizontal_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        columns = ("id", "username", "service", "date", "time", "contact", "status")
        column_widths = {"id": 40, "username": 120, "service": 180, "date": 90,
                         "time": 90, "contact": 100, "status": 90}
        headings = {"id": "🔢 ID", "username": "👤 Patient Name",
                    "service": "🦷 Dental Service", "date": "📅 Appointment Date",
                    "time": "⏰ Appointment Time", "contact": "📱 Contact Number",
                    "status": "📊 Appointment Status"}

        self.appt_tree = ttk.Treeview(left_frame, columns=columns,
                                      show="headings", bootstyle="primary")
        for status, colors in STATUS_TAG_COLORS.items():
            self.appt_tree.tag_configure(status, **colors)
        for col in columns:
            self.appt_tree.heading(col, text=headings[col])
            self.appt_tree.column(col, width=column_widths[col], anchor=CENTER)

        scrollbar = ttk.Scrollbar(left_frame, orient=VERTICAL,
                                  command=self.appt_tree.yview)
        self.appt_tree.configure(yscrollcommand=scrollbar.set)
        self.appt_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        buttons_frame = ttk.Frame(horizontal_frame)
        buttons_frame.pack(side=RIGHT, fill=Y, padx=10, pady=5)

        ttk.Button(buttons_frame, text="✅ Confirm",
                   command=lambda: self.update_appointment_status("confirmed"),
                   bootstyle="success", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="🏥 Completed",
                   command=lambda: self.update_appointment_status("completed"),
                   bootstyle="info", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="❌ Cancel",
                   command=lambda: self.update_appointment_status("cancelled"),
                   bootstyle="danger", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="📊 Generate Report",
                   command=self.generate_appointments_report,
                   bootstyle="warning", **BUTTON_STYLE).pack(fill=X, pady=2)

        self.appt_tree.bind("<Double-1>", self.open_appointment_action_modal)
        self.load_appointments()

    # ---------- data ----------

    def _filters(self):
        return {
            "date_filter": self.date_var.get(),
            "status": self.status_var.get(),
            "search": self.appt_search_var.get().strip(),
        }

    def _populate(self, rows):
        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)
        for appt in rows:
            status = str(appt["status"]).lower()
            self.appt_tree.insert("", "end", values=(
                appt["id"],
                appt["username"],
                appt["service"],
                appt["appointment_date"],
                format_time(appt["appointment_time"]),
                appt["phone_number"],
                f"{STATUS_ICONS.get(status, '')} {status.capitalize()}",
            ), tags=(status,))

    def load_appointments(self):
        try:
            self._populate(self.app.appointments.list_filtered(**self._filters()))
        except Exception as err:
            messagebox.showerror("Error", f"Failed to load appointments: {err}")

    def search_appointments(self):
        self.load_appointments()

    def clear_search(self):
        self.appt_search_var.set("")
        self.load_appointments()

    def _selected_appointment(self):
        selected = self.appt_tree.selection()
        if not selected:
            return None
        return self.appt_tree.item(selected[0])["values"]

    # ---------- status changes ----------

    def update_appointment_status(self, new_status):
        values = self._selected_appointment()
        if not values:
            messagebox.showerror("Error", "Please select an appointment")
            return

        appt_id, username, service, date, time = values[:5]
        title, action_text, action_type = _STATUS_ACTION_TEXT[new_status]
        message = (
            f"Are you sure you want to {action_text}?\n\n"
            f"Client: {username}\nService: {service}\nDate: {date}\nTime: {time}\n\n"
            f"This will notify the client via SMS."
        )
        if not ModernConfirmationDialog(self, title, message, action_type).show():
            return

        try:
            appt = self.app.appointments.get_with_user(appt_id)
            if not appt:
                messagebox.showerror("Error", "Could not find appointment details")
                return

            if not self.app.appointments.update_status(appt_id, new_status):
                messagebox.showerror("Error", "Failed to update appointment status. Please try again.")
                return

            sms_ok, sms_message = self.app.sms.send_appointment_notification(
                appt["phone_number"],
                {
                    "appointment_date": appt["appointment_date"],
                    "appointment_time": appt["appointment_time"],
                    "service": appt["service"],
                    "client_name": appt["username"],
                },
                new_status,
            )
            if not sms_ok:
                messagebox.showwarning(
                    "SMS Notification",
                    f"Appointment updated but SMS notification failed: {sms_message}")

            messagebox.showinfo("Success", f"Appointment marked as {new_status.capitalize()}!")
            self.load_appointments()
        except Exception as err:
            messagebox.showerror("Error", f"Failed to update appointment: {err}")

    # ---------- action modal ----------

    def open_appointment_action_modal(self, _event):
        values = self._selected_appointment()
        if not values:
            return

        _appt_id, username, service, date, time, _contact, status = values

        dialog = tk.Toplevel(self)
        dialog.title(f"Manage Appointment - {username}")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()

        for text in (f"Username: {username}", f"Service: {service}",
                     f"Date: {date}", f"Time: {time}", f"Status: {status}"):
            ttk.Label(dialog, text=text, font=("Helvetica", 12)).pack(pady=5)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        def update_status(new_status):
            self.update_appointment_status(new_status)
            dialog.destroy()

        ttk.Button(button_frame, text="Confirm", bootstyle="success",
                   command=lambda: update_status("confirmed")).pack(fill=X, pady=5)
        ttk.Button(button_frame, text="Mark as Completed", bootstyle="info",
                   command=lambda: update_status("completed")).pack(fill=X, pady=5)
        ttk.Button(button_frame, text="Cancel Appointment", bootstyle="danger",
                   command=lambda: update_status("cancelled")).pack(fill=X, pady=5)
        ttk.Button(dialog, text="Close", command=dialog.destroy,
                   bootstyle="secondary").pack(pady=10)

    # ---------- reports ----------

    def generate_appointments_report(self):
        try:
            filters = self._filters()
            rows = self.app.appointments.list_for_report(**filters)

            if not rows:
                messagebox.showinfo(
                    "Report Generation", "No appointments found for the selected filters.")
                return

            filename = self.app.report_service.generate_appointment_report(rows)

            self.app.reports.create(
                staff_id=self.app.current_user["id"],
                report_type="Appointments Report",
                description=(
                    f"Appointments report generated with filters: "
                    f"Date={filters['date_filter']}, Status={filters['status']}, "
                    f"Client Search={filters['search']}"
                ),
                report_data={
                    "filename": filename,
                    "filters": filters,
                    "appointments": rows,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )

            if messagebox.askyesno(
                "Report Generated",
                "Report has been generated successfully!\nWould you like to open it now?",
            ):
                webbrowser.open(os.path.abspath(filename))
        except Exception as err:
            log.error("Failed to generate report: %s", err)
            messagebox.showerror("Error", f"Failed to generate report: {err}")
