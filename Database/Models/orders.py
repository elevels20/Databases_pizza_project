from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    status = Column(String(32), nullable=False) # Being prepared, In process, Out for delivery
    order_time = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    delivery_time = Column(DateTime, nullable=False)
    # maybe add: delivery_person_id = Column(Integer, ForeignKey('delivery_persons.delivery_person_id'), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    order_pizzas = relationship("OrderPizza", back_populates="order")
    order_drinks = relationship("OrderDrink", back_populates="order")
    order_desserts = relationship("OrderDessert", back_populates="order")
    delivery_person = relationship("DeliveryPerson", back_populates="current_order")

class OrderPizza(Base):
    __tablename__ = 'order_pizzas'

    pizza_id = Column(Integer, ForeignKey('pizzas.pizza_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    pizza = relationship("Pizza", back_populates="order_pizzas")
    order = relationship("Order", back_populates="order_pizzas")

class OrderDrink(Base):
    __tablename__ = 'order_drinks'

    drink_id = Column(Integer, ForeignKey('drinks.drink_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    drink = relationship("Drink", back_populates="order_drinks")
    order = relationship("Order", back_populates="order_drinks")

class OrderDessert(Base):
    __tablename__ = 'order_desserts'

    dessert_id = Column(Integer, ForeignKey('desserts.dessert_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    quantity = Column(Integer, nullable=False)

    dessert = relationship("Dessert", back_populates="order_desserts")
    order = relationship("Order", back_populates="order_desserts")


