import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from connections import get_all_suppliers, insert_supplier, update_supplier, delete_supplier, Supplier


class SupplierListFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Supplier Management System")
        self.master.geometry("800x600")

        # Center the frame in the root window
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Initialize the table data
        self.suppliers_data = self.get_suppliers_data_from_db()

        self.tree = ttk.Treeview(self, columns=(
            "ID", "Tên", "SĐT", "Email", "Địa chỉ"), show="headings")

        # Store the entry values as instance variables
        self.name_entry = None
        self.phone_entry = None
        self.email_entry = None
        self.address_entry = None

        # Set the column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("SĐT", text="SĐT")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Địa chỉ", text="Địa chỉ")

        # Set the column widths based on content
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Tên", width=150, anchor="center")
        self.tree.column("SĐT", width=100, anchor="center")
        self.tree.column("Email", width=50, anchor="center")
        self.tree.column("Địa chỉ", width=100, anchor="center")

        # Insert the supplier data into the Treeview
        for supplier in self.suppliers_data:
            self.tree.insert("", "end", values=(
                supplier['id'], supplier['ten'], supplier['sdt'], supplier['email'], supplier['diachi']))

        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        self.tree.bind("<Double-1>", self.edit_selected_row)

        # Add an "Add supplier" button
        self.add_supplier_button = tk.Button(
            self, text="Add supplier", command=self.open_add_supplier_window)
        self.add_supplier_button.pack(pady=10)

        # Add a search box and button
        self.search_label = tk.Label(self, text="Search by Name:")
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(self)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(
            self, text="Search", command=self.perform_search)
        self.search_button.pack(pady=5)

    def perform_search(self):
        # Get the search keyword from the entry
        search_keyword = self.search_entry.get()

        # Retrieve supplier data that matches the search keyword
        search_results = self.search_suppliers_by_name(search_keyword)

        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert the search results into the Treeview
        for supplier in search_results:
            self.tree.insert("", "end", values=(
                supplier['id'], supplier['ten'], supplier['sdt'], supplier['email'], supplier['diachi']))

    def search_suppliers_by_name(self, keyword):
        # Retrieve supplier data from the database that matches the search keyword
        suppliers_data = []
        suppliers = get_all_suppliers()
        for supplier in suppliers:
            if keyword.lower() in supplier.ten.lower():
                suppliers_data.append({
                    'id': supplier.id,
                    'ten': supplier.ten,
                    'sdt': supplier.sdt,
                    'email': supplier.email,
                    'diachi': supplier.diachi,
                })
        return suppliers_data

    def edit_selected_row(self, event):
        # Get the selected item
        selected_item = self.tree.selection()
        if selected_item:
            # Get the data of the selected row
            row_data = self.tree.item(selected_item)["values"]

            # Open an edit window with the data for editing
            self.open_edit_supplier_window(row_data)

    def open_edit_supplier_window(self, supplier_data):
        # Create a new window for editing supplier details
        edit_window = Toplevel(self.master)
        edit_window.title("Edit supplier")
        edit_window.geometry("400x300")

        # Create labels and entry fields for editing
        labels = ["Tên", "SĐT", "Email", "Địa chỉ"]
        entries = []

        for label in labels:
            label_entry = tk.Label(edit_window, text=label + ":")
            label_entry.pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, supplier_data[labels.index(label) + 1])
            entry.pack()
            entries.append(entry)

        # Create a frame for the buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack()

        # Create a "Save" button within the button frame
        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_edited_supplier(
            supplier_data[0], [entry.get() for entry in entries], edit_window))
        save_button.pack(side=tk.LEFT)

        # Create a "Delete" button within the button frame
        delete_button = tk.Button(
            button_frame, text="Delete", command=lambda: self.delete_supplier(supplier_data[0], edit_window))
        delete_button.pack(side=tk.LEFT)

    def save_edited_supplier(self, supplier_id, updated_data, edit_window):
        try:
            update_supplier(supplier_id, *updated_data)
            messagebox.showinfo("Result", "supplier updated")
            # Refresh the table data
            self.refresh_table_data()

            # Close the edit supplier window after successfully updating
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_supplier(self, supplier_id, edit_window):
        try:
            result = messagebox.askyesno(
                "Confirm Delete", "Are you sure you want to delete this supplier?")
            if result:
                delete_supplier(supplier_id)
                messagebox.showinfo("Result", "supplier deleted")
                # Refresh the table data
                self.refresh_table_data()

                # Close the edit supplier window after successfully deleting
                edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_add_supplier_window(self):
        # Create a new window for adding a new supplier
        add_supplier_window = Toplevel(self.master)
        add_supplier_window.title("Add supplier")
        add_supplier_window.geometry("400x300")

        # Create and arrange input fields for supplier attributes
        labels = ["Tên", "SĐT", "Email", "Địa chỉ"]
        entries = []

        for label in labels:
            label_entry = tk.Label(add_supplier_window, text=label + ":")
            label_entry.pack()
            entry = tk.Entry(add_supplier_window)
            entry.pack()
            entries.append(entry)

        # Store the entry values as instance variables
        self.name_entry = entries[0]
        self.phone_entry = entries[1]
        self.email_entry = entries[2]
        self.address_entry = entries[3]

        # Create a button to submit the new supplier data
        submit_button = tk.Button(
            add_supplier_window, text="Submit", command=lambda: self.add_new_supplier(add_supplier_window))
        submit_button.pack()

    def add_new_supplier(self, add_supplier_window):
        try:
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            address = self.address_entry.get()

            new_supplier = Supplier(ten=name, sdt=phone, email=email,
                                    diachi=address)
            insert_supplier(new_supplier)
            messagebox.showinfo("Result", "New supplier added")
            # Refresh the table data
            self.refresh_table_data()

            # Close the add supplier window after successfully adding
            add_supplier_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_suppliers_data_from_db(self):
        # Retrieve supplier data from the database
        suppliers_data = []
        suppliers = get_all_suppliers()
        for supplier in suppliers:
            suppliers_data.append({
                'id': supplier.id,
                'ten': supplier.ten,
                'sdt': supplier.sdt,
                'email': supplier.email,
                'diachi': supplier.diachi,
            })
        return suppliers_data

    def refresh_table_data(self):
        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve the latest supplier data from the database
        self.suppliers_data = self.get_suppliers_data_from_db()

        # Insert the updated supplier data into the Treeview
        for supplier in self.suppliers_data:
            self.tree.insert("", "end", values=(
                supplier['id'], supplier['ten'], supplier['sdt'], supplier['email'], supplier['diachi']))
