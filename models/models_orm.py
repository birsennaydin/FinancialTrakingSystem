from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import config

Base = declarative_base()

# User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, default='Employee', nullable=False)

    expenses = relationship("Expense", back_populates="user")
    sales = relationship("Sale", back_populates="user")

# Category
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    expenses = relationship("Expense", back_populates="category")

# Expense
class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    user = relationship('User', back_populates='expenses')
    category = relationship('Category', back_populates='expenses')

# Inventory
class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_name = Column(String, unique=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    restock_date = Column(String, nullable=False)

    sales = relationship("Sale", back_populates="inventory")

# Sales
class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, autoincrement=True)
    inventory_id = Column(Integer, ForeignKey('inventory.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    sale_date = Column(String, nullable=False)

    inventory = relationship('Inventory', back_populates='sales')
    user = relationship('User', back_populates='sales')

# SQLAlchemy engine
DATABASE_URL = f"sqlite:///{config.DATABASE_NAME}"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)
