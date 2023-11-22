import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from view import LoginRegisterView
from functions import LoginRegisterFunctions
from shoes_list_frame import ShoesListFrame
from employee_list_frame import EmployeeListFrame
from supplier_list_frame import SupplierListFrame
from import_list_frame import ImportListFrame


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Login and Registration")
        self.geometry("800x600")
        self.current_frame = None

        # Center the window on the screen
        # self.center_window()

        # Switch to the LoginRegisterFrame initially
        self.switch_frame(LoginRegisterFrame)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, *args)

        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def switch_to_main_menu(self):
        # Switch to the MainMenuFrame after successful login
        self.switch_frame(MainMenuFrame)


class LoginRegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Login and Registration")
        self.master.geometry("800x600")

        self.view = LoginRegisterView(
            self, self.login_callback, self.register_callback)
        self.functions = LoginRegisterFunctions(self.view)

    def login_callback(self):
        result, error = self.functions.login()
        self.view.clear_fields()
        if error:
            messagebox.showinfo("Error", result)
        else:
            # After successful login, switch to the main menu
            self.master.switch_to_main_menu()

    def register_callback(self):
        result = self.functions.register()
        messagebox.showinfo("Result", result)
        self.view.clear_fields()


class MainMenuFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Main Menu")
        self.master.geometry("800x600")

        self.employee_window = None
        self.shoes_window = None
        self.import_window = None
        self.supplier_window = None

        # Create a style for the buttons
        style = ttk.Style()
        style.configure("MainMenu.TButton", font=("Helvetica", 14), padding=10)

        # Create buttons for the four management options with the defined style
        employee_button = ttk.Button(self, text="Employee Management",
                                     command=self.show_employee_management, style="MainMenu.TButton")
        employee_button.pack(pady=10)
        shoes_button = ttk.Button(self, text="Shoes Management",
                                  command=self.show_shoes_management, style="MainMenu.TButton")
        shoes_button.pack(pady=10)
        export_button = ttk.Button(self, text="Import Management",
                                   command=self.show_import_management, style="MainMenu.TButton")
        export_button.pack(pady=10)
        supplier_button = ttk.Button(self, text="Supplier Management",
                                     command=self.show_supplier_management, style="MainMenu.TButton")
        supplier_button.pack(pady=10)

    def show_employee_management(self):
        if self.employee_window is None:
            # Switch to the ShoesListFrame for shoes management
            self.employee_window = tk.Toplevel(self.master)
            self.employee_window.title("Employee Management")
            self.employee_window.geometry("800x600")

            # Create a new instance of ShoesListFrame in the new window
            employee_frame = EmployeeListFrame(self.employee_window)
            employee_frame.pack(fill="both", expand=True)

    def show_shoes_management(self):
        # Switch to the ShoesListFrame for shoes management
        # Create a new window for ShoesListFrame
        if self.shoes_window is None:
            self.shoes_window = tk.Toplevel(self.master)
            self.shoes_window.title("Shoes Management")
            self.shoes_window.geometry("800x600")

            # Create a new instance of ShoesListFrame in the new window
            shoes_frame = ShoesListFrame(self.shoes_window)
            shoes_frame.pack(fill="both", expand=True)

    def show_import_management(self):
        if self.import_window is None:
            self.import_window = tk.Toplevel(self.master)
            self.import_window.title("Import Management")
            self.import_window.geometry("800x600")

            # Create a new instance of ShoesListFrame in the new window
            import_frame = ImportListFrame(self.import_window)
            import_frame.pack(fill="both", expand=True)

    def show_supplier_management(self):
        if self.supplier_window is None:
            self.supplier_window = tk.Toplevel(self.master)
            self.supplier_window.title("Supplier Management")
            self.supplier_window.geometry("800x600")

            # Create a new instance of ShoesListFrame in the new window
            supplier_frame = SupplierListFrame(self.supplier_window)
            supplier_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
