"""All SQL for the users table."""


class UserRepository:
    def __init__(self, db):
        self.db = db

    def find_by_email(self, email):
        rows = self.db.execute(
            "SELECT id, username, email, password, phone_number, role FROM users WHERE email = %s",
            (email,),
        )
        return rows[0] if rows else None

    def username_exists(self, username, exclude_id=None):
        if exclude_id is not None:
            rows = self.db.execute(
                "SELECT id FROM users WHERE username = %s AND id != %s",
                (username, exclude_id),
            )
        else:
            rows = self.db.execute(
                "SELECT id FROM users WHERE username = %s", (username,)
            )
        return bool(rows)

    def phone_exists(self, phone, exclude_id=None):
        if exclude_id is not None:
            rows = self.db.execute(
                "SELECT id FROM users WHERE phone_number = %s AND id != %s",
                (phone, exclude_id),
            )
        else:
            rows = self.db.execute(
                "SELECT id FROM users WHERE phone_number = %s", (phone,)
            )
        return bool(rows)

    def create(self, username, email, password_hash, phone, role="client"):
        return self.db.execute(
            """
            INSERT INTO users (username, email, password, phone_number, role)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (username, email, password_hash, phone, role),
            fetch=False,
        )

    def update(self, user_id, username, email, phone, password_hash=None):
        if password_hash:
            return self.db.execute(
                """
                UPDATE users
                SET username = %s, email = %s, phone_number = %s, password = %s
                WHERE id = %s
                """,
                (username, email, phone, password_hash, user_id),
                fetch=False,
            )
        return self.db.execute(
            """
            UPDATE users
            SET username = %s, email = %s, phone_number = %s
            WHERE id = %s
            """,
            (username, email, phone, user_id),
            fetch=False,
        )

    def update_role(self, user_id, role):
        return self.db.execute(
            "UPDATE users SET role = %s WHERE id = %s",
            (role, user_id),
            fetch=False,
        )

    def update_password(self, user_id, password_hash):
        return self.db.execute(
            "UPDATE users SET password = %s WHERE id = %s",
            (password_hash, user_id),
            fetch=False,
        )

    def delete(self, user_id):
        return self.db.execute(
            "DELETE FROM users WHERE id = %s", (user_id,), fetch=False
        )

    def list_all(self):
        return self.db.execute(
            "SELECT id, username, email, phone_number, role FROM users ORDER BY id"
        )

    def search(self, term):
        like = f"%{term}%"
        return self.db.execute(
            """
            SELECT id, username, email, phone_number, role
            FROM users
            WHERE username LIKE %s OR email LIKE %s OR phone_number LIKE %s
            ORDER BY id
            """,
            (like, like, like),
        )

    def count(self):
        rows = self.db.execute("SELECT COUNT(*) AS count FROM users")
        return rows[0]["count"]

    def booking_allowed(self, user_id):
        rows = self.db.execute(
            "SELECT booking_allowed FROM users WHERE id = %s", (user_id,)
        )
        return bool(rows and rows[0]["booking_allowed"])
