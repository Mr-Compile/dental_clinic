"""Reusable month calendar picker used by booking and reschedule views."""
import calendar
from datetime import datetime, timedelta
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import X

from dental_app.utils.constants import CLINIC_CLOSED_WEEKDAY, MAX_BOOKING_DAYS_AHEAD

WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


class CalendarPicker(ttk.Frame):
    """Month-navigable day picker.

    Disabled days: past dates, closed weekdays (Sunday), dates beyond
    max_days_ahead. on_select(date) is called for valid selections.
    """

    def __init__(self, parent, on_select=None, max_days_ahead=MAX_BOOKING_DAYS_AHEAD,
                 closed_weekdays=(CLINIC_CLOSED_WEEKDAY,), **kwargs):
        super().__init__(parent, **kwargs)
        self.on_select = on_select
        self.max_days_ahead = max_days_ahead
        self.closed_weekdays = closed_weekdays
        self.selected_date = None

        today = datetime.now()
        self.current_month = today.month
        self.current_year = today.year

        month_frame = ttk.Frame(self)
        month_frame.pack(fill=X, pady=5)

        ttk.Button(month_frame, text="◀️", command=self.previous_month,
                   style="Primary.TButton", width=3).pack(side="left", padx=5)
        self.month_label = ttk.Label(
            month_frame,
            text=f"{calendar.month_name[self.current_month]} {self.current_year}",
            style="Title.TLabel",
        )
        self.month_label.pack(side="left", padx=20)
        ttk.Button(month_frame, text="▶️", command=self.next_month,
                   style="Primary.TButton", width=3).pack(side="left", padx=5)

        self.dates_frame = ttk.Frame(self)
        self.dates_frame.pack(fill=X, pady=10)

        for i, day in enumerate(WEEKDAYS):
            ttk.Label(
                self.dates_frame, text=day, width=8, anchor="center",
                style="Subtitle.TLabel",
                bootstyle="danger" if i == 0 else "primary",
            ).grid(row=0, column=i, padx=1, pady=1, sticky="nsew")

        for i in range(7):
            self.dates_frame.grid_columnconfigure(i, weight=1)
            self.dates_frame.grid_rowconfigure(i, weight=1)

        self.refresh()

    # ---------- rendering ----------

    def _is_disabled(self, date):
        today = datetime.now().date()
        return (
            date < today
            or date.weekday() in self.closed_weekdays
            or date > today + timedelta(days=self.max_days_ahead)
        )

    def refresh(self):
        for widget in self.dates_frame.grid_slaves():
            if widget.grid_info()["row"] != 0:
                widget.destroy()

        self.month_label.config(
            text=f"{calendar.month_name[self.current_month]} {self.current_year}"
        )

        first_day = datetime(self.current_year, self.current_month, 1)
        total_days = calendar.monthrange(self.current_year, self.current_month)[1]
        start_pos = (first_day.weekday() + 1) % 7  # Sunday-based grid
        today = datetime.now().date()

        day_count = 1
        for week in range(6):
            for weekday in range(7):
                if (week == 0 and weekday < start_pos) or day_count > total_days:
                    ttk.Label(self.dates_frame, text="", width=8).grid(
                        row=week + 1, column=weekday, padx=1, pady=1
                    )
                    continue

                date = datetime(self.current_year, self.current_month, day_count).date()
                disabled = self._is_disabled(date)

                if date == self.selected_date:
                    bootstyle = "success"
                elif date == today:
                    bootstyle = "warning"
                elif disabled:
                    bootstyle = "secondary"
                else:
                    bootstyle = "primary"

                ttk.Button(
                    self.dates_frame,
                    text=str(day_count),
                    bootstyle=bootstyle,
                    state="disabled" if disabled else "normal",
                    command=lambda d=date: self._select(d),
                    width=8,
                    style="Calendar.TButton",
                ).grid(row=week + 1, column=weekday, padx=1, pady=1)
                day_count += 1

    # ---------- navigation ----------

    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.refresh()

    def next_month(self):
        today = datetime.now()
        max_date = today + timedelta(days=self.max_days_ahead)
        next_first = datetime(self.current_year, self.current_month, 1) + timedelta(days=32)
        next_first = datetime(next_first.year, next_first.month, 1)

        if next_first <= max_date:
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
            self.refresh()
        else:
            messagebox.showinfo(
                "Booking Limit",
                f"You can only book appointments up to {self.max_days_ahead} days in advance.",
            )

    # ---------- selection ----------

    def _select(self, date):
        if date.weekday() in self.closed_weekdays:
            messagebox.showwarning(
                "Clinic Closed", "The clinic is closed on that day. Please select another day."
            )
            return
        if date < datetime.now().date():
            messagebox.showwarning("Invalid Date", "Cannot book appointments for past dates.")
            return
        if date > datetime.now().date() + timedelta(days=self.max_days_ahead):
            messagebox.showwarning(
                "Invalid Date",
                f"Cannot book appointments more than {self.max_days_ahead} days in advance.",
            )
            return

        self.selected_date = date
        self.refresh()
        if self.on_select:
            self.on_select(date)
