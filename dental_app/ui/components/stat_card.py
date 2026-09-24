import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT


def create_stat_card(parent, title, value, color, column):
    """Render a dashboard stat card; title starts with an emoji icon."""
    card = ttk.Frame(parent, style="Card.TFrame", padding=15)
    card.grid(row=0, column=column, padx=10, sticky="nsew")
    parent.grid_columnconfigure(column, weight=1)

    icon_frame = ttk.Frame(card)
    icon_frame.pack(side=LEFT, padx=(0, 15))

    icon = title.split()[0]
    title_text = " ".join(title.split()[1:])

    ttk.Label(icon_frame, text=icon, font=("Helvetica", 32), foreground=color).pack()

    content_frame = ttk.Frame(card)
    content_frame.pack(side=LEFT, fill=BOTH, expand=True)

    ttk.Label(content_frame, text=title_text, style="Subtitle.TLabel",
              foreground=color, font=("Helvetica", 14, "bold")).pack(pady=(10, 5))
    ttk.Label(content_frame, text=str(value), font=("Helvetica", 36, "bold"),
              foreground=color).pack(pady=(0, 10))
