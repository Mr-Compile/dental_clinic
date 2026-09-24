"""Application configuration loaded from environment / .env file."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

ASSETS_DIR = BASE_DIR / "assets"
REPORTS_DIR = BASE_DIR / "reports"

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "dental"),
}

SEMAPHORE_API_KEY = os.getenv("SEMAPHORE_API_KEY", "")
SEMAPHORE_SENDER_NAME = os.getenv("SEMAPHORE_SENDER_NAME", "DENTAL")
SEMAPHORE_API_URL = os.getenv("SEMAPHORE_API_URL", "https://api.semaphore.co/api/v4/messages")
SEMAPHORE_ACCOUNT_URL = "https://api.semaphore.co/api/v4/account"

APP_TITLE = "Mirasol Dental Clinic Appointment System With SMS Notifications"
APP_GEOMETRY = "1200x800"


def asset_path(name: str) -> str:
    return str(ASSETS_DIR / name)
