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
            "ID", "Name", "Brand", "Size", "Color", "Genre", "Quantity"), show="headings")

        # Store the entry values as instance variables
        self.name_entry = None
        self.brand_entry = None
        self.size_entry = None
        self.color_entry = None
        self.genre_entry = None
        self.quantity_entry = None

        # Set the column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Brand", text="Brand")
        self.tree.heading("Size", text="Size")
        self.tree.heading("Color", text="Color")
        self.tree.heading("Genre", text="Genre")
        self.tree.heading("Quantity", text="Quantity")

        # Set the column widths based on content
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150, anchor="center")
        self.tree.column("Brand", width=100, anchor="center")
        self.tree.column("Size", width=50, anchor="center")
        self.tree.column("Color", width=100, anchor="center")
        self.tree.column("Genre", width=100, anchor="center")
        self.tree.column("Quantity", width=50, anchor="center")

        # Insert the shoe data into the Treeview
        for shoe in self.shoes_data:
            self.tree.insert("", "end", values=(
                shoe['id'], shoe['name'], shoe['brand'], shoe['size'], shoe['color'], shoe['genre'], shoe['quantity']))

        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        self.tree.bind("<Double-1>", self.edit_selected_row)

        # Add an "Add Shoe" button
        self.add_shoe_button = tk.Button(
            self, text="Add Shoe", command=self.open_add_shoe_window)
        self.add_shoe_button.pack(pady=10)

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

        # Retrieve shoe data that matches the search keyword
        search_results = self.search_shoes_by_name(search_keyword)

        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert the search results into the Treeview
        for shoe in search_results:
            self.tree.insert("", "end", values=(
                shoe['id'], shoe['name'], shoe['brand'], shoe['size'], shoe['color'], shoe['genre'], shoe['quantity']))

    def search_shoes_by_name(self, keyword):
        # Retrieve shoe data from the database that matches the search keyword
        shoes_data = []
        shoes = get_all_shoes()
        for shoe in shoes:
            if keyword.lower() in shoe.name.lower():
                shoes_data.append({
                    'id': shoe.id,
                    'name': shoe.name,
                    'brand': shoe.brand,
                    'size': shoe.size,
                    'color': shoe.color,
                    'genre': shoe.genre,
                    'quantity': shoe.quantity
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
        labels = ["Name", "Brand", "Size", "Color", "Genre", "Quantity"]
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
        save_button = tk.Button(button_frame, text="Save", command=lambda: self.save_edited_shoe(
            shoe_data[0], [entry.get() for entry in entries], edit_window))
        save_button.pack(side=tk.LEFT)

        # Create a "Delete" button within the button frame
        delete_button = tk.Button(
            button_frame, text="Delete", command=lambda: self.delete_shoe(shoe_data[0], edit_window))
        delete_button.pack(side=tk.LEFT)

    def save_edited_shoe(self, shoe_id, updated_data, edit_window):
        try:
            update_shoe(shoe_id, *updated_data)
            messagebox.showinfo("Result", "Shoe updated")
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
                delete_shoe(shoe_id)
                messagebox.showinfo("Result", "Shoe deleted")
                # Refresh the table data
                self.refresh_table_data()

                # Close the edit shoe window after successfully deleting
                edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_add_shoe_window(self):
        # Create a new window for adding a new shoe
        add_shoe_window = Toplevel(self.master)
        add_shoe_window.title("Add Shoe")
        add_shoe_window.geometry("400x300")

        # Create and arrange input fields for shoe attributes
        labels = ["Name", "Brand", "Size", "Color", "Genre", "Quantity"]
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
        self.quantity_entry = entries[5]

        # Create a button to submit the new shoe data
        submit_button = tk.Button(
            add_shoe_window, text="Submit", command=lambda: self.add_new_shoe(add_shoe_window))
        submit_button.pack()

    def add_new_shoe(self, add_shoe_window):
        try:
            name = self.name_entry.get()
            brand = self.brand_entry.get()
            size = self.size_entry.get()
            color = self.color_entry.get()
            genre = self.genre_entry.get()
            quantity = self.quantity_entry.get()

            new_shoe = Shoe(name=name, brand=brand, size=size,
                            color=color, genre=genre, quantity=quantity)
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
                'name': shoe.name,
                'brand': shoe.brand,
                'size': shoe.size,
                'color': shoe.color,
                'genre': shoe.genre,
                'quantity': shoe.quantity
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
                shoe['id'], shoe['name'], shoe['brand'], shoe['size'], shoe['color'], shoe['genre'], shoe['quantity']))
