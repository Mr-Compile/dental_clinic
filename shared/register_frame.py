import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import re
from PIL import Image, ImageTk, ImageDraw

class RegisterFrame(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.pack(expand=True, fill='both')
        
        # Create main container with modern styling
        main_frame = ttk.Frame(self, padding=20, bootstyle="light")
        main_frame.pack(expand=True, fill='both')
        
        # Create two-column layout
        left_frame = ttk.Frame(main_frame, bootstyle="light")
        left_frame.pack(side='left', expand=True, fill='both', padx=(0, 20))
        
        right_frame = ttk.Frame(main_frame, bootstyle="light")
        right_frame.pack(side='right', expand=True, fill='both')
        
        # Left side - Logo and welcome message
        logo_frame = ttk.Frame(left_frame, bootstyle="light")
        logo_frame.pack(expand=True, fill='both')
        
        try:
            logo_img = Image.open("assets/dental.jpg")
            # Create a circular mask
            mask = Image.new('L', (320, 320), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 320, 320), fill=255)
            # Resize and apply mask
            logo_img = logo_img.resize((320, 320), Image.LANCZOS)
            logo_img.putalpha(mask)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(logo_frame, image=logo_photo, bootstyle="light")
            logo_label.image = logo_photo
            logo_label.pack(pady=(50, 20))
        except:
            logo_label = ttk.Label(
                logo_frame,
                text="🦷",
                font=("Helvetica", 120),
                bootstyle="light"
            )
            logo_label.pack(pady=(50, 20))
        
        welcome_label = ttk.Label(
            logo_frame,
            text="Welcome to Dental Clinic",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        welcome_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            logo_frame,
            text="Create your account to manage your dental appointments",
            font=("Helvetica", 12),
            bootstyle="secondary",
            wraplength=300
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Right side - Registration form
        form_frame = ttk.Frame(right_frame, padding=40, bootstyle="light")
        form_frame.pack(expand=True, fill='both')
        
        title_label = ttk.Label(
            form_frame, 
            text="Create Your Account",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        title_label.pack(pady=(0, 30))
        
        # Create a container for all form fields to ensure consistent width
        fields_container = ttk.Frame(form_frame, bootstyle="light")
        fields_container.pack(fill='x', expand=True)
        
        # Define consistent widths
        entry_width = 30
        
        # Username field with icon
        username_frame = ttk.Frame(fields_container, bootstyle="light")
        username_frame.pack(fill='x', pady=10)
        username_label_frame = ttk.Frame(username_frame, bootstyle="light")
        username_label_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(username_label_frame, text="👤", font=("Helvetica", 14)).pack(side='left', padx=(0, 5))
        ttk.Label(username_label_frame, text="Username", bootstyle="secondary").pack(side='left')
        self.username_entry = ttk.Entry(username_frame, bootstyle="primary", width=entry_width)
        self.username_entry.pack(fill='x', expand=True)
        
        # Email field with icon
        email_frame = ttk.Frame(fields_container, bootstyle="light")
        email_frame.pack(fill='x', pady=10)
        email_label_frame = ttk.Frame(email_frame, bootstyle="light")
        email_label_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(email_label_frame, text="📧", font=("Helvetica", 14)).pack(side='left', padx=(0, 5))
        ttk.Label(email_label_frame, text="Email", bootstyle="secondary").pack(side='left')
        self.email_entry = ttk.Entry(email_frame, bootstyle="primary", width=entry_width)
        self.email_entry.pack(fill='x', expand=True)
        
        # Phone field with icon
        phone_frame = ttk.Frame(fields_container, bootstyle="light")
        phone_frame.pack(fill='x', pady=10)
        phone_label_frame = ttk.Frame(phone_frame, bootstyle="light")
        phone_label_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(phone_label_frame, text="📱", font=("Helvetica", 14)).pack(side='left', padx=(0, 5))
        ttk.Label(phone_label_frame, text="Phone", bootstyle="secondary").pack(side='left')
        self.phone_entry = ttk.Entry(phone_frame, bootstyle="primary", width=entry_width)
        self.phone_entry.pack(fill='x', expand=True)
        
        # Add validation for phone number input
        self.phone_entry.bind('<KeyPress>', self.validate_phone_input)
        self.phone_entry.bind('<KeyRelease>', self.format_phone_number)
        
        # Password field with icon
        password_frame = ttk.Frame(fields_container, bootstyle="light")
        password_frame.pack(fill='x', pady=10)
        password_label_frame = ttk.Frame(password_frame, bootstyle="light")
        password_label_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(password_label_frame, text="🔒", font=("Helvetica", 14)).pack(side='left', padx=(0, 5))
        ttk.Label(password_label_frame, text="Password", bootstyle="secondary").pack(side='left')
        self.password_entry = ttk.Entry(password_frame, show="•", bootstyle="primary", width=entry_width)
        self.password_entry.pack(fill='x', expand=True)
        
        # Confirm Password field with icon
        confirm_password_frame = ttk.Frame(fields_container, bootstyle="light")
        confirm_password_frame.pack(fill='x', pady=10)
        confirm_password_label_frame = ttk.Frame(confirm_password_frame, bootstyle="light")
        confirm_password_label_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(confirm_password_label_frame, text="🔒", font=("Helvetica", 14)).pack(side='left', padx=(0, 5))
        ttk.Label(confirm_password_label_frame, text="Confirm Password", bootstyle="secondary").pack(side='left')
        self.confirm_password_entry = ttk.Entry(confirm_password_frame, show="•", bootstyle="primary", width=entry_width)
        self.confirm_password_entry.pack(fill='x', expand=True)
        
        # Buttons with modern styling
        button_frame = ttk.Frame(form_frame, bootstyle="light")
        button_frame.pack(pady=30)
        
        # Register button with icon
        register_btn = ttk.Button(
            button_frame,
            text="📝 Create Account",
            command=self.register,
            bootstyle="success",
            width=entry_width,
            padding=(10, 5)
        )
        register_btn.pack(pady=5)
        
        # Back to login button with icon
        login_btn = ttk.Button(
            button_frame,
            text="↩️ Back to Login",
            command=self.show_login,
            bootstyle="secondary",
            width=entry_width,
            padding=(10, 5)
        )
        login_btn.pack(pady=5)
        
        # Add some helpful text with icon
        help_text = ttk.Label(
            form_frame,
            text="ℹ️ By creating an account, you agree to our Terms of Service and Privacy Policy",
            font=("Helvetica", 8),
            bootstyle="secondary"
        )
        help_text.pack(pady=(20, 0))

    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def validate_phone_input(self, event):
        """Validate phone number input - allow only numbers and limit to 11 digits"""
        if event.char.isdigit():
            current = self.phone_entry.get()
            if len(current) >= 11:
                return "break"  # Prevent input if already 11 digits
        elif event.keysym not in ('BackSpace', 'Delete', 'Left', 'Right'):
            return "break"  # Prevent non-digit input except control keys

    def format_phone_number(self, event):
        """Ensure phone number starts with 09 and is limited to 11 digits"""
        current = self.phone_entry.get()
        
        # Remove any non-digits
        cleaned = ''.join(filter(str.isdigit, current))
        
        # Ensure it starts with 09
        if len(cleaned) >= 2 and cleaned[:2] != '09':
            cleaned = '09' + cleaned[2:] if len(cleaned) > 2 else '09'
            
        # Limit to 11 digits
        cleaned = cleaned[:11]
        
        # Update entry if different
        if cleaned != current:
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, cleaned)

    def validate_phone(self, phone):
        """Validate complete phone number format"""
        # Must be exactly 11 digits starting with 09
        pattern = r'^09\d{9}$'
        return re.match(pattern, phone) is not None
        
    def register(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        phone_number = self.phone_entry.get().strip()
        
        # Basic validation
        if not all([username, email, password, confirm_password, phone_number]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        if not self.validate_phone(phone_number):
            messagebox.showerror("Error", "Invalid phone number format. Please use 11 digits (e.g., 09123456789)")
            return
            
        try:
            # Check if email already exists
            result = self.app.execute_query(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )
            
            if result:
                messagebox.showerror("Error", "Email already registered")
                return
                
            # Store plain text password
            success = self.app.execute_query(
                """
                INSERT INTO users (username, email, password, phone_number, role)
                VALUES (%s, %s, %s, %s, 'client')
                """,
                (username, email, password, phone_number),
                fetch=False
            )
            
            if success:
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                self.app.create_login_frame()  # Return to login screen
            else:
                messagebox.showerror("Error", "Registration failed")
                
        except Exception as err:
            messagebox.showerror("Error", f"Registration failed: {err}")

    def clear_fields(self):
        """Clear all entry fields"""
        self.username_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')

    def show_login(self):
        self.destroy()  # Destroy this frame instead of clearing parent
        self.app.create_login_frame()