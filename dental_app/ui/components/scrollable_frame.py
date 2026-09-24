import tkinter as tk

import ttkbootstrap as ttk


class ScrollableFrame(ttk.Frame):
    """Canvas-backed scrollable container.

    Mouse wheel scrolling is bound only while the pointer is over the widget,
    so bindings never leak into other screens (the old code used bare
    bind_all which kept firing after the frame was destroyed).
    """

    def __init__(self, parent, inner_bootstyle=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        if inner_bootstyle:
            self.inner = ttk.Frame(self.canvas, bootstyle=inner_bootstyle)
        else:
            self.inner = ttk.Frame(self.canvas)

        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self._window_id = self.canvas.create_window(
            (0, 0), window=self.inner, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<Enter>", self._bind_wheel)
        self.canvas.bind("<Leave>", self._unbind_wheel)
        self.bind("<Destroy>", self._on_destroy)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self._window_id, width=event.width)

    def _on_mousewheel(self, event):
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass

    def _bind_wheel(self, _event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_wheel(self, _event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_destroy(self, _event):
        try:
            self.unbind_all("<MouseWheel>")
        except tk.TclError:
            pass
