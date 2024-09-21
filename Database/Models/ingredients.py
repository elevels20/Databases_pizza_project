from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Ingredient(Base):
    __tablename__ = 'ingredient'

    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(32), nullable=False)
    Price = Column(Float)
    Diet = Column(String(32), nullable=True, default=None)

    pizza_ingredients = relationship("PizzaIngredient", back_populates="ingredient")

class PizzaIngredient(Base):
    __tablename__ = 'pizza_ingredient'

    PizzaID = Column(Integer, ForeignKey('pizza.PizzaID'), primary_key=True)
    IngredientID = Column(Integer, ForeignKey('ingredient.IngredientID'), primary_key=True)
    Quantity = Column(Integer, nullable=False)

    pizza = relationship("Pizza", back_populates="pizza_ingredients")
    ingredient = relationship("Ingredient", back_populates="pizza_ingredients")
