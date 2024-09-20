from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderPizza(Base):
    __tablename__ = 'order_pizza'
    order_pizza_id = Column(Integer, primary_key=True)
    pizza_id = Column(Integer, ForeignKey('pizza.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    pizza = relationship("Pizza", back_populates="order_pizzas")
    order = relationship("Order", back_populates="order_pizzas")
