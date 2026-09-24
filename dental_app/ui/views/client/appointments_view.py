"""Client appointments tab — list, filter, reschedule, cancel, details."""
import logging
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, CENTER, LEFT, RIGHT, VERTICAL, X, Y

from dental_app.ui.components.calendar_picker import CalendarPicker
from dental_app.ui.components.time_slot_picker import TimeSlotPicker
from dental_app.utils.constants import APPOINTMENT_STATUSES, STATUS_ICONS, STATUS_TAG_COLORS, TIME_SLOTS
from dental_app.utils.formatting import format_time

log = logging.getLogger(__name__)

_RESCHEDULABLE = ("pending", "confirmed")


class ClientAppointmentsView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Modern.TFrame")
        self.app = app
        self._build()

    def _build(self):
        filter_frame = ttk.Frame(self, style="Card.TFrame")
        filter_frame.pack(fill=X, pady=(0, 20), padx=20)

        ttk.Label(filter_frame, text="🔍 Status:", style="Subtitle.TLabel").pack(
            side=LEFT, padx=20, pady=10)
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame, textvariable=self.status_var,
            values=["All"] + APPOINTMENT_STATUSES, state="readonly",
            width=15, font=("Helvetica", 12),
        )
        status_combo.pack(side=LEFT, padx=5, pady=10)
        status_combo.bind("<<ComboboxSelected>>", lambda e: self.load_appointments())

        search_frame = ttk.Frame(self, style="Card.TFrame")
        search_frame.pack(fill=X, pady=(0, 20), padx=20)

        ttk.Label(search_frame, text="🔎 Search:", style="Subtitle.TLabel").pack(
            side=LEFT, padx=20, pady=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var,
                                 width=30, font=("Helvetica", 12))
        search_entry.pack(side=LEFT, padx=5, pady=10)
        search_entry.bind("<KeyRelease>", lambda e: self.load_appointments())

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=BOTH, expand=True, padx=20)

        columns = ("id", "service", "date", "time", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                 bootstyle="primary", height=10)

        headings = {"id": "🆔 ID", "service": "🦷 Service", "date": "📅 Date",
                    "time": "⏰ Time", "status": "📊 Status"}
        widths = {"id": 50, "service": 150, "date": 100, "time": 100, "status": 100}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor=CENTER)

        for status, colors in STATUS_TAG_COLORS.items():
            self.tree.tag_configure(status, **colors)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        action_frame = ttk.Frame(self, style="Card.TFrame")
        action_frame.pack(fill=X, pady=(20, 0), padx=20)

        self.reschedule_btn = ttk.Button(
            action_frame, text="🔄 Reschedule", command=self.reschedule_appointment,
            bootstyle="info", state="disabled",
        )
        self.reschedule_btn.pack(side=LEFT, padx=5, pady=10)

        self.cancel_btn = ttk.Button(
            action_frame, text="❌ Cancel", command=self.cancel_appointment,
            bootstyle="danger", state="disabled",
        )
        self.cancel_btn.pack(side=LEFT, padx=5, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self.show_appointment_details)

        self.load_appointments()

    # ---------- data ----------

    def load_appointments(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            rows = self.app.appointments.list_by_user(
                self.app.current_user["id"],
                status=self.status_var.get(),
                search=self.search_var.get().strip(),
            )
            for appt in rows:
                status = str(appt["status"]).lower()
                self.tree.insert("", "end", values=(
                    appt["id"],
                    appt["service"],
                    appt["appointment_date"],
                    format_time(appt["appointment_time"]),
                    f"{STATUS_ICONS.get(status, '')} {status.capitalize()}",
                ), tags=(status,))
        except Exception as err:
            messagebox.showerror("Error", f"Failed to load appointments: {err}")

    def _on_select(self, _event):
        selected = self.tree.selection()
        enabled = "disabled"
        if selected:
            raw_status = self.tree.item(selected[0])["values"][4]
            status = str(raw_status).split()[-1].lower()  # strip emoji prefix
            if status in _RESCHEDULABLE:
                enabled = "normal"
        self.reschedule_btn.configure(state=enabled)
        self.cancel_btn.configure(state=enabled)

    def _selected(self):
        selected = self.tree.selection()
        return self.tree.item(selected[0])["values"] if selected else None

    # ---------- reschedule ----------

    def reschedule_appointment(self):
        values = self._selected()
        if not values:
            return
        appt_id, service, date, time, _status = values

        dialog = tk.Toplevel(self)
        dialog.title("Reschedule Appointment")
        dialog.transient(self)
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, style="Card.TFrame", padding=20)
        main_frame.pack(fill=BOTH, expand=True)

        ttk.Label(main_frame, text="Reschedule Appointment",
                  style="Title.TLabel", font=("Helvetica", 24, "bold")).pack(
                  anchor="w", pady=(0, 15))

        info_frame = ttk.LabelFrame(main_frame, text="Current Appointment Details",
                                    padding=15, bootstyle="primary")
        info_frame.pack(fill=X, pady=(0, 20))
        for icon, label, value in (
            ("🦷", "Service:", service),
            ("📅", "Current Date:", date),
            ("⏰", "Current Time:", time),
        ):
            row = ttk.Frame(info_frame)
            row.pack(fill=X, pady=5)
            ttk.Label(row, text=f"{icon} {label}", style="Subtitle.TLabel",
                      font=("Helvetica", 12, "bold")).pack(side=LEFT, padx=(0, 10))
            ttk.Label(row, text=str(value), style="Subtitle.TLabel",
                      font=("Helvetica", 12)).pack(side=LEFT)

        state = {"date": None}

        date_frame = ttk.LabelFrame(main_frame, text="Select New Date",
                                    padding=15, bootstyle="primary")
        date_frame.pack(fill=X, pady=(0, 20))

        def on_date_selected(d):
            state["date"] = d
            state["time"] = None
            slot_picker.selected_time = None
            slot_picker.refresh()

        calendar_picker = CalendarPicker(date_frame, on_select=on_date_selected)
        calendar_picker.pack(fill=X, pady=10)

        time_frame = ttk.LabelFrame(main_frame, text="Select New Time",
                                    padding=15, bootstyle="primary")
        time_frame.pack(fill=X, pady=(0, 20))

        def slot_status(slot):
            if not state["date"]:
                return "available"
            return self.app.booking.slot_status(
                state["date"], slot, self.app.current_user["id"]
            )

        slot_picker = TimeSlotPicker(
            time_frame, TIME_SLOTS, status_fn=slot_status,
            on_select=lambda s: state.__setitem__("time", s),
        )
        slot_picker.pack(fill=X, pady=10)
        state["time"] = None

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=X, pady=(20, 0))
        button_container = ttk.Frame(action_frame)
        button_container.pack(expand=True)

        def confirm():
            if not state["date"] or not state["time"]:
                messagebox.showerror("Error", "Please select both date and time")
                return
            ok, message = self.app.booking.reschedule(
                self.app.current_user["id"], appt_id,
                state["date"].strftime("%Y-%m-%d"), state["time"],
            )
            if ok:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.load_appointments()
            else:
                messagebox.showerror("Error", message)

        ttk.Button(button_container, text="✅ Confirm Reschedule", command=confirm,
                   bootstyle="success", style="Primary.TButton",
                   width=20).pack(side=LEFT, padx=10)
        ttk.Button(button_container, text="✖️ Cancel", command=dialog.destroy,
                   bootstyle="secondary", style="Secondary.TButton",
                   width=15).pack(side=LEFT, padx=10)

        dialog.update_idletasks()
        width = max(600, dialog.winfo_width())
        height = max(700, dialog.winfo_height())
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

    # ---------- cancel ----------

    def cancel_appointment(self):
        values = self._selected()
        if not values:
            return
        appt_id, service, date, time, status = values

        cancel_dialog = tk.Toplevel(self)
        cancel_dialog.title("Cancel Appointment")
        cancel_dialog.transient(self)
        cancel_dialog.grab_set()

        main_frame = ttk.Frame(cancel_dialog, style="Card.TFrame")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        warning_frame = ttk.Frame(main_frame)
        warning_frame.pack(fill=X, pady=10)
        ttk.Label(warning_frame, text="⚠️", font=("Helvetica", 32)).pack(side=LEFT, padx=10)
        ttk.Label(warning_frame, text="Are you sure you want to cancel this appointment?",
                  style="Title.TLabel", wraplength=300).pack(side=LEFT, padx=10)

        details_frame = ttk.LabelFrame(main_frame, text="Appointment Details", padding=10)
        details_frame.pack(fill=X, pady=10)

        for label, value in (("Service:", service), ("Date:", date),
                             ("Time:", time), ("Status:", str(status))):
            row = ttk.Frame(details_frame, style="Modern.TFrame")
            row.pack(fill=X, pady=2)
            ttk.Label(row, text=label, style="Subtitle.TLabel",
                      width=10).pack(side=LEFT, padx=5)
            ttk.Label(row, text=str(value), style="Subtitle.TLabel").pack(side=LEFT, padx=5)

        restrictions_frame = ttk.Frame(main_frame, style="Modern.TFrame")
        restrictions_frame.pack(fill=X, pady=10)
        ttk.Label(restrictions_frame, text="⚠️ Restrictions:",
                  style="Subtitle.TLabel", foreground="#e74c3c").pack(anchor="w", pady=2)
        for restriction in (
            "• Cancellation cannot be undone",
            "• You may need to wait for a new appointment slot",
            "• Late cancellations may affect future bookings",
        ):
            ttk.Label(restrictions_frame, text=restriction, style="Subtitle.TLabel",
                      foreground="#e74c3c").pack(anchor="w", pady=1)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=20)

        def confirm_cancel():
            ok, message = self.app.booking.cancel(self.app.current_user["id"], appt_id)
            if ok:
                messagebox.showinfo("Success", message)
                self.load_appointments()
                cancel_dialog.destroy()
            else:
                messagebox.showerror("Error", message)

        ttk.Button(button_frame, text="No, Keep Appointment",
                   command=cancel_dialog.destroy,
                   style="Secondary.TButton").pack(side=RIGHT, padx=5)
        ttk.Button(button_frame, text="Yes, Cancel Appointment",
                   command=confirm_cancel,
                   bootstyle="danger").pack(side=RIGHT, padx=5)

        cancel_dialog.update_idletasks()
        width = max(400, cancel_dialog.winfo_width())
        height = max(450, cancel_dialog.winfo_height())
        x = (cancel_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (cancel_dialog.winfo_screenheight() // 2) - (height // 2)
        cancel_dialog.geometry(f"{width}x{height}+{x}+{y}")

    # ---------- details ----------

    def show_appointment_details(self, _event):
        values = self._selected()
        if not values:
            return
        _appt_id, service, date, time, status = values

        dialog = tk.Toplevel(self)
        dialog.title("Appointment Details")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        main_frame = ttk.Frame(dialog, style="Card.TFrame")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        for label, value in (("Service:", service), ("Date:", date),
                             ("Time:", time), ("Status:", str(status))):
            row = ttk.Frame(main_frame, style="Modern.TFrame")
            row.pack(fill=X, pady=5)
            ttk.Label(row, text=label, style="Subtitle.TLabel",
                      width=10).pack(side=LEFT, padx=5)
            ttk.Label(row, text=str(value), style="Subtitle.TLabel").pack(side=LEFT, padx=5)

        ttk.Button(main_frame, text="Close", command=dialog.destroy,
                   style="Secondary.TButton").pack(pady=20)
