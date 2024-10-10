from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from .base import Base

class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    gender = Column(String(1), nullable=False) # M/F
    birthdate = Column(Date, nullable=False)
    phone_number = Column(String(15), nullable=False)
    country = Column(String(32), nullable=False)
    city = Column(String(32), nullable=False)
    postal_code = Column(String(5), nullable=False)
    street = Column(String(64), nullable=False)
    house_number = Column(Integer, nullable=False)

    accounts = relationship("CustomerAccount", back_populates="customer")
    orders = relationship("Order", back_populates="customer")

class CustomerAccount(Base):
    __tablename__ = 'customer_accounts'

    customer_account_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    total_pizza_count = Column(Integer, nullable=False, default=0) # Total number of pizzas ordered
    discount_pizza_count = Column(Integer, nullable=False, default=0) # Tracks every 10 pizzas for discount
    birthday_offer_used_year = Column(Integer, nullable=True, default = None)  # Track last year the offer was used
    is_admin = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="accounts")
    discount_codes = relationship("DiscountCode", back_populates="customer_account")

class DiscountCode(Base):
    __tablename__ = 'discount_codes'

    discount_code_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(16), nullable=False, unique=True)
    discount_percentage = Column(Float, nullable=False)
    is_used = Column(Boolean, nullable=False, default=False)
    customer_account_id = Column(Integer, ForeignKey('customer_accounts.customer_account_id'), nullable=False)

    customer_account = relationship("CustomerAccount", back_populates="discount_codes")

