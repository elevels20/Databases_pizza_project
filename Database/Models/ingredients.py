from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    price = Column(Float)
    diet = Column(String(32), nullable=True, default=None)

    pizza_ingredients = relationship("PizzaIngredient", back_populates="ingredient")

class PizzaIngredient(Base):
    __tablename__ = 'pizza_ingredients'

    pizza_id = Column(Integer, ForeignKey('pizzas.pizza_id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredients.ingredient_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    pizza = relationship("Pizza", back_populates="pizza_ingredients")
    ingredient = relationship("Ingredient", back_populates="pizza_ingredients")
