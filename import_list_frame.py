import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from connections import get_all_suppliers, get_all_shoes, get_shoes, get_supplier, get_employee, get_all_employees, get_all_imports, insert_imports, update_imports, delete_imports, insert_import_details, get_import_details, Imports, ImportDetails


class ImportListFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("import_obj Management System")
        self.master.geometry("800x600")

        # Center the frame in the root window
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Initialize the table data
        self.import_objs_data = self.get_import_objs_data_from_db()

        self.tree = ttk.Treeview(self, columns=(
            "ID", "Mã phiếu nhập", "Mã nhân viên", "Ngày nhập"), show="headings")

        # Store the entry values as instance variables
        self.nhaphang_entry = None
        self.id_nhanvien_entry = None

        # Set the column headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Mã phiếu nhập", text="Mã phiếu nhập")
        self.tree.heading("Mã nhân viên", text="Mã nhân viên")
        self.tree.heading("Ngày nhập", text="Ngày nhập")

        # Set the column widths based on content
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Mã phiếu nhập", width=150, anchor="center")
        self.tree.column("Mã nhân viên", width=100, anchor="center")
        self.tree.column("Ngày nhập", width=100, anchor="center")

        # Insert the import_obj data into the Treeview
        for import_obj in self.import_objs_data:
            nhanvien = get_employee(import_obj['id_nhanvien']).ten
            self.tree.insert("", "end", values=(
                import_obj['id'], import_obj['manhap'], nhanvien, import_obj['created_at']))

        self.tree.pack(padx=20, pady=20, fill="both", expand=True)

        self.tree.bind("<Double-1>", self.edit_selected_row)

        # Add an "Add import_obj" button
        self.add_import_obj_button = tk.Button(
            self, text="Thêm sản phẩm", command=self.open_add_import_obj_window)
        self.add_import_obj_button.pack(pady=10)

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

        # Retrieve import_obj data that matches the search keyword
        search_results = self.search_import_objs_by_name(search_keyword)

        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert the search results into the Treeview
        for import_obj in search_results:
            nhanvien = get_employee(import_obj['id_nhanvien']).ten
            self.tree.insert("", "end", values=(
                import_obj['id'], import_obj['manhap'], nhanvien, import_obj['created_at']))

    def search_import_objs_by_name(self, keyword):
        # Retrieve import_obj data from the database that matches the search keyword
        import_objs_data = []
        import_objs = get_all_imports()
        for import_obj in import_objs:
            if keyword.lower() in import_obj.manhap.lower():
                import_objs_data.append({
                    'id': import_obj.id,
                    'manhap': import_obj.manhap,
                    'id_nhanvien': import_obj.id_nhanvien,
                    'created_at': import_obj.created_at,
                })
        return import_objs_data

    def edit_selected_row(self, event):
        # Get the selected item
        selected_item = self.tree.selection()
        if selected_item:
            # Get the data of the selected row
            row_data = self.tree.item(selected_item)["values"]

            # Open an edit window with the data for editing
            self.open_edit_import_obj_window(row_data)

    def open_edit_import_obj_window(self, import_obj_data):
        # Create a new window for editing import_obj details
        edit_window = Toplevel(self.master)
        edit_window.title("Edit import_obj")
        edit_window.geometry("600x400")

        # Create labels and entry fields for editing
        labels = ["Mã phiếu nhập", "Nhân viên"]
        entries = []

        for label in labels:
            label_entry = tk.Label(edit_window, text=label + ":")
            label_entry.pack()
            if label == "Nhân viên":
                # Create a combobox for selecting an employee
                employees = get_all_employees()
                employee_names = [employee.ten for employee in employees]
                self.selected_employee_id = tk.StringVar(
                    value=import_obj_data[2])
                employee_combobox = ttk.Combobox(
                    edit_window, textvariable=self.selected_employee_id, values=employee_names)
                employee_combobox.pack()
            else:
                # Create an entry field for other attributes
                entry = tk.Entry(edit_window)
                entry.insert(0, import_obj_data[labels.index(label) + 1])
                entry.pack()
                entries.append(entry)

        # Create a frame for the buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack()

        # Create a "Save" button within the button frame
        save_button = tk.Button(button_frame, text="Lưu", command=lambda: self.save_edited_import_obj(
            import_obj_data[0], [entry.get() for entry in entries], edit_window))
        save_button.pack(side=tk.LEFT)

        # Create a "Delete" button within the button frame
        delete_button = tk.Button(
            button_frame, text="Xóa", command=lambda: self.delete_import_obj(import_obj_data[0], edit_window))
        delete_button.pack(side=tk.LEFT)

        add_detail_button = tk.Button(edit_window, text="Thêm chi tiết",
                                      command=lambda: self.open_add_import_detail_window(import_obj_data[0]))
        add_detail_button.pack()

        import_details_tree = ttk.Treeview(edit_window, columns=(
            "Sản phẩm ID", "Nhà cung cấp ID", "Số lượng", "Thành tiền"), show="headings")

        # Define column headings
        import_details_tree.heading("#1", text="Sản phẩm ID")
        import_details_tree.heading("#2", text="Nhà cung cấp ID")
        import_details_tree.heading("#3", text="Số lượng")
        import_details_tree.heading("#4", text="Thành tiền")

        # Define column widths
        import_details_tree.column("#1", width=100)
        import_details_tree.column("#2", width=100)
        import_details_tree.column("#3", width=100)
        import_details_tree.column("#4", width=100)

        # You will need to fetch and insert your ImportDetails data into the Treeview here
        import_details_data = get_import_details(
            import_obj_data[0])  # Implement this function

        for detail in import_details_data:
            sanpham = get_shoes(detail.id_sanpham)
            nhacungcap = get_supplier(detail.id_nhacungcap)
            thanhtien = sanpham.gia * detail.soluong
            import_details_tree.insert("", "end", values=(
                sanpham.ten, nhacungcap.ten, detail.soluong, thanhtien))

        import_details_tree.pack(padx=20, pady=20, fill="both", expand=True)

    def open_add_import_detail_window(self, import_id):
        # Create a new window for adding import details
        add_detail_window = Toplevel(self.master)
        add_detail_window.title("Thêm chi tiết phiếu nhập")
        add_detail_window.geometry("600x400")

        # Create a label and dropdown list for "Sản phẩm ID"
        label_sanpham = tk.Label(add_detail_window, text="Sản phẩm:")
        label_sanpham.pack()

        # Get all sản phẩm (products) from the database and create a list of sản phẩm names
        sanpham_data = get_all_shoes()  # You need to implement this function
        sanpham_dict = {sanpham.ten: sanpham.id for sanpham in sanpham_data}
        selected_sanpham_id = tk.StringVar()
        sanpham_names = list(sanpham_dict.keys())
        sanpham_dropdown = ttk.Combobox(
            add_detail_window, textvariable=selected_sanpham_id, values=sanpham_names, state="readonly")
        sanpham_dropdown.pack()

        # Create a label and dropdown list for "Nhà cung cấp ID"
        label_nhacungcap = tk.Label(add_detail_window, text="Nhà cung cấp:")
        label_nhacungcap.pack()

        # Get all nhà cung cấp (suppliers) from the database and create a list of nhà cung cấp names
        # You need to implement this function
        nhacungcap_data = get_all_suppliers()
        nhacungcap_dict = {
            nhacungcap.ten: nhacungcap.id for nhacungcap in nhacungcap_data}

        selected_nhacungcap_id = tk.StringVar()
        nhacungcap_names = list(nhacungcap_dict.keys())
        nhacungcap_dropdown = ttk.Combobox(
            add_detail_window, textvariable=selected_nhacungcap_id, values=nhacungcap_names, state="readonly")
        nhacungcap_dropdown.pack()

        # Create an input field for "Số lượng"
        label_soluong = tk.Label(add_detail_window, text="Số lượng:")
        label_soluong.pack()

        soluong_entry = tk.Entry(add_detail_window)
        soluong_entry.pack()

        # Create a button to submit the new import detail data
        submit_button = tk.Button(
            add_detail_window, text="Thêm", command=lambda: self.add_new_import_detail(import_id, sanpham_dict[selected_sanpham_id.get()], nhacungcap_dict[selected_nhacungcap_id.get()], soluong_entry.get(), add_detail_window))
        submit_button.pack()

    def add_new_import_detail(self, import_id, sanpham, nhacungcap, soluong, add_detail_window):
        try:
            # Retrieve the values from the entry fields
            id_sanpham = sanpham
            id_nhacungcap = nhacungcap
            soluong = soluong

            # Create a new ImportDetails object and insert it into the database
            new_import_detail = ImportDetails(
                id_nhaphang=import_id, id_sanpham=id_sanpham, id_nhacungcap=id_nhacungcap, soluong=soluong, thanhtien=4)
            # Insert the new import detail into the database (you need to implement this function)
            # insert_import_detail(new_import_detail)
            insert_import_details(new_import_detail)

            # Show a success message
            messagebox.showinfo("Result", "Chi tiết đã được thêm")

            # Close the add import detail window after successfully adding
            add_detail_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_edited_import_obj(self, import_obj_id, updated_data, edit_window):
        try:
            update_imports(import_obj_id, *updated_data)
            messagebox.showinfo("Result", "Sản phẩm đã được cập nhật")
            # Refresh the table data
            self.refresh_table_data()

            # Close the edit import_obj window after successfully updating
            edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_import_obj(self, import_obj_id, edit_window):
        try:
            result = messagebox.askyesno(
                "Xác nhận xóa", "Bạn có muốn xóa phiếu nhập này này?")
            if result:
                delete_imports(import_obj_id)
                messagebox.showinfo("Result", "Phiếu nhập đã xóa")
                # Refresh the table data
                self.refresh_table_data()

                # Close the edit import_obj window after successfully deleting
                edit_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def open_add_import_obj_window(self):
        # Create a new window for adding a new import_obj
        add_import_obj_window = Toplevel(self.master)
        add_import_obj_window.title("Thêm phiếu nhập")
        add_import_obj_window.geometry("600x400")

        # Create and arrange input fields for import_obj attributes
        labels = ["Mã phiếu nhập", "Nhân viên"]
        entries = []

        for label in labels:
            label_entry = tk.Label(add_import_obj_window, text=label + ":")
            label_entry.pack()
            if label == "Nhân viên":
                # Create a combobox for selecting an employee
                employees = get_all_employees()
                employee_dict = {
                    employee.ten: employee.id for employee in employees}
                # self.selected_employee_id =
                employee_names = list(employee_dict.keys())
                selected = tk.StringVar()(add_import_obj_window)
                selected.set(employee_names[0])
                employee_combobox = ttk.Combobox(
                    add_import_obj_window, textvariable=selected, values=employee_names, state="readonly")
                employee_combobox.pack()
            else:
                # Create an entry field for other attributes
                entry = tk.Entry(add_import_obj_window)
                entry.pack()
                entries.append(entry)

        # Store the entry values as instance variables
        self.nhaphang_entry = entries[0]
        # self.id_nhanvien_entry = entries[1]

        # Create a button to submit the new import_obj data
        submit_button = tk.Button(
            add_import_obj_window, text="Thêm", command=lambda: self.add_new_import_obj(add_import_obj_window))
        submit_button.pack()

    def add_new_import_obj(self, add_import_obj_window):
        try:
            nhaphang = self.nhaphang_entry.get()
            id_nhanvien = self.employee_combobox.get()

            new_import_obj = Imports(
                manhap=nhaphang, id_nhanvien=id_nhanvien)
            insert_imports(new_import_obj)
            messagebox.showinfo("Result", "Thêm phiếu nhập thành công")
            # Refresh the table data
            self.refresh_table_data()

            # Close the add import_obj window after successfully adding
            add_import_obj_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi: {str(e)}")

    def get_import_objs_data_from_db(self):
        # Retrieve import_obj data from the database
        import_objs_data = []
        import_objs = get_all_imports()
        for import_obj in import_objs:
            import_objs_data.append({
                'id': import_obj.id,
                'manhap': import_obj.manhap,
                'id_nhanvien': import_obj.id_nhanvien,
                'created_at': import_obj.created_at,
            })
        return import_objs_data

    def refresh_table_data(self):
        # Clear the current data in the table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve the latest import_obj data from the database
        self.import_objs_data = self.get_import_objs_data_from_db()

        # Insert the updated import_obj data into the Treeview
        for import_obj in self.import_objs_data:
            self.tree.insert("", "end", values=(
                import_obj['id'], import_obj['manhap'], import_obj['id_nhanvien'], import_obj['created_at']))
