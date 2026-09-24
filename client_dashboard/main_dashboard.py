import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime, timedelta
import calendar
from PIL import Image, ImageTk, ImageDraw
from shared.logout_dialog import LogoutDialog

class ClientDashboard(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_date = None
        self.time_slots = [
            "09:00", "10:00", "11:00",
            "13:00", "14:00", "15:00", "16:00"
        ]
        # Initialize with current date
        today = datetime.now()
        self.current_month = today.month
        self.current_year = today.year
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#34495e',
            'accent': '#3498db',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f1c40f',
            'info': '#1abc9c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'white': '#ffffff'
        }
        
        style = ttk.Style()
        style.configure('Modern.TFrame', background=self.colors['light'])
        style.configure('Card.TFrame', background=self.colors['white'], relief='solid', borderwidth=1)
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), foreground=self.colors['primary'])
        style.configure('Subtitle.TLabel', font=('Helvetica', 16), foreground=self.colors['secondary'])
        style.configure('Primary.TButton', font=('Helvetica', 12, 'bold'), padding=10)
        style.configure('Secondary.TButton', font=('Helvetica', 12), padding=8)
        style.configure('Calendar.TButton', font=('Helvetica', 9))
        style.configure('SelectedDate.TButton', font=('Helvetica', 10, 'bold'), background=self.colors['success'])
        style.configure('SelectedTime.TButton', font=('Helvetica', 10, 'bold'), background=self.colors['success'])
        style.configure('BookedTime.TButton', font=('Helvetica', 10), background=self.colors['warning'])
        style.configure('OtherBookedTime.TButton', font=('Helvetica', 10), background=self.colors['danger'])
        style.configure('AvailableTime.TButton', font=('Helvetica', 10))
        style.configure('DisabledTime.TButton', font=('Helvetica', 10))

    def setup_ui(self):
        # Main container with modern background
        main_container = ttk.Frame(self, style='Modern.TFrame')
        main_container.pack(fill=BOTH, expand=YES)

        # Header section with gradient background
        header_frame = ttk.Frame(main_container, bootstyle="primary")
        header_frame.pack(fill=X, padx=0, pady=0)

        # Logo and title section
        title_frame = ttk.Frame(header_frame, bootstyle="primary")
        title_frame.pack(fill=X, padx=20, pady=10)

        try:
            logo_img = Image.open("assets/dental.jpg")
            # Create a circular mask
            mask = Image.new('L', (60, 60), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 60, 60), fill=255)
            # Resize and apply mask
            logo_img = logo_img.resize((60, 60), Image.LANCZOS)
            logo_img.putalpha(mask)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(title_frame, image=logo_photo, bootstyle="inverse-primary")
            logo_label.image = logo_photo
            logo_label.pack(side=LEFT, padx=(0, 15))
        except:
            logo_label = ttk.Label(title_frame, text="🦷", font=("Helvetica", 32), bootstyle="inverse-primary")
            logo_label.pack(side=LEFT, padx=(0, 15))

        title_label = ttk.Label(
            title_frame,
            text="Mirasol Dental Clinic Appointment System With SMS Notifications",
            style='Title.TLabel',
            bootstyle="inverse-primary"
        )
        title_label.pack(side=LEFT)

        # Welcome section with user info
        welcome_frame = ttk.Frame(main_container, style='Card.TFrame')
        welcome_frame.pack(fill=X, padx=20, pady=10)

        welcome_label = ttk.Label(
            welcome_frame,
            text=f"Welcome, {self.app.current_user['username']}",
            style='Subtitle.TLabel'
        )
        welcome_label.pack(side=LEFT, padx=20, pady=10)

        # Main content area with modern notebook
        content_frame = ttk.Frame(main_container, style='Modern.TFrame')
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        self.notebook = ttk.Notebook(content_frame, bootstyle="primary")
        self.notebook.pack(fill=BOTH, expand=YES)

        # Create Book Appointment tab
        booking_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(booking_frame, text='📅 Book Appointment')
        self.setup_booking_frame(booking_frame)

        # Create My Appointments tab
        appointments_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(appointments_frame, text='📋 My Appointments')
        self.setup_appointments_frame(appointments_frame)

        # Footer with logout button
        footer_frame = ttk.Frame(main_container, style='Card.TFrame')
        footer_frame.pack(fill=X, padx=20, pady=10)

        logout_btn = ttk.Button(
            footer_frame,
            text="🚪 Logout",
            command=self.show_logout_dialog,
            style='Danger.TButton'
        )
        logout_btn.pack(side=RIGHT, padx=20, pady=10)

    def setup_booking_frame(self, parent):
        # Create a canvas with scrollbar for the entire booking frame
        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel to scroll with proper error handling
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                # Ignore the error if the canvas is destroyed
                pass

        # Bind mouse wheel to the canvas and its children
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

        # Unbind when the frame is destroyed
        def _unbind_mousewheel():
            try:
                canvas.unbind_all("<MouseWheel>")
                scrollable_frame.unbind_all("<MouseWheel>")
            except:
                pass

        scrollable_frame.bind("<Destroy>", lambda e: _unbind_mousewheel())

        # Service selection
        service_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        service_frame.pack(fill='x', pady=(20,10), padx=20)
        
        ttk.Label(service_frame, text="Select Service:", style='Subtitle.TLabel').pack(side='left', padx=20, pady=10)
        self.service_var = tk.StringVar()
        service_options = ["Cleaning", "Extraction", "Filling", "Braces Consultation", "Other"]
        self.service_combo = ttk.Combobox(
            service_frame, 
            textvariable=self.service_var,
            values=service_options,
            state="readonly",
            width=30,
            font=('Helvetica', 12)
        )
        self.service_combo.pack(side='left', padx=10, pady=10)

        # Date selection frame
        date_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        date_frame.pack(fill='x', padx=20, pady=10)

        # Add month selection
        today = datetime.now()
        self.current_month = today.month
        self.current_year = today.year

        month_frame = ttk.Frame(date_frame, style='Modern.TFrame')
        month_frame.pack(fill='x', pady=5, padx=20)

        ttk.Button(
            month_frame,
            text="◀️",
            command=self.previous_month,
            style='Primary.TButton',
            width=3
        ).pack(side='left', padx=5)

        self.month_label = ttk.Label(
            month_frame,
            text=f"{calendar.month_name[self.current_month]} {self.current_year}",
            style='Title.TLabel'
        )
        self.month_label.pack(side='left', padx=20)

        ttk.Button(
            month_frame,
            text="▶️",
            command=self.next_month,
            style='Primary.TButton',
            width=3
        ).pack(side='left', padx=5)

        # Create dates frame
        self.dates_frame = ttk.Frame(date_frame, style='Modern.TFrame')
        self.dates_frame.pack(fill='x', pady=10, padx=20)

        # Create weekday labels with proper alignment
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(weekdays):
            label = ttk.Label(
                self.dates_frame,
                text=day,
                width=8,
                anchor='center',
                style='Subtitle.TLabel',
                bootstyle="danger" if i == 0 else "primary"  # Make Sunday red
            )
            label.grid(row=0, column=i, padx=1, pady=1, sticky='nsew')

        # Configure grid weights for proper alignment
        for i in range(7):
            self.dates_frame.grid_columnconfigure(i, weight=1)
        for i in range(7):  # 6 weeks + header
            self.dates_frame.grid_rowconfigure(i, weight=1)

        self.update_calendar()

        # Time slots frame
        self.time_slots_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        self.time_slots_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(
            self.time_slots_frame,
            text="Available Time Slots",
            style='Title.TLabel'
        ).pack(pady=10)

        self.time_buttons_frame = ttk.Frame(self.time_slots_frame, style='Modern.TFrame')
        self.time_buttons_frame.pack(fill='x', pady=5, padx=20)

        # Book button
        self.book_button = ttk.Button(
            scrollable_frame,
            text="📅 Book Appointment",
            command=self.book_appointment,
            style='Success.TButton',
            state='disabled'
        )
        self.book_button.pack(pady=20)

    def setup_appointments_frame(self, parent):
        # Create a frame for filters and search
        filter_frame = ttk.Frame(parent, style='Card.TFrame')
        filter_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        # Status filter with icon
        ttk.Label(filter_frame, text="🔍 Status:", style='Subtitle.TLabel').pack(side='left', padx=20, pady=10)
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["All", "pending", "confirmed", "completed", "cancelled"],
            state="readonly",
            width=15,
            font=('Helvetica', 12)
        )
        status_combo.pack(side='left', padx=5, pady=10)
        status_combo.bind('<<ComboboxSelected>>', lambda e: self.load_user_appointments())
        
        # Search frame with icon
        search_frame = ttk.Frame(parent, style='Card.TFrame')
        search_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        ttk.Label(search_frame, text="🔎 Search:", style='Subtitle.TLabel').pack(side='left', padx=20, pady=10)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=30,
            font=('Helvetica', 12)
        )
        search_entry.pack(side='left', padx=5, pady=10)
        search_entry.bind('<KeyRelease>', lambda e: self.load_user_appointments())
        
        # Create Treeview with modern style
        columns = ('id', 'service', 'date', 'time', 'status')
        self.appointments_tree = ttk.Treeview(
            parent,
            columns=columns,
            show='headings',
            bootstyle="primary",
            height=10
        )
        
        # Define headings with icons and better formatting
        self.appointments_tree.heading('id', text='🆔 ID')
        self.appointments_tree.heading('service', text='🦷 Service')
        self.appointments_tree.heading('date', text='📅 Date')
        self.appointments_tree.heading('time', text='⏰ Time')
        self.appointments_tree.heading('status', text='📊 Status')
        
        # Set column widths and center alignment
        self.appointments_tree.column('id', width=50, anchor='center')
        self.appointments_tree.column('service', width=150, anchor='center')
        self.appointments_tree.column('date', width=100, anchor='center')
        self.appointments_tree.column('time', width=100, anchor='center')
        self.appointments_tree.column('status', width=100, anchor='center')
        
        # Configure tag colors for different statuses with icons
        self.appointments_tree.tag_configure('pending', background='#fff3cd', foreground='#856404')
        self.appointments_tree.tag_configure('confirmed', background='#d4edda', foreground='#155724')
        self.appointments_tree.tag_configure('completed', background='#cce5ff', foreground='#004085')
        self.appointments_tree.tag_configure('cancelled', background='#f8d7da', foreground='#721c24')
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(
            parent,
            orient='vertical',
            command=self.appointments_tree.yview
        )
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons frame with improved styling
        action_frame = ttk.Frame(parent, style='Card.TFrame')
        action_frame.pack(fill='x', pady=(20, 0), padx=20)
        
        # Reschedule button with icon
        self.reschedule_btn = ttk.Button(
            action_frame,
            text="🔄 Reschedule",
            command=self.reschedule_appointment,
            style='Info.TButton',
            state='disabled'
        )
        self.reschedule_btn.pack(side='left', padx=5, pady=10)
        
        # Cancel button with icon
        self.cancel_btn = ttk.Button(
            action_frame,
            text="❌ Cancel",
            command=self.cancel_appointment,
            style='Danger.TButton',
            state='disabled'
        )
        self.cancel_btn.pack(side='left', padx=5, pady=10)
        
        # Bind selection event
        self.appointments_tree.bind('<<TreeviewSelect>>', self.on_appointment_select)
        # Bind double click for details
        self.appointments_tree.bind('<Double-1>', self.show_appointment_details)
        
        # Load user's appointments
        self.load_user_appointments()

    def on_appointment_select(self, event):
        selected = self.appointments_tree.selection()
        if selected:
            item = self.appointments_tree.item(selected[0])
            status = item['values'][4]
            # Enable buttons only for pending or confirmed appointments
            self.reschedule_btn.configure(state='normal' if status in ['pending', 'confirmed'] else 'disabled')
            self.cancel_btn.configure(state='normal' if status in ['pending', 'confirmed'] else 'disabled')
        else:
            self.reschedule_btn.configure(state='disabled')
            self.cancel_btn.configure(state='disabled')

    def reschedule_appointment(self):
        selected = self.appointments_tree.selection()
        if not selected:
            return

        item = self.appointments_tree.item(selected[0])
        appt_id, service, date, time, status = item['values']

        # Create reschedule dialog
        dialog = tk.Toplevel(self)
        dialog.title("Reschedule Appointment")
        dialog.transient(self)
        dialog.grab_set()
        
        # Set dialog to maximize vertically
        dialog.state('zoomed')  # This will maximize the window on Windows

        # Main container with padding
        main_frame = ttk.Frame(dialog, style='Card.TFrame', padding=20)
        main_frame.pack(fill='both', expand=True)

        # Title frame
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))

        ttk.Label(
            title_frame,
            text="Reschedule Appointment",
            style='Title.TLabel',
            font=('Helvetica', 24, 'bold')
        ).pack(side='left')

        # Current appointment info with modern card style
        info_frame = ttk.LabelFrame(
            main_frame,
            text="Current Appointment Details",
            padding=15,
            bootstyle="primary"
        )
        info_frame.pack(fill='x', pady=(0, 20))

        # Create a grid layout for appointment details
        details_frame = ttk.Frame(info_frame)
        details_frame.pack(fill='x', pady=5)

        # Service details
        service_frame = ttk.Frame(details_frame)
        service_frame.pack(fill='x', pady=5)
        ttk.Label(
            service_frame,
            text="🦷 Service:",
            style='Subtitle.TLabel',
            font=('Helvetica', 12, 'bold')
        ).pack(side='left', padx=(0, 10))
        ttk.Label(
            service_frame,
            text=service,
            style='Subtitle.TLabel',
            font=('Helvetica', 12)
        ).pack(side='left')

        # Date details
        date_frame = ttk.Frame(details_frame)
        date_frame.pack(fill='x', pady=5)
        ttk.Label(
            date_frame,
            text="📅 Current Date:",
            style='Subtitle.TLabel',
            font=('Helvetica', 12, 'bold')
        ).pack(side='left', padx=(0, 10))
        ttk.Label(
            date_frame,
            text=date,
            style='Subtitle.TLabel',
            font=('Helvetica', 12)
        ).pack(side='left')

        # Time details
        time_frame = ttk.Frame(details_frame)
        time_frame.pack(fill='x', pady=5)
        ttk.Label(
            time_frame,
            text="⏰ Current Time:",
            style='Subtitle.TLabel',
            font=('Helvetica', 12, 'bold')
        ).pack(side='left', padx=(0, 10))
        ttk.Label(
            time_frame,
            text=time,
            style='Subtitle.TLabel',
            font=('Helvetica', 12)
        ).pack(side='left')

        # New date selection with modern card style
        date_frame = ttk.LabelFrame(
            main_frame,
            text="Select New Date",
            padding=15,
            bootstyle="primary"
        )
        date_frame.pack(fill='x', pady=(0, 20))

        # Month selection with improved styling
        month_frame = ttk.Frame(date_frame)
        month_frame.pack(fill='x', pady=10)

        ttk.Button(
            month_frame,
            text="◀️",
            command=lambda: self.update_reschedule_calendar(dialog, -1),
            width=3,
            style='Primary.TButton',
            bootstyle="primary"
        ).pack(side='left', padx=5)

        self.reschedule_month_label = ttk.Label(
            month_frame,
            text=f"{calendar.month_name[self.current_month]} {self.current_year}",
            style='Title.TLabel',
            font=('Helvetica', 16, 'bold')
        )
        self.reschedule_month_label.pack(side='left', padx=20)

        ttk.Button(
            month_frame,
            text="▶️",
            command=lambda: self.update_reschedule_calendar(dialog, 1),
            width=3,
            style='Primary.TButton',
            bootstyle="primary"
        ).pack(side='left', padx=5)

        # Create dates frame with improved styling
        self.reschedule_dates_frame = ttk.Frame(date_frame)
        self.reschedule_dates_frame.pack(fill='x', pady=10)

        # Create weekday labels with improved styling
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(weekdays):
            label = ttk.Label(
                self.reschedule_dates_frame,
                text=day,
                width=8,
                anchor='center',
                style='Subtitle.TLabel',
                font=('Helvetica', 10, 'bold'),
                bootstyle="secondary" if i == 0 else "primary"
            )
            label.grid(row=0, column=i, padx=1, pady=1)

        # Time slots frame with modern card style
        time_frame = ttk.LabelFrame(
            main_frame,
            text="Select New Time",
            padding=15,
            bootstyle="primary"
        )
        time_frame.pack(fill='x', pady=(0, 20))

        self.reschedule_time_buttons_frame = ttk.Frame(time_frame)
        self.reschedule_time_buttons_frame.pack(fill='x', pady=10)

        # Update calendar and time slots
        self.update_reschedule_calendar(dialog, 0)

        # Add buttons for rescheduling with improved styling
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x', pady=(20, 0))

        # Create a container for the buttons
        button_container = ttk.Frame(action_frame)
        button_container.pack(expand=True)

        # Confirm button with improved styling
        confirm_btn = ttk.Button(
            button_container,
            text="✅ Confirm Reschedule",
            command=lambda: self.confirm_reschedule(dialog, appt_id),
            bootstyle="success",
            style='Primary.TButton',
            width=20
        )
        confirm_btn.pack(side='left', padx=10)

        # Cancel button with improved styling
        cancel_btn = ttk.Button(
            button_container,
            text="✖️ Cancel",
            command=dialog.destroy,
            bootstyle="secondary",
            style='Secondary.TButton',
            width=15
        )
        cancel_btn.pack(side='left', padx=10)

        # Calculate dialog size based on content
        dialog.update_idletasks()
        width = max(600, dialog.winfo_width())  # Increased minimum width
        height = max(700, dialog.winfo_height())  # Increased minimum height
        
        # Center the dialog
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def update_reschedule_calendar(self, dialog, month_change):
        if month_change != 0:
            if month_change > 0:
                if self.current_month == 12:
                    self.current_month = 1
                    self.current_year += 1
                else:
                    self.current_month += 1
            else:
                if self.current_month == 1:
                    self.current_month = 12
                    self.current_year -= 1
                else:
                    self.current_month -= 1

        # Update month label
        self.reschedule_month_label.config(
            text=f"{calendar.month_name[self.current_month]} {self.current_year}",
            style='Title.TLabel'
        )

        # Clear existing date buttons
        for widget in self.reschedule_dates_frame.grid_slaves():
            if widget.grid_info()['row'] != 0:
                widget.destroy()

        # Get the first day of the month and total days
        first_day = datetime(self.current_year, self.current_month, 1)
        total_days = calendar.monthrange(self.current_year, self.current_month)[1]

        # Get the weekday of first day (0=Monday, 6=Sunday)
        # Convert to Sunday-based week (0=Sunday, 6=Saturday)
        start_pos = (first_day.weekday() + 1) % 7

        # Get today's date for comparison
        today = datetime.now().date()

        # Create calendar buttons
        day_count = 1
        for week in range(6):  # Maximum 6 weeks in a month
            for weekday in range(7):  # 7 days in a week
                if (week == 0 and weekday < start_pos) or (day_count > total_days):
                    # Create empty spacer for days before start of month
                    spacer = ttk.Label(self.reschedule_dates_frame, text="", width=8)
                    spacer.grid(row=week + 1, column=weekday, padx=1, pady=1)
                    continue
                else:
                    if day_count <= total_days:
                        current_date = datetime(self.current_year, self.current_month, day_count).date()
                        is_today = current_date == today
                        is_selected = hasattr(self, 'selected_date') and current_date == self.selected_date
                        is_past = current_date < today
                        is_sunday = weekday == 0  # Sunday is at position 0
                        is_future_year = current_date.year > today.year

                        # Format the date for display - only show the number
                        date_text = str(day_count)
                        
                        # Determine button style based on conditions
                        if is_selected:
                            bootstyle = "success"  # Green for selected date
                            style = 'SelectedDate.TButton'
                        elif is_today:
                            bootstyle = "warning"  # Yellow for today
                            style = 'Calendar.TButton'
                        elif is_past or is_sunday or is_future_year:
                            bootstyle = "secondary"  # Gray for disabled dates
                            style = 'Calendar.TButton'
                        else:
                            bootstyle = "primary"  # Blue for available dates
                            style = 'Calendar.TButton'

                        btn = ttk.Button(
                            self.reschedule_dates_frame,
                            text=date_text,
                            bootstyle=bootstyle,
                            state='disabled' if is_past or is_sunday or is_future_year else 'normal',
                            command=lambda d=current_date: self.select_reschedule_date(d, dialog),
                            width=8,
                            style=style
                        )
                        btn.grid(row=week + 1, column=weekday, padx=1, pady=1)
                        day_count += 1

        # Update time slots if a date is selected
        if hasattr(self, 'selected_date'):
            self.update_reschedule_time_slots(dialog)

    def select_reschedule_date(self, date, dialog):
        self.selected_date = date
        self.update_reschedule_calendar(dialog, 0)  # Update calendar to highlight selected date
        self.update_reschedule_time_slots(dialog)

    def update_reschedule_time_slots(self, dialog):
        # Clear existing time slots
        for widget in self.reschedule_time_buttons_frame.winfo_children():
            widget.destroy()

        if not self.selected_date:
            return

        # Check availability for each time slot
        for i, time in enumerate(self.time_slots):
            try:
                # Check if the slot is booked by the current user
                user_query = """
                    SELECT COUNT(*) 
                    FROM appointments 
                    WHERE appointment_date = %s 
                    AND appointment_time = %s 
                    AND status IN ('pending', 'confirmed')
                    AND user_id = %s
                """
                user_result = self.app.execute_query(user_query, (self.selected_date, time, self.app.current_user['id']))
                is_booked_by_user = user_result[0][0] > 0 if user_result else False

                # Check if the slot is booked by other users
                other_query = """
                    SELECT COUNT(*) 
                    FROM appointments 
                    WHERE appointment_date = %s 
                    AND appointment_time = %s 
                    AND status IN ('pending', 'confirmed')
                    AND user_id != %s
                """
                other_result = self.app.execute_query(other_query, (self.selected_date, time, self.app.current_user['id']))
                is_booked_by_others = other_result[0][0] > 0 if other_result else False

                # Determine button style based on booking status and selection
                if hasattr(self, 'selected_time') and time == self.selected_time:
                    # Selected time slot - use success style with bold text
                    button = ttk.Button(
                        self.reschedule_time_buttons_frame,
                        text=time,
                        bootstyle="success",
                        width=8,
                        command=lambda t=time: self.select_reschedule_time(t),
                        style='SelectedTime.TButton'
                    )
                elif is_booked_by_user:
                    # User's own booking - use warning style (yellow)
                    button = ttk.Button(
                        self.reschedule_time_buttons_frame,
                        text=time,
                        bootstyle="warning",
                        width=8,
                        command=lambda t=time: self.select_reschedule_time(t),
                        style='BookedTime.TButton'
                    )
                elif is_booked_by_others:
                    # Others' bookings - use danger style (red)
                    button = ttk.Button(
                        self.reschedule_time_buttons_frame,
                        text=time,
                        bootstyle="danger",
                        width=8,
                        command=lambda t=time: self.select_reschedule_time(t),
                        style='OtherBookedTime.TButton'
                    )
                else:
                    # Available slot - use primary style
                    button = ttk.Button(
                        self.reschedule_time_buttons_frame,
                        text=time,
                        bootstyle="primary",
                        width=8,
                        command=lambda t=time: self.select_reschedule_time(t),
                        style='AvailableTime.TButton'
                    )

                row = i // 4  # Changed to 4 columns for better layout
                col = i % 4
                button.grid(row=row, column=col, padx=2, pady=2)

            except Exception as e:
                print(f"Error in time slot {time}: {str(e)}")
                # Create a disabled button for this slot
                button = ttk.Button(
                    self.reschedule_time_buttons_frame,
                    text=time,
                    bootstyle="secondary",
                    width=8,
                    state='disabled',
                    style='DisabledTime.TButton'
                )
                row = i // 4
                col = i % 4
                button.grid(row=row, column=col, padx=2, pady=2)

    def select_reschedule_time(self, time):
        try:
            # Check if the slot is booked by the current user
            user_query = """
                SELECT COUNT(*) 
                FROM appointments 
                WHERE appointment_date = %s 
                AND appointment_time = %s 
                AND status IN ('pending', 'confirmed')
                AND user_id = %s
            """
            user_result = self.app.execute_query(user_query, (self.selected_date, time, self.app.current_user['id']))
            is_booked_by_user = user_result[0][0] > 0 if user_result else False

            # Check if the slot is booked by other users
            other_query = """
                SELECT COUNT(*) 
                FROM appointments 
                WHERE appointment_date = %s 
                AND appointment_time = %s 
                AND status IN ('pending', 'confirmed')
                AND user_id != %s
            """
            other_result = self.app.execute_query(other_query, (self.selected_date, time, self.app.current_user['id']))
            is_booked_by_others = other_result[0][0] > 0 if other_result else False

            if is_booked_by_user:
                messagebox.showwarning("Already Booked", "You have already booked this time slot.")
                return
            elif is_booked_by_others:
                messagebox.showwarning("Slot Unavailable", "This time slot is already booked by another client.")
                return

            self.selected_time = time
            # Force update of time slots to show the green highlight
            self.update_reschedule_time_slots(self)
            # Enable the confirm button
            for widget in self.reschedule_time_buttons_frame.winfo_children():
                if isinstance(widget, ttk.Button) and widget['text'] == time:
                    widget.configure(bootstyle="success")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to check time slot availability: {str(e)}")

    def confirm_reschedule(self, dialog, appt_id):
        if not hasattr(self, 'selected_date') or not hasattr(self, 'selected_time'):
            messagebox.showerror("Error", "Please select both date and time")
            return

        try:
            # Check if the new slot is available
            query = """
                SELECT COUNT(*) 
                FROM appointments 
                WHERE appointment_date = %s 
                AND appointment_time = %s 
                AND status IN ('pending', 'confirmed')
                AND id != %s
            """
            result = self.app.execute_query(query, (self.selected_date, self.selected_time, appt_id))

            if result[0][0] > 0:
                messagebox.showerror(
                    "Reschedule Error",
                    "This time slot is no longer available. Please select a different time."
                )
                return

            # Update the appointment
            success = self.app.execute_query(
                """
                UPDATE appointments 
                SET appointment_date = %s, 
                    appointment_time = %s,
                    status = 'pending'
                WHERE id = %s AND user_id = %s
                """,
                (self.selected_date, self.selected_time, appt_id, self.app.current_user['id']),
                fetch=False
            )

            if success:
                messagebox.showinfo("Success", "Appointment rescheduled successfully!")
                dialog.destroy()
                self.load_user_appointments()
            else:
                messagebox.showerror("Error", "Failed to reschedule appointment")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to reschedule appointment: {str(e)}")

    def load_user_appointments(self):
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        try:
            # Build query based on filters
            query = """
                SELECT id, service, appointment_date, appointment_time, status
                FROM appointments
                WHERE user_id = %s
            """
            params = [self.app.current_user['id']]
            
            # Add status filter
            if self.status_var.get() != "All":
                query += " AND status = %s"
                params.append(self.status_var.get())
            
            # Add search filter
            if self.search_var.get():
                query += " AND (service LIKE %s OR appointment_date LIKE %s OR appointment_time LIKE %s)"
                search_term = f"%{self.search_var.get()}%"
                params.extend([search_term, search_term, search_term])
            
            query += " ORDER BY appointment_date DESC, appointment_time DESC"
            
            result = self.app.execute_query(query, params)
            
            if result:
                for appointment in result:
                    # Add status icons
                    status = appointment[4]
                    status_icon = {
                        'pending': '⏳',
                        'confirmed': '✅',
                        'completed': '🏥',
                        'cancelled': '❌'
                    }.get(status, '')
                    
                    # Format the values with icons
                    values = (
                        appointment[0],  # ID
                        appointment[1],  # Service
                        appointment[2],  # Date
                        appointment[3],  # Time
                        f"{status_icon} {status.capitalize()}"  # Status with icon
                    )
                    
                    # Set tag based on status
                    self.appointments_tree.insert('', 'end', values=values, tags=(status,))
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {str(e)}")

    def cancel_appointment(self, appointment_id=None, dialog=None):
        if not appointment_id:
            selected = self.appointments_tree.selection()
            if not selected:
                return
            item = self.appointments_tree.item(selected[0])
            appointment_id, service, date, time, status = item['values']

        # Create cancel dialog
        cancel_dialog = tk.Toplevel(self)
        cancel_dialog.title("Cancel Appointment")
        cancel_dialog.transient(self)
        cancel_dialog.grab_set()

        # Main container
        main_frame = ttk.Frame(cancel_dialog, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Warning icon and message
        warning_frame = ttk.Frame(main_frame)
        warning_frame.pack(fill='x', pady=10)

        ttk.Label(
            warning_frame,
            text="⚠️",
            font=("Helvetica", 32)
        ).pack(side='left', padx=10)

        warning_text = ttk.Label(
            warning_frame,
            text="Are you sure you want to cancel this appointment?",
            style='Title.TLabel',
            wraplength=300
        )
        warning_text.pack(side='left', padx=10)

        # Appointment details
        details_frame = ttk.LabelFrame(main_frame, text="Appointment Details", padding=10)
        details_frame.pack(fill='x', pady=10)

        details = [
            ("Service:", service),
            ("Date:", date),
            ("Time:", time),
            ("Status:", status.capitalize())
        ]

        for label, value in details:
            frame = ttk.Frame(details_frame, style='Modern.TFrame')
            frame.pack(fill='x', pady=2)

            ttk.Label(
                frame,
                text=label,
                style='Subtitle.TLabel',
                width=10
            ).pack(side='left', padx=5)

            ttk.Label(
                frame,
                text=value,
                style='Subtitle.TLabel'
            ).pack(side='left', padx=5)

        # Restrictions message
        restrictions_frame = ttk.Frame(main_frame, style='Modern.TFrame')
        restrictions_frame.pack(fill='x', pady=10)

        ttk.Label(
            restrictions_frame,
            text="⚠️ Restrictions:",
            style='Subtitle.TLabel',
            foreground='#e74c3c'
        ).pack(anchor='w', pady=2)

        restrictions = [
            "• Cancellation cannot be undone",
            "• You may need to wait for a new appointment slot",
            "• Late cancellations may affect future bookings"
        ]

        for restriction in restrictions:
            ttk.Label(
                restrictions_frame,
                text=restriction,
                style='Subtitle.TLabel',
                foreground='#e74c3c'
            ).pack(anchor='w', pady=1)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=20)

        def confirm_cancel():
            try:
                success = self.app.execute_query(
                    "UPDATE appointments SET status = 'cancelled' WHERE id = %s AND user_id = %s",
                    (appointment_id, self.app.current_user['id']),
                    fetch=False
                )

                if success:
                    messagebox.showinfo("Success", "Appointment cancelled successfully!")
                    self.load_user_appointments()
                    cancel_dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to cancel appointment")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")

        # Cancel button (to close dialog)
        ttk.Button(
            button_frame,
            text="No, Keep Appointment",
            command=cancel_dialog.destroy,
            style='Secondary.TButton'
        ).pack(side='right', padx=5)

        # Confirm button
        ttk.Button(
            button_frame,
            text="Yes, Cancel Appointment",
            command=confirm_cancel,
            style='Danger.TButton'
        ).pack(side='right', padx=5)

        # Calculate dialog size based on content
        cancel_dialog.update_idletasks()
        width = max(400, cancel_dialog.winfo_width())  # Minimum width of 400
        height = max(450, cancel_dialog.winfo_height())  # Minimum height of 450
        
        # Center the dialog
        x = (cancel_dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (cancel_dialog.winfo_screenheight() // 2) - (height // 2)
        cancel_dialog.geometry(f'{width}x{height}+{x}+{y}')

    def show_logout_dialog(self):
        dialog = LogoutDialog(self, self.app)
        if dialog.show():
            self.app.current_user = None
            self.app.create_login_frame()

    def select_date(self, date):
        # Check if the selected date is a Sunday
        if date.weekday() == 6:  # Sunday is 6 in Python's weekday() function (0=Monday, 6=Sunday)
            messagebox.showwarning("Clinic Closed", "The clinic is closed on Sundays. Please select another day.")
            return
            
        # Check if the date is in the past
        if date < datetime.now().date():
            messagebox.showwarning("Invalid Date", "Cannot book appointments for past dates.")
            return
            
        # Check if the date is more than a year in advance
        if date > datetime.now().date() + timedelta(days=365):
            messagebox.showwarning("Invalid Date", "Cannot book appointments more than a year in advance.")
            return
            
        self.selected_date = date
        self.update_calendar()  # Update calendar to highlight selected date
        self.update_time_slots()
        
    def update_calendar(self):
        # Clear existing date buttons
        for widget in self.dates_frame.grid_slaves():
            if widget.grid_info()['row'] != 0:  # Keep weekday labels
                widget.destroy()

        # Get the first day of the month and total days
        first_day = datetime(self.current_year, self.current_month, 1)
        total_days = calendar.monthrange(self.current_year, self.current_month)[1]

        # Get the weekday of first day (0=Monday, 6=Sunday)
        # Convert to Sunday-based week (0=Sunday, 6=Saturday)
        start_pos = (first_day.weekday() + 1) % 7

        # Get today's date for comparison
        today = datetime.now().date()
        
        # Update month label with current month and year
        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        # Create calendar buttons
        day_count = 1
        for week in range(6):  # Maximum 6 weeks in a month
            for weekday in range(7):  # 7 days in a week
                if (week == 0 and weekday < start_pos) or (day_count > total_days):
                    # Create empty spacer for days before start of month
                    spacer = ttk.Label(self.dates_frame, text="", width=8)
                    spacer.grid(row=week + 1, column=weekday, padx=1, pady=1)
                    continue
                else:
                    if day_count <= total_days:
                        current_date = datetime(self.current_year, self.current_month, day_count).date()
                        is_today = current_date == today
                        is_selected = hasattr(self, 'selected_date') and current_date == self.selected_date
                        is_past = current_date < today
                        is_sunday = weekday == 0  # Sunday is at position 0
                        is_future_year = current_date.year > today.year

                        # Format the date for display - only show the number
                        date_text = str(day_count)
                        
                        # Determine button style based on conditions
                        if is_selected:
                            bootstyle = "success"  # Green for selected date
                            style = 'SelectedDate.TButton'
                        elif is_today:
                            bootstyle = "warning"  # Yellow for today
                            style = 'Calendar.TButton'
                        elif is_past or is_sunday or is_future_year:
                            bootstyle = "secondary"  # Gray for disabled dates
                            style = 'Calendar.TButton'
                        else:
                            bootstyle = "primary"  # Blue for available dates
                            style = 'Calendar.TButton'

                        btn = ttk.Button(
                            self.dates_frame,
                            text=date_text,  # Only show the date number
                            bootstyle=bootstyle,
                            state='disabled' if is_past or is_sunday or is_future_year else 'normal',
                            command=lambda d=current_date: self.select_date(d),
                            width=8,
                            style=style
                        )
                        btn.grid(row=week + 1, column=weekday, padx=1, pady=1)
                        day_count += 1

    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self):
        # Allow booking up to one year in advance
        today = datetime.now()
        max_date = datetime(today.year + 1, today.month, today.day)
        next_date = datetime(self.current_year, self.current_month, 1) + timedelta(days=32)
        next_date = datetime(next_date.year, next_date.month, 1)
        
        if next_date <= max_date:
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else:
                self.current_month += 1
            self.update_calendar()
        else:
            messagebox.showinfo("Booking Limit", "You can only book appointments up to one year in advance.")

    def update_time_slots(self):
        # Clear existing time slots
        for widget in self.time_buttons_frame.winfo_children():
            widget.destroy()

        if not self.selected_date:
            return

        # Check availability for each time slot
        for i, time in enumerate(self.time_slots):
            try:
                # Check if the slot is booked by the current user
                user_query = """
                    SELECT COUNT(*) 
                    FROM appointments 
                    WHERE appointment_date = %s 
                    AND appointment_time = %s 
                    AND status IN ('pending', 'confirmed')
                    AND user_id = %s
                """
                try:
                    user_result = self.app.execute_query(user_query, (self.selected_date, time, self.app.current_user['id']))
                    is_booked_by_user = user_result[0][0] > 0 if user_result else False
                except Exception as e:
                    print(f"Error checking user booking: {str(e)}")
                    is_booked_by_user = False

                # Check if the slot is booked by other users
                other_query = """
                    SELECT COUNT(*) 
                    FROM appointments 
                    WHERE appointment_date = %s 
                    AND appointment_time = %s 
                    AND status IN ('pending', 'confirmed')
                    AND user_id != %s
                """
                try:
                    other_result = self.app.execute_query(other_query, (self.selected_date, time, self.app.current_user['id']))
                    is_booked_by_others = other_result[0][0] > 0 if other_result else False
                except Exception as e:
                    print(f"Error checking other bookings: {str(e)}")
                    is_booked_by_others = False

                # Determine button style based on booking status
                if is_booked_by_user:
                    # User's own booking - use warning style (yellow)
                    button = ttk.Button(
                        self.time_buttons_frame,
                        text=time,
                        bootstyle="warning",
                        width=8,
                        command=lambda t=time: self.select_time_slot(t),
                        style='BookedTime.TButton'
                    )
                elif is_booked_by_others:
                    # Others' bookings - use danger style (red)
                    button = ttk.Button(
                        self.time_buttons_frame,
                        text=time,
                        bootstyle="danger",
                        width=8,
                        command=lambda t=time: self.select_time_slot(t),
                        style='OtherBookedTime.TButton'
                    )
                elif hasattr(self, 'selected_time') and time == self.selected_time:
                    # Selected time slot - use success style with bold text
                    button = ttk.Button(
                        self.time_buttons_frame,
                        text=time,
                        bootstyle="success",
                        width=8,
                        command=lambda t=time: self.select_time_slot(t),
                        style='SelectedTime.TButton'
                    )
                else:
                    # Available slot - use primary style
                    button = ttk.Button(
                        self.time_buttons_frame,
                        text=time,
                        bootstyle="primary",
                        width=8,
                        command=lambda t=time: self.select_time_slot(t),
                        style='AvailableTime.TButton'
                    )

                row = i // 4  # Changed to 4 columns for better layout
                col = i % 4
                button.grid(row=row, column=col, padx=2, pady=2)

            except Exception as e:
                print(f"Error in time slot {time}: {str(e)}")
                # Create a disabled button for this slot
                button = ttk.Button(
                    self.time_buttons_frame,
                    text=time,
                    bootstyle="secondary",
                    width=8,
                    state='disabled',
                    style='DisabledTime.TButton'
                )
                row = i // 4
                col = i % 4
                button.grid(row=row, column=col, padx=2, pady=2)

    def select_time_slot(self, time):
        try:
            # Check if the slot is booked by the current user
            user_query = """
                SELECT COUNT(*) 
                FROM appointments 
                WHERE appointment_date = %s 
                AND appointment_time = %s 
                AND status IN ('pending', 'confirmed')
                AND user_id = %s
            """
            user_result = self.app.execute_query(user_query, (self.selected_date, time, self.app.current_user['id']))
            is_booked_by_user = user_result[0][0] > 0 if user_result else False

            # Check if the slot is booked by other users
            other_query = """
                SELECT COUNT(*) 
                FROM appointments 
                WHERE appointment_date = %s 
                AND appointment_time = %s 
                AND status IN ('pending', 'confirmed')
                AND user_id != %s
            """
            other_result = self.app.execute_query(other_query, (self.selected_date, time, self.app.current_user['id']))
            is_booked_by_others = other_result[0][0] > 0 if other_result else False

            if is_booked_by_user:
                messagebox.showwarning("Already Booked", "You have already booked this time slot.")
                return
            elif is_booked_by_others:
                messagebox.showwarning("Slot Unavailable", "This time slot is already booked by another client.")
                return

            self.selected_time = time
            # Force update of time slots to show the green highlight
            self.update_time_slots()
            # Enable the book button
            self.book_button.configure(state='normal')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to check time slot availability: {str(e)}")

    def book_appointment(self):
        if not self.service_var.get():
            messagebox.showerror("Error", "Please select a service")
            return

        if not self.selected_date or not hasattr(self, 'selected_time'):
            messagebox.showerror("Error", "Please select both date and time")
            return

        try:
            # Check availability one more time
            query = """
                SELECT COUNT(*) 
                FROM appointments 
                WHERE appointment_date = %s 
                AND appointment_time = %s 
                AND status IN ('pending', 'confirmed')
            """
            result = self.app.execute_query(query, (self.selected_date, self.selected_time))

            if result[0][0] > 0:
                messagebox.showerror(
                    "Booking Error",
                    "This time slot is no longer available. Please select a different time."
                )
                self.update_time_slots()
                return

            # Proceed with booking
            appointment_data = {
                "service": self.service_var.get(),
                "date": self.selected_date.strftime('%Y-%m-%d'),
                "time": self.selected_time
            }

            success, message = self.app.book_appointment(appointment_data)

            if success:
                messagebox.showinfo("Success", message)
                self.load_user_appointments()
                
                # Clear selections
                self.service_combo.set('')
                self.selected_date = None
                self.book_button.configure(state='disabled')
                self.update_time_slots()
            else:
                messagebox.showerror("Error", message)

        except Exception as e:
            messagebox.showerror("Error", f"Booking failed: {str(e)}")

    def show_appointment_details(self, event):
        selected = self.appointments_tree.selection()
        if not selected:
            return

        item = self.appointments_tree.item(selected[0])
        appt_id, service, date, time, status = item['values']

        # Create details dialog
        dialog = tk.Toplevel(self)
        dialog.title("Appointment Details")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

        # Main container
        main_frame = ttk.Frame(dialog, style='Card.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Appointment details
        details = [
            ("Service:", service),
            ("Date:", date),
            ("Time:", time),
            ("Status:", status.capitalize())
        ]

        for label, value in details:
            frame = ttk.Frame(main_frame, style='Modern.TFrame')
            frame.pack(fill='x', pady=5)

            ttk.Label(
                frame,
                text=label,
                style='Subtitle.TLabel',
                width=10
            ).pack(side='left', padx=5)

            ttk.Label(
                frame,
                text=value,
                style='Subtitle.TLabel'
            ).pack(side='left', padx=5)

        # Close button
        ttk.Button(
            main_frame,
            text="Close",
            command=dialog.destroy,
            style='Secondary.TButton'
        ).pack(pady=20)
