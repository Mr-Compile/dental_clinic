import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from ttkbootstrap.constants import *
from shared.notifications import SMSNotification
from datetime import datetime

class ModernConfirmationDialog:
    def __init__(self, parent, title, message, action_type="info"):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Prevent closing with X button
        self.dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        # Main container with padding
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Icon and message frame
        icon_frame = ttk.Frame(main_frame)
        icon_frame.pack(fill=X, pady=(0, 20))

        # Icon based on action type
        icon_text = "⚠️" if action_type == "warning" else "ℹ️" if action_type == "info" else "❌" if action_type == "danger" else "✅"
        icon_color = "warning" if action_type == "warning" else "primary" if action_type == "info" else "danger" if action_type == "danger" else "success"
        
        icon_label = ttk.Label(
            icon_frame,
            text=icon_text,
            font=("Segoe UI", 32),
            bootstyle=icon_color
        )
        icon_label.pack(side=LEFT, padx=(0, 15))

        # Message label
        message_frame = ttk.Frame(icon_frame)
        message_frame.pack(side=LEFT, fill=X, expand=YES)

        ttk.Label(
            message_frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            bootstyle="primary"
        ).pack(anchor=W)

        # Split message into lines and create labels for each
        message_lines = message.split('\n')
        for line in message_lines:
            if line.strip():  # Only add non-empty lines
                ttk.Label(
                    message_frame,
                    text=line,
                    font=("Segoe UI", 10),
                    bootstyle="secondary"
                ).pack(anchor=W, pady=(5, 0))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=X, pady=(20, 0))

        # Yes button with icon
        yes_button = ttk.Button(
            button_frame,
            text="Yes, Proceed",
            command=self.confirm,
            bootstyle="success",
            width=15
        )
        yes_button.pack(side=LEFT, padx=(0, 10))

        # No button with icon
        no_button = ttk.Button(
            button_frame,
            text="No, Cancel",
            command=self.cancel,
            bootstyle="secondary",
            width=15
        )
        no_button.pack(side=LEFT)

        # Calculate dialog size based on content
        self.dialog.update_idletasks()
        width = max(450, self.dialog.winfo_width())  # Minimum width of 450
        height = max(350, self.dialog.winfo_height())  # Minimum height of 350
        
        # Center the dialog
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')

        self.confirmed = False
        self.parent.wait_window(self.dialog)

    def confirm(self):
        self.confirmed = True
        self.dialog.destroy()

    def cancel(self):
        self.confirmed = False
        self.dialog.destroy()

    def show(self):
        return self.confirmed

class AppointmentManagementMixin:
    def setup_appointments_view(self):
        self.sms = SMSNotification()

        filters_frame = ttk.Frame(self.appointments_frame)
        filters_frame.pack(fill='x', padx=5, pady=5)

        search_frame = ttk.Frame(filters_frame)
        search_frame.pack(fill='x', pady=5)

        ttk.Label(search_frame, text="🔍 Search Appointment:", bootstyle="primary").pack(side='left', padx=(5,0))
        self.appt_search_var = tk.StringVar()
        appt_search_entry = ttk.Entry(search_frame, textvariable=self.appt_search_var, width=30)
        appt_search_entry.pack(side='left', padx=5)

        ttk.Button(search_frame, text="🔎 Search", bootstyle="primary",
                  command=self.search_appointments).pack(side='left', padx=5)
        ttk.Button(search_frame, text="🔄 Clear", bootstyle="info",
                  command=self.clear_appt_search).pack(side='left', padx=5)

        filter_options_frame = ttk.Frame(filters_frame)
        filter_options_frame.pack(fill='x', pady=5)

        ttk.Label(filter_options_frame, text="📅 Date:", bootstyle="primary").pack(side='left', padx=5)
        self.date_var = tk.StringVar(value="All")
        date_combo = ttk.Combobox(filter_options_frame, textvariable=self.date_var,
                                  values=["All", "Today", "This Week", "This Month"],
                                  state="readonly", width=15)
        date_combo.pack(side='left', padx=5)

        ttk.Label(filter_options_frame, text="📊 Status:", bootstyle="primary").pack(side='left', padx=5)
        self.status_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(filter_options_frame, textvariable=self.status_var,
                                   values=["All", "pending", "confirmed", "completed", "cancelled"],
                                   state="readonly", width=15)
        status_combo.pack(side='left', padx=5)

        ttk.Button(filter_options_frame, text="✅ Apply Filters", bootstyle="primary-outline",
                  command=self.load_appointments).pack(side='left', padx=5)

        # Remove 'id' from columns
        columns = ('id', 'username', 'service', 'date', 'time', 'contact', 'status')
        self.appt_tree = ttk.Treeview(self.appointments_frame, columns=columns,
                                      show='headings', bootstyle="primary")

        # Configure tag colors for different statuses
        self.appt_tree.tag_configure('pending', background='#fff3cd', foreground='#856404')  # Warning color
        self.appt_tree.tag_configure('confirmed', background='#d4edda', foreground='#155724')  # Success color
        self.appt_tree.tag_configure('completed', background='#cce5ff', foreground='#004085')  # Info color
        self.appt_tree.tag_configure('cancelled', background='#f8d7da', foreground='#721c24')  # Danger color

        # Define headings with icons and center alignment
        self.appt_tree.heading('id', text='🔢 ID')
        self.appt_tree.heading('username', text='👤 Patient Name')
        self.appt_tree.heading('service', text='🦷 Dental Service')
        self.appt_tree.heading('date', text='📅 Appointment Date')
        self.appt_tree.heading('time', text='⏰ Appointment Time')
        self.appt_tree.heading('contact', text='📱 Contact Number')
        self.appt_tree.heading('status', text='📊 Appointment Status')

        # Set column widths and center alignment
        self.appt_tree.column('id', width=40, anchor='center')
        self.appt_tree.column('username', width=120, anchor='center')
        self.appt_tree.column('service', width=180, anchor='center')
        self.appt_tree.column('date', width=90, anchor='center')
        self.appt_tree.column('time', width=90, anchor='center')
        self.appt_tree.column('contact', width=100, anchor='center')
        self.appt_tree.column('status', width=90, anchor='center')

        scrollbar = ttk.Scrollbar(self.appointments_frame, orient='vertical',
                                  command=self.appt_tree.yview)
        self.appt_tree.configure(yscrollcommand=scrollbar.set)

        self.appt_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Double-click binding
        self.appt_tree.bind("<Double-1>", self.open_appointment_action_modal)

        buttons_frame = ttk.Frame(self.appointments_frame)
        buttons_frame.pack(fill='y', side='right', padx=10, pady=5)

        # Style configuration for buttons
        button_style = {
            'width': 20,  # Increased width
            'padding': 12  # Increased padding
        }

        ttk.Button(buttons_frame, text="✅ Confirm",
                   command=lambda: self.update_appointment_status('confirmed'),
                   bootstyle="success", **button_style).pack(fill='x', pady=2)
        ttk.Button(buttons_frame, text="🏥 Completed",
                   command=lambda: self.update_appointment_status('completed'),
                   bootstyle="info", **button_style).pack(fill='x', pady=2)
        ttk.Button(buttons_frame, text="❌ Cancel",
                   command=lambda: self.update_appointment_status('cancelled'),
                   bootstyle="danger", **button_style).pack(fill='x', pady=2)
        ttk.Button(buttons_frame, text="📊 Generate Report",
                   command=self.generate_appointments_report,
                   bootstyle="warning", **button_style).pack(fill='x', pady=2)

        self.load_appointments()

    def load_appointments(self):
        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)

        try:
            query = """
                SELECT a.id, u.username, a.service, a.appointment_date,
                       a.appointment_time, u.phone_number, a.status
                FROM appointments a
                JOIN users u ON a.user_id = u.id
                WHERE 1=1
            """
            params = []

            if self.date_var.get() == "Today":
                query += " AND DATE(a.appointment_date) = CURDATE()"
            elif self.date_var.get() == "This Week":
                query += " AND YEARWEEK(a.appointment_date) = YEARWEEK(CURDATE())"
            elif self.date_var.get() == "This Month":
                query += " AND MONTH(a.appointment_date) = MONTH(CURDATE())"

            if self.status_var.get() != "All":
                query += " AND a.status = %s"
                params.append(self.status_var.get())

            if self.appt_search_var.get():
                query += " AND u.username LIKE %s"
                params.append(f"%{self.appt_search_var.get()}%")

            query += " ORDER BY a.appointment_date DESC, a.appointment_time DESC"

            result = self.app.execute_query(query, params)

            if result:
                for appt in result:
                    # Add status icons
                    status = appt[6].lower()
                    status_icon = {
                        'pending': '⏳',
                        'confirmed': '✅',
                        'completed': '🏥',
                        'cancelled': '❌'
                    }.get(status, '')
                    
                    # Format the values with icons (including ID)
                    values = (
                        appt[0],  # ID
                        appt[1],  # Username
                        appt[2],  # Service
                        appt[3],  # Date
                        appt[4],  # Time
                        appt[5],  # Contact
                        f"{status_icon} {status.capitalize()}"  # Status with icon
                    )
                    
                    self.appt_tree.insert('', 'end', values=values, tags=(status,))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {str(e)}")

    def update_appointment_status(self, new_status):
        selected_item = self.appt_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an appointment")
            return

        appt_values = self.appt_tree.item(selected_item[0])['values']
        appt_id = appt_values[0]
        username = appt_values[1]
        service = appt_values[2]
        date = appt_values[3]
        time = appt_values[4]

        # Create confirmation message based on the action
        if new_status == 'confirmed':
            title = "Confirm Appointment"
            message = f"Are you sure you want to confirm this appointment?\n\n" \
                     f"Client: {username}\n" \
                     f"Service: {service}\n" \
                     f"Date: {date}\n" \
                     f"Time: {time}\n\n" \
                     f"This will notify the client via SMS."
            action_type = "success"
        elif new_status == 'completed':
            title = "Mark as Completed"
            message = f"Are you sure you want to mark this appointment as completed?\n\n" \
                     f"Client: {username}\n" \
                     f"Service: {service}\n" \
                     f"Date: {date}\n" \
                     f"Time: {time}\n\n" \
                     f"This will notify the client via SMS."
            action_type = "info"
        elif new_status == 'cancelled':
            title = "Cancel Appointment"
            message = f"Are you sure you want to cancel this appointment?\n\n" \
                     f"Client: {username}\n" \
                     f"Service: {service}\n" \
                     f"Date: {date}\n" \
                     f"Time: {time}\n\n" \
                     f"This will notify the client via SMS."
            action_type = "danger"

        dialog = ModernConfirmationDialog(self, title, message, action_type)
        if not dialog.show():
            return

        try:
            result = self.app.execute_query(
                """
                SELECT a.*, u.phone_number, u.username
                FROM appointments a
                JOIN users u ON a.user_id = u.id
                WHERE a.id = %s
                """,
                (appt_id,)
            )

            if not result:
                messagebox.showerror("Error", "Could not find appointment details")
                return

            success = self.app.execute_query(
                "UPDATE appointments SET status = %s WHERE id = %s",
                (new_status, appt_id),
                fetch=False
            )

            if success:
                if new_status in ['confirmed', 'cancelled', 'completed']:
                    appointment_data = {
                        'appointment_date': result[0][3],
                        'appointment_time': result[0][4],
                        'service': result[0][2],
                        'client_name': result[0][7]
                    }
                    sms_success, sms_message = self.sms.send_appointment_notification(
                        result[0][6],
                        appointment_data,
                        new_status
                    )

                    if not sms_success:
                        messagebox.showwarning(
                            "SMS Notification",
                            f"Appointment updated but SMS notification failed: {sms_message}"
                        )

                messagebox.showinfo("Success", f"Appointment marked as {new_status.capitalize()}!")
                self.load_appointments()
            else:
                messagebox.showerror("Error", "Failed to update appointment status. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update appointment: {str(e)}")

    def open_appointment_action_modal(self, event):
        selected_item = self.appt_tree.selection()
        if not selected_item:
            return

        appt_values = self.appt_tree.item(selected_item[0])['values']
        appt_id = appt_values[0]
        username = appt_values[1]
        service = appt_values[2]
        date = appt_values[3]
        time = appt_values[4]
        status = appt_values[6]

        dialog = tk.Toplevel(self)
        dialog.title(f"Manage Appointment - {username}")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text=f"Username: {username}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(dialog, text=f"Service: {service}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(dialog, text=f"Date: {date}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(dialog, text=f"Time: {self.format_time(time)}", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(dialog, text=f"Status: {status}", font=("Helvetica", 12)).pack(pady=5)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)

        def update_status(new_status):
            self.update_appointment_status(new_status)
            dialog.destroy()

        ttk.Button(button_frame, text="Confirm", bootstyle="success",
                  command=lambda: update_status('confirmed')).pack(fill='x', pady=5)
        ttk.Button(button_frame, text="Mark as Completed", bootstyle="info",
                  command=lambda: update_status('completed')).pack(fill='x', pady=5)
        ttk.Button(button_frame, text="Cancel Appointment", bootstyle="danger",
                  command=lambda: update_status('cancelled')).pack(fill='x', pady=5)
        ttk.Button(dialog, text="Close", command=dialog.destroy, bootstyle="secondary").pack(pady=10)

    def search_appointments(self):
        search_term = self.appt_search_var.get().strip()
        if not search_term:
            self.load_appointments()
            return

        for item in self.appt_tree.get_children():
            self.appt_tree.delete(item)

        try:
            query = """
                SELECT a.id, u.username, a.service, a.appointment_date,
                       a.appointment_time, u.phone_number, a.status
                FROM appointments a
                JOIN users u ON a.user_id = u.id
                WHERE u.username LIKE %s OR a.service LIKE %s OR a.status LIKE %s
                ORDER BY a.appointment_date DESC, a.appointment_time DESC
            """
            like_term = f"%{search_term}%"
            result = self.app.execute_query(query, (like_term, like_term, like_term))

            if result:
                for appt in result:
                    status = appt[6].lower()  # Get the status from the appointment data
                    self.appt_tree.insert('', 'end', values=appt, tags=(status,))
            else:
                messagebox.showinfo("No Results", "No appointments found matching your search.")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def clear_appt_search(self):
        self.appt_search_var.set("")
        self.load_appointments()

    def format_time(self, time_str):
        # Convert time string to datetime object
        time_obj = datetime.strptime(time_str, '%H:%M:%S')
        # Format to show only hour
        return time_obj.strftime('%I:00 %p')
