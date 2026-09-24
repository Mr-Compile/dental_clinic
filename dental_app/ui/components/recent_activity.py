"""Recent-activity list shared by admin and staff overview tabs."""
import ttkbootstrap as ttk
from ttkbootstrap.constants import LEFT, X, Y

from dental_app.ui.styles import status_frame_style, status_label_style
from dental_app.utils.constants import STATUS_ICONS


def render_recent_activity(parent, rows):
    """Parent is a LabelFrame; rows come from AppointmentRepository.list_recent()."""
    for row in rows:
        status = str(row["status"]).lower()
        icon = STATUS_ICONS.get(status, "")

        item = ttk.Frame(parent, style="Card.TFrame")
        item.pack(fill=X, padx=10, pady=5)

        ttk.Frame(item, width=10, style=status_frame_style(status)).pack(
            side=LEFT, padx=(5, 10), pady=5, fill=Y
        )

        ttk.Label(
            item,
            text=(
                f"📅 {row['formatted_date']} {row['formatted_time']} | "
                f"👤 {row['username']} | 🦷 {row['service']} | "
                f"{icon} {status.capitalize()}"
            ),
            style=status_label_style(status),
        ).pack(side=LEFT, padx=10, pady=5)
