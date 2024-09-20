from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
#from ..db import Base
#from Database.Models import Base
from .base import Base

class Orders(Base):
    __tablename__ = 'orders'

    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('customer.CustomerID'), nullable=False)
    Status = Column(String(32), nullable=False)
    OrderTime = Column(DateTime, nullable=False)
    TotalPrice = Column(Float, nullable=False)
    DeliveryTime = Column(DateTime, nullable=False)

    customer = relationship("Customer", back_populates="orders")
    order_pizzas = relationship("OrderPizza", back_populates="order")
    order_drinks = relationship("OrderDrink", back_populates="order")
    order_desserts = relationship("OrderDessert", back_populates="order")
    delivery_person = relationship("DeliveryPerson", back_populates="current_order")

class OrderPizza(Base):
    __tablename__ = 'order_pizza'

    PizzaID = Column(Integer, ForeignKey('pizza.PizzaID'), primary_key=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), primary_key=True)
    Quantity = Column(Integer, nullable=False)

    pizza = relationship("Pizza", back_populates="order_pizzas")
    order = relationship("Order", back_populates="order_pizzas")

class OrderDrink(Base):
    __tablename__ = 'order_drink'

    DrinkID = Column(Integer, ForeignKey('drink.DrinkID'), primary_key=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), primary_key=True)
    Quantity = Column(Integer, nullable=False)

    drink = relationship("Drink", back_populates="order_drinks")
    order = relationship("Order", back_populates="order_drinks")

class OrderDessert(Base):
    __tablename__ = 'order_dessert'

    DessertID = Column(Integer, ForeignKey('dessert.DessertID'), primary_key=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), primary_key=True)
    Quantity = Column(Integer, nullable=False)

    dessert = relationship("Dessert", back_populates="order_desserts")
    order = relationship("Order", back_populates="order_desserts")


