from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class CustomerAccount(Base):
    __tablename__ = 'customer_account'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    username = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    pizza_count = Column(Integer, nullable=False)
    discount_code_id = Column(Integer, ForeignKey('discount_code.id'))
    free_birthday_pizza = Column(Boolean, nullable=True)
    free_birthday_drink = Column(Boolean, nullable=True)

    customer = relationship("Customer", back_populates="customer_account")
    discount_code = relationship("DiscountCode", back_populates="customer_accounts")
