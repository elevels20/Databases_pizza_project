from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderPizza(Base):
    __tablename__ = 'order_pizza'
    pizza_id = Column(Integer, ForeignKey('pizza.id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    pizza = relationship("Pizza", back_populates="order_pizzas")
    order = relationship("Order", back_populates="order_pizzas")
