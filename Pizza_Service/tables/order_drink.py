from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderDrink(Base):
    __tablename__ = 'order_drink'
    drink_id = Column(Integer, ForeignKey('drink.id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    drink = relationship("Drink", back_populates="order_drinks")
    order = relationship("Order", back_populates="order_drinks")
