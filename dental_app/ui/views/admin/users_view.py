"""Admin user management tab — list, search, create, edit, role change, delete."""
import logging
import tkinter as tk
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import BOTH, CENTER, LEFT, RIGHT, VERTICAL, W, X, Y, YES

from dental_app.ui.components.modal import ModernModal
from dental_app.utils.validators import validate_phone

log = logging.getLogger(__name__)

BUTTON_STYLE = {"width": 20, "padding": 12}


class UsersView(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self._build()

    def _build(self):
        main_container = ttk.Frame(self, padding=10)
        main_container.pack(fill=BOTH, expand=YES)

        # Search bar
        search_frame = ttk.Frame(main_container, style="Card.TFrame")
        search_frame.pack(fill=X, pady=(0, 10))

        search_content = ttk.Frame(search_frame, padding=10)
        search_content.pack(fill=X)

        ttk.Label(search_content, text="🔍 Search User:", bootstyle="primary").pack(
            side=LEFT, padx=(5, 0))
        self.user_search_var = tk.StringVar()
        ttk.Entry(search_content, textvariable=self.user_search_var,
                  width=30).pack(side=LEFT, padx=5)
        ttk.Button(search_content, text="🔎 Search", bootstyle="primary",
                   command=self.search_users).pack(side=LEFT, padx=5)
        ttk.Button(search_content, text="🔄 Clear", bootstyle="info",
                   command=self.clear_search).pack(side=LEFT, padx=5)

        horizontal_frame = ttk.Frame(main_container)
        horizontal_frame.pack(fill=BOTH, expand=YES)

        left_frame = ttk.Frame(horizontal_frame)
        left_frame.pack(side=LEFT, fill=BOTH, expand=YES)

        columns = ("id", "username", "email", "phone", "role")
        column_configs = {"id": 40, "username": 120, "email": 180, "phone": 100, "role": 80}
        headings = {"id": "🔢 ID", "username": "👤 Username", "email": "📧 Email",
                    "phone": "📱 Phone", "role": "👑 Role"}

        self.users_tree = ttk.Treeview(left_frame, columns=columns,
                                       show="headings", bootstyle="primary")
        for col in columns:
            self.users_tree.heading(col, text=headings[col], anchor=CENTER)
            self.users_tree.column(col, width=column_configs[col], anchor=CENTER)

        scrollbar = ttk.Scrollbar(left_frame, orient=VERTICAL,
                                  command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        self.users_tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        buttons_frame = ttk.Frame(horizontal_frame, padding=10)
        buttons_frame.pack(side=RIGHT, fill=Y, padx=10)

        ttk.Button(buttons_frame, text="➕ Create User", command=self.create_user,
                   bootstyle="success", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="✏️ Edit User", command=self.edit_user,
                   bootstyle="info", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="🔄 Change Role", command=self.change_user_role,
                   bootstyle="primary", **BUTTON_STYLE).pack(fill=X, pady=2)
        ttk.Button(buttons_frame, text="🗑️ Delete User", command=self.delete_user,
                   bootstyle="danger", **BUTTON_STYLE).pack(fill=X, pady=2)

        self.users_tree.bind("<Double-1>", lambda e: self.edit_user())
        self.load_users()

    # ---------- data ----------

    def _populate(self, rows):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        for user in rows:
            self.users_tree.insert("", "end", values=(
                user["id"], user["username"], user["email"],
                user["phone_number"], user["role"],
            ))

    def load_users(self):
        try:
            self._populate(self.app.users.list_all())
        except Exception as err:
            messagebox.showerror("Error", f"Failed to load users: {err}")

    def search_users(self):
        term = self.user_search_var.get().strip()
        if not term:
            self.load_users()
            return
        try:
            rows = self.app.users.search(term)
            self._populate(rows)
            if not rows:
                messagebox.showinfo("No Results", "No users found matching your search.")
        except Exception as err:
            messagebox.showerror("Error", f"Search failed: {err}")

    def clear_search(self):
        self.user_search_var.set("")
        self.load_users()

    def _selected_user(self):
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a user")
            return None
        return self.users_tree.item(selected[0])["values"]

    # ---------- create ----------

    def create_user(self):
        dialog = ModernModal(self, "Create New User", width=510, height=500)
        dialog.set_icon("➕", "success")

        form_frame = ttk.Frame(dialog.content_frame)
        form_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        ttk.Label(form_frame, text="Username:", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky=W, pady=5)
        username_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=username_var, width=30).grid(
            row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Email:", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky=W, pady=5)
        email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=email_var, width=30).grid(
            row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Phone:", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky=W, pady=5)
        phone_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=phone_var, width=30).grid(
            row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Password:", font=("Segoe UI", 10)).grid(
            row=3, column=0, sticky=W, pady=5)
        password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=password_var, show="*", width=30).grid(
            row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Role:", font=("Segoe UI", 10)).grid(
            row=4, column=0, sticky=W, pady=5)
        role_var = tk.StringVar(value="staff")
        ttk.Combobox(form_frame, textvariable=role_var, values=["staff", "admin"],
                     state="readonly", width=30).grid(row=4, column=1, pady=5)

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
                messagebox.showerror(
                    "Error",
                    "Please enter a valid Philippine mobile number (e.g., 09123456789)")
                return

            ok, message = self.app.auth.create_account(
                username, email, password, phone, role=role)
            if ok:
                messagebox.showinfo("Success", "User created successfully!")
                self.load_users()
                dialog.dialog.destroy()
            else:
                messagebox.showerror("Error", message)

        dialog.add_button("Create", save_user, "success")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")

    # ---------- edit ----------

    def edit_user(self):
        values = self._selected_user()
        if not values:
            return
        user_id, current_username, current_email, current_phone = values[0], values[1], values[2], values[3]

        dialog = ModernModal(self, "Edit User", width=530, height=450)
        dialog.set_icon("👤", "primary")

        form_frame = ttk.Frame(dialog.content_frame)
        form_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        ttk.Label(form_frame, text="Username:", font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky=W, pady=5)
        username_var = tk.StringVar(value=current_username)
        ttk.Entry(form_frame, textvariable=username_var, width=30).grid(
            row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Email:", font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky=W, pady=5)
        email_var = tk.StringVar(value=current_email)
        ttk.Entry(form_frame, textvariable=email_var, width=30).grid(
            row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Phone:", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky=W, pady=5)
        phone_var = tk.StringVar(value=current_phone)
        ttk.Entry(form_frame, textvariable=phone_var, width=30).grid(
            row=2, column=1, pady=5)

        ttk.Label(form_frame, text="New Password:", font=("Segoe UI", 10)).grid(
            row=3, column=0, sticky=W, pady=5)
        password_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=password_var, show="*", width=30).grid(
            row=3, column=1, pady=5)

        def save_changes():
            new_username = username_var.get().strip()
            new_email = email_var.get().strip()
            new_phone = phone_var.get().strip()
            new_password = password_var.get().strip()

            if not all([new_username, new_email, new_phone]):
                messagebox.showerror("Error", "Username, email, and phone are required")
                return
            if not validate_phone(new_phone):
                messagebox.showerror(
                    "Error",
                    "Please enter a valid Philippine mobile number (e.g., 09123456789)")
                return
            if self.app.users.username_exists(new_username, exclude_id=user_id):
                messagebox.showerror("Error", "Username already exists")
                return
            existing = self.app.users.find_by_email(new_email)
            if existing and existing["id"] != user_id:
                messagebox.showerror("Error", "Email already registered")
                return
            if self.app.users.phone_exists(new_phone, exclude_id=user_id):
                messagebox.showerror("Error", "Phone number already registered")
                return

            try:
                password_hash = (self.app.auth.hash_password(new_password)
                                 if new_password else None)
                ok = self.app.users.update(
                    user_id, new_username, new_email, new_phone, password_hash)
                if ok:
                    messagebox.showinfo("Success", "User updated successfully!")
                    self.load_users()
                    dialog.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update user. Please try again.")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to update user: {err}")

        dialog.add_button("Save", save_changes, "success")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")

    # ---------- role ----------

    def change_user_role(self):
        values = self._selected_user()
        if not values:
            return
        user_id, username, current_role = values[0], values[1], values[4]

        if user_id == self.app.current_user["id"]:
            messagebox.showerror("Error", "You cannot change your own role")
            return

        dialog = ModernModal(self, "Change User Role", width=400, height=460)
        dialog.set_icon("🔄", "primary")

        content_frame = ttk.Frame(dialog.content_frame)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        ttk.Label(content_frame, text=f"User: {username}",
                  font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        ttk.Label(content_frame, text="Current Role:",
                  font=("Segoe UI", 10)).pack(pady=(0, 5))
        ttk.Label(content_frame, text=current_role.capitalize(),
                  font=("Segoe UI", 10, "bold"), bootstyle="primary").pack(pady=(0, 20))
        ttk.Label(content_frame, text="Select new role:",
                  font=("Segoe UI", 10)).pack(pady=(0, 5))

        role_var = tk.StringVar(value=current_role)
        ttk.Combobox(content_frame, textvariable=role_var,
                     values=["client", "staff", "admin"], state="readonly",
                     width=20).pack(pady=(0, 20))

        def save_role():
            try:
                ok = self.app.users.update_role(user_id, role_var.get())
                if ok:
                    messagebox.showinfo("Success", "User role updated successfully!")
                    self.load_users()
                    dialog.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update user role. Please try again.")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to update user role: {err}")

        dialog.add_button("Save", save_role, "success")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")

    # ---------- delete ----------

    def delete_user(self):
        values = self._selected_user()
        if not values:
            return
        user_id, username = values[0], values[1]

        if user_id == self.app.current_user["id"]:
            messagebox.showerror("Error", "You cannot delete your own account")
            return

        dialog = ModernModal(self, "Delete User", width=600, height=450)
        dialog.set_icon("⚠️", "danger")

        content_frame = ttk.Frame(dialog.content_frame)
        content_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        ttk.Label(content_frame,
                  text=f"Are you sure you want to delete user {username}?",
                  font=("Segoe UI", 12, "bold"), bootstyle="danger").pack(pady=(0, 10))
        ttk.Label(content_frame, text="This action will:",
                  font=("Segoe UI", 10)).pack(pady=(0, 5))
        ttk.Label(content_frame, text="• Delete all user appointments",
                  font=("Segoe UI", 10)).pack(anchor=W, pady=2)
        ttk.Label(content_frame, text="• Remove all user data",
                  font=("Segoe UI", 10)).pack(anchor=W, pady=2)
        ttk.Label(content_frame, text="• Cannot be undone!",
                  font=("Segoe UI", 10, "bold"), bootstyle="danger").pack(pady=(20, 0))

        def confirm_delete():
            try:
                # Cleanup step — zero appointments for this user is fine
                self.app.appointments.delete_by_user(user_id)
                if self.app.users.delete(user_id):
                    messagebox.showinfo("Success", "User deleted successfully!")
                    self.load_users()
                    dialog.dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to delete user. Please try again.")
            except Exception as err:
                messagebox.showerror("Error", f"Failed to delete user: {err}")

        dialog.add_button("Delete", confirm_delete, "danger")
        dialog.add_button("Cancel", dialog.dialog.destroy, "secondary")
