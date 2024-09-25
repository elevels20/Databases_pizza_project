from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .base import Base

class Pizza(Base):
    __tablename__ = 'pizzas'

    pizza_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)
    diet = Column(String(32), nullable=True, default=None)

    order_pizzas = relationship("OrderPizza", back_populates="pizza")
    pizza_ingredients = relationship("PizzaIngredient", back_populates="pizza")

class Dessert(Base):
    __tablename__ = 'desserts'

    dessert_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)
    diet = Column(String(32), default=None)

    order_desserts = relationship("OrderDessert", back_populates="dessert")

class Drink(Base):
    __tablename__ = 'drinks'

    drink_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    price = Column(Float, nullable=False)

    order_drinks = relationship("OrderDrink", back_populates="drink")
