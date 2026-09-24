"""Reusable time-slot grid used by booking and reschedule views."""
import logging
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import X

log = logging.getLogger(__name__)

_STATUS_STYLE = {
    "selected": ("success", "SelectedTime.TButton"),
    "mine": ("warning", "BookedTime.TButton"),
    "taken": ("danger", "OtherBookedTime.TButton"),
    "available": ("primary", "AvailableTime.TButton"),
    "error": ("secondary", "DisabledTime.TButton"),
}


class TimeSlotPicker(ttk.Frame):
    """Renders time-slot buttons colored by availability.

    status_fn(slot) -> 'available' | 'mine' | 'taken'
    on_select(slot) called when the user picks an available slot.
    """

    def __init__(self, parent, slots, status_fn, on_select=None, columns=4, **kwargs):
        super().__init__(parent, **kwargs)
        self.slots = slots
        self.status_fn = status_fn
        self.on_select = on_select
        self.columns = columns
        self.selected_time = None

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()

        for i, slot in enumerate(self.slots):
            try:
                status = "selected" if slot == self.selected_time else self.status_fn(slot)
            except Exception as err:
                log.error("Error checking slot %s: %s", slot, err)
                status = "error"

            bootstyle, style = _STATUS_STYLE.get(status, _STATUS_STYLE["error"])
            ttk.Button(
                self,
                text=slot,
                bootstyle=bootstyle,
                width=8,
                state="disabled" if status == "error" else "normal",
                command=lambda s=slot: self.select(s),
                style=style,
            ).grid(row=i // self.columns, column=i % self.columns, padx=2, pady=2)

    def select(self, slot):
        try:
            status = self.status_fn(slot)
        except Exception as err:
            messagebox.showerror("Error", f"Failed to check time slot availability: {err}")
            return

        if status == "mine":
            messagebox.showwarning("Already Booked", "You have already booked this time slot.")
            return
        if status == "taken":
            messagebox.showwarning(
                "Slot Unavailable", "This time slot is already booked by another client."
            )
            return

        self.selected_time = slot
        self.refresh()
        if self.on_select:
            self.on_select(slot)

    def clear(self):
        self.selected_time = None
        self.refresh()


class TimeSlotsPanel(ttk.Frame):
    """Card panel wrapping a TimeSlotPicker with a title."""

    def __init__(self, parent, slots, status_fn, on_select=None, **kwargs):
        super().__init__(parent, style="Card.TFrame", **kwargs)
        ttk.Label(self, text="Available Time Slots", style="Title.TLabel").pack(pady=10)
        self.picker = TimeSlotPicker(
            self, slots, status_fn, on_select=on_select
        )
        self.picker.pack(fill=X, pady=5, padx=20)
