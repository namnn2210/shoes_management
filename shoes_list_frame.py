import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from connections import get_all_shoes, insert_shoe, update_shoe, delete_shoe, Shoe


class ShoesListFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Shoe Management System")
        self.master.geometry("800x600")

        # Center the frame in the root window
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Initialize the table data
        self.shoes_data = self.get_shoes_data_from_db()

        self.tree = ttk.Treeview(self, columns=(
            "ID", "Tên", "Thương hiệu", "Kích cỡ", "Màu sắc", "Thể loại", "Giá tiền", "Số lượng"), show="headings")

        # Store the entry values as instance variables
        self.name_entry = None
        self.brand_entry = None
        self.size_entry = None
        self.color_entry = None
        self.genre_entry = None
        self.price_entry = None
        self.quantity_entry = None

        # Set the column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tên", text="Tên")
        self.tree.heading("Thương hiệu", text="Thương hiệu")
        self.tree.heading("Kích cỡ", text="Kích cỡ")
        self.tree.heading("Màu sắc", text="Màu sắc")
        self.tree.heading("Thể loại", text="Thể loại")
        self.tree.heading("Giá tiền", text="Giá tiền")
        self.tree.heading("Số lượng", text="Số lượng")

        # Set the column widths based on content
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Tên", width=150, anchor="center")
        self.tree.column("Thương hiệu", width=100, anchor="center")
        self.tree.column("Kích cỡ", width=50, anchor="center")
        self.tree.column("Màu sắc", width=50, anchor="center")
        self.tree.column("Thể loại", width=50, anchor="center")
        self.tree.column("Giá tiền", width=100, anchor="center")
        self.tree.column("Số lượng", width=50, anchor="center")

        # Insert the shoe data into the Treeview
        for shoe in self.shoes_data:
            self.tree.insert("", "end", values=(
                shoe['id'], shoe['ten'], shoe['thuonghieu'], shoe['kichthuoc'], shoe['mausac'], shoe['theloai'], shoe['gia'], shoe['soluong']))

        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        self.tree.bind("<Double-1>", self.edit_selected_row)

        # Add an "Add Shoe" button
        self.add_shoe_button = tk.Button(
            self, text="Thêm sản phẩm", command=self.open_add_shoe_window)
        self.add_shoe_button.pack(pady=10)

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
        for shoe in search_results:
            self.tree.insert("", "end", values=(
                shoe['id'], shoe['ten'], shoe['thuonghieu'], shoe['kichthuoc'], shoe['mausac'], shoe['theloai'], shoe['gia'], shoe['soluong']))

    def search_shoes_by_name(self, keyword):
        # Retrieve shoe data from the database that matches the search keyword
        shoes_data = []
        shoes = get_all_shoes()
        for shoe in shoes:
            if keyword.lower() in shoe.ten.lower():
                shoes_data.append({
                    'id': shoe.id,
                    'ten': shoe.ten,
                    'thuonghieu': shoe.thuonghieu,
                    'kichthuoc': shoe.kichthuoc,
                    'mausac': shoe.mausac,
                    'theloai': shoe.theloai,
                    'gia': shoe.gia,
                    'soluong': shoe.soluong
                })
        return shoes_data

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
        edit_window.title("Edit Shoe")
        edit_window.geometry("400x300")

        # Create labels and entry fields for editing
        labels = ["Tên", "Thương hiệu", "Kích cỡ",
                  "Màu sắc", "Thể loại", "Giá tiền", "Số lượng"]
        entries = []

        for label in labels:
            label_entry = tk.Label(edit_window, text=label + ":")
            label_entry.pack()
            entry = tk.Entry(edit_window)
            entry.insert(0, shoe_data[labels.index(label) + 1])
            entry.pack()
            entries.append(entry)

        # Create a frame for the buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack()

        # Create a "Save" button within the button frame
        save_button = tk.Button(button_frame, text="Lưu", command=lambda: self.save_edited_shoe(
            shoe_data[0], [entry.get() for entry in entries], edit_window))
        save_button.pack(side=tk.LEFT)

        # Create a "Delete" button within the button frame
        delete_button = tk.Button(
            button_frame, text="Xóa", command=lambda: self.delete_shoe(shoe_data[0], edit_window))
        delete_button.pack(side=tk.LEFT)

    def save_edited_shoe(self, shoe_id, updated_data, edit_window):
        try:
            update_shoe(shoe_id, *updated_data)
            messagebox.showinfo("Result", "Sản phẩm đã được cập nhật")
            # Refresh the table data
            self.refresh_table_data()

            # Close the edit shoe window after successfully updating
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_shoe(self, shoe_id, edit_window):
        try:
            result = messagebox.askyesno(
                "Xác nhận xóa", "Bạn có muốn xóa sản phẩm này?")
            if result:
                delete_shoe(shoe_id)
                messagebox.showinfo("Result", "Sản phẩm đã xóa")
                # Refresh the table data
                self.refresh_table_data()

                # Close the edit shoe window after successfully deleting
                edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_add_shoe_window(self):
        # Create a new window for adding a new shoe
        add_shoe_window = Toplevel(self.master)
        add_shoe_window.title("Thêm sản phẩm")
        add_shoe_window.geometry("400x300")

        # Create and arrange input fields for shoe attributes
        labels = ["Tên", "Thương hiệu", "Kích cỡ",
                  "Màu sắc", "Thể loại", "Giá tiền", "Số lượng"]
        entries = []

        for label in labels:
            label_entry = tk.Label(add_shoe_window, text=label + ":")
            label_entry.pack()
            entry = tk.Entry(add_shoe_window)
            entry.pack()
            entries.append(entry)

        # Store the entry values as instance variables
        self.name_entry = entries[0]
        self.brand_entry = entries[1]
        self.size_entry = entries[2]
        self.color_entry = entries[3]
        self.genre_entry = entries[4]
        self.price_entry = entries[5]
        self.quantity_entry = entries[6]

        # Create a button to submit the new shoe data
        submit_button = tk.Button(
            add_shoe_window, text="Thêm", command=lambda: self.add_new_shoe(add_shoe_window))
        submit_button.pack()

    def add_new_shoe(self, add_shoe_window):
        try:
            name = self.name_entry.get()
            brand = self.brand_entry.get()
            size = self.size_entry.get()
            color = self.color_entry.get()
            genre = self.genre_entry.get()
            price = self.price_entry
            quantity = self.quantity_entry.get()

            new_shoe = Shoe(ten=name, thuonghieu=brand, kichthuoc=size,
                            mausac=color, theloai=genre, gia=price, soluong=quantity)
            insert_shoe(new_shoe)
            messagebox.showinfo("Result", "New shoe added")
            # Refresh the table data
            self.refresh_table_data()

            # Close the add shoe window after successfully adding
            add_shoe_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def get_shoes_data_from_db(self):
        # Retrieve shoe data from the database
        shoes_data = []
        shoes = get_all_shoes()
        for shoe in shoes:
            shoes_data.append({
                'id': shoe.id,
                'ten': shoe.ten,
                'thuonghieu': shoe.thuonghieu,
                'kichthuoc': shoe.kichthuoc,
                'mausac': shoe.mausac,
                'theloai': shoe.theloai,
                'gia': shoe.gia,
                'soluong': shoe.soluong
            })
        return shoes_data

    def refresh_table_data(self):
        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve the latest shoe data from the database
        self.shoes_data = self.get_shoes_data_from_db()

        # Insert the updated shoe data into the Treeview
        for shoe in self.shoes_data:
            self.tree.insert("", "end", values=(
                shoe['id'], shoe['ten'], shoe['thuonghieu'], shoe['kichthuoc'], shoe['mausac'], shoe['theloai'], shoe['gia'], shoe['soluong']))
