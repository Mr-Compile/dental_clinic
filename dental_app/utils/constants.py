"""Shared application constants — single source of truth."""

APP_NAME = "Mirasol Dental Center"

SERVICES = ["Cleaning", "Extraction", "Filling", "Braces Consultation", "Other"]

TIME_SLOTS = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00"]

APPOINTMENT_STATUSES = ["pending", "confirmed", "completed", "cancelled"]

USER_ROLES = ["client", "staff", "admin"]

STATUS_ICONS = {
    "pending": "⏳",
    "confirmed": "✅",
    "completed": "🏥",
    "cancelled": "❌",
}

STATUS_TAG_COLORS = {
    "pending": {"background": "#fff3cd", "foreground": "#856404"},
    "confirmed": {"background": "#d4edda", "foreground": "#155724"},
    "completed": {"background": "#cce5ff", "foreground": "#004085"},
    "cancelled": {"background": "#f8d7da", "foreground": "#721c24"},
}

COLORS = {
    "primary": "#2c3e50",
    "secondary": "#34495e",
    "accent": "#3498db",
    "success": "#2ecc71",
    "danger": "#e74c3c",
    "warning": "#f1c40f",
    "info": "#1abc9c",
    "light": "#ecf0f1",
    "dark": "#2c3e50",
    "white": "#ffffff",
    "completed": "#2980b9",
}

# Booking rules
CLINIC_CLOSED_WEEKDAY = 6      # Sunday (Python weekday(): Monday=0)
MAX_BOOKING_DAYS_AHEAD = 365
DATE_FILTER_OPTIONS = ["All", "Today", "This Week", "This Month"]
