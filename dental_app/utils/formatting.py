"""Display formatting helpers."""
from datetime import datetime, timedelta


def to_hhmm(value) -> str:
    """Normalize a MySQL TIME value ('HH:MM', 'HH:MM:SS', or timedelta) to 'HH:MM'."""
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        return f"{total // 3600:02d}:{(total % 3600) // 60:02d}"
    text = str(value)
    return text[:5] if len(text) >= 5 else text


def format_time(value) -> str:
    """Format a MySQL TIME value ('HH:MM', 'HH:MM:SS', or timedelta) as 'HH:00 AM/PM'."""
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        value = f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"
    text = str(value)
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(text, fmt).strftime("%I:00 %p")
        except ValueError:
            continue
    return text
