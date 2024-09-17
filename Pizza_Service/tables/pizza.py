from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class Pizza(Base):
    __tablename__ = 'pizza'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)
    diet = Column(String(32), nullable=True)

    order_pizzas = relationship("OrderPizza", back_populates="pizza")
    pizza_ingredients = relationship("PizzaIngredient", back_populates="pizza")
