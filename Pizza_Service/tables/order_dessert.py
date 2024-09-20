from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class OrderDessert(Base):
    __tablename__ = 'order_dessert'
    order_dessert_id = Column(Integer, primary_key=True)
    dessert_id = Column(Integer, ForeignKey('dessert.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    dessert = relationship("Dessert", back_populates="order_desserts")
    order = relationship("Order", back_populates="order_desserts")
