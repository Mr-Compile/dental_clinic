"""Admin overview tab — stat cards, recent activity, quick actions."""
import logging
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, X, YES

from dental_app.ui.components.recent_activity import render_recent_activity
from dental_app.ui.components.scrollable_frame import ScrollableFrame
from dental_app.ui.components.stat_card import create_stat_card
from dental_app.utils.constants import COLORS

log = logging.getLogger(__name__)


class AdminOverviewView(ttk.Frame):
    def __init__(self, parent, app, notebook):
        super().__init__(parent, style="Modern.TFrame")
        self.app = app
        self.notebook = notebook
        self.refresh()

    def refresh(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build()

    def _build(self):
        scroller = ScrollableFrame(self)
        scroller.pack(fill=BOTH, expand=YES)
        dashboard_grid = ttk.Frame(scroller.inner, style="Modern.TFrame")
        dashboard_grid.pack(fill=BOTH, expand=YES, padx=20, pady=20)

        header_frame = ttk.Frame(dashboard_grid, style="Modern.TFrame")
        header_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(header_frame, text="📊 Dashboard Overview",
                  style="Title.TLabel").pack(side=LEFT)
        ttk.Button(header_frame, text="🔄 Refresh", command=self.refresh,
                   bootstyle="info-outline", width=15).pack(side=RIGHT)

        try:
            stats_frame = ttk.Frame(dashboard_grid, style="Modern.TFrame")
            stats_frame.pack(fill=X, pady=(0, 20))

            create_stat_card(stats_frame, "👥 Total Users",
                             self.app.users.count(), COLORS["primary"], 0)
            create_stat_card(stats_frame, "📅 Total Appointments",
                             self.app.appointments.count_all(), COLORS["success"], 1)
            create_stat_card(stats_frame, "📆 Today's Appointments",
                             self.app.appointments.count_today(), COLORS["info"], 2)
            create_stat_card(stats_frame, "⏳ Pending Appointments",
                             self.app.appointments.count_by_status("pending"),
                             COLORS["warning"], 3)

            activity_frame = ttk.LabelFrame(
                dashboard_grid, text="📋 Recent Activity", style="Card.TFrame", padding=15
            )
            activity_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))
            render_recent_activity(activity_frame, self.app.appointments.list_recent(10))
        except Exception as err:
            log.error("Failed to load dashboard stats: %s", err)
            messagebox.showerror("Error", f"Failed to load dashboard: {err}")

        actions_frame = ttk.LabelFrame(
            dashboard_grid, text="⚡ Quick Actions", style="Card.TFrame", padding=15
        )
        actions_frame.pack(fill=X, pady=(0, 20))

        actions_grid = ttk.Frame(actions_frame, style="Modern.TFrame")
        actions_grid.pack(fill=X, padx=10, pady=10)

        for text, tab_index in (
            ("📋 Manage Appointments", 2),
            ("👤 Manage Users", 1),
            ("📊 View Reports", 3),
        ):
            ttk.Button(actions_grid, text=text,
                       command=lambda i=tab_index: self.notebook.select(i),
                       style="Primary.TButton", width=25).pack(side=LEFT, padx=5)
