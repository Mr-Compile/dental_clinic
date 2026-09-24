import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk

class LandingPage(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.setup_ui()

    def setup_ui(self):
        # Create main container with scrollbar
        main_canvas = tk.Canvas(self, highlightthickness=0, bg='#f8f9fa')
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas, bootstyle="light")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=main_canvas.winfo_width())
        main_canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel to scroll
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        main_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind_all("<MouseWheel>", _on_mousewheel)

        # Make scrollable frame expand to fill canvas width
        def _on_canvas_configure(event):
            main_canvas.itemconfig(main_canvas.find_withtag("all")[0], width=event.width)
        main_canvas.bind("<Configure>", _on_canvas_configure)

        # Hero Section with modern gradient background
        hero_frame = ttk.Frame(scrollable_frame, bootstyle="primary")
        hero_frame.pack(fill='x', pady=(0, 20))
        
        # Hero content container with improved padding
        hero_content = ttk.Frame(hero_frame, bootstyle="primary")
        hero_content.pack(fill='x', padx=40, pady=40)
        
        # Create a container for the logo and text
        hero_left = ttk.Frame(hero_content, bootstyle="primary")
        hero_left.pack(side='left', fill='y', expand=True)
        
        # Logo with improved styling
        try:
            logo_img = Image.open("assets/dental.jpg")
            # Create a circular mask with modern styling
            mask = Image.new('L', (150, 150), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 150, 150), fill=255)
            # Resize and apply mask with high-quality resizing
            logo_img = logo_img.resize((150, 150), Image.LANCZOS)
            logo_img.putalpha(mask)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(hero_left, image=logo_photo, bootstyle="inverse-primary")
            logo_label.image = logo_photo
            logo_label.pack(pady=(0, 20))
        except:
            logo_label = ttk.Label(
                hero_left,
                text="🦷",
                font=("Helvetica", 80),
                bootstyle="inverse-primary"
            )
            logo_label.pack(pady=(0, 20))
        
        # Title and subtitle with improved styling
        title_label = ttk.Label(
            hero_left,
            text="Mirasol Dental Center",
            font=("Helvetica", 42, "bold"),
            bootstyle="inverse-primary"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            hero_left,
            text="Your Smile, Our Priority",
            font=("Helvetica", 20),
            bootstyle="inverse-primary"
        )
        subtitle_label.pack()
        
        # Back button container with improved positioning
        back_button_frame = ttk.Frame(hero_content, bootstyle="primary")
        back_button_frame.pack(side='right', fill='y', padx=(20, 0))
        
        # Back button with improved styling
        back_btn = ttk.Button(
            back_button_frame,
            text="Back",
            command=self.go_back_to_login,
            bootstyle="secondary",
            width=15,
            padding=(15, 8)
        )
        back_btn.pack(pady=(0, 20))
        
        # Main content container for centering
        main_content = ttk.Frame(scrollable_frame, bootstyle="light")
        main_content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Welcome Section with modern card styling
        welcome_card = ttk.Frame(main_content, bootstyle="light", padding=40)
        welcome_card.pack(fill='x', pady=(0, 30))
        
        welcome_label = ttk.Label(
            welcome_card,
            text="👋 Welcome to Excellence in Dental Care",
            font=("Helvetica", 32, "bold"),
            bootstyle="primary"
        )
        welcome_label.pack(pady=(0, 15))
        
        description_label = ttk.Label(
            welcome_card,
            text="Experience world-class dental care in the heart of Polomolok, South Cotabato. Our state-of-the-art facility and expert team are dedicated to providing you with the highest quality dental services in a comfortable and welcoming environment.",
            font=("Helvetica", 16),
            bootstyle="secondary",
            wraplength=1000  # Increased wraplength for better text flow
        )
        description_label.pack(pady=(0, 20))
        
        # Services Grid Section with improved styling
        services_card = ttk.Frame(main_content, bootstyle="light", padding=40)
        services_card.pack(fill='x', pady=(0, 30))
        
        services_title = ttk.Label(
            services_card,
            text="🦷 Our Comprehensive Services",
            font=("Helvetica", 28, "bold"),
            bootstyle="primary"
        )
        services_title.pack(pady=(0, 25))
        
        # Create a grid of services
        services_grid = ttk.Frame(services_card, bootstyle="light")
        services_grid.pack(fill='x')
        
        services = [
            ("🦷", "Dental Cleaning", "Professional cleaning to maintain optimal oral health"),
            ("🦷", "Tooth Extraction", "Safe and painless tooth removal procedures"),
            ("🦷", "Dental Fillings", "Restore damaged teeth with durable materials"),
            ("🦷", "Braces Consultation", "Expert advice for orthodontic treatment"),
            ("🦷", "Root Canal Treatment", "Save infected teeth with modern techniques"),
            ("🦷", "Dental Crowns", "Protect and restore damaged teeth"),
            ("🦷", "Teeth Whitening", "Brighten your smile safely"),
            ("🦷", "Dental Implants", "Permanent solution for missing teeth"),
            ("🦷", "Pediatric Dentistry", "Specialized care for children"),
            ("🦷", "Emergency Care", "Immediate attention for dental emergencies")
        ]
        
        # Create 2 columns for services with improved styling
        for i in range(0, len(services), 2):
            row_frame = ttk.Frame(services_grid, bootstyle="light")
            row_frame.pack(fill='x', pady=5)
            
            for j in range(2):
                if i + j < len(services):
                    icon, title, desc = services[i + j]
                    service_frame = ttk.Frame(row_frame, bootstyle="light", padding=15)
                    service_frame.pack(side='left', expand=True, fill='both', padx=5)
                    
                    ttk.Label(
                        service_frame,
                        text=f"{icon} {title}",
                        font=("Helvetica", 16, "bold"),
                        bootstyle="primary"
                    ).pack(anchor='w')
                    
                    ttk.Label(
                        service_frame,
                        text=desc,
                        font=("Helvetica", 12),
                        bootstyle="secondary",
                        wraplength=400  # Increased wraplength for better text flow
                    ).pack(anchor='w', pady=(5, 0))
        
        # Why Choose Us Section with improved styling
        why_choose_card = ttk.Frame(main_content, bootstyle="light", padding=40)
        why_choose_card.pack(fill='x', pady=(0, 30))
        
        why_choose_title = ttk.Label(
            why_choose_card,
            text="⭐ Why Choose Mirasol Dental Center?",
            font=("Helvetica", 28, "bold"),
            bootstyle="primary"
        )
        why_choose_title.pack(pady=(0, 25))
        
        benefits = [
            ("🌟", "State-of-the-art Equipment", "Latest dental technology for optimal care"),
            ("🌟", "Expert Team", "Experienced and friendly dental professionals"),
            ("🌟", "Modern Environment", "Comfortable and welcoming clinic atmosphere"),
            ("🌟", "Personalized Care", "Customized treatment plans for each patient"),
            ("🌟", "Emergency Services", "24/7 emergency dental care available"),
            ("🌟", "Affordable Pricing", "Transparent and competitive rates"),
            ("🌟", "Family Care", "Comprehensive dental care for all ages")
        ]
        
        # Create 2 columns for benefits with improved styling
        benefits_grid = ttk.Frame(why_choose_card, bootstyle="light")
        benefits_grid.pack(fill='x')
        
        for i in range(0, len(benefits), 2):
            row_frame = ttk.Frame(benefits_grid, bootstyle="light")
            row_frame.pack(fill='x', pady=5)
            
            for j in range(2):
                if i + j < len(benefits):
                    icon, title, desc = benefits[i + j]
                    benefit_frame = ttk.Frame(row_frame, bootstyle="light", padding=15)
                    benefit_frame.pack(side='left', expand=True, fill='both', padx=5)
                    
                    ttk.Label(
                        benefit_frame,
                        text=f"{icon} {title}",
                        font=("Helvetica", 16, "bold"),
                        bootstyle="primary"
                    ).pack(anchor='w')
                    
                    ttk.Label(
                        benefit_frame,
                        text=desc,
                        font=("Helvetica", 12),
                        bootstyle="secondary",
                        wraplength=400  # Increased wraplength for better text flow
                    ).pack(anchor='w', pady=(5, 0))
        
        # Contact and Hours Section with improved styling
        contact_hours_frame = ttk.Frame(main_content, bootstyle="light")
        contact_hours_frame.pack(fill='x', pady=(0, 30))
        
        # Contact Section
        contact_card = ttk.Frame(contact_hours_frame, bootstyle="light", padding=40)
        contact_card.pack(side='left', expand=True, fill='both', padx=(0, 10))
        
        contact_title = ttk.Label(
            contact_card,
            text="📞 Contact Us",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        contact_title.pack(pady=(0, 20))
        
        contact_info = [
            ("📞", "Phone", "0905 717 0763"),
            ("📍", "Address", "2/F, SD21 Building, Tuazon Subdivision, National Highway, Polomolok, 9504 South Cotabato"),
            ("📧", "Email", "mirasoldentalcenter@gmail.com"),
            ("🌐", "Facebook", "Mirasol Dental Center")
        ]
        
        for icon, label, value in contact_info:
            info_frame = ttk.Frame(contact_card, bootstyle="light")
            info_frame.pack(fill='x', pady=5)
            
            ttk.Label(
                info_frame,
                text=f"{icon} {label}:",
                font=("Helvetica", 14, "bold"),
                bootstyle="primary"
            ).pack(side='left', padx=(0, 10))
            
            ttk.Label(
                info_frame,
                text=value,
                font=("Helvetica", 14),
                bootstyle="secondary",
                wraplength=400  # Increased wraplength for better text flow
            ).pack(side='left')
        
        # Hours Section
        hours_card = ttk.Frame(contact_hours_frame, bootstyle="light", padding=40)
        hours_card.pack(side='right', expand=True, fill='both', padx=(10, 0))
        
        hours_title = ttk.Label(
            hours_card,
            text="⏰ Business Hours",
            font=("Helvetica", 24, "bold"),
            bootstyle="primary"
        )
        hours_title.pack(pady=(0, 20))
        
        hours = [
            ("🕘", "Monday", "9:00 AM - 4:00 PM"),
            ("🕘", "Tuesday", "9:00 AM - 4:00 PM"),
            ("🕘", "Wednesday", "9:00 AM - 4:00 PM"),
            ("🕘", "Thursday", "9:00 AM - 4:00 PM"),
            ("🕘", "Friday", "9:00 AM - 4:00 PM"),
            ("🕘", "Saturday", "9:00 AM - 4:00 PM"),
            ("❌", "Sunday", "Closed")
        ]
        
        for icon, day, time in hours:
            hour_frame = ttk.Frame(hours_card, bootstyle="light")
            hour_frame.pack(fill='x', pady=5)
            
            ttk.Label(
                hour_frame,
                text=f"{icon} {day}:",
                font=("Helvetica", 14, "bold"),
                bootstyle="primary"
            ).pack(side='left', padx=(0, 10))
            
            ttk.Label(
                hour_frame,
                text=time,
                font=("Helvetica", 14),
                bootstyle="secondary"
            ).pack(side='left')
        
        # Footer with modern styling
        footer_frame = ttk.Frame(scrollable_frame, bootstyle="primary")
        footer_frame.pack(fill='x', pady=(20, 0))
        
        footer_label = ttk.Label(
            footer_frame,
            text="© 2024 Mirasol Dental Center. All rights reserved. #MDC #confidentradiantsmile",
            font=("Helvetica", 14),
            bootstyle="inverse-primary"
        )
        footer_label.pack(pady=20)

    def go_back_to_login(self):
        # Unbind mouse wheel events
        for widget in self.winfo_children():
            widget.unbind_all("<MouseWheel>")
        
        # Destroy the current frame
        self.destroy()
        
        # Create new login frame
        self.app.create_login_frame() 