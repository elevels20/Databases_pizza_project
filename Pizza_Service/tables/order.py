from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    status = Column(String(32), nullable=False)
    order_time = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    delivery_time = Column(DateTime, nullable=True)

    order_pizzas = relationship("OrderPizza", back_populates="order")
    order_drinks = relationship("OrderDrink", back_populates="order")
    order_desserts = relationship("OrderDessert", back_populates="order")
    delivery_person = relationship("DeliveryPerson", back_populates="current_order")
    customer = relationship("Customer", back_populates="orders")
