from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class Dessert(Base):
    __tablename__ = 'dessert'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)
    diet = Column(String(32), nullable=True)

    order_desserts = relationship("OrderDessert", back_populates="dessert")