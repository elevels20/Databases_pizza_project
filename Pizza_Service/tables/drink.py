from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class Drink(Base):
    __tablename__ = 'drink'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)

    order_drinks = relationship("OrderDrink", back_populates="drink")