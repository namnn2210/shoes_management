import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel, StringVar
from tkinter import messagebox
from connections import get_all_employees, insert_employee, update_employee, delete_employee, Employee
from tkcalendar import DateEntry
from datetime import datetime


class EmployeeListFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Employee Management System")
        self.master.geometry("800x600")

        # Center the frame in the root window
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Initialize the table data
        self.employees_data = self.get_employees_data_from_db()

        self.tree = ttk.Treeview(self, columns=(
            "ID", "Mã NV", "Tên", "SĐT", "Địa chỉ", "Ngày sinh", "Giới tính"), show="headings")

        # Store the entry values as instance variables
        self.card_id_entry = None
        self.name_entry = None
        self.phone_entry = None
        self.address_entry = None
        self.dob_entry = None
        self.gender_entry = None

        # Set the column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Mã NV", text="Mã NV")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("SĐT", text="SĐT")
        self.tree.heading("Địa chỉ", text="Địa chỉ")
        self.tree.heading("Ngày sinh", text="Ngày sinh")
        self.tree.heading("Giới tính", text="Giới tính")

        # Set the column widths based on content
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Mã NV", width=50, anchor="center")
        self.tree.column("Tên", width=150, anchor="center")
        self.tree.column("SĐT", width=100, anchor="center")
        self.tree.column("Địa chỉ", width=50, anchor="center")
        self.tree.column("Ngày sinh", width=100, anchor="center")
        self.tree.column("Giới tính", width=100, anchor="center")

        # Insert the shoe data into the Treeview
        for employee in self.employees_data:
            if employee['gioitinh'] == 1:
                gender = 'Nam'
            else:
                gender = 'Nữ'
            self.tree.insert("", "end", values=(
                employee['id'], employee['manv'], employee['ten'], employee['sdt'], employee['diachi'], employee['ngaysinh'], gender))

        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        self.tree.bind("<Double-1>", self.edit_selected_row)

        # Add an "Add Shoe" button
        self.add_employee_button = tk.Button(
            self, text="Thêm nhân viên", command=self.open_add_shoe_window)
        self.add_employee_button.pack(pady=10)

        # Add a search box and button
        self.search_label = tk.Label(self, text="Tìm theo tên:")
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(
            self, text="Tìm kiếm", command=self.perform_search)
        self.search_button.pack(pady=5)

    def perform_search(self):
        # Get the search keyword from the entry
        search_keyword = self.search_entry.get()

        # Retrieve shoe data that matches the search keyword
        search_results = self.search_shoes_by_name(search_keyword)

        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert the search results into the Treeview
        for employee in search_results:
            if employee['gioitinh'] == 1:
                gender = 'Nam'
            else:
                gender = 'Nữ'
            self.tree.insert("", "end", values=(
                employee['id'], employee['manv'], employee['ten'], employee['sdt'], employee['diachi'], employee['ngaysinh'], gender))

    def search_shoes_by_name(self, keyword):
        # Retrieve shoe data from the database that matches the search keyword
        employees_data = []
        employees = get_all_employees()
        for employee in employees:
            if keyword.lower() in employee.ten.lower():
                employees_data.append({
                    'id': employee.id,
                    'manv': employee.manv,
                    'ten': employee.ten,
                    'sdt': employee.sdt,
                    'diachi': employee.diachi,
                    'ngaysinh': employee.ngaysinh,
                    'gioitinh': employee.gioitinh,
                })
        return employees_data

    def edit_selected_row(self, event):
        # Get the selected item
        selected_item = self.tree.selection()
        if selected_item:
            # Get the data of the selected row
            row_data = self.tree.item(selected_item)["values"]

            # Open an edit window with the data for editing
            self.open_edit_shoe_window(row_data)

    def open_edit_shoe_window(self, shoe_data):
        # Create a new window for editing shoe details
        edit_window = Toplevel(self.master)
        edit_window.title("Cập nhật nhân viên")
        edit_window.geometry("600x400")

        # Create labels and entry fields for editing
        labels = ["Mã NV", "Tên", "SĐT", "Địa chỉ", "Ngày sinh"]
        entries = []

        for label in labels:
            label_entry = tk.Label(edit_window, text=label + ":")
            label_entry.pack()
            if label == "Ngày sinh":
                # Use DateEntry widget for Date of Birth
                dob_entry = DateEntry(edit_window)
                entry.insert(0, shoe_data[labels.index(label) + 1])
                dob_entry.pack()
                entries.append(dob_entry)
            else:
                entry = tk.Entry(edit_window)
                entry.insert(0, shoe_data[labels.index(label) + 1])
                entry.pack()
                entries.append(entry)

        gender_label = tk.Label(edit_window, text="Giới tính:")
        gender_label.pack()

        gender_values = ["Nam", "Nữ"]
        selected = StringVar(edit_window)
        selected.set(gender_values[0])
        gender_combobox = ttk.Combobox(
            edit_window, textvariable=selected, values=gender_values, state="readonly")
        gender_combobox.pack()

        # Create a frame for the buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack()

        self.card_id_entry = entries[0]
        self.name_entry = entries[1]
        self.phone_entry = entries[2]
        self.address_entry = entries[3]
        self.dob_entry = entries[4]
        self.gender_entry = gender_combobox.get()

        # Create a "Save" button within the button frame
        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_edited_shoe(
            shoe_data[0], edit_window))
        save_button.pack(side=tk.LEFT)

        # Create a "Delete" button within the button frame
        delete_button = tk.Button(
            button_frame, text="Delete", command=lambda: self.delete_shoe(shoe_data[0], edit_window))
        delete_button.pack(side=tk.LEFT)

    def save_edited_shoe(self, shoe_id, edit_window):
        try:
            card_id = self.card_id_entry.get()
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            address = self.address_entry.get()
            dob = self.dob_entry.get()
            date_format = '%m/%d/%y'  # Specify the input date format

            # Parse the string into a datetime object
            date_obj = datetime.strptime(dob, date_format)
            normal_date = date_obj.strftime('%Y-%m-%d')
            if self.gender_entry == 'Nam':
                gender = 1
            else:
                gender = 0
            update_employee(shoe_id, card_id, name, phone,
                            address, normal_date, gender)
            messagebox.showinfo("Result", "Employee updated")
            # Refresh the table data
            self.refresh_table_data()

            # Close the edit shoe window after successfully updating
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_shoe(self, shoe_id, edit_window):
        try:
            result = messagebox.askyesno(
                "Confirm Delete", "Are you sure you want to delete this shoe?")
            if result:
                delete_employee(shoe_id)
                messagebox.showinfo("Result", "Employee deleted")
                # Refresh the table data
                self.refresh_table_data()

                # Close the edit shoe window after successfully deleting
                edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_add_shoe_window(self):
        # Create a new window for adding a new shoe
        add_shoe_window = Toplevel(self.master)
        add_shoe_window.title("Thêm nhân viên mới")
        add_shoe_window.geometry("600x400")

        # Create and arrange input fields for shoe attributes
        labels = ["Mã NV", "Tên", "SĐT", "Địa chỉ", "Ngày sinh"]
        entries = []

        for label in labels:
            label_entry = tk.Label(add_shoe_window, text=label + ":")
            label_entry.pack()
            if label == "Ngày sinh":
                # Use DateEntry widget for Date of Birth
                dob_entry = DateEntry(add_shoe_window)
                dob_entry.pack()
                entries.append(dob_entry)
            else:
                entry = tk.Entry(add_shoe_window)
                entry.pack()
                entries.append(entry)

        gender_label = tk.Label(add_shoe_window, text="Giới tính:")
        gender_label.pack()

        gender_values = ["Nam", "Nữ"]
        selected = StringVar(add_shoe_window)
        selected.set(gender_values[0])
        gender_combobox = ttk.Combobox(
            add_shoe_window, textvariable=selected, values=gender_values, state="readonly")
        gender_combobox.pack()

        # Store the entry values as instance variables
        self.card_id_entry = entries[0]
        self.name_entry = entries[1]
        self.phone_entry = entries[2]
        self.address_entry = entries[3]
        self.dob_entry = entries[4]
        self.gender_entry = gender_combobox.get()

        # print('================================', type(self.dob_entry.get()))

        # Create a button to submit the new shoe data
        submit_button = tk.Button(
            add_shoe_window, text="Thêm", command=lambda: self.add_new_shoe(add_shoe_window))
        submit_button.pack()

    def add_new_shoe(self, add_shoe_window):
        try:
            card_id = self.card_id_entry.get()
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            address = self.address_entry.get()
            dob = self.dob_entry.get()
            date_format = '%m/%d/%y'  # Specify the input date format

            # Parse the string into a datetime object
            date_obj = datetime.strptime(dob, date_format)
            normal_date = date_obj.strftime('%Y-%m-%d')
            if self.gender_entry == 'Nam':
                gender = 1
            else:
                gender = 0
            # gender = self.gender_entry

            new_shoe = Employee(ten=name, manv=card_id, sdt=phone,
                                diachi=address, ngaysinh=normal_date, gioitinh=gender)
            insert_employee(new_shoe)
            messagebox.showinfo("Result", "New employee added")
            # Refresh the table data
            self.refresh_table_data()

            # Close the add shoe window after successfully adding
            add_shoe_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_employees_data_from_db(self):
        # Retrieve shoe data from the database
        employees_data = []
        employees = get_all_employees()
        for employee in employees:
            employees_data.append({
                'id': employee.id,
                'manv': employee.manv,
                'ten': employee.ten,
                'sdt': employee.sdt,
                'diachi': employee.diachi,
                'ngaysinh': employee.ngaysinh,
                'gioitinh': employee.gioitinh,
            })
        return employees_data

    def refresh_table_data(self):
        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve the latest shoe data from the database
        self.employees_data = self.get_employees_data_from_db()

        # Insert the updated shoe data into the Treeview
        for employee in self.employees_data:
            if employee['gioitinh'] == 1:
                gender = 'Nam'
            else:
                gender = 'Nữ'
            self.tree.insert("", "end", values=(employee['id'], employee['manv'], employee['ten'],
                             employee['sdt'], employee['diachi'], employee['ngaysinh'], gender))
