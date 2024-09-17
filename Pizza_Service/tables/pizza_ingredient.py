from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class PizzaIngredient(Base):
    __tablename__ = 'pizza_ingredient'
    pizza_id = Column(Integer, ForeignKey('pizza.id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    pizza = relationship("Pizza", back_populates="pizza_ingredients")
    ingredient = relationship("Ingredient", back_populates="pizza_ingredients")
