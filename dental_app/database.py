import mysql.connector
from tkinter import messagebox

class DatabaseMixin:
    def setup_database(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="dental"
            )
            self.cursor = self.conn.cursor(buffered=True)
            
            if not self.check_database_connection():
                return False

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    phone_number VARCHAR(11) NOT NULL,
                    role ENUM('client', 'staff', 'admin') DEFAULT 'client',
                    booking_allowed BOOLEAN GENERATED ALWAYS AS (role = 'client') STORED
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    service VARCHAR(100) NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            self.conn.commit()
            return True
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to database: {err}")
            return False

    def check_database_connection(self):
        try:
            self.cursor.execute("SELECT 1")
            return True
        except mysql.connector.Error:
            return False

    def execute_query(self, query, params=None, fetch=True):
        try:
            if not self.check_database_connection():
                messagebox.showerror("Database Error", "Lost connection to database. Please restart the application.")
                return None
                
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if fetch:
                result = self.cursor.fetchall()
                self.conn.commit()
                return result
            else:
                self.conn.commit()
                return True
                
        except mysql.connector.Error as err:
            self.conn.rollback()
            messagebox.showerror("Database Error", f"Query failed: {err}")
            return None
