"""ttkbootstrap style configuration — applied once, shared by all views."""
import ttkbootstrap as ttk

from dental_app.utils.constants import COLORS

_configured = False


def configure_styles():
    global _configured
    if _configured:
        return

    style = ttk.Style()
    style.configure("Modern.TFrame", background=COLORS["light"])
    style.configure("Card.TFrame", background=COLORS["white"], relief="solid", borderwidth=1)
    style.configure("Title.TLabel", font=("Helvetica", 24, "bold"), foreground=COLORS["primary"])
    style.configure("Subtitle.TLabel", font=("Helvetica", 16), foreground=COLORS["secondary"])
    style.configure("Primary.TButton", font=("Helvetica", 12, "bold"), padding=10)
    style.configure("Secondary.TButton", font=("Helvetica", 12), padding=8)

    style.configure("Success.TFrame", background=COLORS["success"])
    style.configure("Warning.TFrame", background=COLORS["warning"])
    style.configure("Danger.TFrame", background=COLORS["danger"])
    style.configure("Info.TFrame", background=COLORS["info"])

    style.configure("Status.Success.TLabel", foreground=COLORS["success"])
    style.configure("Status.Warning.TLabel", foreground=COLORS["warning"])
    style.configure("Status.Danger.TLabel", foreground=COLORS["danger"])
    style.configure("Status.Info.TLabel", foreground=COLORS["info"])

    style.configure("Calendar.TButton", font=("Helvetica", 9))
    style.configure("SelectedTime.TButton", font=("Helvetica", 10, "bold"))
    style.configure("BookedTime.TButton", font=("Helvetica", 10))
    style.configure("OtherBookedTime.TButton", font=("Helvetica", 10))
    style.configure("AvailableTime.TButton", font=("Helvetica", 10))
    style.configure("DisabledTime.TButton", font=("Helvetica", 10))

    _configured = True


def status_frame_style(status: str) -> str:
    return {
        "confirmed": "Success.TFrame",
        "pending": "Warning.TFrame",
        "cancelled": "Danger.TFrame",
    }.get(status, "Info.TFrame")


def status_label_style(status: str) -> str:
    return {
        "confirmed": "Status.Success.TLabel",
        "pending": "Status.Warning.TLabel",
        "cancelled": "Status.Danger.TLabel",
    }.get(status, "Status.Info.TLabel")
