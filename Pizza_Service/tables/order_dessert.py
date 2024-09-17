from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderDessert(Base):
    __tablename__ = 'order_dessert'
    dessert_id = Column(Integer, ForeignKey('dessert.id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    dessert = relationship("Dessert", back_populates="order_desserts")
    order = relationship("Order", back_populates="order_desserts")
