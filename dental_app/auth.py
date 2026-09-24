from tkinter import messagebox
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from shared.register_frame import RegisterFrame
from dental_app.landing_page import LandingPage
from PIL import Image, ImageTk, ImageDraw

class AuthMixin:
    def create_login_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        # Create main container with modern styling
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both')
        
        # Create perfect 50-50 split screen layout
        left_frame = ttk.Frame(main_frame, width=self.winfo_screenwidth()//2)
        left_frame.pack(side='left', expand=True, fill='both')
        
        right_frame = ttk.Frame(main_frame, width=self.winfo_screenwidth()//2, bootstyle="light")
        right_frame.pack(side='right', expand=True, fill='both')
        
        # Add background image to left frame
        try:
            bg_img = Image.open("assets/www.jpg")
            # Calculate dimensions to fill the entire height
            window_width = self.winfo_screenwidth() // 2
            window_height = self.winfo_screenheight()
            aspect_ratio = bg_img.width / bg_img.height
            
            # Calculate new dimensions to fill height while maintaining aspect ratio
            new_height = window_height
            new_width = int(new_height * aspect_ratio)
            
            # If the calculated width is less than the window width, adjust to fill width instead
            if new_width < window_width:
                new_width = window_width
                new_height = int(new_width / aspect_ratio)
            
            bg_img = bg_img.resize((new_width, new_height), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(bg_img)
            bg_label = ttk.Label(left_frame, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(relx=0, rely=0.5, anchor="w")
        except Exception as e:
            print(f"Error loading background image: {e}")
        
        # Create centered container for login form with fixed width
        form_container = ttk.Frame(right_frame, bootstyle="light")
        form_container.place(relx=0.5, rely=0.5, anchor="center", width=500)  # Increased width
        
        # Logo and welcome message
        logo_frame = ttk.Frame(form_container, bootstyle="light")
        logo_frame.pack(expand=True, fill='both', pady=(0, 20))
        
        try:
            logo_img = Image.open("assets/dental.jpg")
            # Create a circular mask
            mask = Image.new('L', (120, 120), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 120, 120), fill=255)
            # Resize and apply mask
            logo_img = logo_img.resize((120, 120), Image.LANCZOS)
            logo_img.putalpha(mask)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(logo_frame, image=logo_photo, bootstyle="light")
            logo_label.image = logo_photo
            logo_label.pack(pady=(0, 20))
        except:
            logo_label = ttk.Label(
                logo_frame,
                text="🦷",
                font=("Helvetica", 50),
                bootstyle="light"
            )
            logo_label.pack(pady=(0, 20))
        
        welcome_label = ttk.Label(
            logo_frame,
            text="Mirasol Dental Center",
            font=("Helvetica", 18, "bold"),
            bootstyle="primary"
        )
        welcome_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            logo_frame,
            text="Sign in to manage your dental appointments",
            font=("Helvetica", 10),
            bootstyle="secondary",
            wraplength=400  # Added wraplength
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Login form with modern styling
        form_frame = ttk.Frame(form_container, padding=30, bootstyle="light")
        form_frame.pack(expand=True, fill='both')
        
        title_label = ttk.Label(
            form_frame, 
            text="Sign In",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary"
        )
        title_label.pack(pady=(0, 20))
        
        # Create form fields with modern styling
        fields_container = ttk.Frame(form_frame, bootstyle="light")
        fields_container.pack(expand=True)
        
        # Email field with modern styling
        email_frame = ttk.Frame(fields_container, bootstyle="light")
        email_frame.pack(fill='x', pady=10)
        email_label_frame = ttk.Frame(email_frame, bootstyle="light")
        email_label_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(email_label_frame, text="📧", font=("Helvetica", 12)).pack(side='left', padx=(0, 5))
        ttk.Label(email_label_frame, text="Email", bootstyle="secondary").pack(side='left')
        self.email_entry = ttk.Entry(email_frame, bootstyle="primary", width=35)  # Increased width
        self.email_entry.pack(fill='x', pady=5)
        
        # Password field with modern styling
        password_frame = ttk.Frame(fields_container, bootstyle="light")
        password_frame.pack(fill='x', pady=10)
        password_label_frame = ttk.Frame(password_frame, bootstyle="light")
        password_label_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(password_label_frame, text="🔒", font=("Helvetica", 12)).pack(side='left', padx=(0, 5))
        ttk.Label(password_label_frame, text="Password", bootstyle="secondary").pack(side='left')
        self.password_entry = ttk.Entry(password_frame, show="•", bootstyle="primary", width=35)  # Increased width
        self.password_entry.pack(fill='x', pady=5)
        
        # Login button with modern styling
        login_btn = ttk.Button(
            form_frame,
            text="🔑 Sign In",
            command=self.login,
            bootstyle="success",
            width=35,  # Increased width
            padding=(10, 5)
        )
        login_btn.pack(pady=20)
        
        # Register section with modern styling
        register_frame = ttk.Frame(form_frame, bootstyle="light")
        register_frame.pack(pady=10)
        
        ttk.Label(
            register_frame,
            text="👤 Don't have an account? ",
            font=("Helvetica", 9),
            bootstyle="secondary"
        ).pack(side='left')
        
        register_link = ttk.Label(
            register_frame,
            text="📝 Create Account",
            font=("Helvetica", 9, "bold"),
            cursor="hand2",
            bootstyle="primary"
        )
        register_link.pack(side='left')
        register_link.bind("<Button-1>", lambda e: self.show_register_frame())
        
        # Add landing page link
        landing_frame = ttk.Frame(form_frame, bootstyle="light")
        landing_frame.pack(pady=10)
        
        landing_link = ttk.Label(
            landing_frame,
            text="🏥 Visit Our Clinic Website",
            font=("Helvetica", 9, "bold"),
            cursor="hand2",
            bootstyle="primary"
        )
        landing_link.pack()
        landing_link.bind("<Button-1>", lambda e: self.show_landing_page())
        
        # Add some helpful text
        help_text = ttk.Label(
            form_frame,
            text="❓ Need help? Contact us at mirasoldentalcenter@gmail.com",
            font=("Helvetica", 8),
            bootstyle="secondary",
            wraplength=400  # Added wraplength
        )
        help_text.pack(pady=(20, 0))
        
        self.current_frame = main_frame

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            result = self.execute_query(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password)
            )

            if not result:
                messagebox.showerror("Error", "Invalid email or password")
                return

            user = result[0]
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'phone_number': user[4],
                'role': user[5]
            }
            
            # Clear login frame and show dashboard
            if self.current_frame:
                self.current_frame.destroy()
                
            self.show_dashboard()

        except Exception as err:
            messagebox.showerror("Error", f"Login failed: {err}")

    def show_register_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = RegisterFrame(self, self)
        self.current_frame.pack(pady=50)

    def show_landing_page(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LandingPage(self, self)
        self.current_frame.pack(expand=True, fill='both')
