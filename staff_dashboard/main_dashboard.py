import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageDraw
import mysql.connector
from datetime import datetime, timedelta
from staff_dashboard.appointment_management import AppointmentManagementMixin
from staff_dashboard.report_generation import ReportGenerationMixin
from shared.logout_dialog import LogoutDialog
from shared.notifications import SMSNotification
from tkinter import messagebox

class StaffDashboard(ttk.Frame, AppointmentManagementMixin, ReportGenerationMixin):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.sms = SMSNotification()
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dental"
        )
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
            'white': '#ffffff',
            'completed': '#2980b9'  # Adding a distinct blue color for completed status
        }
        
        style = ttk.Style()
        style.configure('Modern.TFrame', background=self.colors['light'])
        style.configure('Card.TFrame', background=self.colors['white'], relief='solid', borderwidth=1)
        style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), foreground=self.colors['primary'])
        style.configure('Subtitle.TLabel', font=('Helvetica', 16), foreground=self.colors['secondary'])
        style.configure('Primary.TButton', font=('Helvetica', 12, 'bold'), padding=10)
        style.configure('Secondary.TButton', font=('Helvetica', 12), padding=8)
        
        # Add status-specific styles
        style.configure('Success.TFrame', background=self.colors['success'])
        style.configure('Warning.TFrame', background=self.colors['warning'])
        style.configure('Danger.TFrame', background=self.colors['danger'])
        style.configure('Info.TFrame', background=self.colors['info'])
        
        # Add status-specific text colors
        style.configure('Status.Success.TLabel', foreground=self.colors['success'])
        style.configure('Status.Warning.TLabel', foreground=self.colors['warning'])
        style.configure('Status.Danger.TLabel', foreground=self.colors['danger'])
        style.configure('Status.Info.TLabel', foreground=self.colors['info'])

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

        # Dashboard Tab
        self.dashboard_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.dashboard_frame, text='📊 Dashboard')
        self.setup_dashboard_view()

        # Appointments Tab
        self.appointments_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.appointments_frame, text='📅 Appointments')
        self.setup_appointments_view()

        # Bind tab change event
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

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

    def on_tab_change(self, event):
        current_tab = self.notebook.index(self.notebook.select())
        if current_tab == 0:  # If switching to dashboard tab
            self.refresh_dashboard()

    def refresh_dashboard(self):
        # Clear the dashboard frame
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        # Rebuild the dashboard
        self.setup_dashboard_view()
        # Force update
        self.dashboard_frame.update()

    def setup_dashboard_view(self):
        # Create a canvas and scrollbar for scrolling
        canvas = ttk.Canvas(self.dashboard_frame)
        scrollbar = ttk.Scrollbar(self.dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')

        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create a window for the scrollable frame inside the canvas
        canvas_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind the canvas resize event to update the scrollable frame's width
        def on_canvas_configure(event):
            canvas_width = event.width
            canvas.itemconfig(canvas_frame_id, width=canvas_width)
        canvas.bind('<Configure>', on_canvas_configure)

        # Create a grid layout for dashboard widgets within the scrollable frame
        dashboard_grid = ttk.Frame(scrollable_frame, style='Modern.TFrame')
        dashboard_grid.pack(fill=BOTH, expand=YES, padx=20, pady=20)

        # Header with refresh button
        header_frame = ttk.Frame(dashboard_grid, style='Modern.TFrame')
        header_frame.pack(fill=X, pady=(0, 20))

        ttk.Label(
            header_frame,
            text="📊 Dashboard Overview",
            style='Title.TLabel'
        ).pack(side=LEFT)

        ttk.Button(
            header_frame,
            text="🔄 Refresh",
            command=self.refresh_dashboard,
            bootstyle="info-outline",
            width=15
        ).pack(side=RIGHT)

        # Stats Cards Row
        stats_frame = ttk.Frame(dashboard_grid, style='Modern.TFrame')
        stats_frame.pack(fill=X, pady=(0, 20))

        # Get statistics from database
        cursor = self.db_connection.cursor()
        
        # Today's Appointments
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE DATE(appointment_date) = CURDATE()")
        today_appointments = cursor.fetchone()[0]
        
        # Pending Appointments
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'pending'")
        pending_appointments = cursor.fetchone()[0]
        
        # Confirmed Appointments
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'confirmed'")
        confirmed_appointments = cursor.fetchone()[0]
        
        # Completed Appointments
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'completed'")
        completed_appointments = cursor.fetchone()[0]

        # Create stat cards with improved icons and styling
        self.create_stat_card(stats_frame, "📅 Today's Appointments", today_appointments, self.colors['info'], 0)
        self.create_stat_card(stats_frame, "⏳ Pending Appointments", pending_appointments, self.colors['warning'], 1)
        self.create_stat_card(stats_frame, "✅ Confirmed Appointments", confirmed_appointments, self.colors['success'], 2)
        self.create_stat_card(stats_frame, "🏥 Completed Appointments", completed_appointments, self.colors['completed'], 3)

        # Recent Activity Section with improved design
        activity_frame = ttk.LabelFrame(dashboard_grid, text="📋 Recent Activity", style='Card.TFrame', padding=15)
        activity_frame.pack(fill=BOTH, expand=YES, pady=(0, 20))

        # Create activity list with improved formatting
        cursor.execute("""
            SELECT 
                DATE_FORMAT(a.appointment_date, '%Y-%m-%d') as formatted_date,
                TIME_FORMAT(a.appointment_time, '%H:%i') as formatted_time,
                u.username,
                a.service,
                a.status
            FROM appointments a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
            LIMIT 10
        """)
        recent_activities = cursor.fetchall()

        for activity in recent_activities:
            activity_item = ttk.Frame(activity_frame, style='Card.TFrame')
            activity_item.pack(fill=X, padx=10, pady=5)
            
            # Add status icon
            status_icon = {
                'pending': '⏳',
                'confirmed': '✅',
                'completed': '🏥',
                'cancelled': '❌'
            }.get(activity[4].lower(), '')
            
            # Create a colored status indicator
            status_style = 'Success.TFrame' if activity[4] == 'confirmed' else \
                          'Warning.TFrame' if activity[4] == 'pending' else \
                          'Danger.TFrame' if activity[4] == 'cancelled' else \
                          'Info.TFrame'
            
            status_indicator = ttk.Frame(activity_item, width=10, style=status_style)
            status_indicator.pack(side=LEFT, padx=(5, 10), pady=5, fill=Y)
            
            # Get status-specific text style
            status_text_style = 'Status.Success.TLabel' if activity[4] == 'confirmed' else \
                              'Status.Warning.TLabel' if activity[4] == 'pending' else \
                              'Status.Danger.TLabel' if activity[4] == 'cancelled' else \
                              'Status.Info.TLabel'
            
            ttk.Label(
                activity_item,
                text=f"📅 {activity[0]} {activity[1]} | 👤 {activity[2]} | 🦷 {activity[3]} | {status_icon} {activity[4].capitalize()}",
                style=status_text_style
            ).pack(side=LEFT, padx=10, pady=5)

        # Quick Actions Section with improved design
        actions_frame = ttk.LabelFrame(dashboard_grid, text="⚡ Quick Actions", style='Card.TFrame', padding=15)
        actions_frame.pack(fill=X, pady=(0, 20))

        actions_grid = ttk.Frame(actions_frame, style='Modern.TFrame')
        actions_grid.pack(fill=X, padx=10, pady=10)

        # Quick action buttons with improved icons and styling
        ttk.Button(
            actions_grid,
            text="📋 Manage Appointments",
            command=lambda: self.notebook.select(1),  # Switch to appointments tab
            style='Primary.TButton',
            width=25
        ).pack(side=LEFT, padx=5)

        cursor.close()

    def create_stat_card(self, parent, title, value, color, column):
        card = ttk.Frame(parent, style='Card.TFrame', padding=15)
        card.grid(row=0, column=column, padx=10, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)

        # Create a frame for the icon
        icon_frame = ttk.Frame(card)
        icon_frame.pack(side=LEFT, padx=(0, 15))

        # Extract icon from title and make it bigger
        icon = title.split()[0]
        title_text = ' '.join(title.split()[1:])
        
        ttk.Label(
            icon_frame,
            text=icon,
            font=('Helvetica', 32),  # Increased icon size
            foreground=color
        ).pack()

        # Create a frame for the text content
        content_frame = ttk.Frame(card)
        content_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Card content with improved styling
        ttk.Label(
            content_frame,
            text=title_text,
            style='Subtitle.TLabel',
            foreground=color,
            font=('Helvetica', 14, 'bold')
        ).pack(pady=(10, 5))

        ttk.Label(
            content_frame,
            text=str(value),
            font=('Helvetica', 36, 'bold'),
            foreground=color
        ).pack(pady=(0, 10))

    def generate_report(self):
        try:
            # Create a new window for report generation
            report_window = ttk.Toplevel(self)
            report_window.title("Generate Report")
            report_window.geometry("400x300")
            report_window.transient(self)
            report_window.grab_set()

            # Report type selection
            type_frame = ttk.LabelFrame(report_window, text="Report Type", padding=10)
            type_frame.pack(fill=X, padx=10, pady=5)

            report_type = tk.StringVar(value="daily")
            ttk.Radiobutton(type_frame, text="Daily Report", variable=report_type, value="daily").pack(anchor=W, pady=2)
            ttk.Radiobutton(type_frame, text="Weekly Report", variable=report_type, value="weekly").pack(anchor=W, pady=2)
            ttk.Radiobutton(type_frame, text="Monthly Report", variable=report_type, value="monthly").pack(anchor=W, pady=2)

            # Date selection
            date_frame = ttk.LabelFrame(report_window, text="Date Range", padding=10)
            date_frame.pack(fill=X, padx=10, pady=5)

            start_date = ttk.DateEntry(date_frame, width=12)
            start_date.pack(side=LEFT, padx=5)
            ttk.Label(date_frame, text="to").pack(side=LEFT, padx=5)
            end_date = ttk.DateEntry(date_frame, width=12)
            end_date.pack(side=LEFT, padx=5)

            # Generate button
            def on_generate():
                try:
                    report_type_val = report_type.get()
                    start = start_date.entry.get()
                    end = end_date.entry.get()

                    # Get report data from database
                    cursor = self.db_connection.cursor()
                    
                    if report_type_val == "daily":
                        query = """
                            SELECT 
                                DATE_FORMAT(appointment_date, '%Y-%m-%d') as date,
                                COUNT(*) as total_appointments,
                                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
                            FROM appointments
                            WHERE appointment_date BETWEEN %s AND %s
                            GROUP BY DATE(appointment_date)
                            ORDER BY appointment_date
                        """
                    elif report_type_val == "weekly":
                        query = """
                            SELECT 
                                YEARWEEK(appointment_date) as week,
                                COUNT(*) as total_appointments,
                                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
                            FROM appointments
                            WHERE appointment_date BETWEEN %s AND %s
                            GROUP BY YEARWEEK(appointment_date)
                            ORDER BY week
                        """
                    else:  # monthly
                        query = """
                            SELECT 
                                DATE_FORMAT(appointment_date, '%Y-%m') as month,
                                COUNT(*) as total_appointments,
                                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                                SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled
                            FROM appointments
                            WHERE appointment_date BETWEEN %s AND %s
                            GROUP BY DATE_FORMAT(appointment_date, '%Y-%m')
                            ORDER BY month
                        """

                    cursor.execute(query, (start, end))
                    report_data = cursor.fetchall()

                    # Save report to database
                    insert_query = """
                        INSERT INTO reports (staff_id, report_type, generated_date, description, report_data)
                        VALUES (%s, %s, NOW(), %s, %s)
                    """
                    description = f"{report_type_val.capitalize()} report from {start} to {end}"
                    cursor.execute(insert_query, (
                        self.app.current_user['id'],
                        report_type_val,
                        description,
                        str(report_data)
                    ))
                    self.db_connection.commit()

                    messagebox.showinfo("Success", "Report generated successfully!")
                    report_window.destroy()

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
                finally:
                    cursor.close()

            ttk.Button(
                report_window,
                text="Generate Report",
                command=on_generate,
                style='Primary.TButton'
            ).pack(pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open report window: {str(e)}")

    def show_logout_dialog(self):
        dialog = LogoutDialog(self, self.app)
        if dialog.show():
            self.app.current_user = None
            self.app.create_login_frame()
