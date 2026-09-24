"""Authentication and account management.

Passwords are hashed with Werkzeug (scrypt). Legacy plaintext passwords —
including seeded accounts — are transparently upgraded to a hash on first
successful login.
"""
import logging

from werkzeug.security import check_password_hash, generate_password_hash

from dental_app.utils.validators import validate_email, validate_phone

log = logging.getLogger(__name__)

_HASH_PREFIXES = ("scrypt:", "pbkdf2:", "argon2")


class AuthService:
    def __init__(self, user_repo):
        self.users = user_repo

    def hash_password(self, password: str) -> str:
        return generate_password_hash(password)

    def _verify(self, stored: str, candidate: str) -> bool:
        if stored.startswith(_HASH_PREFIXES):
            try:
                return check_password_hash(stored, candidate)
            except (ValueError, TypeError):
                return False
        # Legacy plaintext row
        return stored == candidate

    def login(self, email: str, password: str):
        """Return the user dict on success, None on failure."""
        user = self.users.find_by_email(email)
        if not user or not self._verify(user["password"], password):
            return None

        # Transparent upgrade of legacy plaintext passwords
        if not user["password"].startswith(_HASH_PREFIXES):
            try:
                self.users.update_password(user["id"], self.hash_password(password))
            except Exception as err:
                log.warning("Password rehash failed for user %s: %s", user["id"], err)

        user.pop("password", None)
        return user

    def register(self, username, email, password, confirm_password, phone):
        """Client self-registration. Returns (ok, message)."""
        if not all([username, email, password, confirm_password, phone]):
            return False, "Please fill in all fields"
        if not validate_email(email):
            return False, "Please enter a valid email address"
        if password != confirm_password:
            return False, "Passwords do not match"
        if not validate_phone(phone):
            return False, "Invalid phone number format. Please use 11 digits (e.g., 09123456789)"
        return self.create_account(username, email, password, phone, role="client")

    def create_account(self, username, email, password, phone, role="client"):
        """Create any account (used by registration and admin user creation)."""
        if not validate_email(email):
            return False, "Please enter a valid email address"
        if self.users.username_exists(username):
            return False, "Username already exists"
        if self.users.phone_exists(phone):
            return False, "Phone number already registered"

        # Unique email is enforced by the DB; check here for a friendly message
        if self.users.find_by_email(email):
            return False, "Email already registered"

        try:
            ok = self.users.create(
                username, email, self.hash_password(password), phone, role
            )
        except Exception as err:
            return False, f"Failed to create user: {err}"

        return (True, "Account created") if ok else (False, "Failed to create user")
