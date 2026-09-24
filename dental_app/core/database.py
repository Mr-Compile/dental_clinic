"""Single shared MySQL connection with auto-reconnect and schema setup."""
import logging

import mysql.connector
from mysql.connector import Error as MySQLError
from mysql.connector.constants import ClientFlag

from dental_app.core.config import DB_CONFIG

log = logging.getLogger(__name__)


class DatabaseError(Exception):
    def __init__(self, message, errno=None):
        super().__init__(message)
        self.errno = errno


class Database:
    """Wraps one MySQL connection. All repositories share this instance.

    Rows are returned as dicts (dictionary cursor) so callers never rely on
    positional column indexing.
    """

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            # FOUND_ROWS makes UPDATE return matched rows (not just changed),
            # so repositories can report "no row matched" as failure.
            self.conn = mysql.connector.connect(
                **DB_CONFIG, client_flags=[ClientFlag.FOUND_ROWS])
            self.cursor = self.conn.cursor(buffered=True, dictionary=True)
        except MySQLError as err:
            raise DatabaseError(str(err), errno=err.errno) from err

    def is_connected(self):
        return self.conn is not None and self.conn.is_connected()

    def ensure_connection(self):
        if not self.is_connected():
            self.connect()

    def execute(self, query, params=None, fetch=True):
        """Run a query. Returns list[dict] for SELECT, True for writes."""
        self.ensure_connection()
        try:
            self.cursor.execute(query, params or ())
            if fetch:
                return self.cursor.fetchall()
            self.conn.commit()
            return self.cursor.rowcount > 0
        except MySQLError as err:
            self.conn.rollback()
            raise DatabaseError(str(err), errno=err.errno) from err

    def close(self):
        for resource in (self.cursor, self.conn):
            try:
                if resource:
                    resource.close()
            except Exception:
                pass

    def setup(self):
        """Create tables and run best-effort migrations. Returns True on success."""
        try:
            self.connect()
            self._create_tables()
            self._migrate()
            return True
        except (MySQLError, DatabaseError) as err:
            log.error("Database setup failed: %s", err)
            return False

    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone_number VARCHAR(11) NOT NULL,
                role ENUM('client', 'staff', 'admin') DEFAULT 'client',
                booking_allowed TINYINT GENERATED ALWAYS AS (role = 'client') STORED
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                service VARCHAR(100) NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
                active_slot VARCHAR(32) GENERATED ALWAYS AS (
                    IF(status IN ('pending', 'confirmed'),
                       CONCAT(appointment_date, ' ', appointment_time), NULL)
                ) STORED,
                UNIQUE KEY uq_active_slot (active_slot),
                KEY idx_appointment_date (appointment_date),
                KEY idx_status (status),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id INT AUTO_INCREMENT PRIMARY KEY,
                staff_id INT NOT NULL,
                report_type VARCHAR(100) NOT NULL,
                generated_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                description TEXT NOT NULL,
                report_data LONGTEXT NOT NULL,
                FOREIGN KEY (staff_id) REFERENCES users(id)
            )
        """)
        self.conn.commit()

    def _migrate(self):
        """In-place upgrades for databases created by older versions.

        Each statement is attempted independently; failures (already applied,
        or conflicting existing data) are skipped.
        """
        statements = [
            # password column must fit scrypt/bcrypt hashes
            "ALTER TABLE users MODIFY password VARCHAR(255) NOT NULL",
            "ALTER TABLE users ADD UNIQUE KEY uq_phone_number (phone_number)",
            # DB-level guard against double-booked active slots
            """ALTER TABLE appointments
               ADD COLUMN active_slot VARCHAR(32) GENERATED ALWAYS AS (
                   IF(status IN ('pending', 'confirmed'),
                      CONCAT(appointment_date, ' ', appointment_time), NULL)
               ) STORED""",
            "ALTER TABLE appointments ADD UNIQUE KEY uq_active_slot (active_slot)",
            "ALTER TABLE appointments ADD KEY idx_appointment_date (appointment_date)",
            "ALTER TABLE appointments ADD KEY idx_status (status)",
        ]
        for stmt in statements:
            try:
                self.cursor.execute(stmt)
                self.conn.commit()
            except MySQLError:
                self.conn.rollback()
