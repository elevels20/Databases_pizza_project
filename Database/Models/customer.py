from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
#from ..db import Base
#from Database.Models import Base
from .base import Base

class Customer(Base):
    __tablename__ = 'customer'

    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(32), nullable=False)
    Gender = Column(String(1), nullable=False)
    Birthdate = Column(Date, nullable=False)
    PhoneNumber = Column(String(15), nullable=False)
    Address = Column(String(64))

    accounts = relationship("CustomerAccount", back_populates="customer")
    orders = relationship("Orders", back_populates="customer")

class CustomerAccount(Base):
    __tablename__ = 'customer_account'

    CustomerAccountID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('customer.CustomerID'), nullable=False)
    Username = Column(String(32), nullable=False, unique=True)
    Password = Column(String(32), nullable=False)
    PizzaCount = Column(Integer, nullable=False, default=0)
    DiscountCodeID = Column(Integer, ForeignKey('discount_code.DiscountCodeID'), nullable=True)
    FreeBirthdayPizza = Column(Boolean, nullable=False, default=False)
    FreeBirthdayDrink = Column(Boolean, nullable=False, default=False)

    customer = relationship("Customer", back_populates="accounts")
    discount_code = relationship("DiscountCode", back_populates="customer_accounts")

class DiscountCode(Base):
    __tablename__ = 'discount_code'

    DiscountCodeID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(16), nullable=False, unique=True)
    DiscountPercentage = Column(Float, nullable=False)
    Used = Column(Boolean, nullable=False, default=False)

    customer_accounts = relationship("CustomerAccount", back_populates="discount_code")

