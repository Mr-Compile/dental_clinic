"""Admin appointment management tab — filter, search, edit, delete, status changes."""
import logging
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, CENTER, LEFT, RIGHT, VERTICAL, W, X, Y, YES

from dental_app.ui.components.confirm_dialog import ModernConfirmationDialog
from dental_app.utils.constants import (
    APPOINTMENT_STATUSES,
    DATE_FILTER_OPTIONS,
    SERVICES,
    STATUS_ICONS,
    STATUS_TAG_COLORS,
    TIME_SLOTS,
)
from dental_app.utils.formatting import format_time, to_hhmm

log = logging.getLogger(__name__)

BUTTON_STYLE = {"width": 20, "padding": 12}

_STATUS_ACTION_TEXT = {
    "confirmed": ("Confirm Appointment", "confirm", "success"),
    "completed": ("Mark as Completed", "mark this appointment as completed", "info"),
    "cancelled": ("Cancel Appointment", "cancel this appointment", "danger"),
}


class AdminAppointmentsView(ttk.Frame):
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

        ttk.Button(buttons_frame, text="✏️ Edit", command=self.edit_appointment,
                   bootstyle="primary", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="🗑️ Delete", command=self.delete_appointment,
                   bootstyle="danger", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="✅ Confirm",
                   command=lambda: self.update_appointment_status("confirmed"),
                   bootstyle="success", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="🏥 Completed",
                   command=lambda: self.update_appointment_status("completed"),
                   bootstyle="info", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="❌ Cancel",
                   command=lambda: self.update_appointment_status("cancelled"),
                   bootstyle="warning", **BUTTON_STYLE).pack(fill=X, pady=2)

        self.appt_tree.bind("<Double-1>", self.open_appointment_action_modal)
        self.load_appointments()

    # ---------- data ----------

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
            self._populate(self.app.appointments.list_filtered(
                date_filter=self.date_var.get(),
                status=self.status_var.get(),
            ))
        except Exception as err:
            messagebox.showerror("Error", f"Failed to load appointments: {err}")

    def search_appointments(self):
        term = self.appt_search_var.get().strip()
        if not term:
            self.load_appointments()
            return
        try:
            rows = self.app.appointments.list_filtered(search=term)
            self._populate(rows)
            if not rows:
                messagebox.showinfo("No Results", "No appointments found matching your search.")
        except Exception as err:
            messagebox.showerror("Error", f"Search failed: {err}")

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

        appt_id, username, service, date, time = values[0], values[1], values[2], values[3], values[4]
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
        if not self._selected_appointment():
            return

        dialog = tk.Toplevel(self)
        dialog.title("Appointment Actions")
        dialog.transient(self)
        dialog.grab_set()

        width, height = 400, 300
        x = (dialog.winfo_screenwidth() - width) // 2
        y = (dialog.winfo_screenheight() - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        ttk.Label(main_frame, text="Appointment Actions",
                  font=("Helvetica", 16, "bold"), bootstyle="primary").pack(pady=(0, 20))

        actions = [
            ("Edit", "primary", self.edit_appointment),
            ("Delete", "danger", self.delete_appointment),
            ("Confirm", "success", lambda: self.update_appointment_status("confirmed")),
            ("Mark as Completed", "info", lambda: self.update_appointment_status("completed")),
            ("Cancel Appointment", "warning", lambda: self.update_appointment_status("cancelled")),
        ]
        for text, style, command in actions:
            ttk.Button(main_frame, text=text, bootstyle=style,
                       command=lambda c=command: [c(), dialog.destroy()],
                       width=20, padding=10).pack(pady=5)

        ttk.Button(main_frame, text="Close", bootstyle="secondary",
                   command=dialog.destroy, width=20, padding=10).pack(pady=(20, 0))

    # ---------- edit ----------

    def edit_appointment(self):
        values = self._selected_appointment()
        if not values:
            messagebox.showerror("Error", "Please select an appointment to edit")
            return

        appt_id, username = values[0], values[1]

        appt = self.app.appointments.get_with_user(appt_id)
        if not appt:
            messagebox.showerror("Error", "Could not find appointment details")
            return
        current_service = appt["service"]
        current_date = str(appt["appointment_date"])
        current_time = to_hhmm(appt["appointment_time"])
        current_status = str(appt["status"]).lower()

        dialog = tk.Toplevel(self)
        dialog.title(f"Edit Appointment - {username}")
        dialog.transient(self)
        dialog.grab_set()

        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=BOTH, expand=True)

        ttk.Label(form_frame, text="Service:").grid(row=0, column=0, sticky=W, pady=5)
        service_var = tk.StringVar(value=current_service)
        ttk.Combobox(form_frame, textvariable=service_var, values=SERVICES,
                     state="readonly", width=30).grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Date:").grid(row=1, column=0, sticky=W, pady=5)
        date_var = tk.StringVar(value=str(current_date))
        ttk.Entry(form_frame, textvariable=date_var, width=30).grid(row=1, column=1, pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD)", font=("Helvetica", 8)).grid(
            row=1, column=2, sticky=W)

        ttk.Label(form_frame, text="Time:").grid(row=2, column=0, sticky=W, pady=5)
        time_var = tk.StringVar(value=current_time)
        ttk.Combobox(form_frame, textvariable=time_var, values=TIME_SLOTS,
                     state="readonly", width=30).grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Status:").grid(row=3, column=0, sticky=W, pady=5)
        status_var = tk.StringVar(value=current_status)
        ttk.Combobox(form_frame, textvariable=status_var, values=APPOINTMENT_STATUSES,
                     state="readonly", width=30).grid(row=3, column=1, pady=5)

        def save_changes():
            try:
                new_service = service_var.get()
                new_date = date_var.get()
                new_time = time_var.get()
                new_status = status_var.get()

                try:
                    datetime.strptime(new_date, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD")
                    return

                if (new_date != current_date or new_time != current_time) and \
                        self.app.appointments.slot_taken(new_date, new_time, exclude_id=appt_id):
                    messagebox.showerror("Error", "This time slot is already booked")
                    return

                if self.app.appointments.update(appt_id, new_service, new_date, new_time, new_status):
                    messagebox.showinfo("Success", "Appointment updated successfully!")
                    self.load_appointments()
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update appointment")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to update appointment: {err}")

        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Save", command=save_changes,
                   bootstyle="success").pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy,
                   bootstyle="secondary").pack(side=LEFT, padx=5)

        dialog.update_idletasks()
        width = max(450, dialog.winfo_width())
        height = max(350, dialog.winfo_height())
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    # ---------- delete ----------

    def delete_appointment(self):
        values = self._selected_appointment()
        if not values:
            messagebox.showerror("Error", "Please select an appointment to delete")
            return

        appt_id, username, service, date, time = values[:5]
        message = (
            f"Are you sure you want to delete this appointment?\n\n"
            f"Client: {username}\nService: {service}\nDate: {date}\nTime: {time}\n\n"
            f"This action cannot be undone!\nAll associated data will be permanently removed."
        )
        if not ModernConfirmationDialog(self, "Delete Appointment", message, "danger").show():
            return

        try:
            if self.app.appointments.delete(appt_id):
                messagebox.showinfo("Success", "Appointment deleted successfully!")
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Failed to delete appointment")
        except Exception as err:
            messagebox.showerror("Error", f"Failed to delete appointment: {err}")
