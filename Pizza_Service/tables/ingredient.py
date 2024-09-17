from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)
    diet = Column(String(32), nullable=True)

    pizza_ingredients = relationship("PizzaIngredient", back_populates="ingredient")
