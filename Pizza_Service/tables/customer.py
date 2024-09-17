from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from .base import Base

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    gender = Column(String(1), nullable=False)
    birthdate = Column(Date, nullable=False)
    phone_number = Column(Integer, nullable=False)
    address = Column(String(64), nullable=False)

    customer_account = relationship("CustomerAccount", back_populates="customer")
    orders = relationship("Order", back_populates="customer")
