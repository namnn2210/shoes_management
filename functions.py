# functions.py
from connections import get_connection, User, insert_user, get_user_by_username_password
from sqlalchemy.exc import IntegrityError


class LoginRegisterFunctions:
    def __init__(self, view):
        self.view = view

    def register(self):
        username = self.view.get_username()
        password = self.view.get_password()

        if username == "" or password == "":
            return "Please fill in all fields"
        else:
            try:
                # You would typically insert the username and password into your MySQL database here
                user = User(tendangnhap=username, matkhau=password)
                insert_user(user=user)
                return "Registration successful!", True
            except IntegrityError:
                return "Error", "Username already exists. Please choose a different username.", False

    def login(self):
        username = self.view.get_username()
        password = self.view.get_password()

        if username == "" or password == "":
            return "Please fill in all fields"
        else:
            # You would typically query your MySQL database to check if the username and password match
            # Here, we're using a hardcoded example for simplicity
            user = get_user_by_username_password(
                username=username, password=password)
            if user:
                return "Đăng nhập thành công", False
            else:
                return "Thông tin đăng nhập không chính xác", True
