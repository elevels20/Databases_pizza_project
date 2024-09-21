from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from .base import Base

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    gender = Column(String(1), nullable=False)
    birthdate = Column(Date, nullable=False)
    phone_number = Column(String(15), nullable=False)
    address = Column(String(64))

    accounts = relationship("CustomerAccount", back_populates="customer")
    orders = relationship("Order", back_populates="customer")

class CustomerAccount(Base):
    __tablename__ = 'customer_accounts'

    customer_account_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    pizza_count = Column(Integer, nullable=False, default=0)
    discount_code_id = Column(Integer, ForeignKey('discount_codes.discount_code_id'), nullable=True)
    free_birthday_pizza = Column(Boolean, nullable=False, default=False)
    free_birthday_drink = Column(Boolean, nullable=False, default=False)

    customer = relationship("Customer", back_populates="accounts")
    discount_code = relationship("DiscountCode", back_populates="customer_accounts")

class DiscountCode(Base):
    __tablename__ = 'discount_codes'

    discount_code_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(16), nullable=False, unique=True)
    discount_percentage = Column(Float, nullable=False)
    used = Column(Boolean, nullable=False, default=False)

    customer_accounts = relationship("CustomerAccount", back_populates="discount_code")

