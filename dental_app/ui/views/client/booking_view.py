"""Client booking tab — service, calendar, time slots, book button."""
import logging
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import X

from dental_app.ui.components.calendar_picker import CalendarPicker
from dental_app.ui.components.scrollable_frame import ScrollableFrame
from dental_app.ui.components.time_slot_picker import TimeSlotsPanel
from dental_app.utils.constants import SERVICES, TIME_SLOTS

log = logging.getLogger(__name__)


class BookingView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, style="Modern.TFrame")
        self.app = app
        self.selected_date = None
        self._build()

    def _build(self):
        scroller = ScrollableFrame(self)
        scroller.pack(fill="both", expand=True)
        page = scroller.inner

        # Service selection
        service_frame = ttk.Frame(page, style="Card.TFrame")
        service_frame.pack(fill=X, pady=(20, 10), padx=20)

        ttk.Label(service_frame, text="Select Service:",
                  style="Subtitle.TLabel").pack(side="left", padx=20, pady=10)
        self.service_var = tk.StringVar()
        self.service_combo = ttk.Combobox(
            service_frame, textvariable=self.service_var, values=SERVICES,
            state="readonly", width=30, font=("Helvetica", 12),
        )
        self.service_combo.pack(side="left", padx=10, pady=10)

        # Date selection
        date_frame = ttk.Frame(page, style="Card.TFrame")
        date_frame.pack(fill=X, padx=20, pady=10)

        self.calendar = CalendarPicker(date_frame, on_select=self._on_date_select)
        self.calendar.pack(fill=X, padx=20, pady=10)

        # Time slots
        self.slots_panel = TimeSlotsPanel(
            page, TIME_SLOTS, status_fn=self._slot_status,
            on_select=self._on_time_select,
        )
        self.slots_panel.pack(fill=X, padx=20, pady=10)

        # Book button
        self.book_button = ttk.Button(
            page, text="📅 Book Appointment", command=self.book,
            bootstyle="success", state="disabled",
        )
        self.book_button.pack(pady=20)

    # ---------- callbacks ----------

    def _slot_status(self, slot):
        if not self.selected_date:
            return "available"
        return self.app.booking.slot_status(
            self.selected_date, slot, self.app.current_user["id"]
        )

    def _on_date_select(self, date):
        self.selected_date = date
        # New date invalidates any previously chosen slot (fixes stale selection)
        self.slots_panel.picker.selected_time = None
        self.book_button.configure(state="disabled")
        self.slots_panel.picker.refresh()

    def _on_time_select(self, _slot):
        self.book_button.configure(state="normal")

    # ---------- booking ----------

    def book(self):
        if not self.service_var.get():
            messagebox.showerror("Error", "Please select a service")
            return
        if not self.selected_date or not self.slots_panel.picker.selected_time:
            messagebox.showerror("Error", "Please select both date and time")
            return

        try:
            ok, message = self.app.booking.book(
                user_id=self.app.current_user["id"],
                service=self.service_var.get(),
                date=self.selected_date.strftime("%Y-%m-%d"),
                time=self.slots_panel.picker.selected_time,
            )
            if ok:
                messagebox.showinfo("Success", message)
                self.service_combo.set("")
                self.selected_date = None
                self.calendar.selected_date = None
                self.calendar.refresh()
                self.slots_panel.picker.selected_time = None
                self.slots_panel.picker.refresh()
                self.book_button.configure(state="disabled")
            else:
                messagebox.showerror("Error", message)
                self.slots_panel.picker.refresh()
        except Exception as err:
            log.error("Booking failed: %s", err)
            messagebox.showerror("Error", f"Booking failed: {err}")
