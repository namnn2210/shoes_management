from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    user_type = Column(Integer, default=1, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


class Shoe(Base):
    __tablename__ = 'shoes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(255))
    size = Column(Float)
    color = Column(String(255))
    genre = Column(String(255))
    quantity = Column(Integer)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(255))
    address = Column(String(255))
    dob = Column(Date)
    gender = Column(Integer, default=1, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


class Supplier(Base):
    __tablename__ = 'suppliers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(255))
    address = Column(String(255))
    email = Column(String(255))
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


class Imports(Base):
    __tablename__ = 'imports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    import_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone = Column(String(255))
    address = Column(String(255))
    email = Column(String(255))
    status = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)


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


def get_user_by_username_password(username, password):
    session = get_connection()
    try:
        user_data = session.query(User).filter_by(
            username=username, password=password).first()
        return user_data
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


def update_shoe(shoe_id, name, brand, size, color, genre, quantity):
    session = get_connection()
    try:
        # Get the shoe to edit from the database
        shoe_to_edit = session.query(Shoe).filter_by(id=shoe_id).first()

        # Update the shoe details with the edited values
        shoe_to_edit.name = name
        shoe_to_edit.brand = brand
        shoe_to_edit.size = size
        shoe_to_edit.color = color
        shoe_to_edit.genre = genre
        shoe_to_edit.quantity = quantity
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
        employee_to_edit.card_id = card_id
        employee_to_edit.name = name
        employee_to_edit.phone = phone
        employee_to_edit.address = address
        employee_to_edit.dob = dob
        employee_to_edit.gender = gender
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
        employee_to_edit.name = name
        employee_to_edit.phone = phone
        employee_to_edit.address = address
        employee_to_edit.email = email
        session.commit()
    finally:
        session.close()


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
