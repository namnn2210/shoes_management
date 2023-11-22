from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Date, BIGINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

# Define the database connection URL
# Replace 'username', 'password', 'hostname', 'database_name' with your MySQL credentials
DATABASE_URL = 'mysql://root:@localhost/shoes_manager'

# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()

# Define the User and Shoe models


class User(Base):
    __tablename__ = 'taikhoan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tendangnhap = Column(String(255), nullable=False)
    matkhau = Column(String(255), nullable=False)
    loai = Column(Integer, default=1, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


class Shoe(Base):
    __tablename__ = 'sanpham'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(255), nullable=False)
    thuonghieu = Column(String(255))
    kichthuoc = Column(Float)
    mausac = Column(String(255))
    theloai = Column(String(255))
    soluong = Column(Integer)
    gia = Column(BIGINT)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


class Employee(Base):
    __tablename__ = 'nhanvien'

    id = Column(Integer, primary_key=True, autoincrement=True)
    manv = Column(String(255), nullable=False)
    ten = Column(String(255), nullable=False)
    sdt = Column(String(255))
    diachi = Column(String(255))
    ngaysinh = Column(Date)
    gioitinh = Column(Integer, default=1, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    # Add a relationship to the Imports model
    # imports = relationship('Imports', back_populates='nhanvien')


class Supplier(Base):
    __tablename__ = 'nhacungcap'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ten = Column(String(255), nullable=False)
    sdt = Column(String(255))
    diachi = Column(String(255))
    email = Column(String(255))
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


class Imports(Base):
    __tablename__ = 'nhaphang'

    id = Column(Integer, primary_key=True, autoincrement=True)
    manhap = Column(String(255), nullable=False)
    id_nhanvien = Column(Integer)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    # Add a relationship to the Employee model
    # employee = relationship('Employee', back_populates='nhaphang')


class ImportDetails(Base):
    __tablename__ = 'nhaphang_chitiet'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_nhaphang = Column(Integer, ForeignKey('nhaphang.id'), nullable=False)
    id_sanpham = Column(Integer, ForeignKey('sanpham.id'), nullable=False)
    id_nhacungcap = Column(Integer, nullable=False)
    soluong = Column(Integer, nullable=False)
    thanhtien = Column(Float, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    # Define relationships to the Import, Shoe, and Supplier models
    # import_obj = relationship('Imports', back_populates='nhaphang_chitiet')
    # shoe = relationship('Shoe', back_populates='nhaphang_chitiet')
    # supplier = relationship('Supplier', back_populates='nhaphang_chitiet')


# Create the tables in the database
Base.metadata.create_all(engine)


def get_connection():
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def insert_user(user):
    session = get_connection()
    try:
        session.add(user)
        session.commit()
    finally:
        session.close()


def insert_shoe(shoe):
    session = get_connection()
    try:
        session.add(shoe)
        session.commit()
    finally:
        session.close()


def insert_employee(employee):
    session = get_connection()
    try:
        session.add(employee)
        session.commit()
    finally:
        session.close()


def insert_supplier(supplier):
    session = get_connection()
    try:
        session.add(supplier)
        session.commit()
    finally:
        session.close()


def insert_imports(imports):
    session = get_connection()
    try:
        session.add(imports)
        session.commit()
    finally:
        session.close()


def insert_import_details(import_details):
    session = get_connection()
    try:
        session.add(import_details)
        session.commit()
    finally:
        session.close()


def get_user_by_username_password(username, password):
    session = get_connection()
    try:
        user_data = session.query(User).filter_by(
            tendangnhap=username, matkhau=password).first()
        return user_data
    finally:
        session.close()


def get_import_details(import_id):
    session = get_connection()
    try:
        import_detail_datas = session.query(ImportDetails).filter_by(
            ImportDetails.id_nhaphang == import_id).all()
        return import_detail_datas
    finally:
        session.close()


def get_all_shoes():
    session = get_connection()
    try:
        shoes_data = session.query(Shoe).where(Shoe.status == 1).all()
        return shoes_data
    finally:
        session.close()


def get_all_employees():
    session = get_connection()
    try:
        employees_data = session.query(
            Employee).where(Employee.status == 1).all()
        return employees_data
    finally:
        session.close()


def get_all_suppliers():
    session = get_connection()
    try:
        suppliers_data = session.query(
            Supplier).where(Supplier.status == 1).all()
        return suppliers_data
    finally:
        session.close()


def get_all_imports():
    session = get_connection()
    try:
        imports_data = session.query(
            Imports).where(Imports.status == 1).all()
        return imports_data
    finally:
        session.close()


def update_shoe(shoe_id, name, brand, size, color, genre, price, quantity):
    session = get_connection()
    try:
        # Get the shoe to edit from the database
        shoe_to_edit = session.query(Shoe).filter_by(id=shoe_id).first()

        # Update the shoe details with the edited values
        shoe_to_edit.ten = name
        shoe_to_edit.thuonghieu = brand
        shoe_to_edit.kichthuoc = size
        shoe_to_edit.mausac = color
        shoe_to_edit.theloai = genre
        shoe_to_edit.soluong = quantity
        shoe_to_edit.gia = price
        session.commit()
    finally:
        session.close()


def update_employee(employee_id, card_id, name, phone, address, dob, gender):
    session = get_connection()
    try:
        # Get the shoe to edit from the database
        employee_to_edit = session.query(
            Employee).filter_by(id=employee_id).first()

        # Update the shoe details with the edited values
        employee_to_edit.manv = card_id
        employee_to_edit.ten = name
        employee_to_edit.sdt = phone
        employee_to_edit.diachi = address
        employee_to_edit.ngaysinh = dob
        employee_to_edit.gioitinh = gender
        session.commit()
    finally:
        session.close()


def update_supplier(supplier_id, name, phone, email, address):
    session = get_connection()
    try:
        # Get the shoe to edit from the database
        employee_to_edit = session.query(
            Supplier).filter_by(id=supplier_id).first()

        # Update the shoe details with the edited values
        employee_to_edit.ten = name
        employee_to_edit.sdt = phone
        employee_to_edit.diachi = address
        employee_to_edit.email = email
        session.commit()
    finally:
        session.close()


def update_imports():
    pass


def delete_shoe(shoe_id):
    session = get_connection()
    try:
        # Get the shoe to edit from the database
        shoe_to_edit = session.query(Shoe).filter_by(id=shoe_id).first()

        # Update the shoe details with the edited values
        shoe_to_edit.status = 0

        session.commit()
    finally:
        session.close()


def delete_employee(employee_id):
    session = get_connection()
    try:
        # Get the shoe to edit from the database
        employee_to_edit = session.query(
            Employee).filter_by(id=employee_id).first()

        # Update the shoe details with the edited values
        employee_to_edit.status = 0

        session.commit()
    finally:
        session.close()


def delete_supplier(supplier_id):
    session = get_connection()
    try:
        # Get the shoe to edit from the database
        supplier_to_edit = session.query(
            Supplier).filter_by(id=supplier_id).first()

        # Update the shoe details with the edited values
        supplier_to_edit.status = 0

        session.commit()
    finally:
        session.close()


def delete_imports():
    pass
