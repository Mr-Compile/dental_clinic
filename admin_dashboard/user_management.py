from tkinter import messagebox
import tkinter as tk
import re
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from admin_dashboard.helpers import ModernModal, validate_phone

class UserManagementMixin:
    def setup_users_view(self):
        # Main container with padding
        main_container = ttk.Frame(self.users_frame, padding=10)
        main_container.pack(fill=BOTH, expand=YES)

        # Search frame with modern styling
        search_frame = ttk.Frame(main_container, style='Card.TFrame')
        search_frame.pack(fill=X, pady=(0, 10))

        search_content = ttk.Frame(search_frame, padding=10)
        search_content.pack(fill=X)

        ttk.Label(search_content, text="🔍 Search User:", bootstyle="primary").pack(side=LEFT, padx=(5,0))
        self.user_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_content, textvariable=self.user_search_var, width=30)
        search_entry.pack(side=LEFT, padx=5)

        # Search buttons with icons
        ttk.Button(search_content, text="🔎 Search", bootstyle="primary", 
                  command=self.search_users).pack(side=LEFT, padx=5)
        ttk.Button(search_content, text="🔄 Clear", bootstyle="info", 
                  command=self.clear_user_search).pack(side=LEFT, padx=5)

        # Horizontal container for tree and buttons
        horizontal_frame = ttk.Frame(main_container)
        horizontal_frame.pack(fill=BOTH, expand=YES)

        # Left frame for treeview
        left_frame = ttk.Frame(horizontal_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        # Configure columns with specific widths and center alignment
        columns = ('id', 'username', 'email', 'phone', 'role')
        column_configs = {
            'id': 40,  # Reduced width
            'username': 120,  # Reduced width
            'email': 180,  # Reduced width
            'phone': 100,  # Reduced width
            'role': 80  # Reduced width
        }

        self.users_tree = ttk.Treeview(left_frame, columns=columns, show='headings', bootstyle="primary")

        # Configure columns with icons and center alignment
        self.users_tree.heading('id', text='🔢 ID', anchor=CENTER)
        self.users_tree.heading('username', text='👤 Username', anchor=CENTER)
        self.users_tree.heading('email', text='📧 Email', anchor=CENTER)
        self.users_tree.heading('phone', text='📱 Phone', anchor=CENTER)
        self.users_tree.heading('role', text='👑 Role', anchor=CENTER)

        for col in columns:
            self.users_tree.column(col, width=column_configs[col], anchor=CENTER)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_frame, orient=VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)

        self.users_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Right frame for buttons
        buttons_frame = ttk.Frame(horizontal_frame, padding=10)
        buttons_frame.pack(side=RIGHT, fill=Y, padx=10)

        # Style configuration for buttons
        button_style = {
            'width': 20,  # Increased width
            'padding': 12  # Increased padding
        }

        # Action buttons with icons
        ttk.Button(buttons_frame, text="➕ Create User", 
                  command=self.create_user,
                  bootstyle="success", **button_style).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="✏️ Edit User", 
                  command=self.edit_user,
                  bootstyle="info", **button_style).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="🔄 Change Role", 
                  command=self.change_user_role,
                  bootstyle="primary", **button_style).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="🗑️ Delete User", 
                  command=self.delete_user,
                  bootstyle="danger", **button_style).pack(fill=X, pady=2)

        # Bind double-click event for editing
        self.users_tree.bind("<Double-1>", lambda e: self.edit_user())

        self.load_users()

    def load_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        try:
            result = self.app.execute_query(
                "SELECT id, username, email, phone_number, role FROM users ORDER BY id"
            )

            if result:
                for user in result:
                    # Insert with centered values
                    self.users_tree.insert('', 'end', values=user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load users: {str(e)}")

    def search_users(self):
        search_term = self.user_search_var.get().strip()
        if not search_term:
            self.load_users()
            return

        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        try:
            query = """
                SELECT id, username, email, phone_number, role 
                FROM users 
                WHERE username LIKE %s OR email LIKE %s OR phone_number LIKE %s 
                ORDER BY id
            """
            like_term = f"%{search_term}%"
            result = self.app.execute_query(query, (like_term, like_term, like_term))

            if result:
                for user in result:
                    # Insert with centered values
                    self.users_tree.insert('', 'end', values=user)
            else:
                messagebox.showinfo("No Results", "No users found matching your search.")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")

    def clear_user_search(self):
        self.user_search_var.set("")
        self.load_users()

    def edit_user(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user")
            return

        user_values = self.users_tree.item(selected_item[0])['values']
        user_id = user_values[0]
        current_username = user_values[1]
        current_email = user_values[2]
        current_phone = user_values[3]

        dialog = ModernModal(self, "Edit User", width=530, height=450)
        dialog.set_icon("👤", "primary")

        # Create form fields
        form_frame = ttk.Frame(dialog.content_frame)
        form_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Username
        ttk.Label(form_frame, text="Username:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky=W, pady=5)
        username_var = tk.StringVar(value=current_username)
        username_entry = ttk.Entry(form_frame, textvariable=username_var, width=30)
        username_entry.grid(row=0, column=1, pady=5)

        # Email
        ttk.Label(form_frame, text="Email:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky=W, pady=5)
        email_var = tk.StringVar(value=current_email)
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=1, column=1, pady=5)

        # Phone
        ttk.Label(form_frame, text="Phone:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky=W, pady=5)
        phone_var = tk.StringVar(value=current_phone)
        phone_entry = ttk.Entry(form_frame, textvariable=phone_var, width=30)
        phone_entry.grid(row=2, column=1, pady=5)
        

        # Password
        ttk.Label(form_frame, text="New Password:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky=W, pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=password_var, show="*", width=30)
        password_entry.grid(row=3, column=1, pady=5)

        def save_changes():
            new_username = username_var.get().strip()
            new_email = email_var.get().strip()
            new_phone = phone_var.get().strip()
            new_password = password_var.get().strip()

            if not all([new_username, new_email, new_phone]):
                messagebox.showerror("Error", "Username, email, and phone are required")
                return

            if not validate_phone(new_phone):
                messagebox.showerror("Error", "Please enter a valid Philippine mobile number (e.g., 09123456789)")
                return

            try:
                # Check if username already exists (excluding current user)
                result = self.app.execute_query(
                    "SELECT id FROM users WHERE username = %s AND id != %s",
                    (new_username, user_id)
                )
                if result:
                    messagebox.showerror("Error", "Username already exists")
                    return

                # Check if phone number already exists (excluding current user)
                result = self.app.execute_query(
                    "SELECT id FROM users WHERE phone_number = %s AND id != %s",
                    (new_phone, user_id)
                )
                if result:
                    messagebox.showerror("Error", "Phone number already registered")
                    return

                # Update the user
                if new_password:
                    success = self.app.execute_query(
                        """
                        UPDATE users 
                        SET username = %s, email = %s, phone_number = %s, password = %s 
                        WHERE id = %s
                        """,
                        (new_username, new_email, new_phone, new_password, user_id),
                        fetch=False
                    )
                else:
                    success = self.app.execute_query(
                        """
                        UPDATE users 
                        SET username = %s, email = %s, phone_number = %s 
                        WHERE id = %s
                        """,
                        (new_username, new_email, new_phone, user_id),
                        fetch=False
                    )

                if success:
                    messagebox.showinfo("Success", "User updated successfully!")
                    self.load_users()
                    dialog.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update user. Please try again.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update user: {str(e)}")

        dialog.add_button("Save", save_changes, "success")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")

    def change_user_role(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user")
            return

        user_id = self.users_tree.item(selected_item[0])['values'][0]
        current_role = self.users_tree.item(selected_item[0])['values'][4]
        username = self.users_tree.item(selected_item[0])['values'][1]

        dialog = ModernModal(self, "Change User Role", width=400, height=460)
        dialog.set_icon("🔄", "primary")

        # Content frame
        content_frame = ttk.Frame(dialog.content_frame)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # User info
        ttk.Label(
            content_frame,
            text=f"User: {username}",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(0, 10))

        ttk.Label(
            content_frame,
            text="Current Role:",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 5))

        ttk.Label(
            content_frame,
            text=current_role.capitalize(),
            font=("Segoe UI", 10, "bold"),
            bootstyle="primary"
        ).pack(pady=(0, 20))

        # Role selection
        ttk.Label(
            content_frame,
            text="Select new role:",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 5))

        role_var = tk.StringVar(value=current_role)
        role_combo = ttk.Combobox(
            content_frame,
            textvariable=role_var,
            values=['client', 'staff', 'admin'],
            state="readonly",
            width=20
        )
        role_combo.pack(pady=(0, 20))

        def save_role():
            new_role = role_var.get()
            try:
                success = self.app.execute_query(
                    "UPDATE users SET role = %s WHERE id = %s",
                    (new_role, user_id),
                    fetch=False
                )

                if success:
                    messagebox.showinfo("Success", "User role updated successfully!")
                    self.load_users()
                    dialog.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update user role. Please try again.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update user role: {str(e)}")

        dialog.add_button("Save", save_role, "success")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")

    def delete_user(self):
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user")
            return

        user_id = self.users_tree.item(selected_item[0])['values'][0]
        username = self.users_tree.item(selected_item[0])['values'][1]

        dialog = ModernModal(self, "Delete User", width=600, height=450)
        dialog.set_icon("⚠️", "danger")

        # Content frame
        content_frame = ttk.Frame(dialog.content_frame)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Warning message
        ttk.Label(
            content_frame,
            text=f"Are you sure you want to delete user {username}?",
            font=("Segoe UI", 12, "bold"),
            bootstyle="danger"
        ).pack(pady=(0, 10))

        ttk.Label(
            content_frame,
            text="This action will:",
            font=("Segoe UI", 10)
        ).pack(pady=(0, 5))

        ttk.Label(
            content_frame,
            text="• Delete all user appointments",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=2)

        ttk.Label(
            content_frame,
            text="• Remove all user data",
            font=("Segoe UI", 10)
        ).pack(anchor=W, pady=2)

        ttk.Label(
            content_frame,
            text="• Cannot be undone!",
            font=("Segoe UI", 10, "bold"),
            bootstyle="danger"
        ).pack(pady=(20, 0))

        def confirm_delete():
            try:
                success = self.app.execute_query(
                    "DELETE FROM appointments WHERE user_id = %s",
                    (user_id,),
                    fetch=False
                )

                if not success:
                    messagebox.showerror("Error", "Failed to delete user's appointments")
                    return

                success = self.app.execute_query(
                    "DELETE FROM users WHERE id = %s",
                    (user_id,),
                    fetch=False
                )

                if success:
                    messagebox.showinfo("Success", "User deleted successfully!")
                    self.load_users()
                    dialog.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to delete user. Please try again.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

        dialog.add_button("Delete", confirm_delete, "danger")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")

    def create_user(self):
        dialog = ModernModal(self, "Create New User", width=510, height=500)
        dialog.set_icon("➕", "success")

        # Create form fields
        form_frame = ttk.Frame(dialog.content_frame)
        form_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        # Username
        ttk.Label(form_frame, text="Username:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky=W, pady=5)
        username_var = tk.StringVar()
        username_entry = ttk.Entry(form_frame, textvariable=username_var, width=30)
        username_entry.grid(row=0, column=1, pady=5)

        # Email
        ttk.Label(form_frame, text="Email:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky=W, pady=5)
        email_var = tk.StringVar()
        email_entry = ttk.Entry(form_frame, textvariable=email_var, width=30)
        email_entry.grid(row=1, column=1, pady=5)

        # Phone
        ttk.Label(form_frame, text="Phone:", font=("Segoe UI", 10)).grid(row=2, column=0, sticky=W, pady=5)
        phone_var = tk.StringVar()
        phone_entry = ttk.Entry(form_frame, textvariable=phone_var, width=30)
        phone_entry.grid(row=2, column=1, pady=5)
        

        # Password
        ttk.Label(form_frame, text="Password:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky=W, pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(form_frame, textvariable=password_var, show="*", width=30)
        password_entry.grid(row=3, column=1, pady=5)

        # Role selection (only staff or admin)
        ttk.Label(form_frame, text="Role:", font=("Segoe UI", 10)).grid(row=4, column=0, sticky=W, pady=5)
        role_var = tk.StringVar(value="staff")
        role_combo = ttk.Combobox(
            form_frame,
            textvariable=role_var,
            values=["staff", "admin"],
            state="readonly",
            width=30
        )
        role_combo.grid(row=4, column=1, pady=5)

        def save_user():
            username = username_var.get().strip()
            email = email_var.get().strip()
            phone = phone_var.get().strip()
            password = password_var.get().strip()
            role = role_var.get()

            if not all([username, email, phone, password]):
                messagebox.showerror("Error", "All fields are required")
                return

            if not validate_phone(phone):
                messagebox.showerror("Error", "Please enter a valid Philippine mobile number (e.g., 09123456789)")
                return

            try:
                # Check if username already exists
                result = self.app.execute_query(
                    "SELECT id FROM users WHERE username = %s",
                    (username,)
                )
                if result:
                    messagebox.showerror("Error", "Username already exists")
                    return

                # Check if phone number already exists
                result = self.app.execute_query(
                    "SELECT id FROM users WHERE phone_number = %s",
                    (phone,)
                )
                if result:
                    messagebox.showerror("Error", "Phone number already registered")
                    return

                # Create the user
                success = self.app.execute_query(
                    """
                    INSERT INTO users (username, email, phone_number, password, role)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (username, email, phone, password, role),
                    fetch=False
                )

                if success:
                    messagebox.showinfo("Success", "User created successfully!")
                    self.load_users()
                    dialog.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to create user")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create user: {str(e)}")

        dialog.add_button("Create", save_user, "success")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")
