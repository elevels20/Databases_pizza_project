from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderDrink(Base):
    __tablename__ = 'order_drink'
    order_drink_id = Column(Integer, primary_key=True)
    drink_id = Column(Integer, ForeignKey('drink.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    drink = relationship("Drink", back_populates="order_drinks")
    order = relationship("Order", back_populates="order_drinks")
