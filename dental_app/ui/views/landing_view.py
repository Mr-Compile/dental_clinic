import ttkbootstrap as ttk

from dental_app.ui.components.scrollable_frame import ScrollableFrame
from dental_app.utils.images import load_circular_image

SERVICES = [
    ("🦷", "Dental Cleaning", "Professional cleaning to maintain optimal oral health"),
    ("🦷", "Tooth Extraction", "Safe and painless tooth removal procedures"),
    ("🦷", "Dental Fillings", "Restore damaged teeth with durable materials"),
    ("🦷", "Braces Consultation", "Expert advice for orthodontic treatment"),
    ("🦷", "Root Canal Treatment", "Save infected teeth with modern techniques"),
    ("🦷", "Dental Crowns", "Protect and restore damaged teeth"),
    ("🦷", "Teeth Whitening", "Brighten your smile safely"),
    ("🦷", "Dental Implants", "Permanent solution for missing teeth"),
    ("🦷", "Pediatric Dentistry", "Specialized care for children"),
    ("🦷", "Emergency Care", "Immediate attention for dental emergencies"),
]

BENEFITS = [
    ("🌟", "State-of-the-art Equipment", "Latest dental technology for optimal care"),
    ("🌟", "Expert Team", "Experienced and friendly dental professionals"),
    ("🌟", "Modern Environment", "Comfortable and welcoming clinic atmosphere"),
    ("🌟", "Personalized Care", "Customized treatment plans for each patient"),
    ("🌟", "Emergency Services", "24/7 emergency dental care available"),
    ("🌟", "Affordable Pricing", "Transparent and competitive rates"),
    ("🌟", "Family Care", "Comprehensive dental care for all ages"),
]

CONTACT_INFO = [
    ("📞", "Phone", "0905 717 0763"),
    ("📍", "Address", "2/F, SD21 Building, Tuazon Subdivision, National Highway, Polomolok, 9504 South Cotabato"),
    ("📧", "Email", "mirasoldentalcenter@gmail.com"),
    ("🌐", "Facebook", "Mirasol Dental Center"),
]

HOURS = [
    ("🕘", "Monday", "9:00 AM - 4:00 PM"),
    ("🕘", "Tuesday", "9:00 AM - 4:00 PM"),
    ("🕘", "Wednesday", "9:00 AM - 4:00 PM"),
    ("🕘", "Thursday", "9:00 AM - 4:00 PM"),
    ("🕘", "Friday", "9:00 AM - 4:00 PM"),
    ("🕘", "Saturday", "9:00 AM - 4:00 PM"),
    ("❌", "Sunday", "Closed"),
]


class LandingView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        scroller = ScrollableFrame(self, inner_bootstyle="light")
        scroller.pack(fill="both", expand=True)
        page = scroller.inner

        # Hero
        hero_frame = ttk.Frame(page, bootstyle="primary")
        hero_frame.pack(fill="x", pady=(0, 20))

        hero_content = ttk.Frame(hero_frame, bootstyle="primary")
        hero_content.pack(fill="x", padx=40, pady=40)

        hero_left = ttk.Frame(hero_content, bootstyle="primary")
        hero_left.pack(side="left", fill="y", expand=True)

        logo_photo = load_circular_image("dental.jpg", 150)
        if logo_photo:
            logo_label = ttk.Label(hero_left, image=logo_photo, bootstyle="inverse-primary")
            logo_label.image = logo_photo
        else:
            logo_label = ttk.Label(hero_left, text="🦷", font=("Helvetica", 80),
                                   bootstyle="inverse-primary")
        logo_label.pack(pady=(0, 20))

        ttk.Label(hero_left, text="Mirasol Dental Center", font=("Helvetica", 42, "bold"),
                  bootstyle="inverse-primary").pack(pady=(0, 10))
        ttk.Label(hero_left, text="Your Smile, Our Priority", font=("Helvetica", 20),
                  bootstyle="inverse-primary").pack()

        back_button_frame = ttk.Frame(hero_content, bootstyle="primary")
        back_button_frame.pack(side="right", fill="y", padx=(20, 0))
        ttk.Button(back_button_frame, text="Back", command=self.app.show_login,
                   bootstyle="secondary", width=15, padding=(15, 8)).pack(pady=(0, 20))

        main_content = ttk.Frame(page, bootstyle="light")
        main_content.pack(fill="both", expand=True, padx=40, pady=20)

        # Welcome card
        welcome_card = ttk.Frame(main_content, bootstyle="light", padding=40)
        welcome_card.pack(fill="x", pady=(0, 30))
        ttk.Label(welcome_card, text="👋 Welcome to Excellence in Dental Care",
                  font=("Helvetica", 32, "bold"), bootstyle="primary").pack(pady=(0, 15))
        ttk.Label(
            welcome_card,
            text=("Experience world-class dental care in the heart of Polomolok, "
                  "South Cotabato. Our state-of-the-art facility and expert team are "
                  "dedicated to providing you with the highest quality dental services "
                  "in a comfortable and welcoming environment."),
            font=("Helvetica", 16), bootstyle="secondary", wraplength=1000,
        ).pack(pady=(0, 20))

        # Services grid
        services_card = ttk.Frame(main_content, bootstyle="light", padding=40)
        services_card.pack(fill="x", pady=(0, 30))
        ttk.Label(services_card, text="🦷 Our Comprehensive Services",
                  font=("Helvetica", 28, "bold"), bootstyle="primary").pack(pady=(0, 25))
        self._two_column_grid(services_card, SERVICES)

        # Why choose us
        why_card = ttk.Frame(main_content, bootstyle="light", padding=40)
        why_card.pack(fill="x", pady=(0, 30))
        ttk.Label(why_card, text="⭐ Why Choose Mirasol Dental Center?",
                  font=("Helvetica", 28, "bold"), bootstyle="primary").pack(pady=(0, 25))
        self._two_column_grid(why_card, BENEFITS)

        # Contact + hours
        contact_hours_frame = ttk.Frame(main_content, bootstyle="light")
        contact_hours_frame.pack(fill="x", pady=(0, 30))

        contact_card = ttk.Frame(contact_hours_frame, bootstyle="light", padding=40)
        contact_card.pack(side="left", expand=True, fill="both", padx=(0, 10))
        ttk.Label(contact_card, text="📞 Contact Us", font=("Helvetica", 24, "bold"),
                  bootstyle="primary").pack(pady=(0, 20))
        self._kv_rows(contact_card, CONTACT_INFO, wrap=True)

        hours_card = ttk.Frame(contact_hours_frame, bootstyle="light", padding=40)
        hours_card.pack(side="right", expand=True, fill="both", padx=(10, 0))
        ttk.Label(hours_card, text="⏰ Business Hours", font=("Helvetica", 24, "bold"),
                  bootstyle="primary").pack(pady=(0, 20))
        self._kv_rows(hours_card, HOURS)

        # Footer
        footer_frame = ttk.Frame(page, bootstyle="primary")
        footer_frame.pack(fill="x", pady=(20, 0))
        ttk.Label(footer_frame,
                  text="© 2024 Mirasol Dental Center. All rights reserved. #MDC #confidentradiantsmile",
                  font=("Helvetica", 14), bootstyle="inverse-primary").pack(pady=20)

    def _two_column_grid(self, parent, items):
        grid = ttk.Frame(parent, bootstyle="light")
        grid.pack(fill="x")

        for i in range(0, len(items), 2):
            row_frame = ttk.Frame(grid, bootstyle="light")
            row_frame.pack(fill="x", pady=5)
            for j in range(2):
                if i + j < len(items):
                    icon, title, desc = items[i + j]
                    cell = ttk.Frame(row_frame, bootstyle="light", padding=15)
                    cell.pack(side="left", expand=True, fill="both", padx=5)
                    ttk.Label(cell, text=f"{icon} {title}",
                              font=("Helvetica", 16, "bold"),
                              bootstyle="primary").pack(anchor="w")
                    ttk.Label(cell, text=desc, font=("Helvetica", 12),
                              bootstyle="secondary", wraplength=400).pack(anchor="w", pady=(5, 0))

    def _kv_rows(self, parent, rows, wrap=False):
        for icon, label, value in rows:
            row = ttk.Frame(parent, bootstyle="light")
            row.pack(fill="x", pady=5)
            ttk.Label(row, text=f"{icon} {label}:", font=("Helvetica", 14, "bold"),
                      bootstyle="primary").pack(side="left", padx=(0, 10))
            kwargs = {"wraplength": 400} if wrap else {}
            ttk.Label(row, text=value, font=("Helvetica", 14),
                      bootstyle="secondary", **kwargs).pack(side="left")
