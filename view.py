# view.py
import tkinter as tk


class LoginRegisterView:
    def __init__(self, root, login_callback, register_callback):
        self.root = root

        self.username_label = tk.Label(
            root, text="Username:", font=("Helvetica", 14))
        self.username_label.pack(pady=8)

        self.username_entry = tk.Entry(root, font=("Helvetica", 14))
        self.username_entry.pack(pady=4)

        self.password_label = tk.Label(
            root, text="Password:", font=("Helvetica", 14))
        self.password_label.pack(pady=8)

        self.password_entry = tk.Entry(root, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=4)

        self.login_button = tk.Button(
            root, text="Login", command=login_callback, font=("Helvetica", 14))
        self.login_button.pack(pady=8)

        self.register_button = tk.Button(
            root, text="Register", command=register_callback, font=("Helvetica", 14))
        self.register_button.pack(pady=8)

    def get_username(self):
        return self.username_entry.get()

    def get_password(self):
        return self.password_entry.get()

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
